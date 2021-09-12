import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from os import environ as env
import json

load_dotenv()


def send_message(data_list):
    url_line = 'https://notify-api.line.me/api/notify'
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
    url_line = 'https://notify-api.line.me/api/notify'
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


def scarecrow(_id):
    url_apply = "https://backend-farm.plantvsundead.com/farms/apply-tool"
    payload_apply = json.dumps({
        "farmId": _id,
        "toolId": 4,
        "token": {
            "challenge": "default",
            "seccode": "default",
            "validate": "default"
        }
    })
    headers_apply = {
        'Content-Type': 'application/json'
    }

    response_apply = requests.request("POST", url, headers=headers_apply, data=url_apply)


if __name__ == '__main__':
    url = "https://backend-farm.plantvsundead.com/farms?limit=10&offset=0"
    url_group = "https://backend-farm.plantvsundead.com/farm-status"
    payload = {}
    headers = {
        'Authorization': str(env['TOKEN'])
    }
    le = 0
    count_water = 0
    seed = 0
    crow = 0
    is_notify = False
    while True:
        rq = requests.request("GET", url_group, headers=headers, data=payload)
        if rq.status_code == 200:
            if rq.json()['status'] == 0:
                data_x = rq.json()['data']
                # print(data_x)
                if 'inGroup' in data_x and 'currentGroup' in data_x:
                    in_group = rq.json()['data']['inGroup']
                    currentGroup = rq.json()['data']['currentGroup']
                    print(f'current group {currentGroup} , your group {in_group} ')

                status = rq.json()['data']['status']
                if status == 0:
                    is_notify = False
                if status == 1:
                    if is_notify is False:
                        send_msg(f" สามารถเข้า Plan vs Undead ได้")
                        is_notify = True
                    response = requests.request("GET", url, headers=headers, data=payload)
                    start_time = time.time()
                    data_plant = []
                    if response.status_code == 200:
                        data_source = response.json()
                        # print(data_source)
                        if data_source['status'] == 0:
                            data = data_source['data']
                            for i in data:
                                if i['needWater'] is False:
                                    count_water = count_water + 1
                                if i['totalHarvest'] > 0:
                                    le = le + i['totalHarvest']
                                if i['hasSeed'] is True:
                                    seed = seed + 1
                                if 'hasCrow' in i:
                                    if i['hasCrow'] is True:
                                        crow = crow + 1
                                        # scarecrow(i['_id'])
                        if le != 0 or count_water != 0 or seed != 0 or crow != 0:
                            send_message({'le': le, 'seed': seed, 'water': count_water, 'crow': crow})
                            le = 0
                            seed = 0
                            count_water = 0
                            crow = 0
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        success_msg = '''request success {time} , {ms} ms'''.format(time=dt_string,
                                                                                    ms=round(time.time() - start_time,
                                                                                             5))
                        print(success_msg)
                    else:
                        pass
                    time.sleep(360)
        time.sleep(10)
