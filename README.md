# PyTxt  :email:
## _a library to simplifiy sending texts via email_


##### Example Usage
```python
# Setups up email client for sending messages 
sender = Sender(email="email@gmail.com", pwd="password")
# Creates contact 
bob = Recipient(name="Bob", phone_number="5555555555", carrier_name="straight_talk")
# Start text conversation
conversation = Conversation(sender=sender, recipient=me)
# Sends Text to Bob
conversation.say("Hello World")
# Checks to see if Bob responded to message    
conversation.check()
```
##### *currently only tested with GMAIL*
