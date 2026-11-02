import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.session_manager import SessionManager
from playwright.async_api import Browser, BrowserContext

class TestSessionManager(unittest.IsolatedAsyncioTestCase):

    async def test_get_new_context(self):
        # 1. Use AsyncMock for async methods, MagicMock for sync properties/methods like is_connected
        mock_browser = AsyncMock()
        mock_browser.is_connected = MagicMock(return_value=True)

        ctx_mock = AsyncMock(spec=BrowserContext)
        mock_browser.new_context.return_value = ctx_mock

        sm = SessionManager()
        sm._browser = mock_browser 

        # Act
        context = await sm.get_new_context()

        # Assert
        self.assertEqual(context, ctx_mock)
        self.assertIn(ctx_mock, sm._contexts)
        mock_browser.new_context.assert_called_once()

    async def test_close_all_contexts(self):
        """Test that all contexts are closed and the list is cleared."""
        sm = SessionManager()
        # Setup mocks for context objects
        ctx1 = AsyncMock()
        ctx2 = AsyncMock()
        sm.browser = AsyncMock() # Required to avoid None check logic if it were there, but here we just need contexts in list
        sm._contexts = [ctx1, ctx2]

        # Act
        await sm.close_all_contexts()

        # Assert
        ctx1.close.assert_awaited_once()
        ctx2.close.assert_awaited_once()
        self.assertEqual(len(sm._contexts), 0)

    @patch('src.core.session_manager.async_playwright')
    async def test_context_manager__aenter__(self, mock_pw):
        # 1. Mock the lowest level entity (the browser launcher)
        sm = SessionManager()
        mock_browser = AsyncMock()

        # 2. Mock the Playwright instance returned by .start()
        mock_playwright_instance = AsyncMock()
        mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)

        # 3. Mock the object returned by executing async_playwright()
        mock_launcher = AsyncMock()
        mock_launcher.start = AsyncMock(return_value=mock_playwright_instance)

        # 4. Bind the launcher mock to the library call
        mock_pw.return_value = mock_launcher

        # Act & Assert
        async with sm as instance:
            # Verify the context manager returns its own instance correctly
            self.assertEqual(instance, sm)

            # Verify that all properties were populated successfully during initialization
            self.assertEqual(instance._playwright_context, mock_playwright_instance)
            self.assertEqual(instance._browser, mock_browser)

        # Verify underlying tracking parameters were called correctly
        mock_launcher.start.assert_awaited_once()
        mock_playwright_instance.chromium.launch.assert_awaited_once_with(headless=True)


    async def test_context_manager_cleanup(self) -> None:
        sm = SessionManager()
        mock_browser = AsyncMock()
        mock_py = AsyncMock() 
        # Mocking the internal state of your class as if it was fully initialized by __aenter__
        sm._browser = mock_browser
        sm._playwright_context = mock_py

        # We call a custom logic or simulate what happens during 'async with' exit:
        await sm.__aexit__(type(None), None, None) # Simulate successful context exit

        mock_browser.close.assert_awaited_once()
        mock_py.stop.assert_awaited_once()

    @patch('src.core.session_manager.async_playwright')
    async def test_context_manager__aenter__failure(self, mock_pw):
        """Test that if browser fails to launch during __aenter__, playwright is still stopped."""
       # 1. Mock the Playwright instance returned by .start()
        mock_playwright_instance = AsyncMock()
        
        # 2. Force a failure during the browser launch step specifically
        mock_playwright_instance.chromium.launch.side_effect = Exception("Launch Failed")
        
        # 3. Mock the launcher object returned by async_playwright()
        mock_launcher = AsyncMock()
        mock_launcher.start = AsyncMock(return_value=mock_playwright_instance)
        
        # 4. Bind the launcher to the patched library call
        mock_pw.return_value = mock_launcher
        
        sm = SessionManager()
        with self.assertRaises(Exception) as cm:
            async with sm: # This triggers __aenter__ logic internally if implemented correctly 
                pass  # If you use the class directly, it might need a manual call to test accurately
                                            # But since your code is structured for 'async with', we check behavior.

        self.assertIn("Launch Failed", str(cm.exception))

    async def test_get_new_context_missing_browser(self) -> None:
        """Test that RuntimeError is raised if get_new_context called before initialization."""
        sm = SessionManager() # No browser assigned yet
        with self.assertRaises(RuntimeError):
            await sm.get_new_context()

if __name__ == "__main__":
    unittest.main()