import datetime
from enum import Enum
import streamlit as st
import requests
import json

HOST = "111"

def post(my_json: dict, path: str, token=None) -> dict:
    # print(token)
    if token is not None:
        headers = {
            # "Content-Type": "application/json",
            "Authorization": token
        }
        response = requests.post(url=HOST + path, data=json.dumps(my_json), headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(response.text)
        # return requests.post(url=HOST + path, data=json.dumps(my_json), headers=headers).json()
    else:
        # return requests.post(url=HOST + path, data=json.dumps(my_json)).json()
        response = requests.post(url=HOST + path, data=json.dumps(my_json))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(response.text)


def mode_to_ft(mode: str):
    if mode == "快充":
        return "F"
    elif mode == "慢充":
        return "T"
    else:
        return mode


def ft_to_mode(mode: str):
    if mode == "F":
        return "快充"
    elif mode == "T":
        return "慢充"
    else:
        return mode


def format_datetime_s(time_stamp: float):
    return datetime.datetime.fromtimestamp(time_stamp).strftime("%Y-%m-%d %H:%M:%S")


def get_hour_min_sec(during: float):
    hour = int(during / 3600)
    min = int((during - hour * 3600) / 60)
    sec = int(during - hour * 3600 - min * 60)
    return hour, min, sec