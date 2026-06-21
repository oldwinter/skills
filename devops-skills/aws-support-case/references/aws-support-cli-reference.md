# AWS Support CLI 命令参考

## 常用命令速查

### 列出工单

```bash
# 列出所有工单（默认返回最近的工单）
aws support describe-cases

# 列出包含已解决工单的所有工单
aws support describe-cases --include-resolved-cases

# 列出特定时间范围内的工单（ISO 8601 格式）
aws support describe-cases --after-time "2024-01-01T00:00:00Z"

# 列出未解决的工单
aws support describe-cases --no-include-resolved-cases

# 分页获取更多工单（使用 next-token）
aws support describe-cases --next-token "TOKEN_FROM_PREVIOUS_RESPONSE"
```

### 查看工单详情

```bash
# 查看单个工单详情（包含通信记录）
aws support describe-cases --case-id-list "case-123456789" --include-communications

# 查看工单的所有通信记录
aws support describe-communications --case-id "case-123456789"

# 分页获取通信记录
aws support describe-communications --case-id "case-123456789" --max-results 10
```

### 创建工单

```bash
# 创建工单基本格式
aws support create-case \
  --subject "工单标题" \
  --communication-body "工单详细描述" \
  --service-code "amazon-ec2" \
  --category-code "general-guidance" \
  --severity-code "low" \
  --language "en"

# 严重程度选项（根据 Support 计划可用性不同）
# - critical: 生产系统宕机（仅 Enterprise）
# - urgent: 生产系统严重受损（Business/Enterprise）
# - high: 生产系统受损（Business/Enterprise）
# - normal: 生产系统有问题
# - low: 一般问题或咨询
```

### 回复工单

```bash
# 添加回复/通信
aws support add-communication-to-case \
  --case-id "case-123456789" \
  --communication-body "回复内容"

# 带附件回复
aws support add-communication-to-case \
  --case-id "case-123456789" \
  --communication-body "请查看附件" \
  --attachment-set-id "attachment-set-id"
```

### 附件处理

```bash
# 上传附件（先添加到附件集）
aws support add-attachments-to-set \
  --attachments fileName="screenshot.png",data="BASE64_ENCODED_DATA"

# 查看附件
aws support describe-attachment --attachment-id "attachment-id"
```

### 关闭工单

```bash
# 关闭/解决工单
aws support resolve-case --case-id "case-123456789"
```

### 查询可用服务和类别

```bash
# 获取所有可用的服务列表
aws support describe-services

# 获取特定服务的类别
aws support describe-services --service-code-list "amazon-ec2"

# 获取严重程度选项
aws support describe-severity-levels
```

## 输出格式控制

```bash
# JSON 格式（默认）
aws support describe-cases --output json

# 表格格式（适合快速浏览）
aws support describe-cases --output table

# 仅输出特定字段
aws support describe-cases --query 'cases[*].[caseId,subject,status]'
```

## 常见服务代码 (service-code)

| 服务代码 | 服务名称 |
|----------|----------|
| amazon-ec2 | Amazon EC2 |
| amazon-s3 | Amazon S3 |
| amazon-rds | Amazon RDS |
| amazon-vpc | Amazon VPC |
| aws-lambda | AWS Lambda |
| amazon-cloudfront | Amazon CloudFront |
| amazon-route53 | Amazon Route 53 |
| amazon-dynamodb | Amazon DynamoDB |
| amazon-ecs | Amazon ECS |
| amazon-eks | Amazon EKS |
| aws-iam | AWS IAM |
| amazon-cloudwatch | Amazon CloudWatch |
| aws-billing | AWS Billing |
| account-management | Account Management |

## 常见类别代码 (category-code)

| 类别代码 | 描述 |
|----------|------|
| general-guidance | 一般指导/咨询 |
| performance | 性能问题 |
| connectivity | 连接问题 |
| security | 安全相关 |
| configuration | 配置问题 |
| limits | 服务限额 |
| billing | 账单问题 |

## 注意事项

1. **区域要求**: AWS Support API 仅在 `us-east-1` 区域可用，命令需要指定 `--region us-east-1`
2. **Support 计划**: 部分功能需要 Business 或 Enterprise Support 计划
3. **权限要求**: 需要 `support:*` 相关 IAM 权限
