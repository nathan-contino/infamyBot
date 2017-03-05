import sys
import time
import telepot

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

	if content_type == 'text':
		bot.sendMessage(chat_id, msg['text'])

		bot = telepot.Bot('261334375:AAHlnUWwZ8cxTEu4JSJ90PcMBP__8V9IFiw')
		bot.message_loop(handle)
		print ('Listening ...') 
		# Keep the program running.
		while 1:
			time.sleep(10)
