#!/usr/bin/env python3
#/Users/mahs/Documents/Personal/Personal_Projects/"Movie Tickets"/"base copy.py"
import sys
import os
import re
import time
import urllib.request as urllib2
import tkinter
import webbrowser
import datetime
from IPython import display
from bs4 import BeautifulSoup

url = 'https://in.bookmyshow.com/buytickets/act-1978-bengaluru/movie-bang-ET00300389-MT/20201128'

def open_url():
    #Open the URL in a browser
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(url)
    return

def create_popup():
    root = tkinter.Tk()
    text = "Theatre is now OPEN!"

    label = tkinter.Label(root, text=text)
    label.pack()

    test = tkinter.Button(root, text="Click me!",
              command = open_url)
    test.pack()
    root.test = test

    quit = tkinter.Button(root, text="QUIT", command = root.destroy)
    quit.pack()

    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()

    return

def parse_and_check_tickets(url_openned):
    #Code to parse the HTML document of the url, and check for the particular tickets
    url_soup = BeautifulSoup(url_openned, features="html5lib")

    #Use find_all() to restritct to HTML tags for <a class: __venue-name>
    a_class = url_soup.find_all("a", {"class": "__venue-name"})
    a_class_str = str(a_class)

    #Use BeautifulSoup again to format the remaining HTML text
    a_class_soup = BeautifulSoup(a_class_str, features="html5lib")
    #Use find_all() to further restrict the remaining HTML code to <strong> tags
    strong = a_class_soup.find_all("strong")
    strong_str = str(strong)

    #The remaining <strong> tag text contains the list of Cinema names
    #We iterate through the list to find the one we're looking for.
    for element in strong:
        result = re.search(r'PVR: MSR Elements Mall', str(element))
        if result is None:
            continue
        else:
            create_popup()
            exit()
    display.display("Tickets were not available at :" + str(datetime.datetime.now()))
    return

def fetch_html():
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    #Openning the url using Request() and urlopen() functions
    #We will eventually obtain the raw HTML contents in the "url_openned" variable
    url_request = urllib2.Request(url = url, headers = headers)
    try:
        url_openned = urllib2.urlopen(url = url_request)
    except urllib2.HTTPError as e:
        display.display(e.code)
        display.display(e.read())

    parse_and_check_tickets(url_openned)
    return


def main():
#We have four functions in use here. Their order of execution is as this:-
#fetch_html() -> parse_and_check_tickets() -> create_popup() -> open_url()
    while True:
        fetch_html()
        time.sleep(300)



if __name__ == "__main__":
    main()
