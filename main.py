import requests
import asyncio,time
import os
import sys
import json
from flask import Flask,request
import secrets
import tls_client
import random
from concurrent.futures import ThreadPoolExecutor
import threading
os.system("clear||cls")

guild_id = 1060496595348635739
channel_id = 1103742520858525797
commands_list = ["&help", "&botinfo", "&ping", "&invite", "&av", "&banner user"]

tokens = open("tokens.txt", "r").read().split("\n")

with open("config.json", "r") as f:
  config = json.load(f)

redirect = config["redirect_uri"]
token = config["token"]
secx = config["client_secret"]
secid = config["client_id"]
auth = config["authorize_url"]
dela = config["join_delay"]

def authorize(token):
  res = requests.post(auth, headers={"Authorization": token}, json={"authorize": True, "permissions": 0})
  try:
    r = res.json()
  except:
    print("[-] Cloudflare Blocked")
  if r.get("location"):
    requests.get(r.get("location"))
  

app = Flask(__name__)

@app.route("/")
def mainidk():
  return "ok"

@app.route("/auth")
def index():
  ok = request.args.get("code")
  if ok:
    try:
      bye = {"client_id": secid, "client_secret":secx, "grant_type": "authorization_code", "code": ok, "redirect_uri": redirect}
      req = requests.post("https://discord.com/api/v10/oauth2/token", headers = {'Content-Type': 'application/x-www-form-urlencoded'}, data=bye)
      req.raise_for_status()
      at = req.json()["access_token"]
      headers = {
            "Authorization" : f"Bot {token}",
            'Content-Type': 'application/json'

        }
      r = requests.get("https://discord.com/api/v10/users/@me", headers={"Authorization": f"Bearer {at}"})
      uid = r.json()["id"]
      print(at)
      data = {
            "access_token" : at,
        }
      r = requests.put(f"https://discord.com/api/v10/guilds/{guild_id}/members/{uid}", headers=headers, data=data)
      if r.status_code == 200:
        print("joined server;")
      else:
        print(f"failed to join, status: {r.status_code}, {r.text}")
      return "ok"
    except Exception as e:
      print("error",e)
      return e
  else:
      return "bye"

def getheaders(Toke):
  header = {
			'Authorization': Toke,
			'accept': '*/*',
			'accept-language': 'en-US',
			'connection': 'keep-alive',
			'cookie': f'__cfduid = {secrets.token_hex(43)}; __dcfduid={secrets.token_hex(32)}; locale=en-US',
			'DNT': '1',
			'origin': 'https://discord.com',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'referer': 'https://discord.com/channels/@me',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36',
			'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
		}
  return header

def send_message(token):
  headers = getheaders(token)
  session = tls_client.Session(client_identifier=random.choice(["chrome_103", "chrome_104", "chrome_105", "chrome_106", "chrome_107", "chrome_108"]))
  msg = random.choice(commands_list)
  r = session.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"content": msg})
  if r.status_code in [200,204,201]:
    print("sent ->", msg)
  else:
    print("failed to sent, status ->", r.status_code)

def run():
  app.run(port=8080,host="0.0.0.0")

threading.Thread(target=run).start()

for token in tokens:
  authorize(token)

def worker():
  while True:
    for token in tokens:
      send_message(token)

for i in range(50):
  threading.Thread(target=worker).start()

while True:
  worker()
