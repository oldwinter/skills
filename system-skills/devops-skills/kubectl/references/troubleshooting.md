# Kubectl Troubleshooting Guide

## Pod Issues

### ImagePullBackOff / ErrImagePull

**Symptoms:**
```
NAME                     READY   STATUS             RESTARTS   AGE
myapp-xxx                0/1     ImagePullBackOff   0          5m
```

**Diagnosis:**
```bash
# Check events
k1 describe pod <pod-name> | grep -A5 Events

# Common causes:
# 1. Wrong image name/tag
# 2. Private registry without credentials
# 3. Image doesn't exist
```

**Solutions:**
```bash
# Check image name in deployment
k1 get deploy <name> -o jsonpath='{.spec.template.spec.containers[0].image}'

# Verify ECR credentials
k1 get secret ecr-credentials -o yaml

# Refresh ECR credentials
kubectl create secret docker-registry ecr-credentials \
  --namespace <ns> \
  --docker-server=830101142436.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-1) \
  --dry-run=client -o yaml | kubectl apply -f -
```

### CrashLoopBackOff

**Symptoms:**
```
NAME                     READY   STATUS             RESTARTS   AGE
myapp-xxx                0/1     CrashLoopBackOff   5          10m
```

**Diagnosis:**
```bash
# Check current logs
k1 logs <pod-name>

# Check previous container logs
k1 logs --previous <pod-name>

# Check exit code
k1 get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}'
```

**Common Causes:**
| Exit Code | Meaning | Common Fix |
|-----------|---------|------------|
| 0 | Success (but restarted) | Check liveness probe |
| 1 | Application error | Check app logs |
| 137 | OOMKilled | Increase memory limits |
| 143 | SIGTERM | Graceful shutdown issue |

### Pending

**Symptoms:**
```
NAME                     READY   STATUS    RESTARTS   AGE
myapp-xxx                0/1     Pending   0          10m
```

**Diagnosis:**
```bash
# Check events
k1 describe pod <pod-name> | grep -A10 Events

# Check node resources
k1 describe nodes | grep -A5 "Allocated resources"

# Check if PVC is pending
k1 get pvc
```

**Common Causes:**
- Insufficient CPU/memory on nodes
- Node selector/affinity not matching
- PVC not bound
- Taints preventing scheduling

### OOMKilled

**Diagnosis:**
```bash
# Check if OOM killed
k1 get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'

# Check memory usage before crash
k1 top pod <pod-name>

# Check memory limits
k1 get pod <pod-name> -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

**Solution:**
```bash
# Increase memory limit in deployment
k1 patch deployment <name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container>","resources":{"limits":{"memory":"512Mi"}}}]}}}}'
```

## Service Issues

### Service Has No Endpoints

**Diagnosis:**
```bash
# Check endpoints
k1 get endpoints <service-name>

# Check service selector
k1 get svc <service-name> -o jsonpath='{.spec.selector}'

# Check if pods have matching labels
k1 get pods --show-labels

# Verify pods are Ready
k1 get pods -l <selector>
```

**Common Causes:**
- Selector doesn't match pod labels
- Pods not in Ready state
- Pods in different namespace

### Connection Refused

**Diagnosis:**
```bash
# Check if pods are running
k1 get pods -l <selector>

# Check container port
k1 get pod <pod-name> -o jsonpath='{.spec.containers[0].ports}'

# Test from within cluster
k1 exec -it <another-pod> -- curl <service>:<port>

# Check network policies
k1 get networkpolicies
```

## Deployment Issues

### Deployment Stuck

**Diagnosis:**
```bash
# Check rollout status
k1 rollout status deployment/<name>

# Check deployment events
k1 describe deployment <name>

# Check replica sets
k1 get rs -l app=<name>

# Check new pods
k1 get pods -l app=<name>
```

**Common Causes:**
- New pods failing to start
- Readiness probe failing
- Resource quota exceeded

**Solutions:**
```bash
# Rollback if needed
k1 rollout undo deployment/<name>

# Check quota
k1 get resourcequota

# Force restart
k1 rollout restart deployment/<name>
```

### Rollout Undo Not Working

```bash
# Check revision history
k1 rollout history deployment/<name>

# Rollback to specific revision
k1 rollout undo deployment/<name> --to-revision=<n>

# Verify the rollback
k1 rollout status deployment/<name>
```

## Node Issues

### Node NotReady

**Diagnosis:**
```bash
# Check node status
k1 get nodes

# Check node conditions
k1 describe node <node-name> | grep -A20 Conditions

# Check kubelet logs (if accessible)
# For EKS, check CloudWatch logs
```

**Common Causes:**
- Kubelet not running
- Network issues
- Disk pressure
- Memory pressure

### Evicted Pods

**Diagnosis:**
```bash
# Find evicted pods
k1 get pods --field-selector=status.phase=Failed

# Check eviction reason
k1 describe pod <evicted-pod> | grep -A5 "Status:"

# Check node pressure
k1 describe node <node> | grep -A5 Conditions
```

**Cleanup:**
```bash
# Delete evicted pods
k1 delete pods --field-selector=status.phase=Failed
```

## Resource Issues

### High CPU/Memory Usage

**Diagnosis:**
```bash
# Pod resource usage
k1 top pods --sort-by=cpu
k1 top pods --sort-by=memory

# Node resource usage
k1 top nodes

# Check limits vs actual
k1 get pods -o custom-columns="NAME:.metadata.name,CPU_REQ:.spec.containers[0].resources.requests.cpu,CPU_LIM:.spec.containers[0].resources.limits.cpu,MEM_REQ:.spec.containers[0].resources.requests.memory,MEM_LIM:.spec.containers[0].resources.limits.memory"
```

### HPA Not Scaling

**Diagnosis:**
```bash
# Check HPA status
k1 get hpa
k1 describe hpa <name>

# Check metrics-server
k1 get pods -n kube-system | grep metrics-server

# Check current metrics
k1 top pods
```

**Common Causes:**
- Metrics server not running
- No resource requests defined
- Min replicas reached
- Target metric not available

## ConfigMap/Secret Issues

### ConfigMap Changes Not Applied

**Note:** Pods don't automatically restart when ConfigMaps change.

**Solutions:**
```bash
# Option 1: Restart deployment
k1 rollout restart deployment/<name>

# Option 2: Use configMapGenerator with hash suffix (in Kustomize)
# This creates new ConfigMap name on changes, triggering pod update
```

### Secret Not Mounting

**Diagnosis:**
```bash
# Check if secret exists
k1 get secret <name>

# Check pod volume mounts
k1 get pod <pod-name> -o yaml | grep -A10 volumeMounts

# Check pod events
k1 describe pod <pod-name>
```

## Quick Diagnostic Commands

```bash
# Overall cluster health
k1 get nodes
k1 get pods --all-namespaces | grep -v Running

# Recent events (sorted by time)
k1 get events --sort-by='.lastTimestamp'

# Failed pods
k1 get pods --field-selector=status.phase=Failed

# Pods with restarts
k1 get pods -o custom-columns="NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount" | awk '$2>0'

# Resource summary
k1 top nodes
k1 top pods --sort-by=memory | head -10
```
