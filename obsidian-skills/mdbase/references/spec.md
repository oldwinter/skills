# mdbase Specification

**Spec version:** 0.1.0

A collection is identified by an `mdbase.yaml` file at the root. Type definitions live in `_types/` (configurable). Records are `.md` files with YAML frontmatter.

```
my-collection/
├── mdbase.yaml          # Marks as collection
├── _types/              # Type definitions
│   ├── task.md
│   └── person.md
├── tasks/
│   └── fix-bug.md       # Record
└── people/
    └── alice.md          # Record
```

---

## Configuration (mdbase.yaml)

Minimal:

```yaml
spec_version: "0.1.0"
```

Full:

```yaml
spec_version: "0.1.0"
name: "My Project"
description: "Description"

settings:
  extensions: ["mdx"]              # Additional extensions beyond .md
  exclude: [".git", "node_modules", ".mdbase", "drafts/**"]
  include_subfolders: true          # Recursive scan (default: true)
  types_folder: "_types"            # Where type defs live (default: "_types")
  explicit_type_keys: ["type", "types"]  # Keys for type declaration (default)
  default_validation: "warn"        # off | warn | error (default: "warn")
  default_strict: false             # false | "warn" | true (default: false)
  id_field: "id"                    # Unique ID field for link resolution (default: "id")
  write_nulls: "omit"              # omit | explicit (default: "omit")
  write_empty_lists: true           # Write [] or omit (default: true)
  rename_update_refs: true          # Update refs on rename (default: true)
  cache_folder: ".mdbase"           # Cache location (default: ".mdbase")
```

---

## Type Definitions

Types are markdown files in `_types/`. The frontmatter defines the schema; the body documents it.

```yaml
# _types/task.md
---
name: task                          # REQUIRED, must match filename
description: "A task"               # Optional
extends: base                       # Optional single inheritance
strict: false                       # false | "warn" | true

match:                              # Optional auto-matching rules
  path_glob: "tasks/**/*.md"
  fields_present: [status]
  where:
    status:
      exists: true
    priority:
      gte: 1

filename_pattern: "{id}.md"         # Optional

fields:
  id:
    type: string
    required: true
    generated: ulid
    unique: true
  title:
    type: string
    required: true
    min_length: 1
    max_length: 200
  status:
    type: enum
    values: [open, in_progress, blocked, done]
    default: open
  priority:
    type: integer
    min: 1
    max: 5
  due_date:
    type: date
  tags:
    type: list
    items:
      type: string
    unique: true
    default: []
  assignee:
    type: link
    target: person
    validate_exists: true
  full_name:
    type: string
    computed: "first_name + ' ' + last_name"   # Read-only, evaluated at read time
---

# Task

Documentation for the type goes here in the body.
```

### Type name rules

- Lowercase letters, numbers, hyphens, underscores
- Must start with a letter, max 64 chars
- Must match filename without extension
- Reserved: names starting with `_`, and `file`, `formula`, `this`

### Inheritance

- Single inheritance via `extends`
- Chains allowed (child -> parent -> grandparent)
- Child fields override parent fields completely (no constraint merging)
- Circular inheritance is an error

### Computed fields

- `computed: "expression"` — evaluated at read time, never persisted
- Cannot be `required`, cannot have `default` or `generated`
- May reference other computed fields (dependency-ordered)
- Circular computed dependencies are an error

---

## Field Types

### Primitives

| Type | YAML | Constraints |
|------|------|-------------|
| `string` | String | `min_length`, `max_length`, `pattern` (ES2018 regex) |
| `integer` | Integer | `min`, `max` |
| `number` | Float/Int | `min`, `max` |
| `boolean` | Boolean | — (accepts true/false, yes/no, on/off) |
| `date` | `YYYY-MM-DD` | — |
| `datetime` | ISO 8601 | — (preserves timezone) |
| `time` | `HH:MM[:SS]` | — |
| `enum` | String | `values` (required list of allowed strings) |

### Composites

| Type | YAML | Constraints |
|------|------|-------------|
| `list` | Array | `items` (required), `min_items`, `max_items`, `unique` |
| `object` | Mapping | `fields` (required) |
| `link` | String | `target` (type constraint), `validate_exists` |
| `any` | Any | — |

### Common field options (all types)

```yaml
field_name:
  type: string          # Required
  required: false       # Must be present and non-null (default: false)
  default: "value"      # Applied when field is MISSING (not when null)
  generated: ulid       # ulid | uuid | now | now_on_write | {from, transform}
  description: "Help"   # Human-readable
  deprecated: false     # Warn on use
  unique: true          # Cross-file uniqueness
```

### Generated field strategies

