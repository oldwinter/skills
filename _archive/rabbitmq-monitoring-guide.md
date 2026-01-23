# RabbitMQ CloudWatch 监控告警配置指南

## Broker 信息
- **Broker Name**: k8s-prod
- **Broker ID**: b-457ff24e-033d-47c2-90c2-f4334fac25db
- **Region**: us-east-1
- **日志组**: 
  - `/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general`
  - `/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/connection`

## 发现的问题
从日志中检测到大量 **TLS 握手错误**：
- Fatal - Unexpected Message
- Fatal - Protocol Version  
- Fatal - Insufficient Security
- unsupported_record_type 错误
- no_suitable_ciphers 错误

## 监控方案

由于 Amazon MQ RabbitMQ 没有提供标准的 CloudWatch Metrics，我们使用 **Metric Filters** 从日志中提取错误并创建自定义 metrics。

### 方案 1: 使用自动化脚本（推荐）

直接运行已创建的脚本：

```bash
chmod +x setup-rabbitmq-alerts.sh
./setup-rabbitmq-alerts.sh
```

### 方案 2: 手动逐步配置

#### 步骤 1: 创建 SNS Topic（用于接收告警通知）

```bash
# 创建 SNS Topic
aws sns create-topic \
    --name rabbitmq-alerts \
    --region us-east-1

# 订阅邮箱（替换为你的邮箱）
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --protocol email \
    --notification-endpoint your-email@example.com \
    --region us-east-1
```

**注意**: 订阅后会收到确认邮件，必须点击确认链接才能生效。

#### 步骤 2: 创建 Metric Filters

##### 2.1 TLS 错误过滤器

```bash
aws logs put-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --filter-name "RabbitMQ-TLS-Errors" \
    --filter-pattern '[time, level=ERROR, ...msg="*TLS*"]' \
    --metric-transformations \
        metricName=TLSErrors,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region us-east-1
```

##### 2.2 连接错误过滤器

```bash
aws logs put-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --filter-name "RabbitMQ-Connection-Errors" \
    --filter-pattern '[time, level=ERROR, ...msg="*connection*" || msg="*accept*"]' \
    --metric-transformations \
        metricName=ConnectionErrors,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region us-east-1
```

##### 2.3 通用错误计数器

```bash
aws logs put-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --filter-name "RabbitMQ-Error-Count" \
    --filter-pattern '[time, level=ERROR, ...]' \
    --metric-transformations \
        metricName=ErrorCount,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region us-east-1
```

##### 2.4 警告计数器

```bash
aws logs put-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --filter-name "RabbitMQ-Warning-Count" \
    --filter-pattern '[time, level=WARNING, ...]' \
    --metric-transformations \
        metricName=WarningCount,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region us-east-1
```

#### 步骤 3: 创建 CloudWatch 告警

##### 3.1 TLS 错误告警（5分钟内超过10次）

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-b-457ff24e-033d-47c2-90c2-f4334fac25db-TLS-Errors" \
    --alarm-description "RabbitMQ TLS 握手错误过多" \
    --metric-name TLSErrors \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --treat-missing-data notBreaching \
    --region us-east-1
```

##### 3.2 连接错误告警（5分钟内超过5次）

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-b-457ff24e-033d-47c2-90c2-f4334fac25db-Connection-Errors" \
    --alarm-description "RabbitMQ 连接错误" \
    --metric-name ConnectionErrors \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 5 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --treat-missing-data notBreaching \
    --region us-east-1
```

##### 3.3 高错误率告警（连续2个5分钟周期内超过20次）

```bash
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-b-457ff24e-033d-47c2-90c2-f4334fac25db-High-Error-Rate" \
    --alarm-description "RabbitMQ 错误率过高" \
    --metric-name ErrorCount \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 20 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --treat-missing-data notBreaching \
    --region us-east-1
```

## 验证配置

### 查看 Metric Filters

```bash
aws logs describe-metric-filters \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --region us-east-1
```

### 查看告警状态

```bash
aws cloudwatch describe-alarms \
    --alarm-name-prefix "RabbitMQ-b-457ff24e" \
    --region us-east-1
```

### 测试 Metric Filters（可选）

