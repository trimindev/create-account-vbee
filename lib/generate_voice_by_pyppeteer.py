# async def paste_text_into_title(self, text, number):
#     title_input = await self.page.waitForSelector(".input-wrapper")
#     await title_input.click()
#     await sleep(0.5)

#     limited_text = " ".join(text.split()[:5])
#     await pp_clear_input_field(self.page)
#     await pp_copy_paste(self.page, str(number) + limited_text)

# async def click_generate_voice(self):
#     await self.page.evaluate(
#         'document.querySelector(".request-info > button").click();'
#     )
#     await sleep(0.5)

# async def paste_text_into_editor(self, text):
#     content_editor = await self.page.waitForSelector(
#         ".DraftEditor-editorContainer > div > div"
#     )
#     await content_editor.click()
#     await sleep(0.5)

#     await pp_clear_input_field(self.page)
#     await pp_copy_paste(self.page, text)

# async def generate_all_subtitle_voices(self, subtitles):
#     filtered_subtitles = self.filter_subtitles_by_range(
#         subtitles, self.start, self.end
#     )
#     for subtitle in filtered_subtitles:
#         await self.generate_subtitle_voice(subtitle)
#         if await self.is_not_enough_characters_popup_displayed():
#             break

# async def generate_subtitle_voice(self, subtitle):

#     await self.paste_text_into_title(subtitle["text"], subtitle["number"])

#     await self.paste_text_into_editor(subtitle["text"])

#     await self.click_generate_voice()

# async def is_not_enough_characters_popup_displayed(self):
#     try:
#         title_element = await self.page.waitForSelector(
#             ".dialog-wrapper > .title", timeout=100
#         )
#         if title_element:
#             title_text = await self.page.evaluate(
#                 "(element) => element.textContent.trim()", title_element
#             )
#             return title_text in ["Not Enough Characters", "Không đủ ký tự"]
#     except pyppeteer.errors.TimeoutError:
#         pass

#     return False

# async def filter_subtitles_by_range(self, subtitles, start, end):
#     return [
#         subtitle for subtitle in subtitles if start <= subtitle["number"] <= end
#     ]

# async def click_delete_all_voice(self):
#     delete_all_btn = await self.page.waitForSelector(
#         ".MuiTableCell-root .delete-button:nth-child(2)"
#     )
#     await delete_all_btn.click()

#     confirm_yes_btn = await self.page.waitForSelector(".content button")
#     await confirm_yes_btn.click()

#     return

# async def choose_all_voice(self):
#     await self.await_voice_generation_completion()

#     while True:
#         header_checkbox = ".header-checkbox .PrivateSwitchBase-input"
#         await click_selector(self.page, header_checkbox)

#         next_page_btn = 'button[aria-label="Go to next page"]:not([disabled])'
#         if not (
#             await click_selector(self.page, next_page_btn, 0.1, skip_timeout=True)
#         ):
#             break

#     return

# async def expand_download_tab(self):
#     expand_icon = await self.page.querySelector(
#         'button > [data-testid="KeyboardArrowDownIcon"]'
#     )
#     if expand_icon:
#         await expand_icon.click()
#         await sleep(0.5)
#     else:
#         pass

#     return

# async def click_download_voice(self):
#     download_btn = await self.page.waitForSelector(
#         ".MuiTableCell-root .download-button"
#     )
#     await download_btn.click()
#     return

# async def await_voice_generation_completion(self):
#     await self.page.waitForSelector(".request-info > .MuiTypography-body1")
#     return
