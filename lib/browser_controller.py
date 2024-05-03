from pyppeteer import launch
from asyncio import run


class BrowserController:
    def __init__(
        self,
        executable_path=None,
    ):
        self.executable_path = executable_path

    async def initialize_browser(self, profile_path):
        browser = await launch(
            {
                "executablePath": self.executable_path,
                "userDataDir": profile_path,
                "headless": False,
                "defaultViewport": None,
                "width": 1024,
                "height": 960,
                "autoClose": True,
            }
        )

        return browser


async def main():
    browser_controller = BrowserController(
        executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        chrome_profile_path="C:/Users/xinch/AppData/Local/Google/Chrome/User Data/Profile 1",
    )
    await browser_controller.initialize_browser()


if __name__ == "__main__":
    run(main())
