"""
DONE BY: CHIN CLEMENT

This program automatically sends daily safety reminders to a Whatsapp group of my choosing
The safety messages are stored in a text file called 'safety_messages.txt'
The safety quotes are stored in a text file called 'safety_quotes.txt'
"""

import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep
from datetime import datetime
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

PATH_TO_CHROMEDRIVER = r'.\chrome_webdriver\chromedriver.exe'
PATH_TO_SAFETY_MESSSAGES = r'.\safety_messages.txt'
PATH_TO_SAFETY_QUOTES = r'.\safety_quotes.txt'
PATH_TO_GROUP_NAMES = r'.\safety_message_groups.txt'
MSG_BOX_CLASS_NAME = '_3u328'
SEND_BUTTON_CLASS_NAME = '_3M-N-'
FULL_SAFETY_MSG = '''Safety Message of the day ({})

_{}_

{}'''
SECONDS_TO_NEXT_DAY_SAME_TIME = 60 * 60 * 24
# in 24HR format
TIME_TO_SEND_SAFETY_MESSAGE = '0530'

# for testing
# TIME_TO_SEND_SAFETY_MESSAGE = '1818'


def whatsapp_bot():
    """This function opens a browser and sends a safety message when the conditions are correct"""
    driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)
    print 'Safety Message WhatsApp Bot Started.'
    print 'Scan QR code.'
    # Opens whatsapp web
    driver.get('https://web.whatsapp.com/')

    # Wait for qr to be scanned
    raw_input('Type anything after scanning QR code > ')

    while True:
        safety_messages_lst = get_safety_messages()
        safety_quotes_lst = get_safety_quotes()
        curr_hour_min = datetime.now().strftime('%H%M')
        curr_date = datetime.now().strftime('%d%m%Y')
        safety_msg = safety_messages_lst[random.randint(0, len(safety_messages_lst) - 1)]
        safety_quotes = safety_quotes_lst[random.randint(0, len(safety_quotes_lst) - 1)]
        full_safety_msg = FULL_SAFETY_MSG.format(curr_date, safety_quotes, safety_msg)
        groups_lst = get_groups()

        # Do action every minute
        if curr_hour_min == TIME_TO_SEND_SAFETY_MESSAGE:

            # send to all the groups that can be found in the list
            for group in groups_lst:

                # Finds the target group
                group = driver.find_elements_by_xpath('//span[contains(text(), "{}")]'.format(group))
                
                # To catch if the group does not exist, move on to the next group
                if not len(group) > 0:
                    continue
                group[0].click()

                # Finds the msgbox
                msg_box = driver.find_element_by_class_name(MSG_BOX_CLASS_NAME)

                # putting multiline comments without sending multiple messages into the msgbox
                for part in full_safety_msg.split('\n'):
                    msg_box.send_keys(part)
                    ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                        Keys.ENTER).perform()

                # Finds and clicks the send button
                send_button = driver.find_element_by_class_name(SEND_BUTTON_CLASS_NAME)
                send_button.click()

            print 'Safety message sent to the groups.'
            print 'Sleeping to tomorrow.'
            # sleep till its 30 seconds before we need to send another safety message (the next day)
            sleep(SECONDS_TO_NEXT_DAY_SAME_TIME - 30)


def get_groups():
    """Returns a list of groups in the safety_message_groups.txt file"""
    with open(PATH_TO_GROUP_NAMES, 'rb') as f:
        groups_lst = [msg.rstrip('\r\n') for msg in f]
    return groups_lst


def get_safety_quotes():
    """Returns a list of safety quotes in the safety_quotes.txt file"""
    with open(PATH_TO_SAFETY_QUOTES, 'rb') as f:
        safety_quotes_lst = [msg.rstrip('\r\n') for msg in f]
    return safety_quotes_lst


def get_safety_messages():
    """Returns a list of safety messages in the safety_messages.txt file"""
    with open(PATH_TO_SAFETY_MESSSAGES, 'rb') as f:
        safety_messages_lst = [msg.rstrip('\r\n') for msg in f]
    return safety_messages_lst


def main():
    """This function starts off the program"""
    try:
        whatsapp_bot()
    except WebDriverException:
        print 'Browser closed.\nTerminating Program.'
        sys.exit(1)


if __name__ == '__main__':
    main()
