export const meta = {
  name: 'inspect_project',
  description: 'Inspect a repository and summarize the main modules',
  phases: [
    { title: 'Scan' },
    { title: 'Analyze' }
  ]
}

phase('Scan')
const inventory = await agent('Inspect the repository structure and list important entrypoints.', {
  label: 'repo inventory'
})

phase('Analyze')
const summary = await agent('Summarize the main modules using the inventory from the previous packet.', {
  label: 'module summary'
})

return { inventory, summary }
