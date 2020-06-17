"""
Created Jan 2020
@author: somhalder
"""


import speech_recognition as sr
from time import ctime
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from selenium import webdriver

r = sr.Recognizer()


def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            riri_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            riri_speak('Sorry , I did not get that')
        except sr.RequestError:
            riri_speak('Sorry, my speech service is down')
        return voice_data

def riri_speak(audio_string):
    tts = gTTS(text = audio_string, lang='en')
    r = random.randint(1,10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if 'what is your name' in voice_data:
        riri_speak ('My name is Riri')
    if 'how are you' in voice_data:
        riri_speak ('I am good, thanks for asking, how may I help you?')
    if 'what time is it' in voice_data:
        riri_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        riri_speak('Here is what i found for' + search)
    if 'location' in voice_data:
        location = record_audio('What is the location you want to find?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        riri_speak('Here is the location of' + location)
    if 'play' in voice_data:
        artist = record_audio('Which artist do you want to listen to?')
        riri_speak('Playing ' + artist)
        artist = '%20'.join(artist.split(' '))
        browser = webdriver.Chrome()
        browser.get('https://soundcloud.com/search?q=' + artist)
        playbutton = browser.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[3]/div/div/div/ul/li[2]/div/div/div/div[2]/div[1]/div/div/div[1]/a')
        playbutton.click()
    if 'exit' in voice_data:
        exit()


time.sleep(1)
riri_speak('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)
