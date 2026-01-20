# Adapter Templates

This document provides three common adapter patterns for integrating third-party API services.

## Pattern 1: Standard JSON Response with Balance Fields

**Use when**: The API returns a JSON response with clear balance/quota fields.

**Example Services**: OneRouter, SiliconFlow

```typescript
import axios from "axios";
import { BillingMetric } from "../src/types";

export async function fetchServiceName(apiKey: string): Promise<BillingMetric> {
  const response = await axios.get("https://api.example.com/balance", {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    }
  });

  // Extract balance data from response
  const { total_balance, remaining_balance, currency } = response.data;

  // Mask API key: show first 6 and last 6 chars
  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  const total = total_balance || 0;
  const remaining = remaining_balance || 0;

  return {
    service: "service_name",
    apiKeyMask,
    total,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0,
    currency: currency || "USD"
  };
}
```

**Common Response Formats**:
```json
// Format A: Direct fields
{
  "balance": 100.50,
  "total": 500.00,
  "currency": "USD"
}

// Format B: Nested object
{
  "account": {
    "balance": {
      "total": 500.00,
      "remaining": 100.50,
      "currency": "USD"
    }
  }
}

// Format C: Separate endpoints
// GET /balance → { "remaining": 100.50 }
// GET /quota → { "total": 500.00 }
```

---

## Pattern 2: Response Headers Containing Quota

**Use when**: The API returns quota information in HTTP response headers rather than the body.

**Example Services**: Resend

```typescript
import axios from "axios";
import { BillingMetric } from "../src/types";

/**
 * Service Name
 * Docs: https://api.example.com/docs
 *
 * Quota is provided in response headers:
 * - x-quota-remaining: Remaining quota
 * - x-quota-limit: Total quota (optional)
 */
export async function fetchServiceName(apiKey: string): Promise<BillingMetric> {
  // Make a lightweight API call to get response headers
  // Use a simple GET endpoint that requires minimal processing
  const response = await axios.get("https://api.example.com/account", {
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    }
  });

  // Extract quota from response headers
  const remainingHeader = response.headers['x-quota-remaining'];
  const limitHeader = response.headers['x-quota-limit'];

  // Mask API key
  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  // Parse quota values
  const remaining = parseInt(remainingHeader || "0", 10);
  const total = parseInt(limitHeader || remaining.toString(), 10);

  return {
    service: "service_name",
    apiKeyMask,
    total,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0,
    unit: "emails"  // or "requests", "credits", etc.
  };
}
```

**Common Header Names**:
- `x-ratelimit-remaining` / `x-ratelimit-limit`
- `x-quota-remaining` / `x-quota-limit`
- `x-daily-quota` / `x-monthly-quota`
- `ratelimit-remaining` / `ratelimit-limit`

---

## Pattern 3: Prepaid Credits with No Total Amount

**Use when**: The API only returns remaining credits/balance without a total quota (common for prepaid accounts).

**Example Services**: Serper, TwitterAPI

```typescript
import axios from "axios";
import { BillingMetric } from "../src/types";

/**
 * Service Name (Prepaid Credits)
 * Docs: https://api.example.com/docs
 */
export async function fetchServiceName(apiKey: string): Promise<BillingMetric> {
  const response = await axios.get("https://api.example.com/account", {
    headers: {
      "X-API-KEY": apiKey,  // Note: Different auth method
      "Content-Type": "application/json"
    }
  });

  // Extract remaining credits
  const { credits, balance } = response.data;
  const remaining = credits || balance || 0;

  // Mask API key
  const apiKeyMask = apiKey.length >= 12
    ? `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`
    : apiKey;

  // For prepaid accounts: total = remaining
  // This means remainingRatio will always be 1
  return {
    service: "service_name",
    apiKeyMask,
    total: remaining,      // Use remaining as total
    remaining,
    remainingRatio: 1,     // Always 1 for prepaid accounts
    unit: "credits"
  };
}
```

