# Reddit Bot
Cyber Security project by Anna Novin and Barak Sofir that successfully implements the concept of a super resilient C&C communication based on public infrastructure in a cost-effective way. 
We designed a fully functional communication system based on comments on Reddit content that is extremely difficult to detect and more importantly, one that is impossible to dismantle.
We were able to revise the Reddit system in a way that allowed full-duplex communication between the bots and the controller. One of the key features of our system is that it is designed in a manner that does not require the controller of the botnet to create new content but piggybacking on existing content. In this manner we were able to avoid any chance of detection by literally hiding the control messages in plain sight.

## Requirements
- Python 3.11+

## Installation

Before running the project install the following:
```sh
pip install undetected-chromedriver
```
Install the module SpeechRecognition with the version 3.8+
```sh
pip install SpeechRecognition
```
Also, install the correct version of chromedriver.exe for your Chrome browser from here: https://chromedriver.chromium.org/downloads
