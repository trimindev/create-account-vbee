from tkinter import Tk

from lib.data_manager import DataManager
from lib.gologin_controller import GologinController
from lib.auto_pyppeteer_utils import (
    goto_page_with_url_containing,
    set_auto_download_behavior,
    click_selector,
    pp_clear_input_field,
    pp_copy_paste,
)
from lib.browser_controller import BrowserController
from lib.text_utils import append_text_to_file, is_valid_email
from asyncio import sleep
import os


class AutoVbee:
    def __init__(self, root):
        # GUI --------------------------------------------------------------------
        self.root = root
        self.root.title("Auto Vbee")
        self.dm = DataManager(root)

        self.dm.create_entry(
            "Download Location:", "desc_path", isBrowse=True, isFolder=True
        )
        self.dm.create_entry(
            "Profiles Folder:", "profiles_folder_path", isFolder=True, isBrowse=True
        )
        self.dm.create_button("Sign Up", self.sign_up_vbee, self.load_data)

        self.gc = GologinController(self.dm.get_data("gologin_token"))
        self.bc = BrowserController(self.dm.get_data("executable_path"))

    def load_data(self):
        self.desc_path = self.dm.get_data("desc_path")
        self.profiles_folder_path = self.dm.get_data("profiles_folder_path")
        self.pass_vbee = "1aaaaaa1"

    async def sign_up_vbee(self):
        # Create profile
        await self.gc.delete_all()
        new_profile_path = await self.gc.clone(self.profiles_folder_path)
        self.browser = await self.bc.initialize_browser(new_profile_path)

        await self.load_temp_mail_page()

        await self.navigate_to_vbee_sign_in()

        temp_mail = await self.get_temp_mail()

        await self.fill_vbee_sign_in_form(temp_mail, self.pass_vbee)

        vbee_confirm_link = await self.fetch_vbee_confirm_link()

        self.page = await self.browser.newPage()
        await self.page.goto(vbee_confirm_link)

        vbee_mail_list_path = os.path.join(
            self.profiles_folder_path, "vbee_mail_list.txt"
        )
        append_text_to_file(vbee_mail_list_path, temp_mail)

        await set_auto_download_behavior(self.page, self.desc_path)

        await self.setup_initial_sign_in()
        await self.setup_voice()

    async def load_temp_mail_page(self):
        self.page = await self.browser.newPage()
        await self.page.goto("https://temp-mail.org/vi", waitUntil="domcontentloaded")

    async def navigate_to_vbee_sign_in(self):
        self.page = await self.browser.newPage()
        await self.page.goto("https://studio.vbee.vn/studio/text-to-speech")
        await sleep(2)

        await click_selector(self.page, ".mid\:block .bg-primary")

    async def get_temp_mail(self):
        self.page = await goto_page_with_url_containing(
            self.browser, "https://temp-mail.org"
        )

        email = None
        while email is None or not is_valid_email(email):
            email = await self.page.evaluate('document.getElementById("mail").value')
            if email is None:
                await sleep(1)
        if not email:
            return False

        return email

    async def fill_vbee_sign_in_form(self, email, password):
        self.page = await goto_page_with_url_containing(
            self.browser, "https://accounts.vbee.ai/"
        )

        await self.page.type("#email", email)
        await self.page.type("#password", password)
        await self.page.type("#passwordConfirm", password)

        login_btn = await self.page.waitForSelector('button[name="login"]')
        await login_btn.click()

    async def fetch_vbee_confirm_link(self):
        self.page = await goto_page_with_url_containing(
            self.browser, "https://temp-mail.org"
        )

        confirm_mail = await self.page.waitForSelector(
            "div.inbox-dataList > ul > li:nth-child(2) > div:nth-child(1) > a"
        )
        await confirm_mail.click()

        confirm_btn = await self.page.waitForSelector(
            "div.inbox-data-content > div.inbox-data-content-intro > div > div > div:nth-child(2) > a"
        )
        vbee_confirm_link = await self.page.evaluate(
            '(element) => element.getAttribute("href")', confirm_btn
        )

        return vbee_confirm_link

    async def close_initial_popups_on_sign_in(self):
        agree_btn = ".dialog-checkbox input"
        await click_selector(self.page, agree_btn)

        continue_btn = ".dialog-action > button"
        await click_selector(self.page, continue_btn)

        dont_show_again_btn = ".not-show-again input"
        await click_selector(self.page, dont_show_again_btn, 2, skip_timeout=True)

        close_ad_btn = ".MuiDialogContent-root > button"
        await click_selector(self.page, close_ad_btn, 2, skip_timeout=True)

        skip_enter_text_btn = ".button-back"
        await click_selector(self.page, skip_enter_text_btn)

        skip_hightlight_to_listen_btn = ".ignore-text"
        await click_selector(self.page, skip_hightlight_to_listen_btn)

    async def setup_initial_sign_in(self):
        await self.close_initial_popups_on_sign_in()

        await self.paste_text_into_editor("demo")
        await self.click_generate_voice()

        await self.close_popup_during_generation()
        await self.expand_download_tab()
        await self.choose_all_voice()
        await self.click_delete_all_voice()

        return

    async def close_popup_during_generation(self):
        close_popup_btn = await self.page.waitForSelector(
            ".dialog-content > h2 > button"
        )
        await close_popup_btn.click()
        await sleep(0.5)

    async def setup_voice(self):
        # Click choose voice
        choose_voice_btn = await self.page.waitForSelector(
            ".group-adjust-voice > button"
        )
        await choose_voice_btn.click()
        await sleep(0.5)

        # Click vn language checkbox
        await self.page.evaluate(
            "document.querySelector(\"input[value='vi-VN']\").click();"
        )
        await sleep(0.5)

        # Click first voice
        first_voice = await self.page.waitForSelector(".voice-list > button ")
        await first_voice.click()
        await sleep(0.5)

        # Adjust speed
        speed_input = await self.page.waitForSelector("[id='mui-8']")
        await speed_input.click()
        await speed_input.type("1.1")
        await self.page.keyboard.press("Enter")
        await sleep(0.5)

    async def paste_text_into_title(self, text, number):
        title_input = await self.page.waitForSelector(".input-wrapper")
        await title_input.click()
        await sleep(0.5)

        limited_text = " ".join(text.split()[:5])
        await pp_clear_input_field(self.page)
        await pp_copy_paste(self.page, str(number) + limited_text)

    async def click_generate_voice(self):
        await self.page.evaluate(
            'document.querySelector(".request-info > button").click();'
        )
        await sleep(0.5)

    async def paste_text_into_editor(self, text):
        content_editor = await self.page.waitForSelector(
            ".DraftEditor-editorContainer > div > div"
        )
        await content_editor.click()
        await sleep(0.5)

        await pp_clear_input_field(self.page)
        await pp_copy_paste(self.page, text)


def main():
    root = Tk()
    app = AutoVbee(root)
    root.mainloop()


if __name__ == "__main__":
    main()
