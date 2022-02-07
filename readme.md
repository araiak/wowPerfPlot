### Wow Perfplot

## Goals
Wow is mostly dominated by DPS logs, which are a good tool for improving as a player but can encourage some bad behavior in pursuit of top damage the expense of teammates experiences.  Some tools, for example WipeFest, exist to help tell the other side of the story.  PerfPlot attempts to merge the two to create a better picture of where players sit relative to one another in these two metrics only.

## Pre-Reqs

You will need to install chromedriver for you current version of chrome.

https://chromedriver.chromium.org/downloads

You will need to install the pip requirements.

```
pip install -r requirements.txt
```

Create an API key for warcraft logs.

https://www.warcraftlogs.com/api/clients/

_(Maybe) You may need to submit your logs to wipefest.gg, we use the wipefest.gg bot to monitor our reports._

## Limitations

Only public logs are supported.

Chrome is not running in headless mode, its probably an easy fix, but I haven't done it yet.

As always this is just a tool for visualizing data, it doesn't take into account all factors and doesn't provide a complete picture of player performance.  This probably doesn't work very well for healers/tanks (maybe something I can add in the future).

## Setup

In the plot.py application you need to setup your API keys for Warcraft Logs.  Update these lines:

```
client_id = '<<your client_id here>>'
client_secret = '<<your client_secret here>>'
```

Insert your report ID and set the boss you want it to parse.

```
report_id = "<<your report_id>>" # This is the report ID URL from wcl (https://www.warcraftlogs.com/reports/<<this part>>)
encounter_id = encounters["sylvanas"] # Change the boss here, or just replace with the encounter ID, you can find them here: https://wowpedia.fandom.com/wiki/DungeonEncounterID
```

## Running the Script

```
python plot.py
```

## What am I looking at?

*The Y is DPS.
*The X is WipeFest Scores.
*Each pull is a dot.
*Each player gets a rectangle over 1 standard deviation from their mean for both DPS and WF.  This is roughly their expected performance.

## How can this help me improve?

By itself it cannot, but it can help you see in a visual way where you might be lagging other players in your raid, then ask them.  If you are low in WF score you may need to look into your WF scores to see what mechanics you can improve then study those mechanics and watch videos of how to better deal with those mechanics.  If you are low in damage you need to consult your class discords, guides, hekili, improve uptime, and generally just go hit some target dummies.  Unless you are a Rank 1, WF Raider you can improve, and hopefully in doing so you can find more and more joy in playing the game.

## TLDR - How can I read it?

*High on the Y axis is better than low.
*High on the X axis is better than low.
*Small boxes are more consistent.

## Support

This is a quick script I threw together and I probably won't support it much.