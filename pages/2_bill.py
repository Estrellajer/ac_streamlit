import streamlit as st
from typing import List
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from streamlit_autorefresh import st_autorefresh
from utils import utils
from utils.utils import post
import threading

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 解决图像中的“-”负号的乱码问题

st.set_page_config(
    page_title="查看报表",
    page_icon="👋",
)

# 设置全局变量
if 'stage' not in st.session_state:
    st.session_state['stage'] = 'login'
if 'token' not in st.session_state:
    st.session_state['token'] = '0'
if 'amount' not in st.session_state:
    st.session_state['amount'] = 0
if 'high_speed_ac' not in st.session_state:
    st.session_state['high_speed_ac'] = []
if 'medium_speed_ac' not in st.session_state:
    st.session_state['medium_speed_ac'] = []
if 'low_speed_ac' not in st.session_state:
    st.session_state['low_speed_ac'] = []

def check_all_zeros(df):
    return (df == 0).all().all()

def transform():
    ac_label = []
    amount = st.session_state.get('amount')
    high_speed_ac_list: List = st.session_state.get('high_speed_ac')
    medium_speed_ac_list: List = st.session_state.get('medium_speed_ac')
    low_speed_ac_list: List = st.session_state.get('low_speed_ac')
    ac_list = high_speed_ac_list + medium_speed_ac_list + low_speed_ac_list
    for i in range(1, amount + 1):
        if i <= len(high_speed_ac_list):
            ac_label.append("高风速空调" + chr(64 + i))
        elif i <= len(high_speed_ac_list) + len(medium_speed_ac_list):
            ac_label.append("中风速空调" + chr(64 + i - len(high_speed_ac_list)))
        else:
            ac_label.append("低风速空调" + chr(64 + i - len(high_speed_ac_list) - len(medium_speed_ac_list))
    return ac_list, ac_label

def query_ac_report(ac_id, start_date, end_date):
    my_json = {'ac_id': ac_id, 'start_date': start_date, 'end_date': end_date}
    data = utils.post(my_json, "/admin/queryACReport", st.session_state['token'])
    if data['code'] == 1:
        target = data['data']
        target['ac_id'] = ac_id
        return target
    else:
        st.error(data['message'])

# 展示费用
def display_fee(data_list, labels):
    # Your code to display fee report here
    pass

# 展示充电次数
def display_charge(data_list, labels):
    # Your code to display charge report here
    pass

def send_post_request(ac_id, start_date, end_date, data_list, header):
    my_json = {'ac_id': ac_id, 'start_date': start_date, 'end_date': end_date}
    data = utils.post(my_json, "/admin/queryACReport", st.session_state['token'])
    if data['code'] == 1:
        target = data['data']
        target['ac_id'] = ac_id
        data_list.append(target)
    else:
        data_list = None
        return data_list

def get_data(start_date, end_date):
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    high_speed_ac_list = []
    medium_speed_ac_list = []
    low_speed_ac_list = []
    for high_speed_ac_id in st.session_state['high_speed_ac']:
        high_speed_ac_list.append(query_ac_report(high_speed_ac_id, start_date, end_date))
    for medium_speed_ac_id in st.session_state['medium_speed_ac']:
        medium_speed_ac_list.append(query_ac_report(medium_speed_ac_id, start_date, end_date))
    for low_speed_ac_id in st.session_state['low_speed_ac']:
        low_speed_ac_list.append(query_ac_report(low_speed_ac_id, start_date, end_date))
    high_speed_list = sorted(high_speed_ac_list, key=lambda x: x['ac_id'])
    medium_speed_list = sorted(medium_speed_ac_list, key=lambda x: x['ac_id'])
    low_speed_list = sorted(low_speed_ac_list, key=lambda x: x['ac_id'])
    data_list = high_speed_list + medium_speed_list + low_speed_list
    return data_list

if st.session_state['stage'] == 'login':
    st.title('管理员登录')
    st.markdown("#### 请输入管理员密码")
    password = st.text_input("密码")

    def login():
        if password:
            my_json = {"password": password}
            data = utils.post(my_json, "/admin/login")
            if data['code'] == 1:
                st.session_state['token'] = data['data']['token']
                st.session_state['stage'] = 'show_report'
                token = st.session_state.get('token')
                headers = {
                    "Authorization": token
                }
                data = utils.post({}, "/admin/queryACAmount", token)
                if data['code'] == 1:
                    st.session_state['amount'] = data['data']['amount']
                    st.session_state['high_speed_ac'] = data['data']['high_speed_ac']
                    st.session_state['medium_speed_ac'] = data['data']['medium_speed_ac']
                    st.session_state['low_speed_ac'] = data['data']['low_speed_ac']
                else:
                    st.error(data['message'])
            else:
                st.error(data['message'])
        else:
            st.error("密码不能为空")
            return

    st.button("登录", on_click=login)
else:
    st.title("查看报表")
    col1, col2 = st.columns(2)
    with col1:
        option = st.selectbox(
            "显示方式",
            ("日", "月", "年")
        )
    with col2:
        start_date = st.date_input("起始日期", datetime.date.today())
    if option == '日':
        Days = datetime.timedelta(days=0)
    elif option == '月':
        Days = datetime.timedelta(days=30)
    else:
        Days = datetime.timedelta(days=365)
    end_date = start_date + Days
    tabs = ['费用', '充电']
    tab1, tab2, = st.tabs(tabs)
    data_list = get_data(start_date, end_date)
    ac_list, labels = transform()
    with tab1:
        st.subheader("报表时间" + str(start_date) + "~" + str(end_date))
        display_fee(data_list, labels)
    with tab2:
        st.subheader("报表时间" + str(start_date) + "~" + str(end_date))
        display_charge(data_list, labels)
    time.sleep(3)
    st.experimental_rerun()
