import json
import random
import time

import requests
import urllib3

from cdps.plugin.manager import Manager
from cdps.plugin.thread import new_thread
from cdps.utils.logger import Log
from plugins.http_get_eew.src.events import onEew

urllib3.disable_warnings()


@new_thread
def get_eew():
    eews = []
    authors = []
    with open("./config/http_get_eew.json", 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    
    if config["cwa"]: authors.append("cwa")
    if config["nied"]: authors.append("nied")
    if config["kma"]: authors.append("kma")
    if config["scdzj"]: authors.append("scdzj")
    
    if authors == []:
        log.logger.error(f"未指定任何速報單位")
        return
    url = f"https://api-{random.randint(1,2)}.exptech.dev/api/v1/eq/eew"
    while True:
        data = []
        eew = []
        try:
            data = requests.get(url, timeout=1)
        except Exception as e:
            log.logger.warning(f"取得地震速報時發生錯誤\n{e}")
            time.sleep(config["timeout"])
            continue
        try:
            data = (json.loads(data.text))
        except Exception as e:
            log.logger.warning(f"解析速報資料發生錯誤\n{e}")
            time.sleep(config["timeout"])
            continue

        for i in data:
            if i["author"] in authors:
                eew.append(i)
        eews = eew
        event_manager.call_event(onEew(eews))
        time.sleep(config["timeout"])


log = Log()
event_manager = Manager()
get_eew()