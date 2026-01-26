# GitHub CLI Complete Command Reference

This reference provides detailed documentation for all `gh` CLI commands with full flag options.

## Repository Commands

### gh repo list

```bash
gh repo list [<owner>] [flags]

Flags:
  --archived          Show only archived repositories
  --fork              Show only forks
  --json <fields>     Output JSON with specified fields
  -q, --jq <expr>     Filter JSON output using jq syntax
  -L, --limit <int>   Maximum number of repositories (default 30)
  --no-archived       Omit archived repositories
  --source            Show only non-forks
  -t, --template <s>  Format output using Go template
  --topic <strings>   Filter by topic
  --visibility <s>    Filter by visibility: public, private, internal
```

### gh repo create

```bash
gh repo create [<name>] [flags]

Flags:
  --add-readme             Add a README file
  -c, --clone              Clone the new repository locally
  -d, --description <s>    Repository description
  --disable-issues         Disable issues
  --disable-wiki           Disable wiki
  -g, --gitignore <s>      Specify gitignore template
  -h, --homepage <URL>     Repository homepage URL
  --include-all-branches   Include all branches from template
  --internal               Make internal (Enterprise only)
  -l, --license <s>        Specify license
  --private                Make private
  --public                 Make public
  --push                   Push local commits to new remote
  -r, --remote <s>         Specify remote name (default "origin")
  -s, --source <s>         Path to local repository
  -t, --team <s>           Organization team with access
  -p, --template <repo>    Create from template repository
```

### gh repo clone

```bash
gh repo clone <repository> [<directory>] [-- <gitflags>...]

Examples:
  gh repo clone owner/repo
  gh repo clone owner/repo my-directory
  gh repo clone owner/repo -- --depth 1 --single-branch
```

### gh repo fork

```bash
gh repo fork [<repository>] [flags]

Flags:
  --clone                Clone fork locally
  --default-branch-only  Only include default branch
  --fork-name <s>        Rename the fork
  --org <s>              Fork to organization
  --remote               Add remote for fork
  --remote-name <s>      Name for new remote (default "origin")
```

### gh repo view

```bash
gh repo view [<repository>] [flags]

Flags:
  -b, --branch <s>    View specific branch
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
  -w, --web           Open in browser
```

### gh repo edit

```bash
gh repo edit [<repository>] [flags]

Flags:
  --add-topic <ss>           Add topics
  --allow-forking            Allow forking (org repos)
  --allow-update-branch      Allow update branch button
  --default-branch <s>       Set default branch
  --delete-branch-on-merge   Auto-delete merged branches
  --description <s>          Set description
  --enable-auto-merge        Enable auto-merge
  --enable-discussions       Enable discussions
  --enable-issues            Enable issues
  --enable-merge-commit      Allow merge commits
  --enable-projects          Enable projects
  --enable-rebase-merge      Allow rebase merging
  --enable-squash-merge      Allow squash merging
  --enable-wiki              Enable wiki
  --homepage <URL>           Set homepage
  --remove-topic <ss>        Remove topics
  --template                 Make template repository
  --visibility <s>           Set visibility
```

### gh repo delete

```bash
gh repo delete [<repository>] [flags]

Flags:
  --yes    Confirm deletion without prompting
```

### gh repo archive / unarchive

```bash
gh repo archive [<repository>] [flags]
gh repo unarchive [<repository>] [flags]

Flags:
  -y, --yes    Skip confirmation prompt
```

### gh repo rename

```bash
gh repo rename [<new-name>] [flags]

Flags:
  -y, --yes    Skip confirmation prompt
```

### gh repo sync

```bash
gh repo sync [<destination-repository>] [flags]

Flags:
  -b, --branch <s>    Branch to sync (default: main)
  --force             Force sync (overwrite destination)
  -s, --source <s>    Source repository
```

## Pull Request Commands

### gh pr list

