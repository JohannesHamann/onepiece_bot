#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time

""" functions the bot shall execute """

""" Einfache Test Befehle """
def stop(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id , text = "See you next time, Senchou!")
    #Updater(token= Bot_token, use_context=True).stop()

def hello(update, context):
    context.bot.send_message(chat_id= update.effective_chat.id , text = "Hey Senchou! Are we good for an adventure?")


# Vorherige Scraping methode, die jedoch nicht von Telegram aus unterbrochen werden kann
# ----> Zum Unterbrechen der Fuktion muss entweder in jedem Lauf updater.poll() aufgerufen werden, um interrupts möglich zu machen, oder die Methode in eigenem Thread oder asynchron 
# ----> ausgeführt werden, siehe asyncIO oder threading
def scraping_old( update, context):
    # scrapes the manga website, filters, saves latest manga and sends out the wanted
    # text messages via telegram
    while True:
        text_file_name = "onepiece_chapter.txt" 
        # make the get request
        website = requests.get("https://w16.read-onepiece.com/")
        # extract the html code and convert it from unicode to str
        html_text = str(website.text)
        # the relevant string to search for 
        search_string = "one-piece-chapter-"
        # find only neccessary link (it's the first because of the architechure of the site)
        # it searches for the first time "one-piece-chapter-" is used and looks as far until the link bracket is ended ">"
        latest_chapter_string = html_text[html_text.find(search_string) :html_text.find(search_string) + html_text[html_text.find(search_string):].find("/>") -1] 
        latest_chapter = int(latest_chapter_string[len(search_string):len(search_string) + latest_chapter_string[len(search_string):].find("/")])
        print (latest_chapter)
        latest_chapter_link = "https://w16.read-onepiece.com/manga/"+search_string+str(latest_chapter)+"/"


        with open(text_file_name , "r") as text_file:
            old_chapter = int(text_file.read())
        if latest_chapter > old_chapter:
            print ("Senchou! Kapitel %s ist raus!" % str(latest_chapter))
            context.bot.send_message(chat_id= update.effective_chat.id , text = "Senchou! Kapitel %s ist raus!" % str(latest_chapter)+ "\n" + "\n" + latest_chapter_link)
            with open(text_file_name, "w") as text_file:
                text_file.write(str(latest_chapter))
        if latest_chapter < old_chapter:
            print ("Heee, da war etwas falsch abgespeichert. Ich habe mich darum gekümmert, Senchou!")
            context.bot.send_message(chat_id= update.effective_chat.id , text = "Heee, da war etwas falsch abgespeichert. Ich habe mich darum gekümmert, Senchou!")            
            with open(text_file_name, "w") as text_file:
                text_file.write(str(latest_chapter))
        time.sleep(10)
    # Falls die loop jemals ungewollt beendet wird, dient diese Nachricht dazu, darauf hinzuweisen.
    context.bot.send_message(chat_id= update.effective_chat.id , text = "Senchou, ich bin müde. Bitte weck mich, um meine Dienste erneut zu nutzen!")


# Dies ist bisher eine allgemeine Funktion, muss aber eventuell noch auf Telegram (z.B. mit update, context) erweitert werden
def scraping_new(website, saving:bool, save_name):  
    http_request = requests.get(website)    # make the get request
    html_text = str(http_request.text)      # extract html code and convert it from unicode to str
    if type(saving) == bool:                # save it to file or return its value
        if saving == True:
            with open(save_name, "w", encoding="utf-8") as file:
                file.write(html_text)
        elif saving == False:
            return html_text
    elif type(saving) != bool: 
        print ("Bitte geben Sie als zweiten Parameter True/False an, jenachdem ob Sie den scrape speichern möchten oder nicht.")

#scraping("https://w16.read-onepiece.com/", True, "read-onepiece_com.txt")

