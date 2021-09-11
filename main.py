import requests
import time
from datetime import datetime
from dotenv import load_dotenv
from os import environ as env

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
    '''.format(dt_string=dt_string, data_le=data_list['le'], data_water=data_list['water'], data_seed=data_list['seed'],data_crow=data_list['crow'])
    r = requests.post(url_line, headers=headers, data={'message': msg})
    print(r.text, dt_string)


def send_error(message):
    url_line = 'https://notify-api.line.me/api/notify'
    token = str(env['LINE_TOKEN'])
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = '''
    --------------------------
    {dt_string}
    Message : {err_msg}
    ---------------------------
    Power by Thanthip Dev.
    ---------------------------
    '''.format(dt_string=dt_string,err_msg=message)
    r = requests.post(url_line, headers=headers, data={'message': msg})
    print(r.text, dt_string)


if __name__ == '__main__':
    url = "https://backend-farm-stg.plantvsundead.com/farms?limit=10&offset=0"

    payload = {}
    headers = {
        'Authorization': str(env['TOKEN'])
    }
    le = 0
    count_water = 0
    seed = 0
    crow = 0
    while True:
        response = requests.request("GET", url, headers=headers, data=payload)

        start_time = time.time()
        if response.status_code == 200:
            data_source = response.json()
            if data_source['status'] == 0:
                data = data_source['data']
                for i in data:
                    if i['needWater'] is True:
                        count_water = count_water + 1
                    if i['totalHarvest'] > 0:
                        le = le + i['totalHarvest']
                    if i['hasSeed'] is True:
                        seed = seed + 1
                    if 'hasCrow' in i:
                        if i['hasCrow'] is True:
                            crow = crow + 1
                if le != 0 or count_water != 0 or seed != 0 or crow != 0:
                    send_message({'le': le, 'seed': seed, 'water': count_water, 'crow': crow})
                    le = 0
                    seed = 0
                    count_water = 0
                    crow = 0
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                success_msg = '''request success {time} , {ms} ms'''.format(time=dt_string, ms=round(time.time() - start_time,5))
                print(success_msg)
            else:
                send_error("Access token is invalid 🥶")
        else:
            send_error("Error please contact developer")
        time.sleep(300)
