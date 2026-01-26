# AWS CLI Troubleshooting Guide

## Common Errors and Solutions

### Authentication & Authorization

#### Error: `Unable to locate credentials`

```
Unable to locate credentials. You can configure credentials by running "aws configure".
```

**Solutions:**
1. Check AWS credentials file: `cat ~/.aws/credentials`
2. Check environment variables: `env | grep AWS`
3. Verify IAM role if on EC2/ECS
4. Run `aws configure` to set credentials

#### Error: `ExpiredToken`

```
An error occurred (ExpiredToken) when calling the X operation: The security token included in the request is expired
```

**Solutions:**
1. Refresh SSO session: `aws sso login`
2. Get new temporary credentials from STS
3. Check system time is synchronized

#### Error: `AccessDenied`

```
An error occurred (AccessDenied) when calling the X operation: User: arn:aws:iam::xxx is not authorized to perform: xxx
```

**Solutions:**
1. Check current identity: `aws sts get-caller-identity`
2. Review IAM policies attached to user/role
3. Check for explicit deny statements
4. Verify resource-based policies (S3 bucket policy, etc.)

### Region Issues

#### Error: `Could not connect to the endpoint URL`

```
Could not connect to the endpoint URL: "https://ec2.xx-xxxx-x.amazonaws.com/"
```

**Solutions:**
1. Verify region is valid: `aws ec2 describe-regions --query 'Regions[].RegionName'`
2. Set correct region: `--region us-east-1`
3. Check network connectivity
4. Verify VPC endpoints if in private subnet

#### Error: Resource not found (wrong region)

```
An error occurred (ResourceNotFoundException) when calling the X operation
```

**Solutions:**
1. Confirm resource region with console
2. List resources across regions with loop
3. Use `--region` parameter explicitly

### Service-Specific Errors

#### S3: `NoSuchBucket`

```bash
# Verify bucket exists and check region
aws s3api head-bucket --bucket <bucket-name> 2>&1

# List all buckets
aws s3 ls
```

#### EC2: `InvalidInstanceID.NotFound`

```bash
# Verify instance exists
aws ec2 describe-instances --instance-ids <id> --query 'Reservations[].Instances[].State.Name'

# Check if terminated (terminated instances disappear after ~1 hour)
aws ec2 describe-instances --filters "Name=instance-state-name,Values=terminated" --query 'Reservations[].Instances[].InstanceId'
```

#### ECS: `ClusterNotFoundException`

```bash
# List available clusters
aws ecs list-clusters

# Check cluster status
aws ecs describe-clusters --clusters <cluster-name>
```

#### RDS: `DBInstanceNotFound`

```bash
# List all DB instances
aws rds describe-db-instances --query 'DBInstances[].DBInstanceIdentifier'

# Check if instance is being deleted
aws rds describe-db-instances --db-instance-identifier <id> --query 'DBInstances[].DBInstanceStatus'
```

### Rate Limiting

#### Error: `Throttling` or `Rate exceeded`

```
An error occurred (Throttling) when calling the X operation: Rate exceeded
```

**Solutions:**
1. Add delays between calls: `sleep 1`
2. Implement exponential backoff
3. Use pagination for large result sets
4. Request service limit increase

### Pagination Issues

#### Incomplete Results

Many AWS commands paginate by default. Use `--no-paginate` carefully.

```bash
# Get all results (handles pagination automatically)
aws s3api list-objects-v2 --bucket <bucket>

# Manual pagination
aws s3api list-objects-v2 --bucket <bucket> --max-items 1000 --starting-token <token>
```

### JSON/Query Errors

#### Error: `Invalid JSON`

```bash
# Validate JSON before sending
echo '{"key": "value"}' | jq .

# Use heredoc for complex JSON
aws lambda invoke --payload "$(cat <<'EOF'
{
  "key": "value"
}
EOF
)" output.json
```

#### Error: `Bad value for --query`

```bash
# Test JMESPath queries with jp or jq
aws ec2 describe-instances | jp "Reservations[].Instances[]"

# Escape backticks in strings
--query 'Instances[?State.Name==`running`]'  # Note: backticks, not quotes
```

## Debugging Commands

### Verbose Output

```bash
# Debug mode
aws ec2 describe-instances --debug

# Show HTTP requests/responses
aws ec2 describe-instances --debug 2>&1 | grep -E '(DEBUG|Request|Response)'
```

### Check Configuration

```bash
# Current configuration
aws configure list

# All profiles
cat ~/.aws/config

# Environment overrides
env | grep -E '^AWS_'
```

### Validate Credentials

```bash
# Who am I?
aws sts get-caller-identity

# Test specific permission
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::xxx:user/xxx \
  --action-names ec2:DescribeInstances
```

## Performance Tips

### Use Filters Server-Side

```bash
# Bad: fetch all, filter locally
aws ec2 describe-instances | jq '.Reservations[].Instances[] | select(.State.Name=="running")'

# Good: filter server-side
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
```

### Limit Output Fields

```bash
# Bad: fetch everything
aws ec2 describe-instances

# Good: only needed fields
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'
```

### Use Specific Resource IDs

```bash
# Bad: describe all
aws ec2 describe-instances

# Good: specific instances
aws ec2 describe-instances --instance-ids i-xxx i-yyy
```
