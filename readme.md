### Wow Perfplot

## Goals
Wow is mostly dominated by DPS logs, which are a good tool for improving as a player but can encourage some bad behavior in persuit of top damage the expense of teammates experiances.  Some tools, for example WipeFest, exist to help tell the other side of the story.  Perfplot attempts to merge the two to create a better picture of where players sit relative to one another in these two metrics only.

## Pre-Reqs

You will need to install chromedriver for you current version of chrome.

https://chromedriver.chromium.org/downloads

You will need to install the pip requirements.

pip install -r requirements.txt

Create an API key for warcraft logs.

https://www.warcraftlogs.com/api/clients/

_(Maybe) You may need to submit your logs to wipefest.gg, we use the wipefest.gg bot to monitor our reports.

## Limitations

Only public logs are supported.

As always this is just a tool for visualizing data, it doesn't take into account all factors and doesn't provide a complete picture of player performance.

## Setup

In the plot.py application you need to setup your API keys for Warcraft Logs.  Update these lines:

client_id = '<<your client_id here>>'
client_secret = '<<your client_secret here>>'

Insert your report ID and set the boss you want it to parse.

## Running the Script

python plot.py

## What am I looking at?

The script reads a report

## Support

This is a quick script I threw together and I probably won't support it.