```bash
gh pr list [flags]

Flags:
  -a, --assignee <s>    Filter by assignee
  -A, --author <s>      Filter by author
  -B, --base <s>        Filter by base branch
  -d, --draft           Filter draft PRs
  -H, --head <s>        Filter by head branch
  --json <fields>       Output JSON
  -q, --jq <expr>       Filter JSON
  -l, --label <ss>      Filter by labels
  -L, --limit <int>     Maximum number (default 30)
  -S, --search <query>  Search query
  -s, --state <s>       Filter by state: open, closed, merged, all
  -t, --template <s>    Format with Go template
  -w, --web             Open in browser
```

### gh pr create

```bash
gh pr create [flags]

Flags:
  -a, --assignee <ss>      Assign users
  -B, --base <s>           Base branch
  -b, --body <s>           PR body
  -F, --body-file <file>   Read body from file
  -d, --draft              Create as draft
  -f, --fill               Auto-fill title/body from commits
  --fill-first             Fill from first commit only
  --fill-verbose           Fill with commit body
  -H, --head <s>           Head branch
  -l, --label <ss>         Add labels
  -m, --milestone <s>      Add to milestone
  --no-maintainer-edit     Disallow maintainer edits
  -p, --project <ss>       Add to projects
  --recover <s>            Recover from failed create
  -r, --reviewer <ss>      Request reviewers
  -t, --title <s>          PR title
  -w, --web                Open in browser after create
```

### gh pr view

```bash
gh pr view [<number> | <url> | <branch>] [flags]

Flags:
  -c, --comments      Show comments
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
  -w, --web           Open in browser
```

### gh pr checkout

```bash
gh pr checkout {<number> | <url> | <branch>} [flags]

Flags:
  -b, --branch <s>         Local branch name
  --detach                 Checkout in detached HEAD
  -f, --force              Force checkout
  --recurse-submodules     Update submodules
```

### gh pr merge

```bash
gh pr merge [<number> | <url> | <branch>] [flags]

Flags:
  --admin               Use admin privileges
  --auto                Enable auto-merge
  -b, --body <s>        Merge commit body
  -F, --body-file <f>   Read body from file
  -d, --delete-branch   Delete branch after merge
  --disable-auto        Disable auto-merge
  --match-head-commit   Require HEAD match
  -m, --merge           Merge commit
  -r, --rebase          Rebase and merge
  -s, --squash          Squash and merge
  -t, --subject <s>     Merge commit subject
```

### gh pr review

```bash
gh pr review [<number> | <url> | <branch>] [flags]

Flags:
  -a, --approve              Approve PR
  -b, --body <s>             Review body
  -F, --body-file <file>     Read body from file
  -c, --comment              Comment without approval
  -r, --request-changes      Request changes
```

### gh pr checks

```bash
gh pr checks [<number> | <url> | <branch>] [flags]

Flags:
  --fail-fast         Exit on first failed check
  -i, --interval <s>  Refresh interval (default 10s)
  --required          Only show required checks
  --watch             Watch checks progress
  -w, --web           Open in browser
```

### gh pr diff

```bash
gh pr diff [<number> | <url> | <branch>] [flags]

Flags:
  --color <s>         Color output: always, never, auto
  --name-only         Show only file names
  --patch             Display raw patch
  -w, --web           Open in browser
```

### gh pr ready

```bash
gh pr ready [<number> | <url> | <branch>] [flags]

Flags:
  --undo    Convert back to draft
```

### gh pr close / reopen

```bash
gh pr close [<number> | <url> | <branch>] [flags]
gh pr reopen [<number> | <url> | <branch>] [flags]

Flags:
  -c, --comment <s>      Add comment
  -d, --delete-branch    Delete branch (close only)
```

### gh pr edit

```bash
gh pr edit [<number> | <url> | <branch>] [flags]

Flags:
  --add-assignee <ss>       Add assignees
  --add-label <ss>          Add labels
  --add-project <ss>        Add to projects
  --add-reviewer <ss>       Add reviewers
  -B, --base <s>            Change base branch
  -b, --body <s>            Set body
  -F, --body-file <file>    Read body from file
  -m, --milestone <s>       Set milestone
  --remove-assignee <ss>    Remove assignees
  --remove-label <ss>       Remove labels
  --remove-project <ss>     Remove from projects
  --remove-reviewer <ss>    Remove reviewers
  -t, --title <s>           Set title
```

