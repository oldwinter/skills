# JMESPath Query Reference for AWS CLI

JMESPath is a query language for JSON used with `--query` parameter in AWS CLI.

## Basic Syntax

### Selecting Fields

```bash
# Single field
--query 'Reservations'

# Nested field
--query 'Reservations[].Instances[]'

# Multiple fields (projection)
--query 'Reservations[].Instances[].[InstanceId,State.Name]'

# Named fields (hash/object projection)
--query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}'
```

### Filtering

```bash
# Filter by value
--query 'Reservations[].Instances[?State.Name==`running`]'

# Filter with contains
--query 'Reservations[].Instances[?contains(Tags[].Value, `production`)]'

# Filter with starts_with
--query 'SecurityGroups[?starts_with(GroupName, `prod-`)]'

# Multiple conditions (AND)
--query 'Reservations[].Instances[?State.Name==`running` && InstanceType==`t3.medium`]'

# OR condition
--query 'Reservations[].Instances[?State.Name==`running` || State.Name==`pending`]'

# NOT condition
--query 'Reservations[].Instances[?State.Name!=`terminated`]'
```

### Sorting

```bash
# Sort by field
--query 'sort_by(Images, &CreationDate)'

# Sort descending (reverse)
--query 'reverse(sort_by(Images, &CreationDate))'

# Get latest item
--query 'sort_by(Images, &CreationDate) | [-1]'

# Get first N items
--query 'sort_by(Images, &CreationDate) | [-5:]'
```

### Functions

```bash
# Length/count
--query 'length(Reservations[].Instances[])'

# Max/Min
--query 'max_by(Images, &CreationDate)'
--query 'min_by(Images, &CreationDate)'

# Keys
--query 'keys(SecurityGroups[0])'

# Join strings
--query 'join(`, `, Reservations[].Instances[].InstanceId)'

# Type conversion
--query 'to_string(length(Reservations))'
```

### Working with Tags

```bash
# Get specific tag value
--query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value | [0]]'

# Filter by tag
--query 'Reservations[].Instances[?Tags[?Key==`Environment` && Value==`production`]]'

# Multiple tag values
--query 'Reservations[].Instances[].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],Env:Tags[?Key==`Environment`].Value|[0]}'
```

## Common Query Patterns

### EC2

```bash
# Running instances with name
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name==`running`].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],Type:InstanceType,IP:PrivateIpAddress}' \
  --output table

# Instances by tag
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?Tags[?Key==`Environment` && Value==`production`]].[InstanceId,InstanceType]' \
  --output table
```

### S3

```bash
# Buckets sorted by name
aws s3api list-buckets --query 'sort_by(Buckets, &Name)[].[Name,CreationDate]' --output table

# Bucket count
aws s3api list-buckets --query 'length(Buckets)'
```

### RDS

```bash
# Available instances
aws rds describe-db-instances \
  --query 'DBInstances[?DBInstanceStatus==`available`].[DBInstanceIdentifier,Engine,DBInstanceClass]' \
  --output table
```

### ECS

```bash
# Services with desired count > 0
aws ecs describe-services --cluster <cluster> --services <svc1> <svc2> \
  --query 'services[?desiredCount>`0`].[serviceName,runningCount,desiredCount]' \
  --output table
```

### CloudWatch Logs

```bash
# Log groups over 1GB
aws logs describe-log-groups \
  --query 'logGroups[?storedBytes>`1073741824`].[logGroupName,storedBytes]' \
  --output table
```

## Pipe Expressions

Chain operations with `|`:

```bash
# Flatten, filter, then select fields
--query 'Reservations[].Instances[] | [?State.Name==`running`] | [].{ID:InstanceId,Type:InstanceType}'

# Sort then get last 5
--query 'sort_by(imageDetails, &imagePushedAt) | [-5:].[imageTags[0],imagePushedAt]'
```

## Handling Null Values

```bash
# Default value for null
--query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0]||`unnamed`]'

# Filter out nulls
--query 'Reservations[].Instances[?PrivateIpAddress!=null]'
```

## Output Formats

```bash
--output table    # Human-readable table
--output json     # Full JSON (default)
--output text     # Tab-separated values
--output yaml     # YAML format
```
