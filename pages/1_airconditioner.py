import streamlit as st
from typing import List

import time
import datetime

st.set_page_config(
    page_title="显示空调状态",
)

# 设置全局变量
if 'stage' not in st.session_state:
    st.session_state['stage'] = 'test'
#存储非明文的密码值
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
            ac_label.append("低风速空调" + chr(64 + i - len(high_speed_ac_list) - len(medium_speed_ac_list)))
    return ac_list, ac_label

#ToDo
def send_post_request(ac_id: int, data_list):
    my_json = {'ac_id': ac_id}
    print(ac_id)


def query_ac_state(ac_id: int):
    my_json = {'ac_id': ac_id}
    print(ac_id)
    data = 1
    if data == 1:
        target = data['data']
        target['ac_id'] = ac_id
        return target
    else:
        st.error(data['message'])

def get_data():
    ac_list, ac_label = transform()
    tab_list = st.tabs(ac_label)
    high_speed_ac_list = []
    medium_speed_ac_list = []
    low_speed_ac_list = []
    for high_speed_ac_id in st.session_state['high_speed_ac']:
        high_speed_ac_list.append(query_ac_state(high_speed_ac_id))
    for medium_speed_ac_id in st.session_state['medium_speed_ac']:
        medium_speed_ac_list.append(query_ac_state(medium_speed_ac_id))
    for low_speed_ac_id in st.session_state['low_speed_ac']:
        low_speed_ac_list.append(query_ac_state(low_speed_ac_id))
    high_speed_list = sorted(high_speed_ac_list, key=lambda x: x['ac_id'])
    medium_speed_list = sorted(medium_speed_ac_list, key=lambda x: x['ac_id'])
    low_speed_list = sorted(low_speed_ac_list, key=lambda x: x['ac_id'])
    data_list = high_speed_list + medium_speed_list + low_speed_list
    return data_list, tab_list

def display(ac_state, temperature, totalOperationTime, totalPowerConsumption, fan_speed):
    col1, col2, col3, col4, col5= st.columns(5)
    col1.metric("空调状态", ac_state)
    col2.metric("空调温度", temperature)
    col3.metric("累计运行时间", totalOperationTime)
    col4.metric("总电力消耗", totalPowerConsumption)
    col5.metric("风速", fan_speed)



if st.session_state['stage'] == 'login':
    st.title('管理员登录')
    st.markdown("#### 请输入管理员密码")
    password = st.text_input("密码", type="password")

    def login():
        if password == '123':
            st.balloons()
        else:
            st.error("密码不能为空")
            return

    st.button("登录", on_click=login)
else:
    st.title("空调状态")
    tabs = []
    data_list, tab_list = get_data()

    def powerOn(args):
        my_json = {"ac_id": args}
        headers = {
            "Authorization": st.session_state['token']
        }
        data = 1
        if data == 0:
            st.error(data['message'])
        else:
            st.success("成功开启空调")

    def powerOff(args):
        my_json = {"ac_id": args}
        headers = {
            "Authorization": st.session_state['token']
        }
        data = 1
        if data == 0:
            st.error(data['message'])
        else:
            st.success("成功关闭空调")


    for tab, tab_content in zip(tab_list, data_list):
        with tab:
            if tab_content:
                display(tab_content['ac_state'], tab_content['temperature'],
                        tab_content['power_consumption'], tab_content['operation_time'], tab_content['fan_speed'])
                if tab_content['ac_state'] == '关闭':
                    st.button("开启", key=f"poweron_{tab_content['ac_id']}", on_click=powerOn,
                              args=(tab_content['ac_id'],), use_container_width=True)
                elif tab_content['ac_state'] == '空闲':
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.button("关闭", key=f"poweroff_{tab_content['ac_id']}", on_click=powerOff,
                                  args=(tab_content['ac_id'],), use_container_width=True)