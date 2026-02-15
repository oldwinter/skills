#!/usr/bin/env python3
"""
Screenshot capture utilities for E2E testing
"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from playwright.async_api import Page


class ScreenshotCapture:
    """Handles screenshot capture for test evidence"""
    
    def __init__(self, output_dir: str = "screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_count = 0
    
    async def capture(
        self,
        page: Page,
        name: str,
        full_page: bool = False,
        quality: int = 90
    ) -> str:
        """
        Capture screenshot
        
        Args:
            page: Playwright page object
            name: Screenshot name (without extension)
            full_page: Whether to capture full page
            quality: JPEG quality (0-100)
        
        Returns:
            Path to saved screenshot
        """
        self.screenshot_count += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = self.output_dir / filename
        
        try:
            await page.screenshot(
                path=str(filepath),
                full_page=full_page
            )
            print(f"📸 Screenshot saved: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")
            return ""
    
    async def capture_element(
        self,
        page: Page,
        selector: str,
        name: str
    ) -> str:
        """
        Capture screenshot of specific element
        
        Args:
            page: Playwright page object
            selector: CSS selector of element
            name: Screenshot name
        
        Returns:
            Path to saved screenshot
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = self.output_dir / filename
        
        try:
            element = await page.query_selector(selector)
            if element:
                await element.screenshot(path=str(filepath))
                print(f"📸 Element screenshot saved: {filepath}")
                return str(filepath)
            else:
                print(f"⚠️ Element not found: {selector}")
                return ""
        except Exception as e:
            print(f"❌ Failed to capture element screenshot: {e}")
            return ""
    
    async def capture_on_failure(
        self,
        page: Page,
        test_case_id: str,
        error_message: str = ""
    ) -> str:
        """
        Capture screenshot when test fails
        
        Args:
            page: Playwright page object
            test_case_id: Test case identifier
            error_message: Optional error message
        
        Returns:
            Path to saved screenshot
        """
        name = f"failure_test_{test_case_id}"
        if error_message:
            # Sanitize error message for filename
            safe_error = error_message[:30].replace(" ", "_").replace("/", "_")
            name = f"{name}_{safe_error}"
        
        return await self.capture(page, name, full_page=True)
    
    async def capture_comparison(
        self,
        page: Page,
        name: str,
        before_action,
        after_action
    ) -> tuple[str, str]:
        """
        Capture before/after screenshots
        
        Args:
            page: Playwright page object
            name: Base name for screenshots
            before_action: Action to perform before first screenshot
            after_action: Action to perform after first screenshot
        
        Returns:
            Tuple of (before_path, after_path)
        """
        await before_action()
        before_path = await self.capture(page, f"{name}_before")
        
        await after_action()
        after_path = await self.capture(page, f"{name}_after")
        
        return (before_path, after_path)
    
    def get_screenshot_count(self) -> int:
        """Get total number of screenshots captured"""
        return self.screenshot_count
    
    def clear_screenshots(self):
        """Remove all screenshots from output directory"""
        for file in self.output_dir.glob("*.png"):
            try:
                file.unlink()
            except Exception as e:
                print(f"⚠️ Failed to delete {file}: {e}")


class VideoRecorder:
    """Records browser session as video"""
    
    def __init__(self, output_dir: str = "videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.recording = False
    
    async def start_recording(self, context, test_name: str):
        """
        Start video recording
        
        Args:
            context: Playwright browser context
            test_name: Name of test for video file
        """
        # Video recording is configured when creating browser context
        # This is more of a placeholder for future enhancement
        self.recording = True
        print(f"🎥 Video recording started for: {test_name}")
    
    async def stop_recording(self, page: Page, test_name: str) -> str:
        """
        Stop video recording and save
        
        Args:
            page: Playwright page object
            test_name: Name of test
        
        Returns:
            Path to saved video
        """
        if not self.recording:
            return ""
        
        try:
            # Get video path from page
            video_path = await page.video.path()
            
            # Move to output directory with proper naming
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_path = self.output_dir / f"{timestamp}_{test_name}.webm"
            
            import shutil
            shutil.move(video_path, new_path)
            
            self.recording = False
            print(f"🎥 Video saved: {new_path}")
            return str(new_path)
            
        except Exception as e:
            print(f"❌ Failed to save video: {e}")
            return ""


class EvidenceCollector:
    """Collects various types of test evidence"""
    
    def __init__(self, output_dir: str = "evidence"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.screenshots_dir = self.output_dir / "screenshots"
        self.logs_dir = self.output_dir / "logs"
        self.videos_dir = self.output_dir / "videos"
        
        self.screenshots_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.videos_dir.mkdir(exist_ok=True)
        
        self.screenshot_capture = ScreenshotCapture(str(self.screenshots_dir))
        self.video_recorder = VideoRecorder(str(self.videos_dir))
    
    async def collect_failure_evidence(
        self,
        page: Page,
        test_case_id: str,
        error_message: str = ""
    ) -> dict:
        """
        Collect comprehensive evidence when test fails
        
        Returns:
            Dictionary containing paths to all collected evidence
        """
        evidence = {
            'screenshot': '',
            'html': '',
            'console_logs': '',
            'network_logs': ''
        }
        
        # Capture screenshot
        evidence['screenshot'] = await self.screenshot_capture.capture_on_failure(
            page, test_case_id, error_message
        )
        
        # Save HTML
        html_path = self.logs_dir / f"failure_test_{test_case_id}.html"
        try:
            html_content = await page.content()
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            evidence['html'] = str(html_path)
        except Exception as e:
            print(f"⚠️ Failed to save HTML: {e}")
        
        # Save console logs (if available)
        # This would require console log collection to be set up
        
        return evidence
    
    async def save_console_logs(
        self,
        console_messages: list,
        test_case_id: str
    ):
        """Save console logs to file"""
        log_path = self.logs_dir / f"console_test_{test_case_id}.log"
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                for msg in console_messages:
                    f.write(f"{msg}\n")
            print(f"📝 Console logs saved: {log_path}")
        except Exception as e:
            print(f"⚠️ Failed to save console logs: {e}")
    
    async def save_network_logs(
        self,
        network_data: dict,
        test_case_id: str
    ):
        """Save network logs to file"""
        import json
        
        log_path = self.logs_dir / f"network_test_{test_case_id}.json"
        
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(network_data, f, indent=2)
            print(f"📝 Network logs saved: {log_path}")
        except Exception as e:
            print(f"⚠️ Failed to save network logs: {e}")
    
    def get_evidence_summary(self) -> dict:
        """Get summary of all collected evidence"""
        return {
            'screenshots': len(list(self.screenshots_dir.glob("*.png"))),
            'html_snapshots': len(list(self.logs_dir.glob("*.html"))),
            'log_files': len(list(self.logs_dir.glob("*.log"))),
            'videos': len(list(self.videos_dir.glob("*.webm")))
        }
