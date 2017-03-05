import sys
import time
import telepot
id_count = {};
id_nicks = {};
bot = telepot.Bot('261334375:AAHlnUWwZ8cxTEu4JSJ90PcMBP__8V9IFiw');

def write_id_info():
	open('ids.txt', 'a').close()
	f = open('ids.txt', 'w')
	buffer = ''	
	for id in id_count:
		buffer += str(id) + ' '
		buffer += str(id_count[id]) + ' '
		for nick in id_nicks[id]:
			buffer += nick + ' ' 
		buffer += '\n'
	f.write(buffer)
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
	receiver = '';
	if str(sender['id']) not in id_count:
		id_nicks[str(sender['id'])] = []
		if 'username' in sender:
			id_nicks[str(sender['id'])].append(sender['username'].lower())
		if 'first_name' in sender:
			id_nicks[str(sender['id'])].append(sender['first_name'].lower())
		if 'last_name' in sender:
			id_nicks[str(sender['id'])].append(sender['last_name'].lower())
		id_count[str(sender['id'])] = 0;
		write_id_info()
	if content_type == 'text':
		if 'rename' in msg['text']:
			msg_words = msg['text'].split()
			if len(msg_words) == 3:
				if msg_words[2] not in id_nicks[str(sender['id'])]:
					rename(str(sender['id']), msg_words[2]) 
				else:
					swap_index = id_nicks[str(sender['id'])].index(msg_words[2])
					temp_nick = id_nicks[str(sender['id'])][0]
					id_nicks[str(sender['id'])][0] = id_nicks[str(sender['id'])][swap_index]
					id_nicks[str(sender['id'])][swap_index] = temp_nick
		elif '++' in msg['text']:
			count_handler(1 , msg['text'], sender['id'], chat_id)
		elif '--' in msg['text']:
			count_handler(-1 , msg['text'], sender['id'], chat_id)
		elif 'count pls' in msg['text']:
			count_pls = 'Current counts:\n'
			for user in id_count:
				count_pls += id_nicks[user][0] + ' = ' + str(id_count[user]) + '\n'
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
	if last_of_first == 'bot':
		id_nicks['0'] = ['bot']
		if '0' in id_count:
			count = int(id_count['0'])
			count += direction;
			id_count['0'] = str(count)
		else:
			id_count['0'] = 0;
			id_nicks['0'] = ['bot']
		bot.sendMessage(chat_id, 'Updated bot\'s score')
	else :
		for id in id_nicks:
			if last_of_first in id_nicks[id]:
				if int(id) != sender_id:
					count = int(id_count[id])
					count += direction;
					id_count[id] = str(count)
					bot.sendMessage(chat_id, 'Updated ' + str(last_of_first) + '\'s score')
					write_id_info()
					return last_of_first; 

def rename(sender_id, new_name):
	id_nicks[sender_id].insert(0, new_name);

def main():
	bot.message_loop(handle)
	print ('Listening ...')
	read_id_info()
	# Keep the program running.
	while 1:
		time.sleep(10)

main();
