#!/usr/bin/python3

import nodriver as uc
import asyncio

##########################################################

async def sleep(sec: int):
    await asyncio.sleep(sec)

async def clean_up_and_type_text(element: uc.Element, text: str):
    # Nodriver's send_keys is very reliable and behaves like a human
    await element.send_keys(text)

##########################################################

async def type_tab(page: uc.Tab):
    await page.key_down("Tab")
    await page.key_up("Tab")

##########################################################

async def find_element_by_xpath_with_timeout(page, xpath: str, timeout: int = 10) -> uc.Element:
    """
    Robustly finds an element, handling CDP 'DOM Error -32000'
    which occurs if the DOM is in a transient state.
    """
    start_time = asyncio.get_event_loop().time()

    while (asyncio.get_event_loop().time() - start_time) < timeout:
        try:
            # .select() handles both CSS and XPath (if it starts with / or ()
            element = await page.select(xpath, timeout=1)
            if element:
                return element
        except uc.core.connection.ProtocolException as e:
            # This is the -32000 error. We wait 0.5s for the DOM to settle and retry.
            await asyncio.sleep(0.5)
            continue
        except Exception:
            await asyncio.sleep(0.5)

    raise Exception(f"Timeout: Element {xpath} not found after {timeout}s")

##########################################################

async def does_xpath_exist_with_timeout(page, xpath: str, timeout: int) -> bool:
    try:
        await find_element_by_xpath_with_timeout(page, xpath, timeout)
        return True
    except:
        return False

##########################################################
