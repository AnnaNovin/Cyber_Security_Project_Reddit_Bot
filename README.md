# Cyber Security Project - Super-Resilient C&C System Based on Reddit
Cyber Security project by Anna Novin and Barak Sofir with the guidance of Amichai Shulman at the Computer Science Faculty, Technion.
The project focused on proving the concept of super-resilient Command and Control (C&C) systems, leveraging public infrastructure while maintaining cost-effectiveness.

## MOTIVATION
Command and Control infrastructure is a critical component of any modern cyber attack campaign. Presently, most of the C&C infrastructures rely on server-based systems, which are expensive to maintain and require complicated technical skills to operate them in a stealthy and resilient way. The disruption and dismantling of these servers consequently incapacitate the attack communication, effectively bringing the campaign to a standstil.

## OUR SOLUTION 
We have developed a sophisticated C&C insfrastructure that seamlessly integrates into the existing infrastructure or Reddit, by concealing the command messages in comments on existing content. This innovative approach effectively hides the communication in plain sight.
Leveraging the search functionality of Reddit, we established a link between the controller and the bot. This is accomplished by using everyday keywords embedded within the command message.
Intriguingly, commands are identified only by these keywords and not by the user that posted the comment, making it harder to detect or dismantle the infrastructure.
Each control message serves as a breadcrumb to the next - by incorporating the keywords for the subsequent command into the current one, creating a continuous and hard-to-detect chain of commands.
We have made a significant finding that it is possible to create a Reddit account using a false email address, combined with breaking through the reCAPTCHA security measure. This revelation allowed us to establish an under the-radar reverse communication channel from the bot back to the controller, based on comments as well.
Interestingly, not only do our comments comply with Reddit's policy, but they also prompt positive interactions from legitimate users. This unexpected engagement stands as compelling evidence that our covert infrastructure effectively remains undetectable.

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
