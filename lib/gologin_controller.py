from pyppeteer import connect
from asyncio import run, sleep
from gologin import GoLogin
from lib.file_utils import copy_and_rename_folder
import random


class GologinController:
    def __init__(
        self,
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NTk3OWJkMGViOWU2M2YzNDcwZDU5MjMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjM0MjM2ZDU5ZjI2ZGJkYWNkYjU5NTkifQ.fOMAtoj8di6FWYqeQ9uLHSv0UXvOLhZZjFUtAc300wE",
    ):
        self.token = token
        self.gl = GoLogin({"token": self.token})

    async def connect(self, profile_id=None):
        if not profile_id:
            profile_id = self.gl_profile_id

        self.gl.setProfileId(profile_id)
        debugger_address = self.gl.start()
        self.browser = await connect(
            browserURL="http://" + debugger_address, defaultViewport=None
        )
        return self.browser

    async def create(self, name, auto_proxy=False, proxy=False):
        if auto_proxy and not proxy:
            proxy_config = {
                "mode": "gologin",
                "autoProxyRegion": "us",
            }

        if not auto_proxy:
            proxy_config = {
                "mode": "none",
            }

        if proxy:
            proxy_config = {
                "host": proxy.host,
                "port": proxy.port,
                "username": proxy.username,
                "password": proxy.password,
            }

        self.gl_profile_id = self.gl.create(
            {
                "name": f"{name}",
                "os": "mac",
                "navigator": {
                    "language": "en-US",
                    "userAgent": "random",
                    "resolution": "1920x1080",
                    "platform": "mac",
                },
                "proxy": proxy_config,
                "webRTC": {
                    "mode": "alerted",
                    "enabled": True,
                },
                "storage": {
                    "local": True,  # Local Storage is special browser caches that websites may use for user tracking in a way similar to cookies.
                    # Having them enabled is generally advised but may increase browser profile loading times.
                    "extensions": True,  # Extension storage is a special cotainer where a browser stores extensions and their parameter.
                    # Enable it if you need to install extensions from a browser interface.
                    "bookmarks": True,  # This option enables saving bookmarks in a browser interface.
                    "history": True,  # Warning! Enabling this option may increase the amount of data required
                    # to open/save a browser profile significantly.
                    # In the interests of security, you may wish to disable this feature,
                    # but it may make using GoLogin less convenient.
                    "passwords": True,  # This option will save passwords stored in browsers.
                    # It is used for pre-filling login forms on websites.
                    # All passwords are securely encrypted alongside all your data.
                    "session": True,  # This option will save browser session. It is used to save last open tabs.
                    "indexedDb": False,  # IndexedDB is special browser caches that websites may use for user tracking in a way similar to cookies.
                    # Having them enabled is generally advised but may increase browser profile loading times.
                },
            }
        )

        print("profile id=", self.gl_profile_id)

    async def stop(self):
        await self.browser.close()
        self.gl.stop()

    async def delete_all(self):
        profiles = self.gl.profiles()["profiles"]
        for profile in profiles:
            profile_id = profile["id"]
            self.gl.delete(profile_id)

    async def clone(self, desc_path, profile_id=None):
        if not profile_id:
            profile_id = str(random.randint(0, 1000))

        await self.delete_all()
        await self.create(profile_id)
        await self.connect()
        await sleep(1)

        profile_path = copy_and_rename_folder(
            self.gl.profile_path, desc_path, profile_id
        )

        await self.stop()
        return profile_path


async def main():
    pass


if __name__ == "__main__":
    run(main())
