# import threading
# import requests
# from app.mac import mac, signals

# @signals.message_received.connect
# def handle(message):
#     BotRequest(message)
#
# class BotRequest(object):
#     def __init__(self, msg):
#         self.message = msg
#         thread = threading.Thread(target=self.run, args=())
#         thread.daemon = True
#         thread.start()
#
#     def run(self):
#         try:
#             message = self.message
#             mac.send_message("Hello", message.conversation)
#             # requests.post('http://localhost:3001/paymentbot/whatsappwebhook', json={'event': 'INBOX', 'from': message.who, 'name': message.who_name, 'conversation': message.conversation, 'text': message.text, 'AppClient': 'Yowsup'})
#         except Exception as e:
#             print(e)
#             print("Error sending Orchestrator Request")
