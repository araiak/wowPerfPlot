from tracemalloc import start
import requests
import json
import sys
import time
import math
import os
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests.structures import CaseInsensitiveDict
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

plt.rc('figure', max_open_warning = 0)

#client (application) credentials
client_id = '
client_secret = ''


def mean(data):
    n = len(data)
    mean = sum(data) / n
    return mean


def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


def get_access_token():
    print(" ? Authenticating to WarcraftLogs")
    #WarcraftLogs URLS
    auth_uri = "https://www.warcraftlogs.com/oauth/authorize"
    token_uri = "https://www.warcraftlogs.com/oauth/token"

    # curl -u {client_id}:{client_secret} -d grant_type=client_credentials https://www.warcraftlogs.com/oauth/token
    data = {
    'grant_type': 'client_credentials'
    }

    response = requests.post('https://www.warcraftlogs.com/oauth/token', data=data, auth=(client_id, client_secret))

    json_response = json.loads(response.content)
    if "access_token" in json_response:
        print(" + Authentication Successful")
        return json_response["access_token"]
    else:
        print(" ! Authentication failed.")


def make_request(query):
    # API Root
    public_api_root = "https://www.warcraftlogs.com/api/v2/client"
    headers = CaseInsensitiveDict()
    headers['Accept'] = 'application/json'
    headers['Authorization'] = f'Bearer {access_token}'
    response = requests.post(public_api_root, json={'query': query}, headers=headers)
    return response.content


