# Browser Selector Strategies

This document provides guidance on selecting DOM elements reliably for E2E testing.

## Selector Priority

Use selectors in this order of preference:

1. **Test-specific attributes** (best)
   ```css
   [data-testid="submit-button"]
   [data-test="login-form"]
   [data-cy="user-menu"]
   ```

2. **Semantic HTML elements**
   ```css
   button[type="submit"]
   nav > ul > li
   main article
   ```

3. **Unique IDs**
   ```css
   #login-button
   #search-input
   ```

4. **Unique classes** (use cautiously)
   ```css
   .submit-btn (only if unique)
   .login-form (only if unique)
   ```

5. **ARIA attributes**
   ```css
   [aria-label="Search"]
   [role="navigation"]
   ```

6. **Combination selectors** (as last resort)
   ```css
   form.login-form input[name="username"]
   div.modal button.close
   ```

## Avoid

❌ **Generic classes** (brittle, likely to change)
```css
.btn
.primary
.container
```

❌ **XPath with absolute paths** (breaks easily)
```xpath
/html/body/div[1]/div[2]/form/button
```

❌ **Text content only** (breaks with i18n)
```css
button:contains("Submit")
```

## Common Patterns

### Forms

```css
/* Input fields */
input[name="username"]
input[type="email"]
textarea[name="message"]

/* Labels */
label[for="username"]

/* Submit buttons */
button[type="submit"]
form button:last-child
```

### Navigation

```css
/* Main navigation */
nav[role="navigation"]
header nav

/* Links */
a[href="/dashboard"]
nav a[aria-current="page"]

/* Menus */
[role="menu"]
[role="menuitem"]
```

### Dynamic Content

```css
/* Modals */
[role="dialog"]
.modal:not(.hidden)
div[aria-modal="true"]

/* Dropdowns */
[role="listbox"]
select[name="country"]

/* Loading states */
[aria-busy="true"]
.loading-spinner
```

### Tables

```css
/* Table elements */
table tbody tr
td[data-column="email"]

/* Specific rows */
tr[data-id="123"]
tbody tr:first-child
```

### Lists

```css
/* List items */
ul[role="list"] li
[role="listitem"]

/* Specific items */
li[data-index="0"]
li:nth-child(3)
```

## Wait Strategies

### Wait for element to be visible

```javascript
await page.waitForSelector('button[type="submit"]', { state: 'visible' })
```

### Wait for element to be clickable

```javascript
await page.waitForSelector('button', { state: 'attached' })
await page.waitForSelector('button:not([disabled])')
```

### Wait for text content

```javascript
await page.waitForSelector('text="Success"')
await page.waitForFunction(() => 
  document.querySelector('.message').textContent.includes('Complete')
)
```

### Wait for network idle

```javascript
await page.goto(url, { waitUntil: 'networkidle' })
```

### Custom wait conditions

```javascript
await page.waitForFunction(() => {
  const element = document.querySelector('.status')
  return element && element.textContent === 'Ready'
})
```

## Best Practices

### 1. Make selectors resilient

✅ **Good**: Semantic and specific
```css
form[aria-label="Login"] button[type="submit"]
```

❌ **Bad**: Implementation-dependent
```css
div.css-1dbjc4n div.css-18t94o4 button
```

### 2. Use data attributes for testing

Add test-specific attributes to critical elements:

```html
<button data-testid="checkout-button" class="btn primary">
  Checkout
</button>
```

```css
[data-testid="checkout-button"]
```

### 3. Handle dynamic IDs

If IDs are generated dynamically, use partial matching:

```css
[id^="user-menu-"]  /* Starts with */
[id*="menu"]        /* Contains */
[id$="-dropdown"]   /* Ends with */
```

### 4. Group related selectors

Create reusable selector patterns:

```javascript
const selectors = {
  loginForm: {
    username: 'input[name="username"]',
    password: 'input[name="password"]',
    submit: 'button[type="submit"]',
    error: '.error-message'
  },
  dashboard: {
    welcome: '.welcome-message',
    navigation: 'nav[role="navigation"]',
    logout: 'button[aria-label="Logout"]'
  }
}
```

### 5. Verify uniqueness

Before using a selector, verify it returns exactly one element:

```javascript
const elements = await page.$$('button.submit')
if (elements.length !== 1) {
  throw new Error(`Selector returned ${elements.length} elements, expected 1`)
}
```

## Playwright-Specific Recommendations

### Use built-in locators (recommended)

```javascript
// By role
await page.getByRole('button', { name: 'Submit' })
await page.getByRole('link', { name: 'Login' })

// By label
await page.getByLabel('Username')
await page.getByLabel('Password')

// By placeholder
await page.getByPlaceholder('Enter your email')

// By text
await page.getByText('Welcome back')

// By test ID
await page.getByTestId('submit-button')
```

### Combine locators

```javascript
await page.getByRole('form', { name: 'Login' })
  .getByRole('button', { name: 'Submit' })
```

### Use filters

```javascript
await page.getByRole('listitem')
  .filter({ hasText: 'Active' })
  .first()
```

## Debugging Selectors

### Chrome DevTools

1. Open DevTools (F12)
2. Press Ctrl/Cmd + F in Elements tab
3. Enter CSS selector or XPath
4. Verify matches

### Playwright Inspector

```bash
PWDEBUG=1 python test_script.py
```

### Selector evaluation in console

```javascript
// Test in browser console
document.querySelectorAll('your-selector')
$$('your-selector')  // Chrome DevTools shorthand
```

## Common Issues

### Issue: Selector matches multiple elements

**Solution**: Make selector more specific or use `:first-child`, `:nth-child()`

### Issue: Element not found

**Solutions**:
- Check if element is in iframe
- Wait for element to be rendered
- Verify selector spelling
- Check if element is hidden by CSS

### Issue: Element not clickable

**Solutions**:
- Wait for element to be visible
- Check for overlaying elements
- Scroll element into view
- Verify element is not disabled

### Issue: Stale element reference

**Solutions**:
- Re-query element before action
- Use implicit waits
- Avoid storing element references

## Resources

- [Playwright Locators](https://playwright.dev/docs/locators)
- [CSS Selectors Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- [ARIA Roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles)
