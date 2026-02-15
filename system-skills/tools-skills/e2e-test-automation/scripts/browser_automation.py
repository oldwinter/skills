#!/usr/bin/env python3
"""
Browser automation utilities for E2E testing
"""

from typing import Optional, Dict, Any
from playwright.async_api import Page, Browser, BrowserContext


class BrowserHelper:
    """Helper utilities for browser automation"""
    
    @staticmethod
    async def wait_for_element(
        page: Page,
        selector: str,
        timeout: int = 30000,
        state: str = 'visible'
    ) -> bool:
        """Wait for element to be in specified state"""
        try:
            await page.wait_for_selector(
                selector,
                timeout=timeout,
                state=state
            )
            return True
        except Exception as e:
            print(f"⚠️ Element not found: {selector} - {e}")
            return False
    
    @staticmethod
    async def safe_click(page: Page, selector: str, timeout: int = 5000) -> bool:
        """Safely click an element with retry"""
        try:
            # Wait for element
            await page.wait_for_selector(selector, state='visible', timeout=timeout)
            
            # Scroll into view
            await page.locator(selector).scroll_into_view_if_needed()
            
            # Click
            await page.click(selector, timeout=timeout)
            
            return True
        except Exception as e:
            print(f"❌ Failed to click {selector}: {e}")
            return False
    
    @staticmethod
    async def safe_fill(page: Page, selector: str, value: str, timeout: int = 5000) -> bool:
        """Safely fill an input field"""
        try:
            await page.wait_for_selector(selector, state='visible', timeout=timeout)
            await page.fill(selector, value)
            return True
        except Exception as e:
            print(f"❌ Failed to fill {selector}: {e}")
            return False
    
    @staticmethod
    async def get_text(page: Page, selector: str) -> Optional[str]:
        """Get text content of element"""
        try:
            element = await page.query_selector(selector)
            if element:
                return await element.text_content()
            return None
        except Exception:
            return None
    
    @staticmethod
    async def check_element_exists(page: Page, selector: str) -> bool:
        """Check if element exists on page"""
        try:
            element = await page.query_selector(selector)
            return element is not None
        except Exception:
            return False
    
    @staticmethod
    async def wait_for_navigation(page: Page, timeout: int = 30000):
        """Wait for page navigation to complete"""
        try:
            await page.wait_for_load_state('networkidle', timeout=timeout)
        except Exception as e:
            print(f"⚠️ Navigation wait timeout: {e}")
    
    @staticmethod
    async def get_console_errors(page: Page) -> list:
        """Collect console errors from page"""
        errors = []
        
        def on_console(msg):
            if msg.type == 'error':
                errors.append(msg.text)
        
        page.on('console', on_console)
        return errors
    
    @staticmethod
    async def measure_load_time(page: Page, url: str) -> float:
        """Measure page load time"""
        import time
        
        start = time.time()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        end = time.time()
        
        return end - start
    
    @staticmethod
    async def take_full_page_screenshot(page: Page, path: str):
        """Take full page screenshot"""
        await page.screenshot(path=path, full_page=True)
    
    @staticmethod
    async def get_element_count(page: Page, selector: str) -> int:
        """Count elements matching selector"""
        try:
            elements = await page.query_selector_all(selector)
            return len(elements)
        except Exception:
            return 0
    
    @staticmethod
    async def wait_for_text(
        page: Page,
        text: str,
        timeout: int = 30000
    ) -> bool:
        """Wait for specific text to appear on page"""
        try:
            await page.wait_for_selector(
                f'text="{text}"',
                timeout=timeout,
                state='visible'
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    async def select_option(
        page: Page,
        selector: str,
        value: str
    ) -> bool:
        """Select option from dropdown"""
        try:
            await page.select_option(selector, value)
            return True
        except Exception as e:
            print(f"❌ Failed to select option: {e}")
            return False
    
    @staticmethod
    async def hover(page: Page, selector: str) -> bool:
        """Hover over element"""
        try:
            await page.hover(selector)
            return True
        except Exception as e:
            print(f"❌ Failed to hover: {e}")
            return False
    
    @staticmethod
    async def press_key(page: Page, key: str):
        """Press keyboard key"""
        await page.keyboard.press(key)
    
    @staticmethod
    async def upload_file(page: Page, selector: str, file_path: str) -> bool:
        """Upload file to input field"""
        try:
            await page.set_input_files(selector, file_path)
            return True
        except Exception as e:
            print(f"❌ Failed to upload file: {e}")
            return False
    
    @staticmethod
    async def get_attribute(page: Page, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value"""
        try:
            element = await page.query_selector(selector)
            if element:
                return await element.get_attribute(attribute)
            return None
        except Exception:
            return None
    
    @staticmethod
    async def is_visible(page: Page, selector: str) -> bool:
        """Check if element is visible"""
        try:
            element = await page.query_selector(selector)
            if element:
                return await element.is_visible()
            return False
        except Exception:
            return False
    
    @staticmethod
    async def is_enabled(page: Page, selector: str) -> bool:
        """Check if element is enabled"""
        try:
            element = await page.query_selector(selector)
            if element:
                return await element.is_enabled()
            return False
        except Exception:
            return False
    
    @staticmethod
    async def wait_for_timeout(milliseconds: int):
        """Wait for specified milliseconds"""
        import asyncio
        await asyncio.sleep(milliseconds / 1000)


class NetworkMonitor:
    """Monitor network requests and responses"""
    
    def __init__(self, page: Page):
        self.page = page
        self.requests = []
        self.responses = []
        self.failed_requests = []
        
        page.on('request', self._on_request)
        page.on('response', self._on_response)
        page.on('requestfailed', self._on_request_failed)
    
    def _on_request(self, request):
        """Handle request event"""
        self.requests.append({
            'url': request.url,
            'method': request.method,
            'headers': request.headers,
            'timestamp': None  # Can add timestamp if needed
        })
    
    def _on_response(self, response):
        """Handle response event"""
        self.responses.append({
            'url': response.url,
            'status': response.status,
            'headers': response.headers,
            'timestamp': None
        })
    
    def _on_request_failed(self, request):
        """Handle failed request"""
        self.failed_requests.append({
            'url': request.url,
            'failure': request.failure,
            'timestamp': None
        })
    
    def get_failed_requests(self) -> list:
        """Get all failed requests"""
        return self.failed_requests
    
    def get_slow_requests(self, threshold_ms: int = 2000) -> list:
        """Get requests that took longer than threshold"""
        # This would require timing implementation
        # Placeholder for now
        return []
    
    def clear(self):
        """Clear all recorded data"""
        self.requests.clear()
        self.responses.clear()
        self.failed_requests.clear()


class PerformanceMonitor:
    """Monitor page performance metrics"""
    
    @staticmethod
    async def get_metrics(page: Page) -> Dict[str, Any]:
        """Get performance metrics"""
        metrics = await page.evaluate('''() => {
            const perfData = window.performance.timing;
            const navigationStart = perfData.navigationStart;
            
            return {
                domContentLoaded: perfData.domContentLoadedEventEnd - navigationStart,
                loadComplete: perfData.loadEventEnd - navigationStart,
                firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
                domInteractive: perfData.domInteractive - navigationStart
            };
        }''')
        
        return metrics
    
    @staticmethod
    async def measure_interaction_time(page: Page, action_fn) -> float:
        """Measure time taken for an interaction"""
        import time
        
        start = time.time()
        await action_fn()
        end = time.time()
        
        return (end - start) * 1000  # Convert to milliseconds


class AccessibilityChecker:
    """Check basic accessibility compliance"""
    
    @staticmethod
    async def check_page(page: Page) -> Dict[str, Any]:
        """Run basic accessibility checks"""
        results = {
            'missing_alt_text': [],
            'missing_labels': [],
            'low_contrast': [],
            'missing_aria': []
        }
        
        # Check for images without alt text
        images = await page.query_selector_all('img:not([alt])')
        results['missing_alt_text'] = [
            await img.get_attribute('src') for img in images
        ]
        
        # Check for inputs without labels
        inputs = await page.query_selector_all('input:not([aria-label]):not([id])')
        results['missing_labels'] = len(inputs)
        
        return results