**Important Notes for Prepaid Pattern**:
- Use **absolute value alarms** instead of percentage alarms
- `remainingRatio` will always be 1.0
- Monitor the actual `remaining` value, not the ratio
- Example alarm threshold: `remaining < 10000` (not `ratio < 0.05`)

---

## Special Cases

### Case 1: Query Parameter Authentication

Some APIs use query parameters instead of headers:

```typescript
const response = await axios.get("https://api.example.com/balance", {
  params: {
    token: apiKey,
    // or: api_key: apiKey
  }
});
```

**Example Services**: Scrape.do

### Case 2: Multiple Sub-Quotas

Some services have separate quotas (e.g., daily + monthly):

```typescript
// Option A: Monitor both separately
export async function fetchServiceDaily(apiKey: string): Promise<BillingMetric> {
  // ... return daily quota with service: "service_name_daily"
}

export async function fetchServiceMonthly(apiKey: string): Promise<BillingMetric> {
  // ... return monthly quota with service: "service_name_monthly"
}

// Option B: Monitor only the most restrictive
export async function fetchService(apiKey: string): Promise<BillingMetric> {
  // ... return whichever quota is lower
  const dailyRemaining = response.headers['x-daily-quota'];
  const monthlyRemaining = response.headers['x-monthly-quota'];
  const remaining = Math.min(dailyRemaining, monthlyRemaining);
  // ...
}
```

### Case 3: Different Endpoints for Different Data

```typescript
export async function fetchServiceName(apiKey: string): Promise<BillingMetric> {
  // Make multiple API calls
  const [balanceRes, quotaRes] = await Promise.all([
    axios.get("https://api.example.com/balance", { headers: { Authorization: `Bearer ${apiKey}` } }),
    axios.get("https://api.example.com/quota", { headers: { Authorization: `Bearer ${apiKey}` } })
  ]);

  const remaining = balanceRes.data.balance;
  const total = quotaRes.data.limit;

  return {
    service: "service_name",
    apiKeyMask: `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`,
    total,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0,
    currency: "USD"
  };
}
```

### Case 4: Custom Service Name Parameter

Some adapters accept additional parameters:

```typescript
// For services with multiple API keys (e.g., openrouter_2)
export async function fetchServiceName(
  apiKey: string,
  suffix?: string
): Promise<BillingMetric> {
  // ...
  return {
    service: suffix ? `service_name_${suffix}` : "service_name",
    apiKeyMask,
    total,
    remaining,
    remainingRatio: total > 0 ? remaining / total : 0
  };
}
```

---

## Error Handling

All adapters should handle common errors gracefully:

```typescript
export async function fetchServiceName(apiKey: string): Promise<BillingMetric> {
  try {
    const response = await axios.get("https://api.example.com/balance", {
      headers: { Authorization: `Bearer ${apiKey}` },
      timeout: 10000  // 10 second timeout
    });

    // ... parse response

    return {
      service: "service_name",
      apiKeyMask: `${apiKey.slice(0, 6)}...${apiKey.slice(-6)}`,
      total,
      remaining,
      remainingRatio: total > 0 ? remaining / total : 0
    };
  } catch (error: any) {
    // Log detailed error for debugging
    console.error(`Failed to fetch service_name balance:`, {
      status: error.response?.status,
      message: error.message,
      data: error.response?.data
    });

    // Re-throw to be handled by Lambda handler
    throw new Error(`service_name API error: ${error.message}`);
  }
}
```

---

## Testing Adapters

Before deployment, test the adapter locally:

```typescript
// test-adapter.ts
import { fetchServiceName } from "./adapters/service_name";

async function test() {
  const apiKey = process.env.SERVICE_API_KEY || "your-test-key";

  try {
    const metric = await fetchServiceName(apiKey);
    console.log("✅ Adapter test successful:", metric);
  } catch (error) {
    console.error("❌ Adapter test failed:", error);
  }
}

test();
```

Run with:
```bash
npx ts-node test-adapter.ts
```
