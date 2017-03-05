import sys
import time
import telepot
id_count = {};
id_nicks = {};
id_chats = {};
bot = telepot.Bot('261334375:AAHlnUWwZ8cxTEu4JSJ90PcMBP__8V9IFiw');

def write_id_info():
	open('ids.txt', 'a').close()
	f = open('ids.txt', 'w')
	buffer = ''	
	for id in id_count:
		buffer += str(id) + ' '
		buffer += str(id_count[id]) + ' '
		for chat in id_chats[id]:
			buffer += chat + ' '
		buffer += '-n '
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
			id_chats[val[0]] = []
			if len(val) > 2:
				counter = 2
				while val[counter] != '-n':
					id_chats[val[0]].append(val[counter])
					counter += 1
			counter += 1
			id_nicks[val[0]] = []
			if len(val) > counter:
				for i in range(counter, len(val)):
					id_nicks[val[0]].append(val[i])

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	sender = msg['from']
	sender_id = str(sender['id']);
	receiver = '';
	if str(sender['id']) not in id_count:
		id_nicks[str(sender['id'])] = []
		if 'username' in sender:
			id_nicks[sender_id].append(sender['username'].lower())
		if 'first_name' in sender:
			id_nicks[sender_id].append(sender['first_name'].lower())
		if 'last_name' in sender:
			id_nicks[sender_id].append(sender['last_name'].lower())
		id_count[str(sender['id'])] = 0;
		write_id_info()
	if content_type == 'text':
		if 'rename' in msg['text']:
			conflict = False;
			msg_words = msg['text'].split()
			if len(msg_words) == 3 and not msg_words[2].isdigit():
				if msg_words[2] in id_nicks[sender_id]:
					swap_index = id_nicks[sender_id].index(msg_words[2])
					temp_nick = id_nicks[sender_id][0]
					id_nicks[sender_id][0] = id_nicks[sender_id][swap_index]
					id_nicks[sender_id][swap_index] = temp_nick
					bot.sendMessage(chat_id, 'Successfully changed primary nickname to existing nickname ' + msg_words[2])
				else:
					for id in id_nicks:
						for nick in id_nicks[id]:
							if nick.lower() == msg_words[2].lower():
								conflict = True;
								bot.sendMessage(chat_id, 'Bad user. Don\'t steal usernames.')
								break;
				if not conflict:
					if msg_words[2] not in id_nicks[sender_id]:
						rename(sender_id, msg_words[2])
						bot.sendMessage(chat_id, 'Successfully renamed to ' + msg_words[2])
				write_id_info()
		elif '++' in msg['text']:
			count_handler(1 , msg['text'], sender['id'], chat_id)
		elif '--' in msg['text']:
			count_handler(-1 , msg['text'], sender['id'], chat_id)
		elif 'count pls' in msg['text']:
			count_pls = 'Current counts:\n'
			for user in id_count:
				if str(chat_id) in id_chats[user]:
					count_pls += id_nicks[user][0] + ' = ' + str(id_count[user]) + '\n'
			bot.sendMessage(chat_id, count_pls)
		elif '+=' in msg['text']:
			bot.sendMessage(chat_id, 'Unsupported behaviour. Pls increment by one brownie point at a time.')
		elif '-=' in msg['text']:
			bot.sendMessage(chat_id, 'Unsupported behaviour. Pls decrement by one brownie point at a time.')
		elif '*=' in msg['text']:
			bot.sendMessage(chat_id, 'Unsupported behaviour. Pls increment by one brownie point at a time.')
		elif '/=' in msg['text']:
			bot.sendMessage(chat_id, 'Unsupported behaviour. Pls decrement by one brownie point at a time.')
		#else:
			#bot.sendMessage(chat_id, 'I didn\'t understand that. Please consult the docs at https://github.com/nathan-contino/infamyBot')
				

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
				else:
					bot.sendMessage(chat_id, 'Bad user. Don\'t try to change your own score.')

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