## Issue Commands

### gh issue list

```bash
gh issue list [flags]

Flags:
  -a, --assignee <s>    Filter by assignee (@me for self)
  -A, --author <s>      Filter by author
  --json <fields>       Output JSON
  -q, --jq <expr>       Filter JSON
  -l, --label <ss>      Filter by labels
  -L, --limit <int>     Maximum number (default 30)
  --mention <s>         Filter by mention
  -m, --milestone <s>   Filter by milestone
  -S, --search <query>  Search query
  -s, --state <s>       Filter by state: open, closed, all
  -t, --template <s>    Format with Go template
  -w, --web             Open in browser
```

### gh issue create

```bash
gh issue create [flags]

Flags:
  -a, --assignee <ss>      Assign users
  -b, --body <s>           Issue body
  -F, --body-file <file>   Read body from file
  -l, --label <ss>         Add labels
  -m, --milestone <s>      Add to milestone
  -p, --project <ss>       Add to projects
  --recover <s>            Recover from failed create
  -t, --title <s>          Issue title
  -w, --web                Open in browser after create
```

### gh issue view

```bash
gh issue view <number> [flags]

Flags:
  -c, --comments      Show comments
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
  -w, --web           Open in browser
```

### gh issue edit

```bash
gh issue edit <numbers>... [flags]

Flags:
  --add-assignee <ss>       Add assignees
  --add-label <ss>          Add labels
  --add-project <ss>        Add to projects
  -b, --body <s>            Set body
  -F, --body-file <file>    Read body from file
  -m, --milestone <s>       Set milestone
  --remove-assignee <ss>    Remove assignees
  --remove-label <ss>       Remove labels
  --remove-project <ss>     Remove from projects
  -t, --title <s>           Set title
```

### gh issue close / reopen

```bash
gh issue close <numbers>... [flags]
gh issue reopen <numbers>... [flags]

Close Flags:
  -c, --comment <s>    Add comment
  -r, --reason <s>     Reason: completed, not planned
```

### gh issue transfer

```bash
gh issue transfer <number> <destination-repo> [flags]
```

### gh issue pin / unpin

```bash
gh issue pin <number> [flags]
gh issue unpin <number> [flags]
```

### gh issue delete

```bash
gh issue delete <number> [flags]

Flags:
  --yes    Confirm deletion
```

## Workflow Commands

### gh workflow list

```bash
gh workflow list [flags]

Flags:
  -a, --all           Include disabled workflows
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -L, --limit <int>   Maximum number (default 50)
  -t, --template <s>  Format with Go template
```

### gh workflow view

```bash
gh workflow view [<workflow-id> | <workflow-name> | <filename>] [flags]

Flags:
  -r, --ref <s>    Branch or tag
  -w, --web        Open in browser
  -y, --yaml       View workflow YAML
```

### gh workflow run

```bash
gh workflow run [<workflow-id> | <workflow-name> | <filename>] [flags]

Flags:
  -F, --field <ss>       Workflow input (key=value)
  --json                 Read inputs from stdin as JSON
  -f, --raw-field <ss>   Workflow input string (key=value)
  -r, --ref <s>          Branch or tag to run on
```

### gh workflow enable / disable

```bash
gh workflow enable [<workflow-id> | <workflow-name> | <filename>]
gh workflow disable [<workflow-id> | <workflow-name> | <filename>]
```

### gh run list

```bash
gh run list [flags]

Flags:
  -b, --branch <s>       Filter by branch
  -c, --commit <SHA>     Filter by commit
  --created <date>       Filter by creation date
  -e, --event <s>        Filter by event
  --json <fields>        Output JSON
  -q, --jq <expr>        Filter JSON
  -L, --limit <int>      Maximum number (default 20)
  -s, --status <s>       Filter by status
  -t, --template <s>     Format with Go template
  -u, --user <s>         Filter by user
  -w, --workflow <s>     Filter by workflow
```

### gh run view

