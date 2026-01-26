# Examples

## Example 1 (Flow review, cross-functional)
**Prompt:** “Use `running-design-reviews`. We have a new web onboarding flow (Figma link). Decision: choose between Flow A and Flow B to ship next sprint. Target user: first-time admin setting up a team. Constraints: must be accessible (WCAG AA), limited eng bandwidth. Run a 45-minute live review and output a Design Review Pack.”

**Expected output:** Brief with decision + requested feedback; timed agenda; feedback log categorized by Value/Ease/Delight; decision record with rationale and owners; follow-up message + next review gate.

## Example 2 (Ship-readiness review)
**Prompt:** “Run a ship-readiness design review for 12 screens in our checkout flow. We need a final pass on edge cases, error states, and microcopy before release. Output a structured checklist, a feedback log, and a decision record.”

**Expected output:** Pre-read that calls out in-scope screens/states; agenda oriented around edge cases; feedback log with severities; a clear go/no-go recommendation with risks, open questions, and next steps.

## Boundary example (when NOT to use)
**Prompt:** “Can you give me general feedback on this Dribbble shot?” (no user, no goal, no decision)

**Expected response:** Ask for the decision and target user + success criteria. If it’s purely aesthetic inspiration with no product context, decline the Design Review Pack and recommend a different critique format (or propose a lightweight visual critique template only after goals are set).