| Strategy | Behavior |
|----------|----------|
| `ulid` | Generate ULID on create (if field missing) |
| `uuid` | Generate UUID v4 on create (if field missing) |
| `now` | Current datetime on create only (if field missing) |
| `now_on_write` | Current datetime on EVERY write |
| `{from: field, transform: slugify\|lowercase\|uppercase}` | Derive from another field |

### Link formats

```yaml
# Wikilinks
assignee: "[[alice]]"
assignee: "[[alice|Alice Smith]]"       # With alias
ref: "[[docs/api#auth]]"               # With path and anchor
sibling: "[[./other-task]]"            # Relative

# Markdown links
parent: "[Parent](./parent.md)"

# Bare paths
config: "./config.md"
```

---

## Frontmatter Rules

### Null semantics

| YAML | Value | `exists()` | Satisfies `required`? |
|------|-------|------------|----------------------|
| `field: null` | null | true | No |
| `field: ~` | null | true | No |
| `field:` (empty) | null | true | No |
| `field: ""` | empty string | true | Yes |
| *(key absent)* | undefined | false | No |

### Writing rules — CRITICAL

1. **NEVER write bare `field:` form** — it is ambiguous. Always use `field: null` or omit.
2. **Empty strings** must be quoted: `field: ""`
3. **Null handling** depends on `write_nulls` setting:
   - `"omit"` (default): Don't write null fields
   - `"explicit"`: Write `field: null`
4. **Preserve body content** — frontmatter updates must not modify the markdown body.
5. **Preserve line endings** (LF vs CRLF).
6. **Try to preserve** field order, quoting style, multi-line format, and comments.

---

## Type Matching

### Order of precedence

1. **Explicit declaration** (`type: task` or `types: [task, urgent]`) — highest precedence, match rules NOT evaluated
2. **Match rules** — all types' `match` rules evaluated; ALL matching types apply
3. **Untyped** — if nothing matches

### Match conditions (AND logic)

```yaml
match:
  path_glob: "tasks/**/*.md"          # Glob pattern on file path
  fields_present: [status, assignee]  # Fields must be present AND non-null
  where:                              # Field value conditions
    status:
      exists: true                    # Key present and non-null
    priority:
      gte: 3                         # Comparison operators
    tags:
      contains: "urgent"              # List contains
```

Match `where` operators: direct value (equality), `exists`, `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `contains`, `containsAll`, `containsAny`, `startsWith`, `endsWith`, `matches`

### Multi-type validation

When a file matches multiple types, constraints merge (most restrictive):
- `required`: true if EITHER requires it
- `min`/`min_length`: higher value wins
- `max`/`max_length`: lower value wins
- `pattern`: must match ALL patterns
- `enum values`: intersection
- Incompatible base types → `type_conflict` error

---

## Querying

```yaml
query:
  types: [task]                       # Filter by type(s)
  folder: "projects/alpha"            # Filter by path prefix
  where:                              # Expression-based filters
    and:
      - 'status != "done"'
      - "priority >= 3"
  order_by:
    - field: due_date
      direction: asc                  # asc | desc
    - field: priority
      direction: desc
  limit: 20
  offset: 0
  include_body: false
```

### Query+ (optional advanced features)

```yaml
  formulas:
    overdue: "due_date < today() && status != 'done'"
  groupBy:
    property: status
    direction: ASC
  summaries:
    avg_priority: "values.reduce(acc + value, 0) / values.length"
  property_summaries:
    priority: Average
    due_date: Earliest