```bash
gh run view [<run-id>] [flags]

Flags:
  -a, --attempt <int>    View specific attempt
  --exit-status          Exit with run status code
  -j, --job <s>          View specific job
  --json <fields>        Output JSON
  -q, --jq <expr>        Filter JSON
  --log                  View full log
  --log-failed           View failed step logs
  -t, --template <s>     Format with Go template
  -v, --verbose          Show job steps
  -w, --web              Open in browser
```

### gh run watch

```bash
gh run watch [<run-id>] [flags]

Flags:
  --exit-status          Exit with run status code
  -i, --interval <int>   Refresh interval (default 3s)
```

### gh run rerun

```bash
gh run rerun [<run-id>] [flags]

Flags:
  -d, --debug     Enable debug logging
  --failed        Rerun only failed jobs
  -j, --job <s>   Rerun specific job
```

### gh run cancel

```bash
gh run cancel [<run-id>]
```

### gh run download

```bash
gh run download [<run-id>] [flags]

Flags:
  -D, --dir <s>       Download directory
  -n, --name <ss>     Download specific artifacts
  -p, --pattern <ss>  Download matching artifacts
```

## Release Commands

### gh release list

```bash
gh release list [flags]

Flags:
  --exclude-drafts       Exclude drafts
  --exclude-pre-releases Exclude pre-releases
  --json <fields>        Output JSON
  -q, --jq <expr>        Filter JSON
  -L, --limit <int>      Maximum number (default 30)
  -t, --template <s>     Format with Go template
```

### gh release create

```bash
gh release create <tag> [<files>...] [flags]

Flags:
  --discussion-category <s>   Create discussion
  -d, --draft                 Create as draft
  --generate-notes            Auto-generate notes
  --latest                    Mark as latest
  -n, --notes <s>             Release notes
  -F, --notes-file <file>     Read notes from file
  --notes-start-tag <s>       Start tag for notes
  -p, --prerelease            Mark as pre-release
  --target <s>                Target branch/commit
  -t, --title <s>             Release title
  --verify-tag                Verify tag exists
```

### gh release view

```bash
gh release view [<tag>] [flags]

Flags:
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
  -w, --web           Open in browser
```

### gh release edit

```bash
gh release edit <tag> [flags]

Flags:
  --discussion-category <s>   Set discussion category
  --draft                     Set draft status
  --latest                    Set as latest
  -n, --notes <s>             Set notes
  -F, --notes-file <file>     Read notes from file
  --prerelease                Set prerelease status
  --tag <s>                   Change tag name
  --target <s>                Change target
  -t, --title <s>             Set title
  --verify-tag                Verify tag exists
```

### gh release delete

```bash
gh release delete <tag> [flags]

Flags:
  --cleanup-tag    Delete the tag as well
  -y, --yes        Skip confirmation
```

### gh release download

```bash
gh release download [<tag>] [flags]

Flags:
  -A, --archive <format>    Download archive: zip, tar.gz
  --clobber                 Overwrite existing files
  -D, --dir <s>             Download directory
  -O, --output <s>          Output file name
  -p, --pattern <ss>        Download matching assets
  --skip-existing           Skip existing files
```

### gh release upload

```bash
gh release upload <tag> <files>... [flags]

Flags:
  --clobber    Overwrite existing assets
```

## Gist Commands

### gh gist list

```bash
gh gist list [flags]

Flags:
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -L, --limit <int>   Maximum number (default 10)
  --public            Show only public gists
  --secret            Show only secret gists
  -t, --template <s>  Format with Go template
```

### gh gist create

```bash
gh gist create [<filename>...] [flags]

Flags:
  -d, --desc <s>      Gist description
  -f, --filename <s>  Filename for stdin content
  -p, --public        Make public
  -w, --web           Open in browser
```

### gh gist view

```bash
gh gist view [<id> | <url>] [flags]

Flags:
  -f, --filename <s>  View specific file
  --files             List files only
  -r, --raw           Raw output
  -w, --web           Open in browser
```

### gh gist edit

