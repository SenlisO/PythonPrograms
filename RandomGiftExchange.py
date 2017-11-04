"""
RandomGiftExchange.py

This program is designed to receive a list of gift givers, in code, and randomly choose
gift recipients.  The gift givers can be the recipients also, or there can be a separate
recipients list.  Givers and recipient lists must be the same length
"""

import random

givers = ["INSERT GIFT GIVERS NAMES"] # ATTENTION: input the gift givers names here

# generate recipients here
separate_recipients = True
if separate_recipients:
    recipients = ["INSERT RECIPIENT NAMES IF DIFFERENT"] # ATTENTION: input the recipients names here if different
else:
    recipient = givers

pairs = {} # result from the program.  Stores giver, recipient pairs
index = 0 # temporary array reference number

for giver in givers: # pair givers with recipients
    index = random.randint(0, (len(recipients) - 1)) # from 0 to last index of recipients
    pairs[giver] = recipients.pop(index) # remove item and index and add to pair dictionary

for giver in givers:
    print(giver + ": " + pairs[giver])