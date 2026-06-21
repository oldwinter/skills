# JSONPath and Output Formatting Reference

## JSONPath Basics

JSONPath is used with `-o jsonpath='{...}'` to extract specific fields from kubectl output.

### Basic Syntax

```bash
# Single field
k1 get pod <name> -o jsonpath='{.metadata.name}'

# Nested field
k1 get pod <name> -o jsonpath='{.status.phase}'

# Array element
k1 get pod <name> -o jsonpath='{.spec.containers[0].name}'

# All array elements
k1 get pods -o jsonpath='{.items[*].metadata.name}'
```

### Common Patterns

#### Pod Information

```bash
# All pod names
k1 get pods -o jsonpath='{.items[*].metadata.name}'

# Pod names with newlines
k1 get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'

# Pod name and status
k1 get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# Container images
k1 get pods -o jsonpath='{.items[*].spec.containers[*].image}'

# Pod IPs
k1 get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'
```

#### Deployment Information

```bash
# Current image
k1 get deploy <name> -o jsonpath='{.spec.template.spec.containers[0].image}'

# Replicas status
k1 get deploy <name> -o jsonpath='Desired: {.spec.replicas}, Available: {.status.availableReplicas}'

# All deployment images
k1 get deploy -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.template.spec.containers[0].image}{"\n"}{end}'
```

#### Service Information

```bash
# Service ClusterIP
k1 get svc <name> -o jsonpath='{.spec.clusterIP}'

# LoadBalancer hostname
k1 get svc <name> -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# All service ports
k1 get svc <name> -o jsonpath='{range .spec.ports[*]}{.port}{":"}{.targetPort}{"\n"}{end}'
```

#### Node Information

```bash
# Node internal IPs
k1 get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.addresses[?(@.type=="InternalIP")].address}{"\n"}{end}'

# Node capacity
k1 get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}CPU:{.status.capacity.cpu}{"\t"}Mem:{.status.capacity.memory}{"\n"}{end}'
```

#### Secret Decoding

```bash
# Decode secret value
k1 get secret <name> -o jsonpath='{.data.password}' | base64 -d

# All secret keys
k1 get secret <name> -o jsonpath='{.data}' | jq 'keys'
```

### Filtering with JSONPath

```bash
# Filter by condition (pods on specific node)
k1 get pods -o jsonpath='{.items[?(@.spec.nodeName=="node-1")].metadata.name}'

# Running pods only
k1 get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'

# Containers with specific image
k1 get pods -o jsonpath='{.items[*].spec.containers[?(@.image=="nginx")].name}'
```

## Custom Columns

For tabular output with specific fields:

```bash
# Basic custom columns
k1 get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase

# With headers
k1 get pods -o custom-columns=\
"POD:.metadata.name,\
STATUS:.status.phase,\
IP:.status.podIP,\
NODE:.spec.nodeName"

# Container info
k1 get pods -o custom-columns=\
"POD:.metadata.name,\
CONTAINER:.spec.containers[0].name,\
IMAGE:.spec.containers[0].image"

# Resource requests
k1 get pods -o custom-columns=\
"POD:.metadata.name,\
CPU_REQ:.spec.containers[0].resources.requests.cpu,\
MEM_REQ:.spec.containers[0].resources.requests.memory"
```

## Go Templates

For complex formatting:

```bash
# Basic template
k1 get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'

# With conditions
k1 get pods -o go-template='{{range .items}}{{if eq .status.phase "Running"}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}'

# Formatted table
k1 get pods -o go-template='{{range .items}}{{printf "%-40s %-10s\n" .metadata.name .status.phase}}{{end}}'
```

## Sorting Output

```bash
# Sort by creation time
k1 get pods --sort-by=.metadata.creationTimestamp

# Sort by restart count
k1 get pods --sort-by=.status.containerStatuses[0].restartCount

# Sort by name
k1 get pods --sort-by=.metadata.name
```

## Combining with Shell Tools

```bash
# Count pods per status
k1 get pods -o jsonpath='{.items[*].status.phase}' | tr ' ' '\n' | sort | uniq -c

# Find pods using most memory (combine with top)
k1 top pods --no-headers | sort -k3 -h | tail -5

# Export as CSV
k1 get pods -o jsonpath='{range .items[*]}{.metadata.name},{.status.phase},{.status.podIP}{"\n"}{end}'
```

## Useful One-Liners

```bash
# All images in use
k1 get pods -o jsonpath='{.items[*].spec.containers[*].image}' | tr ' ' '\n' | sort -u

# Pods with high restart count
k1 get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}' | awk '$2>3'

# Pods not Running
k1 get pods -o jsonpath='{range .items[?(@.status.phase!="Running")]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'

# Deployment rollout status
k1 get deploy -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.readyReplicas}{"/"}{.spec.replicas}{"\n"}{end}'

# PVC storage usage
k1 get pvc -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.resources.requests.storage}{"\n"}{end}'
```
