#!/bin/bash

# RabbitMQ CloudWatch 监控告警设置脚本
# Broker ID: b-457ff24e-033d-47c2-90c2-f4334fac25db
# Region: us-east-1

BROKER_ID="b-457ff24e-033d-47c2-90c2-f4334fac25db"
REGION="us-east-1"
LOG_GROUP="/aws/amazonmq/broker/${BROKER_ID}/general"
SNS_TOPIC_NAME="rabbitmq-alerts"

echo "设置 RabbitMQ 监控告警..."

# 1. 创建 SNS Topic 用于接收告警（如果还没有的话）
echo "步骤 1: 创建 SNS Topic..."
SNS_TOPIC_ARN=$(aws sns create-topic \
    --name ${SNS_TOPIC_NAME} \
    --region ${REGION} \
    --query 'TopicArn' \
    --output text 2>/dev/null || \
    aws sns list-topics --region ${REGION} --query "Topics[?contains(TopicArn, '${SNS_TOPIC_NAME}')].TopicArn" --output text)

echo "SNS Topic ARN: ${SNS_TOPIC_ARN}"

# 订阅邮箱（请替换为你的邮箱）
read -p "输入接收告警的邮箱地址: " EMAIL_ADDRESS
if [ -n "$EMAIL_ADDRESS" ]; then
    aws sns subscribe \
        --topic-arn ${SNS_TOPIC_ARN} \
        --protocol email \
        --notification-endpoint ${EMAIL_ADDRESS} \
        --region ${REGION}
    echo "已发送确认邮件到 ${EMAIL_ADDRESS}，请检查邮箱并确认订阅"
fi

# 2. 创建 Metric Filter - TLS 错误
echo -e "\n步骤 2: 创建 Metric Filters..."

# TLS 握手错误
aws logs put-metric-filter \
    --log-group-name ${LOG_GROUP} \
    --filter-name "RabbitMQ-TLS-Errors" \
    --filter-pattern '[time, level=ERROR, ...msg="*TLS*"]' \
    --metric-transformations \
        metricName=TLSErrors,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region ${REGION}

echo "✓ 创建了 TLS 错误 Metric Filter"

# 连接错误
aws logs put-metric-filter \
    --log-group-name ${LOG_GROUP} \
    --filter-name "RabbitMQ-Connection-Errors" \
    --filter-pattern '[time, level=ERROR, ...msg="*connection*" || msg="*accept*"]' \
    --metric-transformations \
        metricName=ConnectionErrors,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region ${REGION}

echo "✓ 创建了连接错误 Metric Filter"

# 通用错误和警告
aws logs put-metric-filter \
    --log-group-name ${LOG_GROUP} \
    --filter-name "RabbitMQ-Error-Count" \
    --filter-pattern '[time, level=ERROR, ...]' \
    --metric-transformations \
        metricName=ErrorCount,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region ${REGION}

echo "✓ 创建了通用错误 Metric Filter"

# 警告级别
aws logs put-metric-filter \
    --log-group-name ${LOG_GROUP} \
    --filter-name "RabbitMQ-Warning-Count" \
    --filter-pattern '[time, level=WARNING, ...]' \
    --metric-transformations \
        metricName=WarningCount,\
metricNamespace=RabbitMQ/CustomMetrics,\
metricValue=1,\
defaultValue=0,\
unit=Count \
    --region ${REGION}

echo "✓ 创建了警告级别 Metric Filter"

# 3. 创建 CloudWatch 告警
echo -e "\n步骤 3: 创建 CloudWatch 告警..."

# TLS 错误告警 - 5分钟内超过10次
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-${BROKER_ID}-TLS-Errors" \
    --alarm-description "RabbitMQ TLS 握手错误过多" \
    --metric-name TLSErrors \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions ${SNS_TOPIC_ARN} \
    --treat-missing-data notBreaching \
    --region ${REGION}

echo "✓ 创建了 TLS 错误告警 (阈值: 5分钟内>10次)"

# 连接错误告警 - 5分钟内超过5次
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-${BROKER_ID}-Connection-Errors" \
    --alarm-description "RabbitMQ 连接错误" \
    --metric-name ConnectionErrors \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 1 \
    --threshold 5 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions ${SNS_TOPIC_ARN} \
    --treat-missing-data notBreaching \
    --region ${REGION}

echo "✓ 创建了连接错误告警 (阈值: 5分钟内>5次)"

# 通用错误告警 - 5分钟内超过20次
aws cloudwatch put-metric-alarm \
    --alarm-name "RabbitMQ-${BROKER_ID}-High-Error-Rate" \
    --alarm-description "RabbitMQ 错误率过高" \
    --metric-name ErrorCount \
    --namespace RabbitMQ/CustomMetrics \
    --statistic Sum \
    --period 300 \
    --evaluation-periods 2 \
    --threshold 20 \
    --comparison-operator GreaterThanThreshold \
    --alarm-actions ${SNS_TOPIC_ARN} \
    --treat-missing-data notBreaching \
    --region ${REGION}

echo "✓ 创建了高错误率告警 (阈值: 连续2个5分钟周期内>20次)"

# 4. 验证设置
echo -e "\n步骤 4: 验证设置..."

echo -e "\n已配置的 Metric Filters:"
aws logs describe-metric-filters \
    --log-group-name ${LOG_GROUP} \
    --region ${REGION} \
    --query 'metricFilters[*].[filterName,metricTransformations[0].metricName]' \
    --output table

echo -e "\n已配置的告警:"
aws cloudwatch describe-alarms \
    --alarm-name-prefix "RabbitMQ-${BROKER_ID}" \
    --region ${REGION} \
    --query 'MetricAlarms[*].[AlarmName,StateValue,Threshold]' \
    --output table

echo -e "\n✅ 监控告警设置完成！"
echo "注意："
echo "1. 如果配置了邮箱订阅，请检查邮箱并确认 SNS 订阅"
echo "2. Metric Filter 需要有新的日志数据才会开始产生 metrics"
echo "3. 可以在 CloudWatch Console 查看 metrics: RabbitMQ/CustomMetrics"
echo "4. 根据实际情况调整告警阈值"
