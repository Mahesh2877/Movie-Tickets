# Movie-Tickets
Here, we describe the code which will ping a ticket booking webpage and alert the user as and when tickets are available.

This code works for bookmyshow.com, an India based ticket booking platform.
The user has to provide the particular webpage url of Bookmyshow which contains the listings of Cinema's for the particular movie on the particular date.

If the code detects that the particular Cinema is NOT listed, it sleeps for 300 seconds(5 minutes) before re-running.
If the code detects that the particular Cinema IS listed, it displays a PopUp alerting the user of the same. Clicking on the "Click me" button on the popup will open the webpage url in Chrome Browser, where the user can proceed to book the tickets! If a Chrome browser session was already openned, a new tab will be openned in the same session.
