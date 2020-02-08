"""
DONE BY: CHIN CLEMENT

This program automatically sends daily safety reminders to a Whatsapp group of my choosing
The groups to send to are stored in a text file called 'safety_messages_groups.txt'
The safety messages are stored in a text file called 'safety_messages.txt'
The safety quotes are stored in a text file called 'safety_quotes.txt'
The config file has all the variables that we can change, stored in 'config.py'

// TODO
1. Telegram bot to add custom text to the back of the script (safety_message_urgent.txt)
2. Add categories to the safety messages and quotes that we randomise (dict, tagging)
"""

from safety_message_bot_supporting_funcs import *
import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from time import sleep
from datetime import datetime
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def whatsapp_bot():
    """
    This function opens a browser and waits for user to scan QR code and send an empty string
    here to continue the program.
    Then it will send a safety message to the different groups of our choosing, when the conditions are met (time)
    """
    driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)
    print 'Safety Message WhatsApp Bot Started.'
    print 'Scan QR code.'
    # Opens whatsapp web
    driver.get('https://web.whatsapp.com/')

    # Wait for qr to be scanned
    raw_input('Type anything after scanning QR code > ')

    while True:

        curr_hour_min = datetime.now().strftime('%H%M')

        if curr_hour_min == TIME_TO_SEND_SAFETY_MESSAGE:

            safety_messages_lst = get_safety_messages()
            safety_quotes_lst = get_safety_quotes()
            curr_date = datetime.now().strftime('%d%m%Y')
            safety_msg = safety_messages_lst[random.randint(0, len(safety_messages_lst) - 1)]
            safety_quotes = safety_quotes_lst[random.randint(0, len(safety_quotes_lst) - 1)]
            full_safety_msg = FULL_SAFETY_MSG.format(curr_date, safety_quotes, safety_msg)
            groups_lst = get_groups()

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

        # Does not keep trying to get its current time and waste resources
        # Tries every 30s
        sleep(35)


def main():
    """This function starts off the program"""
    try:
        whatsapp_bot()
    except WebDriverException:
        print 'Browser closed.\nTerminating Program.'
        sys.exit(1)


if __name__ == '__main__':
    main()