```bash
gh gist edit <id> [<filename>] [flags]

Flags:
  -a, --add <s>        Add file
  -d, --desc <s>       Update description
  -f, --filename <s>   Edit specific file
  -r, --remove <s>     Remove file
```

### gh gist clone

```bash
gh gist clone <id> [<directory>] [-- <gitflags>...]
```

### gh gist delete

```bash
gh gist delete <id>
```

## API Commands

### gh api

```bash
gh api <endpoint> [flags]

Flags:
  --cache <duration>      Cache response
  -F, --field <ss>        Typed parameter (key=value)
  -H, --header <ss>       HTTP headers
  --hostname <s>          GitHub hostname
  -i, --include           Include response headers
  --input <file>          Read body from file
  -q, --jq <expr>         Filter JSON response
  -X, --method <s>        HTTP method (default GET)
  --paginate              Fetch all pages
  -p, --preview <ss>      API preview features
  -f, --raw-field <ss>    String parameter
  --silent                No output
  --slurp                 Slurp paginated output
  -t, --template <s>      Format with Go template
  --verbose               Include request/response
```

## Label Commands

### gh label list

```bash
gh label list [flags]

Flags:
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -L, --limit <int>   Maximum number (default 30)
  --order <s>         Order: asc, desc
  -S, --search <s>    Search labels
  --sort <s>          Sort: created, name
  -t, --template <s>  Format with Go template
  -w, --web           Open in browser
```

### gh label create

```bash
gh label create <name> [flags]

Flags:
  -c, --color <s>        Label color (hex without #)
  -d, --description <s>  Label description
  -f, --force            Update if exists
```

### gh label edit

```bash
gh label edit <name> [flags]

Flags:
  -c, --color <s>        New color
  -d, --description <s>  New description
  -n, --name <s>         New name
```

### gh label delete

```bash
gh label delete <name> [flags]

Flags:
  --yes    Confirm deletion
```

### gh label clone

```bash
gh label clone <source-repository> [flags]

Flags:
  -f, --force    Overwrite existing labels
```

## Search Commands

### gh search repos

```bash
gh search repos [<query>] [flags]

Flags:
  --archived              Filter archived
  --created <date>        Filter by creation date
  --followers <s>         Filter by followers count
  --forks <s>             Filter by forks count
  --good-first-issues <s> Filter by good first issues
  --help-wanted-issues <s> Filter by help wanted issues
  --include-forks <s>     Include forks: false, true, only
  --json <fields>         Output JSON
  -q, --jq <expr>         Filter JSON
  --language <s>          Filter by language
  --license <ss>          Filter by license
  -L, --limit <int>       Maximum number (default 30)
  --match <ss>            Match in: name, description, readme
  --number-topics <s>     Filter by topic count
  --order <s>             Order: asc, desc
  --owner <ss>            Filter by owner
  --size <s>              Filter by size (KB)
  --sort <s>              Sort: stars, forks, etc.
  --stars <s>             Filter by stars
  -t, --template <s>      Format with Go template
  --topic <ss>            Filter by topic
  --updated <date>        Filter by update date
  --visibility <s>        Filter by visibility
  -w, --web               Open in browser
```

### gh search issues

```bash
gh search issues [<query>] [flags]

Similar flags to search repos, plus:
  --app <s>               Filter by app author
  -a, --assignee <s>      Filter by assignee
  --author <s>            Filter by author
  --closed <date>         Filter by close date
  --commenter <s>         Filter by commenter
  --comments <s>          Filter by comments count
  --created <date>        Filter by creation date
  --include-prs           Include pull requests
  --interactions <s>      Filter by interactions
  --involves <s>          Filter by involvement
  -l, --label <ss>        Filter by labels
  --mentions <s>          Filter by mentions
  -m, --milestone <s>     Filter by milestone
  --no-assignee           No assignee
  --no-label              No labels
  --no-milestone          No milestone
  --no-project            No project
  --project <s>           Filter by project
  --reactions <s>         Filter by reactions
  --state <s>             Filter by state
  --team-mentions <s>     Filter by team mentions
  --updated <date>        Filter by update date
```

