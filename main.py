import requests
import time

###########
#Variables#
###########
router_name="" #Bobber Name so the embeds are fancy, could get from API, but this way is faster.
web_hook_url="" #Discord Webhook URL.
hostip="" #The LocalIP of the router (Keep in mind, this script only works if its run in the local envourment of the Bobber.)
roll_id="" #Roll ID from your Discord server so you get @ when the script is executed.

###############################################
#Sending out Webhook that the Bobber Rebooted.#
###############################################
def restart_webhook():
    restart_data = {
    "content": "<@&"+roll_id+">",
    "embeds": [
        {
        "title": "**"+router_name+"** is rebooting.",
        "description": "It may take 2 or more minutes.",
        "color": 64100,
        "author": {
            "name": "Reboot executed.",
            "icon_url": "https://icons.iconarchive.com/icons/dakirby309/windows-8-metro/256/Other-Power-Restart-Metro-icon.png"
        },
        "footer": {
            "text": "Reboot time",
            "icon_url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
        },
        "thumbnail": {
            "url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
        }
        }
    ]
    }
    response_restart = requests.post(web_hook_url, json=restart_data)

    print(response_restart.status_code)
    print(response_restart.content)

#######################################################
#Sending out Webhook that the Bobber Failed to reboot.#
#######################################################
def restart_fail_webhook():

    restart_fail_data = {
    "content": "<@&"+roll_id+">",
    "embeds": [
        {
        "title": "**"+router_name+"** faild to reboot.",
        "description": "Will try again in 4 hours.",
        "color": 14497848,
        "author": {
            "name": "Rebooting faild.",
            "icon_url": "https://www.freeiconspng.com/uploads/error-icon-4.png"
        },
        "footer": {
            "text": "Faild at",
            "icon_url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
        },
        "thumbnail": {
            "url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
        }
        }
    ]
    }
    response_restart_fail = requests.post(web_hook_url, json=restart_fail_data)

    print(response_restart_fail.status_code)
    print(response_restart_fail.content)


############################################################################
#Sending out Request to check status and Sending out Embed after the check.#
############################################################################
def CheckStatus():
    response = requests.get('http://'+ hostip +'/miner.json')
    data = response.json()
    state = data["miner"]["State"]
    status = data["miner"]["Status"]
    temp0 = data["temp0"]
    height = data["miner_height"]

    status_data = {
  "content": "<@&"+roll_id+">",
  "embeds": [
    {
      "title": "**"+router_name+"** is "+state+"",
      "color": 11010047,
      "fields": [
        {
          "name": ":vertical_traffic_light: State",
          "value": state,
          "inline": True
        },
        {
          "name": "‎",
          "value": "‎",
          "inline": True
        },
        {
          "name": ":bell: Status",
          "value": status,
          "inline": True
        },
        {
          "name": ":fire_extinguisher: Temp",
          "value": temp0,
          "inline": True
        },
        {
          "name": "‎",
          "value": "‎",
          "inline": True
        },
        {
          "name": ":arrows_clockwise: Height",
          "value": height,
          "inline": True
        }
      ],
      "author": {
        "name": "Status report.",
        "icon_url": "https://icon-library.com/images/info-icon-png/info-icon-png-28.jpg"
      },
      "footer": {
        "text": "Report Time",
        "icon_url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
      },
      "thumbnail": {
        "url": "https://theme.zdassets.com/theme_assets/11115208/78fec3139c0184ebab241a4520e3dfe087203f1f.png"
      }
    }
  ]
}
    response_status = requests.post(web_hook_url, json=status_data)

    print(response_status.status_code)
    print(response_status.content)
    print("Cya in 4 hours.")

##############################
#The Initial Restart Request.#
##############################
print("Send out the initial Reboot request to Bobcat Diagnoser.")
headers = {
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Authorization': 'Basic Ym9iY2F0Om1pbmVy',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'DNT': '1',
    'Accept': '*/*',
    'Origin': 'http://'+ hostip +'',
    'Referer': 'http://'+ hostip +'/',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.post('http://'+ hostip +'/admin/reboot', headers=headers, verify=False)

if response.status_code == 200:
    print("Status Code is 200, telling Discord.")
    restart_webhook()
    print("Sleeping for 120 seconds.")
    time.sleep(120)
    print("Checking status of the Bobber and Telling Discord.")
    CheckStatus()
else:
    print("Status Code is not 200, telling Discord.")
    restart_fail_webhook()