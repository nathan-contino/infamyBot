import sys
import time
import telepot
id_count = {};
id_nicks = {};
bot = telepot.Bot('261334375:AAHlnUWwZ8cxTEu4JSJ90PcMBP__8V9IFiw');

def write_id_info():
	f = open('ids.txt', 'w')
	
	for id in id_count:
		f.write(str(id) + ' ')
		f.write(str(id_count[id]) + ' ')
		for nick in id_nicks[id]:
			f.write(nick + ' ') 
		f.write('\n')
	f.close()

def read_id_info():
	f = open('ids.txt', 'r')
	filedata = f.read().split('\n')
	f.close()
	for id in filedata:
		if id != '':
			val = id.split()
			id_count[val[0]] = int(val[1])
			id_nicks[val[0]] = []
			if len(val) > 2:
				for i in range(2, len(val)):
					id_nicks[val[0]].append(val[i])

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	sender = msg['from']
#	print(content_type, chat_type, chat_id)
#	print(msg)
	receiver = '';
	if sender['id'] not in id_count:
		id_nicks[sender['id']] = []
		if 'username' in sender:
			id_nicks[sender['id']].append(sender['username'].lower())
		if 'first_name' in sender:
			id_nicks[sender['id']].append(sender['first_name'].lower())
		if 'last_name' in sender:
			id_nicks[sender['id']].append(sender['last_name'].lower())
		id_count[sender['id']] = 0;
		write_id_info()
	if content_type == 'text':
		if '++' in msg['text']:
			count_handler(1 , msg['text'], sender['id'], chat_id)
		if '--' in msg['text']:
			count_handler(-1 , msg['text'], sender['id'], chat_id)
		if 'count pls' in msg['text']:
			count_pls = 'Current counts:\n'
			for user in id_count:
				count_pls += id_nicks[user][2] + ' = ' + str(id_count[user]) + '\n'
			bot.sendMessage(chat_id, count_pls)
				

def count_handler(direction, text, sender_id, chat_id):
	crtyp = ''
	if direction > 0:
		crtyp = '++';
	if direction < 0:
		crtyp = '--';
	halves = text.split(crtyp)
	first = halves[0].split()
	last_of_first = first[len(first)-1].lower()
	for id in id_nicks:
		if last_of_first in id_nicks[id]:
			if int(id) != sender_id:
				count = int(id_count[id])
				count += direction;
				id_count[id] = str(count)
				bot.sendMessage(chat_id, 'Updated ' + str(last_of_first) + '\'s score')
				write_id_info()
				return last_of_first; 

def main():
	bot.message_loop(handle)
	print ('Listening ...')
	read_id_info()
	# Keep the program running.
	while 1:
		time.sleep(10)

main();