```bash
# 测试过滤器是否能正确匹配日志
aws logs test-metric-filter \
    --filter-pattern '[time, level=ERROR, ...msg="*TLS*"]' \
    --log-event-messages "2024-01-15 13:36:08.123 ERROR TLS handshake failed"
```

## 查看监控数据

### CloudWatch Console

1. 前往 CloudWatch Console
2. 左侧菜单选择 "Metrics" > "All metrics"
3. 选择命名空间 `RabbitMQ/CustomMetrics`
4. 可以看到以下 metrics：
   - TLSErrors
   - ConnectionErrors
   - ErrorCount
   - WarningCount

### 使用 CloudWatch Logs Insights 查询

```sql
# 查看最近的 TLS 错误
fields @timestamp, @message
| filter @message like /TLS/ and @message like /ERROR/
| sort @timestamp desc
| limit 100
```

```sql
# 统计最近1小时的错误类型分布
fields @message
| filter @message like /ERROR/
| parse @message /ERROR.*- (?<error_type>.*)/
| stats count() by error_type
```

```sql
# 查看错误趋势（每5分钟）
fields @timestamp
| filter @message like /ERROR/
| stats count() as error_count by bin(5m)
```

## 告警阈值调整建议

根据实际业务情况，你可能需要调整告警阈值：

| 告警类型 | 当前阈值 | 调整建议 |
|---------|---------|---------|
| TLS 错误 | 5分钟内>10次 | 如果 TLS 错误是正常现象（如客户端配置问题），可以提高到 50-100 |
| 连接错误 | 5分钟内>5次 | 根据连接频率调整 |
| 高错误率 | 连续2个周期>20次 | 可调整为更严格（如>10）或更宽松（如>50）|

### 修改告警阈值示例

```bash
# 将 TLS 错误阈值提高到 50
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-b-457ff24e-033d-47c2-90c2-f4334fac25db-TLS-Errors" \
    --alarm-description "RabbitMQ TLS 握手错误过多" \
    --metric-name TLSErrors \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 50 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --treat-missing-data notBreaching \
    --region us-east-1
```

## 扩展监控（可选）

### 添加 Slack 通知

```bash
# 使用 AWS Chatbot 将告警发送到 Slack
# 需要先在 AWS Chatbot Console 中配置 Slack workspace
```

### 添加 Connection 日志监控

```bash
# 为 connection 日志组添加过滤器
aws logs put-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/connection" \
    --filter-name "RabbitMQ-Connection-Events" \
    --filter-pattern '[time, level, ...msg="*closed*" || msg="*refused*"]' \
    --metric-transformations \
        metricName=ConnectionIssues,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region us-east-1
```

## 清理命令（如需删除）

```bash
# 删除 Metric Filters
aws logs delete-metric-filter \
    --log-group-name "/aws/amazonmq/broker/b-457ff24e-033d-47c2-90c2-f4334fac25db/general" \
    --filter-name "RabbitMQ-TLS-Errors" \
    --region us-east-1

# 删除告警
aws cloudwatch delete-alarms \
    --alarm-names "RabbitMQ-b-457ff24e-033d-47c2-90c2-f4334fac25db-TLS-Errors" \
    --region us-east-1

# 删除 SNS Topic
aws sns delete-topic \
    --topic-arn arn:aws:sns:us-east-1:830101142436:rabbitmq-alerts \
    --region us-east-1
```

## 成本估算

- **CloudWatch Logs**: 基于日志存储量和查询次数
- **CloudWatch Metrics**: 自定义 metrics 前 10 个免费，之后 $0.30/metric/月
- **CloudWatch Alarms**: 前 10 个告警免费，之后 $0.10/alarm/月
- **SNS**: 前 1000 封邮件免费，之后 $2.00/100,000 封

预计月成本：**$0-2** (取决于 metrics 和告警数量)

## 故障排查

### 问题 1: Metric Filters 没有数据

**原因**: Metric Filters 只处理创建后的新日志
**解决**: 等待新的日志产生，或者生成一些测试流量

### 问题 2: 告警没有触发

**原因**: 
1. SNS 订阅未确认
2. 阈值设置过高
3. 没有足够的错误发生

**解决**:
1. 检查邮箱确认 SNS 订阅
2. 降低阈值测试
3. 查看 CloudWatch Metrics 确认有数据

### 问题 3: 收到太多告警

**解决**: 提高阈值或增加 evaluation_periods
