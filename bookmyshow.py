#!/usr/bin/env python3
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

#Specify the exact webpage url containing the listings of cinema's for the
#particular date and movie;
url = 'https://in.bookmyshow.com/buytickets/act-1978-bengaluru/movie-bang-ET00300389-MT/20201128'

#Specify the Cinema name you want to look for.
#This "cinema" will be searched as a RegEx, so you need not provide the complete
#cinema name.
cinema = 'PVR: Central Spirit Mall, Bellandur'

#This function will be called if we find the tickets to be available
#It will open(or using an already openned) Chrome session to open the webpage
def open_url():
    #Open the URL in a browser
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(url)
    return

#This function will be used to create the popup alert for the user informing
#them of the availability of the ticket.
#The "Click me!" button will call the "open_url()" method described above.
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

#This function is called once we obtain the raw HTML document of the webpage;
#It will parse the document layer by layer, through the <a> and <strong> tags;
#Then, it will do a line-by-line Regex search for the input cinema name;
#If the cinema is found -> It will call the "create_popup()" method;
#If the cinema is not found -> It will return the control to the calling method;
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
        result = re.search(rf'{cinema}', str(element))
        if result is None:
            continue
        else:
            create_popup()
            exit()
    display.display("Tickets were not available at :" + str(datetime.datetime.now()))
    return

#This function is called by "main()";
#It will "process" the input webpage url to obtain the raw HTML document;
#Then, it will call the "parse_and_check_tickets()" method described above;
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

#In parse_and_check_tickets(), if the cinema name wasn't present, control will
#return back to main(). The execution thread will then "sleep/wait" for
#300 seconds/5 minutes, before re-running the list of functions again.
#When we re-run them, the webpage url is fetched again, so it will account for
#any changes in the url's contents.
    while True:
        fetch_html()
        time.sleep(300)



if __name__ == "__main__":
    main()
