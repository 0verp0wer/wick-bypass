#thanks to https://github.com/imAETHER/AI-CaptchaSolver for his model

import os
import re
import json
import time
import torch
import random
import string
import requests
import websocket

from PIL import Image
from pystyle import Center, Anime, Colors, Colorate, System, Write
from colorama import init, Fore

init()

model = torch.hub.load('ultralytics/yolov5', 'custom', path='bypass/captcha.pt', force_reload=True)
os.system("cls")

text = '''
╦ ╦╦╔═╗╦╔═  ╔═╗╦ ╦╔═╗╦╔═╔═╗╦═╗
║║║║║  ╠╩╗  ╠╣ ║ ║║  ╠╩╗║╣ ╠╦╝
╚╩╝╩╚═╝╩ ╩  ╚  ╚═╝╚═╝╩ ╩╚═╝╩╚═'''

print(Colorate.Diagonal(Colors.blue_to_purple, Center.XCenter(text)))

channel_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'insert the channel id:')
guild_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'insert the guild id:')
button_id = input('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'insert the button id:')

failed = 0
bypassed = 0

def connect(ws):
  ws.connect('wss://gateway.discord.gg/?encoding=json&v=9&compress=json')
  ws.send(
    json.dumps(
      {
        "op":2,
        "d":{
          "token":token,
          "capabilities":8189,
          "properties":
          {
            "os":"Windows",
            "browser":"Chrome",
            "device":"",
            "system_locale":"it-IT",
            "browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "browser_version":"114.0.0.0",
            "os_version":"10",
            "referrer":"",
            "referring_domain":"",
            "referrer_current":"",
            "referring_domain_current":"",
            "release_channel":"stable",
            "client_build_number":201332,
            "client_event_source":None},
            "presence":
            {
              "status":"online",
              "since":0,
              "activities":[],
              "afk":False
            },
            "compress":False,
            "client_state":
            {
              "guild_versions":{},
              "highest_last_message_id":"0",
              "read_state_version":0,
              "user_guild_settings_version":-1,
              "user_settings_version":-1,
              "private_channels_version":"0",
              "api_code_version":0
            }
          }
        }
      )
    )
  
def process(img, hex_color, tolerance = 20):
  image_data = img.load()
  height, width = img.size
  r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
  r_min, r_max = max(0, r - tolerance), min(255, r + tolerance)
  g_min, g_max = max(0, g - tolerance), min(255, g + tolerance)
  b_min, b_max = max(0, b - tolerance), min(255, b + tolerance)
  for loop1 in range(height):
    for loop2 in range(width):
      try:
        pixel_r, pixel_g, pixel_b, _ = image_data[loop1, loop2]
      except ValueError:
        pixel_r, pixel_g, pixel_b = image_data[loop1, loop2]
      if not (r_min <= pixel_r <= r_max and g_min <= pixel_g <= g_max and b_min <= pixel_b <= b_max):
        image_data[loop1, loop2] = 0, 0, 0, 0
  return img

def solveCaptcha(url, color = "fcc434") -> str:
  img = Image.open(requests.get(url, stream=True).raw)
  img = process(img, color)

  result = model(img)

  a = result.pandas().xyxy[0].sort_values('xmin')
  while len(a) > 6: 
    lines = a.confidence
    linev = min(a.confidence)
    for line in lines.keys():
      if lines[line] == linev:
        a = a.drop(line)

  result = ""
  for _, key in a.name.items():
    result = result + key
  return result

with open("tokens.txt", "r") as f:
  tokens = f.readlines()
  for i in tokens:
    token = i.rstrip()

    System.Title(f"Wick Fucker by over_on_top - {bypassed} verification bypassed - {failed} verification failed")

    authorization = {
      'Authorization': token
    }

    r = requests.get("https://discord.com/api/v9/users/@me", headers=authorization).json()
    token_id = r["id"]

    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50', headers=authorization)
    response = r.content

    match = re.search(r'"custom_id": "([^"]+)"', str(response))
    if match:
      custom_id = match.group(1)
    
    match2 = re.search(r'"author": {"id": "([^"]{18})"', str(response))
    if match2:
      application_id = match2.group(1)
    
    headers = {
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
      'Authorization': token,
      'Content-Length': '318',
      'Content-Type': 'application/json',
      'Cookie': '__dcfduid=891dff9010ab11ed90c90d12ffc986ae; __sdcfduid=891dff9110ab11ed90c90d12ffc986ae85bbb81c810406a1f87aee8de8359de48e5eb21623770d623a1e763dd3c8424b; locale=it;',
      'Origin': 'https://discord.com',
      'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
      'Sec-Ch-Ua-Mobile': '?0',
      'Sec-Ch-Ua-Platform': '"Windows"',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
      'X-Debug-Options': 'bugReporterEnabled',
      'X-Discord-Locale': 'it',
      'X-Discord-Timezone': 'Europe/Rome',
      'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Iml0LUlUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2l0LnNlYXJjaC55YWhvby5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6Iml0LnNlYXJjaC55YWhvby5jb20iLCJzZWFyY2hfZW5naW5lIjoieWFob28iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjA4MzE5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    }

    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + 'Button clicked succesfully')
    print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Getting captcha...')

    ws = websocket.WebSocket()
    connect(ws)
    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type":3,"nonce":"".join([str(random.randint(1, 9)) for _ in range(19)]),"guild_id":guild_id,"channel_id":channel_id,"message_flags":0,"message_id":button_id,"application_id":application_id,"session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),"data":{"component_type":2,"custom_id":custom_id}})
    while True:
      response = json.loads(ws.recv())
      if response['t'] == 'MESSAGE_CREATE':
        try:
          value = response['d']['embeds'][0]['fields'][0]['value']
          if value == '`Please type the captcha below to be able to access this server!`':
            message_id = response['d']['id']
            link = response['d']['embeds'][0]['image']['url']
            ws.close()
            break
        except:
          continue

    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + 'Captcha obtained correctly')
    print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Bypassing captcha...')
        
    connect(ws)
    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type":3,"nonce":"".join([str(random.randint(1, 9)) for _ in range(19)]),"guild_id":guild_id,"channel_id":channel_id,"message_flags":64,"message_id":message_id,"application_id":application_id,"session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),"data":{"component_type":2,"custom_id":f"mver_{guild_id}_{token_id}"}})
    while True:
      response = json.loads(ws.recv())
      if response['t'] == 'INTERACTION_SUCCESS':
        id_value = response['d']['id']
        ws.close()
        break

    captcha = solveCaptcha(link)
    print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + f'Captcha bypassed: {captcha}')
    print('['+ Fore.BLUE + '>' + Fore.RESET + ']' + 'Bypassing verification...')
    
    r = requests.post("https://discord.com/api/v9/interactions", headers=headers, json={"type":5,"application_id":application_id,"channel_id":channel_id,"guild_id":guild_id,"data":{"id":id_value,"custom_id":f"modalmmbrver_{token_id}","components":[{"type":1,"components":[{"type":4,"custom_id":"answer","value":captcha}]}]},"session_id":"".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),"nonce":"".join([str(random.randint(1, 9)) for _ in range(19)])})
    time.sleep(1)
    r = requests.get(f'https://discord.com/api/v9/channels/893443303683534889/messages?limit=50', headers=authorization)
    if r.status_code == 200:
      failed+=1
      print('['+ Fore.RED + '!' + Fore.RESET + ']' + f'Verification bypass failed with {token[:-5]}.....')
    else:
      bypassed+=1
      print('['+ Fore.GREEN + '+' + Fore.RESET + ']' + f'Verification bypassed correctly with {token[:-5]}.....')
