import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from os import environ as env
import json

load_dotenv()


def send_message(data_list):
    url_line = str(env['URL_LINE'])
    token = str(env['LINE_TOKEN'])
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = '''
    --------------------------
    {dt_string}
    LE ☘️ = {data_le}
    Water 💧 = {data_water}
    Crow 🦜 = {data_crow}
    Seed 🌱 = {data_seed}
    ---------------------------
    Power by Thanthip Dev.
    ---------------------------
    '''.format(dt_string=dt_string, data_le=data_list['le'], data_water=data_list['water'], data_seed=data_list['seed'],
               data_crow=data_list['crow'])
    r = requests.post(url_line, headers=headers, data={'message': msg})
    print(r.text, dt_string)


def send_msg(message):
    url_line = str(env['URL_LINE'])
    token = str(env['LINE_TOKEN'])
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = '''
    --------------------------
    {dt_string}
    {err_msg}
    ---------------------------
    Power by Thanthip Dev.
    ---------------------------
    '''.format(dt_string=dt_string, err_msg=message)
    r = requests.post(url_line, headers=headers, data={'message': msg})
    print(r.text, dt_string)


def apply_tools(_id, toolId):
    url_apply = f"{str(env['URL_PVU'])}/farms/apply-tool"
    payload_apply = json.dumps({
        "farmId": _id,
        "toolId": toolId,
        "token": {
            "challenge": "default",
            "seccode": "default",
            "validate": "default"
        }
    })
    headers_apply = {
        'Authorization': str(env['TOKEN']),
        'Content-Type': 'application/json'
    }

    response_apply = requests.request("POST", url, headers=headers_apply, data=url_apply)
    if response_apply.status_code == 200:
        if response_apply.json()['status'] == 0:
            return True
        else:
            return False
    else:
        return False


def group():
    url_group = f"{str(env['URL_PVU'])}/farm-status"
    headers = {
        'Authorization': str(env['TOKEN'])
    }
    payload = {}
    start_time = time.time()
    rq = requests.request("GET", url_group, headers=headers, data=payload)
    if rq.status_code == 200:
        if rq.json()['status'] == 0:
            data_x = rq.json()['data']
            status = data_x['status']
            if 'inGroup' in data_x and 'currentGroup' in data_x:
                in_group = rq.json()['data']['inGroup']
                currentGroup = rq.json()['data']['currentGroup']
                totalGroup = rq.json()['data']['totalGroup']
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |⚡️ your group {in_group} | 🔥 current group {currentGroup} / {totalGroup} | 🧾 load {round(time.time() - start_time,5)} ms.")
            elif rq.json()['status'] == 0 and status == 0:
                print("⚡️ Farm Maintenance")
            else:
                pass
            return status


if __name__ == '__main__':
    url = f"{str(env['URL_PVU'])}/farms?limit=10&offset=0"
    payload = {}
    headers = {
        'Authorization': str(env['TOKEN'])
    }
    le = 0
    count_water = 0
    seed = 0
    crow = 0
    is_notify_group = False
    is_notify_msg = False
    old_data = {}
    while True:
        check_group = group()
        if check_group == 0:
            is_notify_group = False
        if check_group == 1:
            if is_notify_group is False:
                send_msg(f" สามารถเข้า Plan vs Undead ได้")
                is_notify_group = True

            response = requests.request("GET", url, headers=headers, data=payload)
            start_time = time.time()
            data_plant = []
            if response.status_code == 200:
                data_source = response.json()
                # print(data_source)
                if data_source['status'] == 0:
                    data = data_source['data']
                    for i in data:
                        if i['needWater'] is True:
                            count_water = count_water + 1
                            # apply_tools(i['_id'],3)
                        if i['totalHarvest'] > 0:
                            le = le + i['totalHarvest']
                        if i['hasSeed'] is True:
                            seed = seed + 1
                        if 'hasCrow' in i:
                            if i['hasCrow'] is True:
                                crow = crow + 1
                                # apply_tools(i['_id'],4)
                _data = {'le': le, 'seed': seed, 'water': count_water, 'crow': crow}
                if old_data == _data:
                    is_notify_msg = True
                if le != 0 or count_water != 0 or seed != 0 or crow != 0:
                    if is_notify_msg is False:
                        send_message(_data)
                        old_data = _data.copy()
                        le = 0
                        seed = 0
                        count_water = 0
                        crow = 0
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    success_msg = ''' ⚡️ {time} request success  , 🧾 load {ms} ms'''.format(time=dt_string,
                                                                                ms=round(time.time() - start_time,
                                                                                         5))
                    print(success_msg)
                time.sleep(300)
            else:
                pass
        else:
            time.sleep(30)
