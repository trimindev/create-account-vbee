import cv2
from asyncio import sleep
import pyperclip, pyppeteer
from time import time


async def pp_click_img(page, img_path):
    result = await pp_find_img(page, img_path, timeout=10)
    if result:
        center_x, center_y = result
        await page.mouse.click(center_x, center_y)
    else:
        print("Image not found within the specified timeout.")


async def pp_find_img(page, img_path, timeout=10):
    start_time = time.time()

    while True:
        if time() - start_time > timeout:
            return False

        await page.screenshot({"path": "screenshot.png"})

        template_image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        screen_image = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)

        result = cv2.matchTemplate(screen_image, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8

        if max_val >= threshold:
            template_width, template_height = template_image.shape[::-1]
            center_x = max_loc[0] + template_width / 2
            center_y = max_loc[1] + template_height / 2

            return center_x, center_y

        await sleep(0.1)


async def goto_page_with_url_containing(browser, url_part):
    pages = await browser.pages()
    for page in pages:
        if url_part in page.url:
            await page.bringToFront()
            return page
    return None


async def close_other_pages(browser, current_page):
    # Get all pages in the browser
    pages = await browser.pages()

    other_pages = pages.copy()

    # Iterate through each page
    for page in other_pages:
        # Check if the page is not the current page
        if page != current_page:
            # Close the page
            await page.close()


async def pp_copy_paste(page, text):
    pyperclip.copy(text)

    await page.keyboard.down("Control")
    await page.keyboard.press("KeyV")
    await page.keyboard.up("Control")


async def pp_clear_input_field(page):
    await page.keyboard.down("Control")
    await page.keyboard.press("KeyA")
    await page.keyboard.up("Control")
    await page.keyboard.press("Delete")


async def set_auto_download_behavior(page, downloadPath):
    await page._client.send(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "auto_downloads": 1,
            "downloadPath": downloadPath,
        },
    )


async def click_selector(
    page, selector, timeout=15, sleep_after_click=0.5, skip_timeout=False
):
    try:
        element = await page.waitForSelector(selector, timeout=timeout * 1000)
        await element.click()
        await sleep(sleep_after_click)
        return True
    except pyppeteer.errors.TimeoutError:
        error_msg = f"Selector {selector} not found after {timeout} seconds."
        if not skip_timeout:
            raise TimeoutError(error_msg)
        else:
            print(error_msg)
            return False


async def scroll_to_element(page, selector):
    await page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')