### gh search prs

```bash
gh search prs [<query>] [flags]

Similar to search issues, plus:
  -B, --base <s>          Filter by base branch
  --checks <s>            Filter by checks status
  --draft                 Filter drafts
  -H, --head <s>          Filter by head branch
  --merged                Filter merged
  --merged-at <date>      Filter by merge date
  --review <s>            Filter by review status
  --review-requested <s>  Filter by requested reviewer
  --reviewed-by <s>       Filter by reviewer
```

### gh search commits

```bash
gh search commits [<query>] [flags]

Flags:
  --author <s>            Filter by author
  --author-date <date>    Filter by author date
  --author-email <s>      Filter by author email
  --author-name <s>       Filter by author name
  --committer <s>         Filter by committer
  --committer-date <date> Filter by committer date
  --committer-email <s>   Filter by committer email
  --committer-name <s>    Filter by committer name
  --hash <s>              Filter by commit hash
  --merge                 Filter merge commits
  --order <s>             Order: asc, desc
  --owner <s>             Filter by owner
  --parent <s>            Filter by parent hash
  --repo <ss>             Filter by repo
  --sort <s>              Sort: author-date, committer-date
  --tree <s>              Filter by tree hash
  --visibility <s>        Filter by visibility
```

### gh search code

```bash
gh search code <query> [flags]

Flags:
  --extension <s>         Filter by extension
  --filename <s>          Filter by filename
  --json <fields>         Output JSON
  -q, --jq <expr>         Filter JSON
  --language <s>          Filter by language
  -L, --limit <int>       Maximum number
  --match <ss>            Match in: file, path
  --owner <s>             Filter by owner
  --path <s>              Filter by path
  --repo <ss>             Filter by repo
  --size <s>              Filter by size
  -t, --template <s>      Format with Go template
  -w, --web               Open in browser
```

## SSH Key Commands

### gh ssh-key list

```bash
gh ssh-key list [flags]

Flags:
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
```

### gh ssh-key add

```bash
gh ssh-key add [<key-file>] [flags]

Flags:
  -t, --title <s>    Key title
  --type <s>         Key type: authentication, signing
```

### gh ssh-key delete

```bash
gh ssh-key delete <id> [flags]

Flags:
  -y, --yes    Skip confirmation
```

## GPG Key Commands

### gh gpg-key list

```bash
gh gpg-key list [flags]

Flags:
  --json <fields>     Output JSON
  -q, --jq <expr>     Filter JSON
  -t, --template <s>  Format with Go template
```

### gh gpg-key add

```bash
gh gpg-key add [<key-file>]
```

### gh gpg-key delete

```bash
gh gpg-key delete <key-id> [flags]

Flags:
  -y, --yes    Skip confirmation
```

## Authentication Commands

### gh auth status

```bash
gh auth status [flags]

Flags:
  -h, --hostname <s>    Check specific host
  -t, --show-token      Display auth token
```

### gh auth login

```bash
gh auth login [flags]

Flags:
  -h, --hostname <s>         GitHub hostname
  -p, --git-protocol <s>     Protocol: https, ssh
  --insecure-storage         Store token in plain text
  -s, --scopes <ss>          Additional scopes
  --skip-ssh-key             Skip SSH key upload
  -w, --web                  Open browser for auth
  --with-token               Read token from stdin
```

### gh auth logout

```bash
gh auth logout [flags]

Flags:
  -h, --hostname <s>    Logout from specific host
  -u, --user <s>        Logout specific user
```

### gh auth refresh

```bash
gh auth refresh [flags]

Flags:
  -h, --hostname <s>         Refresh for specific host
  --insecure-storage         Store in plain text
  -r, --remove-scopes <ss>   Remove scopes
  --reset-scopes             Reset to default scopes
  -s, --scopes <ss>          Add scopes
```

### gh auth token

```bash
gh auth token [flags]

Flags:
  -h, --hostname <s>    Get token for specific host
  -u, --user <s>        Get token for specific user
```

### gh auth setup-git