def get_wipefest(report_id, fight_id, death_threshold):
    wipefest_url = f'https://www.wipefest.gg/report/{report_id}/fight/{fight_id}?ignore=true&deathThreshold=2&fightSummaryTab=players'
    driver = webdriver.Chrome()
    driver.get(wipefest_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(10)
    players_in_order = []
    scores_in_order = []
    return_dict = {}
    players = driver.find_elements_by_class_name("player-card__name")
    scores = driver.find_elements_by_class_name("player-card__score")
    for player in players:
        players_in_order.append(player.text)
    for score in scores:
        scores_in_order.append(int(score.text))
    i = 0
    while i < len(players_in_order):
        return_dict[players_in_order[i]] = scores_in_order[i]
        i = i + 1
    driver.quit()
    print(return_dict)
    return return_dict


def get_player_dam(report_id, encounter_id, start_time, end_time):
    return_dict = {}
    fight_len_sec = (end_time - start_time)/1000
    damage_query = f'''{{
        reportData	{{
            report(code: "{report_id}") {{
                table(dataType: DamageDone, encounterID: {encounter_id}, startTime: {start_time}, endTime: {end_time})
            }}
        }}
    }}'''

    damage = json.loads(make_request(damage_query))
    player_damage = damage['data']['reportData']['report']['table']['data']['entries']
    for player in player_damage:
        name = player['name']
        total_dam = player['total']
        dps = total_dam/fight_len_sec
        return_dict[name] = dps
    return return_dict


def plot(ax, player_wf_list, player_dps_list, player, min_dps, max_dps):
    # https://problemsolvingwithpython.com/06-Plotting-with-Matplotlib/06.10-Scatter-Plots/
    ax.scatter(player_wf_list, player_dps_list)
    ax.set_title(player)
    #add rectangle to plot
    wf_mean = mean(player_wf_list)
    wf_std = stdev(player_wf_list)
    dps_mean = mean(player_dps_list)
    dps_std = stdev(player_dps_list)
    ax.add_patch(Rectangle(((wf_mean-wf_std), (dps_mean-dps_std)), (wf_std*2), (dps_std*2)))
    ax.set_ylim([min_dps, max_dps])
    ax.set_xlim([0, 100])
    return plt


access_token = get_access_token()

encounters = {
    "terra": 2423,
    "eye": 2433,
    "nine": 2429,
    "remnant": 2432,
    "soulrender": 2434,
    "painsmith": 2430,
    "guardian": 2436,
    "fatescribe": 2431,
    "kt": 2422,
    "sylvanas": 2435,
}

# Set your report and encounter IDs here.
report_id = "<<your report_id>>" # This is the report ID URL from wcl (https://www.warcraftlogs.com/reports/<<this part>>)
encounter_id = encounters["sylvanas"] # Change the boss here, or just replace with the encounter ID, you can find them here: https://wowpedia.fandom.com/wiki/DungeonEncounterID

player_list = []
player_matrix = {}
min_dps = 0
max_dps = 0
file_path = f'./data/{report_id}-{encounter_id}.json'
img_path = f'./data/{report_id}-{encounter_id}.png'

if os.path.exists(file_path):
    print(" - JSON File Found")
    with open(file_path) as f:
        player_matrix = json.load(f)
    for key in player_matrix.keys():
        if "_dps" in key:
            player_name = key[:-4]
            if player_name not in player_list:
                print(f' Player found: {player_name}')
                player_list.append(player_name)
            dps_list = player_matrix[key]
            for dps in dps_list:
                if dps > max_dps:
                    max_dps = dps
                elif dps < min_dps:
                    min_dps = dps
else:
    print(" - JSON not found, querying APIs")
    query_fights = f'''{{
        reportData	{{
            report(code: "{report_id}") {{
                masterData {{
                    actors {{
                        id
                        name
                        petOwner
                    }}
                }}
                fights(
                encounterID: {encounter_id}
                ){{
                    id
                    name
                    fightPercentage
                    startTime
                    endTime
                    enemyNPCs {{
                        gameID
                        id
                        instanceCount
                        groupCount
                    }}
                }}
            }}
        }}
    }}'''

    overview = json.loads(make_request(query_fights))
    fights = overview['data']['reportData']['report']['fights']
    actors = overview['data']['reportData']['report']['masterData']['actors']
    min_fight_len_sec = 30

    for fight in fights:
        fight_id = fight['id']
        start_time = fight['startTime']
        end_time = fight['endTime']
        fight_len_sec = (end_time - start_time)/1000
        if fight_len_sec > min_fight_len_sec:
            # Get fight info
            print(f' - Fight over {min_fight_len_sec}s getting damage from Fight ID: {fight_id} with startTime {start_time} and endTime {end_time}')
            print(f' - Getting Player DPS for report: {report_id}, encounter{encounter_id}')
            dps_dict = get_player_dam(report_id, encounter_id, start_time, end_time)
            print(f' - Getting Wipefest for report: {report_id}, fight {fight_id}')
            wf_dict = get_wipefest(report_id, fight_id, 2)
            for player in wf_dict.keys():
                if player not in player_list:
                    player_list.append(player)
                if player in dps_dict:
                    player_dps = dps_dict[player]
                    if player_dps > max_dps:
                        max_dps = player_dps
                    elif player_dps < min_dps:
                        min_dps = player_dps
                    player_wf = wf_dict[player]
                    if f'{player}_dps' in player_matrix:
                        player_matrix[f'{player}_dps'].append(player_dps)
                    else:
                        player_matrix[f'{player}_dps'] = [player_dps]
                    if f'{player}_wf' in player_matrix:
                        player_matrix[f'{player}_wf'].append(player_wf)
                    else:
                        player_matrix[f'{player}_wf'] = [player_wf]
                else:
                    print(f' ! Player {player} not found in pull in WCL, but found in Wipefest? Data point dropped.')
        else:
            print(f' - Fight Fight ID: {fight_id} under {min_fight_len_sec}s, ignoring.')

    print(json.dumps(player_matrix, indent=4, sort_keys=True))
    with open(file_path, 'w') as outfile:
        json.dump(player_matrix, outfile)




if len(player_list) > 0:
    depth = int(math.ceil(len(player_list)/5))
    f, axarr = plt.subplots(5, depth, figsize=(16,12))
    i = 0
    d = 0
    for player in player_list:
        player_dps_list = player_matrix[f'{player}_dps']
        player_wf_list = player_matrix[f'{player}_wf']
        plot(axarr[i, d], player_wf_list, player_dps_list, player, min_dps, max_dps)
        i = i + 1
        if i > 4:
            i = 0
            d = d + 1
    plt.tight_layout()
    if not os.path.exists(img_path):
        plt.savefig(img_path)
    plt.show()
else:
    print(' No plots found!')

plt.close('all')
