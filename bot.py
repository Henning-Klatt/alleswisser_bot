#!/usr/bin/env python
# coding: utf8

import sys, os, random, time, codecs
import telepot
import MySQLdb
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from termcolor import colored

codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


os.environ['TZ'] = 'Europe/Berlin'

bot = telepot.Bot('xxxxxxx:xxxxxxxxxxxxxxxxx')

connection = MySQLdb.connect (host = "lexodexo.de",
				user = "xxxxx",
			  	passwd = "xxxx",
			  	db = "xxxx",
			  	charset = 'utf8mb4',
			  	use_unicode=True)

cursor = connection.cursor()
cursor.execute("set names utf8mb4;")

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	chat_id = str(chat_id).replace(" ", "")
	try:
		vorname = msg['from']['first_name'].encode('utf8')
	except KeyError, e:
		vorname = "NULL"
	try:
		nachname = msg['from']['last_name'].encode('utf8')
	except KeyError, e:
		nachname = "NULL"
	try:
		username = msg['from']['username'].encode('utf8')
	except KeyError, e:
		username = "NULL"

	msg_id = msg['message_id']

	if(content_type == "text"):

		cursor.execute("UPDATE user SET time='" + zeit + "' WHERE chat_id='" + chat_id + "'")
		connection.commit()

		nachricht = msg['text']#.encode('utf8').replace("ß", "ss")

		if nachricht.startswith ( '/' ):

			if(nachricht.lower() == "/help" or nachricht.lower() == "/hilfe"):
				show_keyboard = {'keyboard': [['/user', '/hide', '/admins', '/count'], ['Hallo', 'Guten Abend', 'Wie alt bist du?', 'Wer bist du?']]}
				bot.sendMessage(chat_id, "Hilfe:" , reply_markup=show_keyboard)
			elif(nachricht.lower() == "/hide"):
				hide_keyboard = {'hide_keyboard': True}
				bot.sendMessage(chat_id, "Keyboard versteckt." , reply_markup=hide_keyboard)

			elif(nachricht.lower() == "/count"):
				cursor.execute("SELECT * FROM messages;")
				count = cursor.rowcount
				bot.sendMessage(chat_id, "Ich kann schon " + str(count) + " Sätze verstehen und auf sie antworten." )

			elif(nachricht.lower() == "/user"):
				cursor.execute("SELECT * FROM user;")
				count = cursor.rowcount
				bot.sendMessage(chat_id, "Es sind schon " + str(count) + " Benutzer bei mir registriert." )

			elif(nachricht == "/list"):
				bot.sendMessage(chat_id, "Dieser Command kann nur von Admins ausgeführt werden.")
				#cursor.execute("SELECT coming, going FROM messages;")
				#result = cursor.fetchall()
				#for data in result:
					#frage = data[0].encode('utf8')
					#antwort = data[1].encode('utf8')
					#bot.sendMessage(chat_id, str(frage) + " - " + str(antwort))

			elif(nachricht.lower() == "/admins"):
				cursor.execute("SELECT vorname FROM user WHERE job ='admin';")
				result = cursor.fetchall()
				bot.sendMessage(chat_id, "Admins:")
				for data in result:
					admin_vorname = data[0]
					bot.sendMessage(chat_id, str(admin_vorname))

			elif(nachricht.lower() == "/akzeptieren"):
				cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
				user_exists = cursor.rowcount
				if(user_exists != 0):
					cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
					result = cursor.fetchall()
					for data in result:
						aktuellerjob = data[5]
					if(aktuellerjob != "frei"):
						job = "frei"
						cursor.execute("UPDATE user SET job='" + job + "' WHERE chat_id='" + chat_id + "'")
						connection.commit()
						bot.sendMessage(chat_id, "Du hast erfolgreich den Haftungsausschluss akzeptiert und kannst jetzt mit dem Bot schreiben!")
						print "============[" + zeit + "]==============="
						print vorname + " " + nachname + " (" + username + ")"
						print "Hat Haftungsausschluss akzeptiert."
					else:
						bot.sendMessage(chat_id, "Du hast den Haftungsausschluss bereits akzeptiert.")
						print "============[" + zeit + "]==============="
						print vorname + " " + nachname + " (" + username + ")"
						print "Hat Haftungsausschluss bereits akzeptiert."


			elif nachricht.lower().startswith ( '/save ' ):
				neue_antwort = nachricht[6:]
				#Bekomme letzte Nachricht
				cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
				result = cursor.fetchall()
				for data in result:
					letzte_nachricht = data[1]
					username = data[2]
					vorname = data[3]
					nachname = data[4]

				cursor.execute("SELECT * FROM messages WHERE coming ='" + letzte_nachricht + "' AND going ='" + neue_antwort + "';")
				eintrag_exists = cursor.rowcount
				if(eintrag_exists == 0):
					cursor.execute("INSERT INTO messages (chat_id, coming, going, username, vorname, nachname, time) VALUES ('" + chat_id + "','" + letzte_nachricht + "','" + neue_antwort + "','" + username + "','" + vorname + "','" + nachname + "','" + zeit + "');")
					connection.commit()
					bot.sendMessage(chat_id, "Du hast folgendes eingespeichert:")
					bot.sendMessage(chat_id, "Frage: " + letzte_nachricht)
					bot.sendMessage(chat_id, "Antwort: " + neue_antwort)
					print "============[" + zeit + "]==============="
					print vorname + " " + nachname + " (" + username + ")"
					print "Frage: " + letzte_nachricht.encode('utf8')
					print "Antwort: " + neue_antwort.encode('utf8')
					print "Eingespeichert!"


				if(eintrag_exists != 0):
					bot.sendMessage(chat_id, "Dieser Eintrag wurde bereits eingespeichert!")
					print "============[" + zeit + "]==============="
					print vorname + " " + nachname + " (" + username + ")"
					print "Frage: " + letzte_nachricht.encode('utf8')
					print "Antwort: " + neue_antwort.encode('utf8')
					print "Nicht eingespeichert, da es schon existiert."

			#elif nachricht.lower().startswith('/save'):
				#Bekomme Satz auf den das Bild geschickt werden soll
				#cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
				#result = cursor.fetchall()
				#for data in result:
					#letzte_nachricht = data[1]
					#username = data[2]
					#vorname = data[3]
					#nachname = data[4]

				#cursor.execute("SELECT * FROM messages WHERE coming ='" + letzte_nachricht + "' AND going ='" + neue_antwort + "';")
				#eintrag_exists = cursor.rowcount
				#Wenn noch nicht eingespeichert wurde
				#if(eintrag_exists == 0):



			else:
				bot.sendMessage(chat_id, "Unbekannter Command: " + nachricht)
				bot.sendMessage(chat_id, "Übersicht der Commands: /help")

		#Wenn kein Command
		else:
			if(chat_type == "private"):

				#Neuer Benutzer?
				cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
				user_exists = cursor.rowcount
				if(user_exists == 0):
					job = "neu"
					try:
						cursor.execute("INSERT INTO user (chat_id, letzte_nachricht, username, vorname, nachname, job, time) VALUES ('" + str(chat_id) + "','" + nachricht + "','" + username + "','" + vorname + "','" + nachname + "','" + job + "','" + zeit + "');")
						connection.commit()
					except UnicodeDecodeError:
						bot.sendMessage(chat_id, "Deine Userdaten sind ungültig. Bitte verwende keine Smileys etc.. in deinem Namen.")

				#Datenbank updaten
				cursor.execute("SELECT * FROM user WHERE chat_id ='" + chat_id + "';")
				result = cursor.fetchall()
				for data in result:
					aktuellerjob = data[5]
					zuletztonline = data[6]

				#Wenn Erlaubnis hat
				if(aktuellerjob == "frei" or aktuellerjob == "admin"):
					#Update seiner Usernamen etc...
					cursor.execute("UPDATE user SET letzte_nachricht='" + nachricht + "', username='" + username + "', vorname='" + vorname + "', nachname='" + nachname + "', time='" + zeit + "' WHERE chat_id='" + chat_id + "'")
					connection.commit()

					#Bekomme alle Nachrichten
					cursor.execute("SELECT coming FROM messages;")
					db_nachrichten = cursor.fetchall()
					nachrichten = []
					#Wenn Antwort gefunden
					if len(db_nachrichten) != 0:
						#Jede einzelne Nachricht in einen Array
						for data in db_nachrichten:
							nachrichten.insert(0, data[0])

						beste_nachricht = process.extractOne(nachricht, nachrichten)[0]
						genauigkeit = process.extractOne(nachricht, nachrichten)[1]

						#Ist Antwort genau genug?
						if(genauigkeit > 94):
							#Suche nach Antwort auf ähnlichste Frage
							cursor.execute("SELECT * FROM messages WHERE coming ='" + beste_nachricht + "';")
							going = cursor.fetchall()
							antworten = []
							#Speicher Antworten in Array
							for data in going:
								antworten.insert(0, data[2])

							#Wähle zufällige aus falls es mehrere gibt
							antwort = random.choice(antworten)
							bot.sendMessage(chat_id, antwort)
							print "============[" + zeit + "]==============="
							print vorname + " " + nachname + " (" + username + ")"
							print "Frage: " + nachricht.encode('utf8')
							print "Antwort(" + str(genauigkeit) + "): " + antwort.encode('utf8')

						else:
							bot.sendMessage(chat_id, "Leider habe ich keine genaue Antwort gefunden... Du kannst aber eine Antwort einspeichern, in dem du /save DEINE ANTWORT eingibst.")
							print "============[" + zeit + "]==============="
							print vorname + " " + nachname + " (" + username + ")"
							print "Frage: " + nachricht.encode('utf8')
							print "Genauigkeit: " + str(genauigkeit) + "%"
							print "Keine genaue Antwort gefunden."
					else:
						bot.sendMessage(chat_id, "Leider habe ich keine Antwort gefunden... Du kannst aber eine Antwort einspeichern, in dem du /save DEINE ANTWORT eingibst.")
						print "============[" + zeit + "]==============="
						print vorname + " " + nachname + " (" + username + ")"
						print "Frage: " + nachricht.encode('utf8')
						print "Genauigkeit: " + str(genauigkeit) + "%"
						print "Keine Antwort gefunden."


				elif(aktuellerjob == "frage"):
					bot.sendMessage(chat_id, "Bitte habe etwas geduld, bis deine Frage beantwortet wird.")
					print "============[" + zeit + "]==============="
					print vorname + " " + nachname + " (" + username + ")"
					print "Nachricht: " + nachricht
					print "Mehrere Fragen gestellt"

				elif(aktuellerjob == "-"):
					bot.sendMessage(chat_id, "Du wurdest von dem Bot blockiert, damit ein Admin ihn besser testen kann. Keine Sorge, bald kannst du wieder mit ihm schreiben!")
					print "============[" + zeit + "]==============="
					print vorname + " " + nachname + " (" + username + ")"
					print "Nachricht: " + nachricht
					print "Status: -"

				elif(aktuellerjob == "neu"):
					bot.sendMessage(chat_id, "Um diesen Bot benutzen zu können, musst du erst den Haftungsausschluss Akzeptieren.")
					result = bot.sendDocument(chat_id, open('haftungsausschluss.txt', 'rb'))
					file_id = result['document']['file_id']
					bot.sendDocument(chat_id, file_id)
					bot.sendMessage(chat_id, "Um den Haftungsausschluss zu akzeptieren, klicke hier: /akzeptieren")


	if(content_type == "audio"):
		print "ID: ",chat_id
		print "Audio Nachricht"
		print "Art: " + chat_type

		bot.sendMessage(chat_id, "Du hast eine Audio-Datei geschickt")

	if(content_type == "voice"):
		print "============[" + zeit + "]==============="
		print vorname + " " + nachname + " (" + username + ")"
		print "Hat eine Sprachmemo geschickt."

		bot.sendMessage(chat_id, "Du hast eine Sprachmemo geschickt", reply_to_message_id=msg_id)


bot.message_loop(handle)

print ('Listening ...')

while 1:
	zeit = time.strftime("%d.%m - %H:%M:%S")
	time.sleep(1)
