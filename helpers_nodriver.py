#!/usr/bin/python3

import nodriver as uc
import asyncio

##########################################################

async def sleep(sec: int):
    await asyncio.sleep(sec)

async def clean_up_and_type_text(element: uc.Element, text: str):
    # nodriver elements have a clear/send_keys equivalent
    # We click and then send keys. Nodriver handles 'clear' differently 
    # but for most inputs, simply calling send_keys or selecting all works.
    await element.click()
    # Simulating Ctrl+A, Backspace/Delete if needed, but send_keys often handles focus
    await element.send_keys(text)

##########################################################

async def type_tab(page: uc.Tab):
    await page.key_down("Tab")
    await page.key_up("Tab")

##########################################################

async def does_xpath_exist_with_timeout(page: uc.Tab, xpath: str, timeout: int) -> bool:
    try:
        # page.select() waits internally for the element to appear
        res = await page.select(xpath, timeout=timeout)
        return res is not None
    except Exception:
        return False

##########################################################

async def find_element_by_xpath_with_timeout(page: uc.Tab, xpath: str, timeout: int) -> uc.Element:
    res = await page.select(xpath, timeout=timeout)
    if not res:
        raise Exception(f"cannot load element {xpath} in {timeout} sec")
    return res