```

Null values sort LAST ascending, FIRST descending.

---

## Expression Language

### Operators

| Category | Operators |
|----------|-----------|
| Comparison | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Boolean | `&&`, `\|\|`, `!` |
| Null coalescing | `??` |
| Grouping | `( )` |
| Property access | `.`, `[]` |

### Precedence (high to low)

`()` → `.` `[]` → `!` `-`(unary) → `*` `/` `%` → `+` `-` → `<` `<=` `>` `>=` → `==` `!=` → `&&` → `||` → `??`

### String methods

`.length`, `.contains(str)`, `.containsAll(...)`, `.containsAny(...)`, `.startsWith(str)`, `.endsWith(str)`, `.isEmpty()`, `.lower()`, `.upper()`, `.title()`, `.trim()`, `.slice(start, end?)`, `.split(sep)`, `.replace(old, new)` (replaces ALL), `.repeat(n)`, `.reverse()`, `.matches(regex)`

### List methods

`.length`, `.contains(val)`, `.containsAll(...)`, `.containsAny(...)`, `.isEmpty()`, `[index]`, `.filter(expr)`, `.map(expr)`, `.reduce(expr, init)`, `.flat()`, `.reverse()`, `.slice(start, end?)`, `.sort()`, `.unique()`, `.join(sep)`

In `filter`/`map`/`reduce`: `value` = current element, `index` = position, `acc` = accumulator.

### File properties

`file.name`, `file.basename`, `file.path`, `file.folder`, `file.ext`, `file.size`, `file.ctime`, `file.mtime`, `file.body`, `file.links`, `file.backlinks`, `file.tags`, `file.properties`, `file.embeds`

### Date/time

Functions: `now()`, `today()`, `date("YYYY-MM-DD")`, `datetime("...")`, `duration("7d")`

Components: `.year`, `.month`, `.day`, `.hour`, `.minute`, `.second`, `.dayOfWeek`

Arithmetic: `due_date + "7d"`, `now() - "1h"`, `date_a - date_b` (returns milliseconds)

Duration units: `y`/`years`, `M`/`months`, `w`/`weeks`, `d`/`days`, `h`/`hours`, `m`/`minutes`, `s`/`seconds`

### Other functions

- `if(cond, then, else)`
- `exists(field)` — key present in raw frontmatter (even if null)
- `isEmpty(field)` — null, empty, or missing
- `default(field, value)` — fallback if null/missing
- `typeof(value)`, `value.isType("string")`
- `link.asFile()` — resolve link to file object (null-propagating, max 10 hops)
- `file.hasLink(target)`, `file.hasTag(...)`, `file.hasProperty(name)`, `file.inFolder(path)`
- `length()`, `min()`, `max()`, `sum()`, `avg()`, `count()`

### Error handling in expressions

- Property access on null → null
- Method call on null → null
- Division by zero → null + `type_error`
- Type mismatch → null + `type_error`
- Errors don't abort queries; file is just excluded from results

---

## CRUD Operations

### Create

1. Determine type(s)
2. Apply defaults (to effective record, not necessarily persisted)
3. Generate values (ulid, uuid, now, etc.)
4. Validate
5. Determine path (explicit, or from `filename_pattern`)
6. Check no file exists at path
7. Write atomically (temp file + rename)
8. Include all explicitly provided fields and generated fields
9. Omit default-only fields unless caller requests materialization

### Read

1. Parse frontmatter and body
2. Determine types (explicit → match rules → untyped)
3. Validate
4. Return effective frontmatter (defaults applied, computed excluded)

### Update

1. Read existing file
2. Merge field updates (new fields added, existing replaced, explicit null removes/writes null per setting)
3. Update `now_on_write` generated fields
4. Apply defaults to effective record
5. Validate
6. Write atomically, preserving formatting

### Delete

1. Check existence
2. Optionally warn about backlinks
3. Delete from filesystem

### Rename

1. Validate both paths
2. Rename file
3. If `rename_update_refs`: update all references in frontmatter links AND body links
4. Preserve link style (wikilink stays wikilink, relative stays relative)
5. Report partial failures

### Concurrency

Use optimistic concurrency: read mtime, check before write, abort with `concurrent_modification` if changed.

---

## Link Resolution Algorithm

Given a link value and the containing file's path:

1. **Parse** into components (target, alias, anchor, format, is_relative)
2. **Markdown/path format**: resolve relative to containing file's directory (or root if starts with `/`)
3. **Wikilink with `./`, `../`**: resolve relative to containing file
4. **Wikilink with `/`**: resolve from root (but no relative prefix)
5. **Wikilink with path separators** (no relative prefix): resolve from root
6. **Simple name wikilink** (no `/`, no relative prefix):
   - If link field has `target` constraint, scope to that type's files
   - Search by `id_field` first → exact one match resolves
   - Then search by filename → tiebreakers: same directory → shortest path → alphabetical
7. **Extension handling**: try configured extensions (.md, .mdx, etc.)
8. **Path traversal check**: resolved path must stay within collection root

---

## Error Codes

### Validation
`missing_required`, `type_mismatch`, `constraint_violation`, `invalid_enum`, `unknown_field`, `deprecated_field`, `duplicate_id`, `duplicate_value`

### Lists
`list_too_short`, `list_too_long`, `list_duplicate`, `list_item_invalid`

### Strings
`string_too_short`, `string_too_long`, `pattern_mismatch`

### Numbers
`number_too_small`, `number_too_large`, `not_integer`

### Links
`invalid_link`, `link_not_found`, `link_wrong_type`, `ambiguous_link`

### Dates
`invalid_date`, `invalid_datetime`, `invalid_time`

### Types
`unknown_type`, `circular_inheritance`, `missing_parent_type`, `type_conflict`, `invalid_type_definition`, `circular_computed`

### Operations
`file_not_found`, `path_conflict`, `path_required`, `invalid_path`, `invalid_frontmatter`, `validation_failed`, `permission_denied`, `concurrent_modification`, `path_traversal`, `rename_ref_update_failed`

### Config
`invalid_config`, `missing_config`, `unsupported_version`

### Expressions
`invalid_expression`, `unknown_function`, `wrong_argument_count`, `type_error`, `expression_depth_exceeded`
