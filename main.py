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
    {name}
    {dt_string}
    LE ☘️ = {data_le}
    Water 💧 = {data_water}
    Crow 🦜 = {data_crow}
    Seed 🌱 = {data_seed}
    ---------------------------
    '''.format(dt_string=dt_string, data_le=data_list['le'], data_water=data_list['water'], data_seed=data_list['seed'],
               data_crow=data_list['crow'], name=str(env['NAME_PVU_ACCOUNT']))
    r = requests.post(url_line, headers=headers, data={'message': msg})
    if r.json()['status'] == 200:
        print("💬 send message : {data}".format(data=data_list))


def send_msg(message):
    url_line = str(env['URL_LINE'])
    token = str(env['LINE_TOKEN'])
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = '''
    {name}
    {dt_string}
    {err_msg}
    '''.format(dt_string=dt_string, err_msg=message, name=str(env['NAME_PVU_ACCOUNT']))
    r = requests.post(url_line, headers=headers, data={'message': msg})
    if r.json()['status'] == 200:
        print("💬 send message : {data}".format(data=message))


async def apply_tools(_id, toolId):
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

    response_apply = await requests.request("POST", url_apply, headers=headers_apply, data=url_apply)
    print(response_apply.json())
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
    status = 0
    try:
        rq = requests.request("GET", url_group, headers=headers, data=payload)
        if rq.status_code == 200:
            if rq.json()['status'] == 0:
                data_x = rq.json()['data']
                status = data_x['status']
                if 'inGroup' in data_x and 'currentGroup' in data_x:
                    in_group = rq.json()['data']['inGroup']
                    currentGroup = rq.json()['data']['currentGroup']
                    totalGroup = rq.json()['data']['totalGroup']
                    next_time_group = datetime.strptime(str(rq.json()['data']['nextGroup']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    currentTime = datetime.strptime(str(rq.json()['data']['currentTime']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    time_next_group = (next_time_group - currentTime)
                    seconds = time_next_group.seconds
                    hours = seconds // 3600
                    minutes = (seconds // 60) % 60

                    if hours == int(env['TIME_NEAR_H']) and minutes == int(env['TIME_NEAR_M']):
                        msg = f"อีก {env['TIME_NEAR_H']} Hour  {env['TIME_NEAR_M']} Minute สามารถเข้ากลุ่มได้"
                        send_msg(msg)

                    print(
                        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |⚡️ your group {in_group} | 🔥 current "
                        f"group {currentGroup} / {totalGroup} | next round => {hours} H {minutes} M | 🧾 load "
                        f"{round(time.time() - start_time, 5)} ms.")
                elif rq.json()['status'] == 0 and status == 0:
                    print("⚡️ Farm Maintenance")
                else:
                    pass
                return status
    except Exception as e:
        print(f'Error : {e}')
        return status


def request_data():
    url = f"{str(env['URL_PVU'])}/farms?limit=10&offset=0"
    payload = {}
    headers = {
        'Authorization': str(env['TOKEN'])
    }
    le = 0
    count_water = 0
    seed = 0
    crow = 0
    _data = {'le': le, 'seed': seed, 'water': count_water, 'crow': crow}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        start_time = time.time()
        if response.status_code == 200:
            data_source = response.json()
            # print(data_source)
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

            _data = {'le': le, 'seed': seed, 'water': count_water, 'crow': crow}
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            success_msg = ''' ⚡️ {time} request success  , 🧾 load {ms} ms'''.format(time=dt_string,
                                                                                     ms=round(
                                                                                         time.time() - start_time,
                                                                                         5))

            success_msg_ = ''' 🔥 {time} request success  , 🧾 load {ms} ms'''.format(time=dt_string,
                                                                                      ms=round(
                                                                                          time.time() - start_time,
                                                                                          5))
            if le != 0 or count_water != 0 or seed != 0 or crow != 0:
                le = 0
                seed = 0
                count_water = 0
                crow = 0
                print(success_msg_)
                return _data
            else:
                print(success_msg)
            return _data
    except Exception as e:
        print(f'Error : {e}')
        return _data


if __name__ == '__main__':

    is_notify_group = False
    is_notify_msg = False
    old_data = {}
    while True:
        check_group = group()
        if check_group == 0:
            is_notify_group = False
        if check_group == 1:
            if is_notify_group is False:
                send_msg('สามารถเข้า Plant vs Undead ได้')
                is_notify_group = True

            res = request_data()
            # print(res)
            if old_data == res:
                is_notify_msg = True
            # print("Data : ",res, is_notify_msg)
            # print("Old data " , old_data, is_notify_msg)
            if res['le'] != 0 or res['water'] != 0 or res['seed'] != 0 or res['crow'] != 0:
                if is_notify_msg is False:
                    old_data = res.copy()
                    send_message(res)
                    is_notify_msg = True
                elif old_data != res:
                    old_data.clear()
                    is_notify_msg = False
                else:
                    pass
            time.sleep(120)
        else:
            time.sleep(60)
