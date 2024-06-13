#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
#from print_helpers.print_helpers import print_fatal, print_error, print_warning, print_info, print_debug

import time

##########################################################

def init_driver( driver_path, binary_location = "", cookie_dir = "", is_headless = False, proxy = "" ):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if is_headless:
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("disable-gpu")
        options.add_argument("window-size=1024,768")

    if proxy:
        options.add_argument( "--proxy-server=" + proxy )

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    if binary_location:
        options.binary_location = binary_location

    if cookie_dir:
        options.add_argument( "user-data-dir=" + cookie_dir )

    service = Service( executable_path=driver_path )

    driver = webdriver.Chrome( options=options, service=service )

    return driver

##########################################################

def sleep( sec: int, verbose: bool = True ):
    if verbose:
        pass
        #print( "sleeping {} sec".format( sec ) )
    else:
        pass
        #print( '.', end='', flush=True )

    time.sleep( sec )

##########################################################

def clean_up_and_type_text( element, text: str ):

    element.send_keys( Keys.CONTROL + "a" )
    element.send_keys( Keys.DELETE )
    element.send_keys( text )

def type_tab( element ):

    element.send_keys( Keys.TAB )

##########################################################

def does_class_exist( parent, class_name ) -> bool:

    elems = parent.find_elements( 'class_name', class_name )

    if len( elems ) > 0 :
        return True

    return False

def does_tag_exist( parent, name: str ) -> bool:

    elems = parent.find_elements( 'tag_name',  name )

    if len( elems ) > 0 :
        return True

    return False

def does_css_selector_exist( parent, name: str ) -> bool:

    elems = parent.find_elements( 'css_selector', name )

    if len( elems ) > 0 :
        return True

    return False

def does_xpath_exist( parent, name: str ) -> bool:

    elems = parent.find_elements( 'xpath', name )

    if len( elems ) > 0 :
        return True

    return False

def does_xpath_exist_with_timeout( parent, name: str, timeout: int ) -> bool:
    i = 0

    #print_debug( "waiting till loaded ", '', True );

    while i <= timeout:
        res = does_xpath_exist( parent, name )
        if res:
            #print()
            #print_debug( "loaded element in {} sec".format( i ) )
            return res

        i += 1
        sleep( 1, False )

    #print()
    return False

def do_xpaths_exist( parent, names: list ) -> [ bool, list, int ]:

    i: int = 0
    for n in names:
        if does_xpath_exist( parent, n ):
            return True, n, i
        i += 1

    return False, None, 0

def do_xpaths_exist_with_timeout( parent, names, timeout ) -> [ bool, list, int ]:
    i = 0

    #print_debug( "waiting till loaded ", '', True );

    while i <= timeout:
        res = do_xpaths_exist( parent, names )
        if res[0]:
            #print()
            #print_debug( "loaded element in {} sec".format( i ) )
            return res

        i += 1
        sleep( 1, False )

    #print()
    return False, None, 0

def find_element_by_xpath_with_timeout( parent, name: str, timeout: int ):
    i = 0

    #print_debug( "waiting till loaded ", '', True );

    while i <= timeout:
        if does_xpath_exist( parent, name ):
            #print()
            #print_debug( "loaded element in {} sec".format( i ) )
            return parent.find_element( 'xpath', name )

        i += 1
        sleep( 1, False )

    raise Exception( f"cannot load element {name} in {timeout} sec" )

def find_elements_by_xpath_with_timeout( parent, name: str, timeout: int ):
    i = 0

    #print_debug( "waiting till loaded ", '', True );

    while i <= timeout:
        if does_xpath_exist( parent, name ):
            #print()
            #print_debug( "loaded element in {} sec".format( i ) )
            return parent.find_elements( 'xpath', name )

        i += 1
        sleep( 1, False )

    raise Exception( f"cannot load element {name} in {timeout} sec" )

##########################################################

def scroll_to_bottom( parent ):

    parent.execute_script( "window.scrollTo(0, document.body.scrollHeight);" )

##########################################################

def is_clickable( parent ) -> bool:
    return parent.is_enabled() and parent.is_displayed()

def wait_till_clickable( parent, timeout: int ):
    i = 0

    #print_debug( "waiting till clickable ", '', True );

    while i <= timeout:
        if is_clickable( parent ):
            #print()
            #print_debug( "element is clickable in {} sec".format( i ) )
            return

        i += 1
        sleep( 1, False )

    raise Exception( f"element is not clickable in {timeout} sec" )

def wait_till_clickable_and_click( parent, timeout: int ):

    wait_till_clickable( parent, timeout )

    parent.click()

def get_optional_element_text_by_class_name( parent, class_name, default_value ):

    if does_class_exist( parent, class_name ):
        div = parent.find_element( 'class_name', class_name )
        return div.text

    return default_value

def find_element_by_tag_name_and_attribute_name( driver, tag_name, attribute_name, attribute_val, is_whole_name = True ):

    #print_info( "looking for '{}' '{}' = '{}':".format( tag_name, attribute_name, attribute_val ) )

    all_elems = driver.find_elements( 'tag_name',  tag_name )

    #print_debug( "find_element_by_tag_name_and_attribute_name: all '{}' {}:".format( tag_name, len( all_elems ) ) )

    for i in all_elems:
        i_val = i.get_attribute( attribute_name )
        #print_debug( "find_element_by_tag_name_and_attribute_name: {} '{}' '{}'".format( i.text, attribute_name, i_val ) )
        if is_whole_name:
            if i_val == attribute_val:
                #print_debug( "find_element_by_tag_name_and_attribute_name: FOUND - {}".format( i_val ) )
                return i
        else:
            if attribute_val in i_val:
                #print_debug( "find_element_by_tag_name_and_attribute_name: FOUND - {} ".format( i_val ) )
                return i

    #print_debug( "find_element_by_tag_name_and_attribute_name: not found - tag '{}' attr '{}' = '{}':".format( tag_name, attribute_name, attribute_val ) )

    return None

def find_element_by_tag_and_class_name( driver, tag_name, class_name, is_whole_name = True ):

    return find_element_by_tag_name_and_attribute_name( driver, tag_name, "class", class_name, is_whole_name )

def dump_elements_by_tag_name( driver, tag_name ):

    all_elems = driver.find_elements( 'tag_name',  tag_name )

    #print( "dump_elements_by_tag_name: tag '{}', found {} element(s):".format( tag_name, len( all_elems ) ) )

    #for i in all_elems:
    #    pass
    #    print( "class '{}', id '{}'".format( i.get_attribute( 'class' ), i.get_attribute( 'id' ) ) )

def quote_quotes( s: str ) -> str:
    res = s.replace( '"', '""' )
    return res

def to_csv_conform_string( s: str, separator = ';' ) -> str:

    if s.find( separator ) != -1 or s.find( '"' ) != -1:
        return '"' + quote_quotes( s ) + '"'

    return s

##########################################################

def harmonize_link( link: str ) -> str:

    if link.endswith('/'):
        return link

    return link + '/'