```bash
gh auth setup-git [flags]

Flags:
  -f, --force           Force setup
  -h, --hostname <s>    Configure for specific host
```

## Configuration Commands

### gh config list

```bash
gh config list [flags]

Flags:
  -h, --host <s>    List for specific host
```

### gh config get

```bash
gh config get <key> [flags]

Flags:
  -h, --host <s>    Get for specific host
```

### gh config set

```bash
gh config set <key> <value> [flags]

Flags:
  -h, --host <s>    Set for specific host

Keys:
  git_protocol     Default protocol: https, ssh
  editor           Preferred editor
  prompt           Enable interactive prompts: enabled, disabled
  pager            Pager program
  http_unix_socket Unix socket path
  browser          Web browser
```

## Other Useful Commands

### gh browse

```bash
gh browse [<number> | <path> | <commit-SHA>] [flags]

Flags:
  -b, --branch <s>      Open specific branch
  -c, --commit          Open commit page
  -n, --no-browser      Print URL only
  -p, --projects        Open projects tab
  -r, --releases        Open releases tab
  -s, --settings        Open settings tab
  -w, --wiki            Open wiki tab
```

### gh codespace

```bash
gh codespace create [flags]
gh codespace list [flags]
gh codespace code [flags]      # Open in VS Code
gh codespace ssh [flags]       # SSH into codespace
gh codespace stop [flags]
gh codespace delete [flags]
```

### gh extension

```bash
gh extension list
gh extension install <repo>
gh extension upgrade <name>
gh extension remove <name>
gh extension browse
gh extension search [<query>]
gh extension create [<name>]
```

### gh secret

```bash
gh secret list [flags]
gh secret set <secret-name> [flags]
gh secret delete <secret-name> [flags]

Flags:
  -a, --app <s>           Target app: actions, codespaces, dependabot
  -b, --body <s>          Secret value
  -e, --env <s>           Environment name
  -f, --env-file <file>   Load from env file
  --no-store              Don't store in secret store
  -o, --org <s>           Organization name
  -r, --repos <ss>        Repository access
  -u, --user              Set user secret
  -v, --visibility <s>    Visibility: all, private, selected
```

### gh variable

```bash
gh variable list [flags]
gh variable set <variable-name> [flags]
gh variable get <variable-name> [flags]
gh variable delete <variable-name> [flags]

Flags:
  -b, --body <s>          Variable value
  -e, --env <s>           Environment name
  -f, --env-file <file>   Load from env file
  -o, --org <s>           Organization name
  -r, --repos <ss>        Repository access
  -v, --visibility <s>    Visibility: all, private, selected
```

### gh cache

```bash
gh cache list [flags]
gh cache delete <cache-id> [flags]

Flags:
  -a, --all               Delete all caches
  -B, --branch <s>        Filter by branch
  -k, --key <s>           Filter by key
  --json <fields>         Output JSON
  -L, --limit <int>       Maximum number
  --order <s>             Order: asc, desc
  -S, --sort <s>          Sort: created_at, last_accessed_at, size_in_bytes
```

### gh ruleset

```bash
gh ruleset list [flags]
gh ruleset view [<ruleset-id>] [flags]
gh ruleset check [<branch>] [flags]

Flags:
  --default               Check default branch
  -o, --org <s>           Organization name
  -w, --web               Open in browser
```

### gh status

```bash
gh status [flags]

Shows notifications, assigned issues/PRs, and review requests.

Flags:
  -e, --exclude <ss>    Exclude repos
  -o, --org <s>         Filter by org
```

### gh attestation

```bash
gh attestation verify <artifact-path> [flags]

Flags:
  --bundle-from-oci          Get bundle from OCI
  -d, --deny-self-hosted     Deny self-hosted runners
  --digest-alg <s>           Digest algorithm
  -L, --limit <int>          Maximum attestations
  --no-public-good           Skip public good instance
  -o, --owner <s>            Verify against owner
  -q, --predicate-type <s>   Filter by predicate type
  -R, --repo <s>             Verify against repo
  --signer-repo <s>          Verify signer repo
  --signer-workflow <s>      Verify signer workflow
```
