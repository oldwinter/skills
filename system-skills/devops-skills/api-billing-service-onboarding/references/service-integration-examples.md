# Service Integration Examples

Real-world examples of successfully integrated services.

## Example 1: Resend (Email Service)

**API Documentation**: https://resend.com/docs/api-reference/rate-limit

**Characteristics**:
- Quota in response headers (`x-resend-monthly-quota`)
- No dedicated balance endpoint
- Free plan: 100 emails/month, Pro: 50k/month

**Integration Details**:

```typescript
// adapters/resend.ts
import axios from "axios";
import { BillingMetric } from "../src/types";

export async function fetchResend(apiKey: string): Promise<BillingMetric> {
  const response = await axios.get("https://api.resend.com/api-keys", {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    }
  });

  const monthlyQuota = response.headers['x-resend-monthly-quota'];
  const dailyQuota = response.headers['x-resend-daily-quota'];

  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  const remaining = parseInt(monthlyQuota || dailyQuota || "0", 10);

  return {
    service: "resend",
    apiKeyMask,
    total: remaining,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0,
    unit: "emails"
  };
}
```

**Alarm Configuration**:
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "Resend-Low-Quota" \
  --namespace "ThirdPartyAPIBilling" \
  --metric-name "Remaining" \
  --dimensions Name=Service,Value=resend \
  --threshold 10 \
  --comparison-operator LessThanThreshold \
  --alarm-actions "arn:aws:sns:us-east-1:830101142436:CloudWatchAlarmsToFeishu"
```

**Dashboard Entry**:
- Service name: `resend`
- Display name: `Resend`
- Unit: `emails`
- Masked key: `re_WF8...7wHQzm`

---

## Example 2: OpenRouter (LLM Service)

**API Documentation**: https://openrouter.ai/docs#limits

**Characteristics**:
- Standard JSON response with balance fields
- Returns total credit and usage
- Pay-as-you-go pricing

**Integration Details**:

```typescript
// adapters/openrouter.ts
import axios from "axios";
import { BillingMetric } from "../src/types";

export async function fetchOpenRouter(
  apiKey: string,
  suffix?: string
): Promise<BillingMetric> {
  const response = await axios.get("https://openrouter.ai/api/v1/auth/key", {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    }
  });

  const { data } = response.data;
  const limit = parseFloat(data.limit) || 0;
  const usage = parseFloat(data.usage) || 0;
  const remaining = Math.max(0, limit - usage);

  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  const serviceName = suffix ? `openrouter_${suffix}` : "openrouter";

  return {
    service: serviceName,
    apiKeyMask,
    total: limit,
    remaining,
    remainingRatio: limit > 0 ? remaining / limit : 0,
    usage,
    currency: "USD"
  };
}
```

**Alarm Configuration** (Percentage-based):
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "OpenRouter-Low-Balance" \
  --metric-name "RemainingRatio" \
  --threshold 0.05 \
  --comparison-operator LessThanThreshold
```

---

## Example 3: Scrape.do (Web Scraping)

**API Documentation**: https://scrape.do/docs

**Characteristics**:
- Query parameter authentication
- Returns max and remaining requests
- Monthly quota resets

**Integration Details**:

```typescript
// adapters/scrapedo.ts
import axios from "axios";
import { BillingMetric } from "../src/types";

export async function fetchScrapeDo(apiToken: string): Promise<BillingMetric> {
  const response = await axios.get("https://api.scrape.do/info", {
    params: { token: apiToken }
  });

  const {
    MaxMonthlyRequest,
    RemainingMonthlyRequest
  } = response.data;

  const apiKeyMask = apiToken.length >= 12
    ? `${apiToken.slice(0, 6)}...${apiToken.slice(-6)}`
    : apiToken;

  const total = MaxMonthlyRequest || 0;
  const remaining = RemainingMonthlyRequest || 0;

  return {
    service: "scrapedo",
    apiKeyMask,
    total,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0,
    unit: "requests"
  };
}
```

**Alarm Configuration** (Percentage-based):
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "ScrapeDo-Low-Quota" \
  --metric-name "RemainingRatio" \
  --threshold 0.05
```

---

## Example 4: SiliconFlow (Multi-Region)

**API Documentation**: https://siliconflow.cn/docs

**Characteristics**:
- Two separate instances (China + Global)
- Different API base URLs
- CNY currency

**Integration Details**:

```typescript
// adapters/siliconflow.ts
import axios from "axios";
import { BillingMetric } from "../src/types";

interface SiliconFlowParams {
  apiKey: string;
  apiBase: string;
  serviceName: string;
}

export async function fetchSiliconFlow(
  params: SiliconFlowParams
): Promise<BillingMetric> {
  const { apiKey, apiBase, serviceName } = params;

  const response = await axios.get(`${apiBase}/user/info`, {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    }
  });

  const { balance } = response.data.data;
  const remaining = parseFloat(balance) || 0;

  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  return {
    service: serviceName,
    apiKeyMask,
    total: remaining,
    remaining,
    remainingRatio: 1,
    currency: "CNY"
  };
}
```

**Handler Usage**:
```typescript
// src/handler.ts
const metric = await adapters.siliconflow({
  apiKey: apiKeys.siliconflow_main,
  apiBase: "https://api.siliconflow.cn/v1",
  serviceName: "siliconflow_main"
});
```

---

## Example 5: Serper (Prepaid Credits)

**API Documentation**: https://serper.dev/docs

**Characteristics**:
- Prepaid credits model
- No total quota (only remaining)
- Custom header authentication

**Integration Details**:

```typescript
// adapters/serper.ts
import axios from "axios";
import { BillingMetric } from "../src/types";

export async function fetchSerper(apiKey: string): Promise<BillingMetric> {
  const response = await axios.get("https://google.serper.dev/account", {
    headers: {
      "X-API-KEY": apiKey,
      "Content-Type": "application/json"
    }
  });

  const { balance } = response.data;
  const remaining = balance || 0;

  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  return {
    service: "serper",
    apiKeyMask,
    total: remaining,  // Use remaining as total for prepaid
    remaining,
    remainingRatio: 1, // Always 1 for prepaid
    unit: "credits"
  };
}
```

**Alarm Configuration** (Absolute value):
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "Serper-Low-Credits" \
  --metric-name "Remaining" \
  --threshold 100000 \
  --comparison-operator LessThanThreshold
```

---

## Common Integration Patterns Summary

| Service | Auth Method | Response Type | Alarm Type | Unit |
|---------|-------------|---------------|------------|------|
| Resend | Bearer token | Headers | Absolute | emails |
| OpenRouter | Bearer token | JSON body | Percentage | USD |
| Scrape.do | Query param | JSON body | Percentage | requests |
| SiliconFlow | Bearer token | JSON body | Absolute | CNY |
| Serper | Custom header | JSON body | Absolute | credits |

---

## Troubleshooting Common Issues

### Issue: API returns 401 Unauthorized

**Cause**: Invalid or expired API key

**Solution**:
1. Verify API key in Secrets Manager: `just secrets-full`
2. Test API key manually with curl
3. Check if key needs specific scopes/permissions
4. Regenerate key if necessary

### Issue: Quota is always 0

**Cause**: Wrong response field or missing quota data

**Solutions**:
1. Log the full API response to inspect structure
2. Check API documentation for correct field names
3. Verify the API endpoint returns quota information
4. Some services require specific query parameters

### Issue: RemainingRatio calculation error

**Cause**: Division by zero or incorrect total value

**Solution**:
```typescript
// Always check for zero before division
remainingRatio: total > 0 ? remaining / total : 0
```

### Issue: Metrics not updating

**Cause**: Adapter throwing errors silently

**Solution**:
- Add comprehensive error logging
- Check CloudWatch Logs for Lambda errors
- Verify adapter returns valid BillingMetric object
