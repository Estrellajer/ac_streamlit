import streamlit as st
import requests
import json
from Utils2 import utils2
from enum import Enum
import time



st.set_page_config(
    page_title="房客空调面板",
    page_icon="👋",
)

class Stage(Enum):
    LOGIN = "用户登录"
    REGISTER = "用户注册"
    SELECT_ROOM = "选择房间"
    SET_TEMPERATURE = "设置温度"
    SET_FAN_SPEED = "设置风速"
    WAIT_FOR_SERVICE = "等待服务"
    START_AC = "启动空调"
    END_STAY = "结束住宿"
    PAY = "结账"

# 设置全局变量
if 'stage' not in st.session_state:
    st.session_state['stage'] = Stage.LOGIN.value
if 'room_number' not in st.session_state:
    st.session_state['room_number'] = None
if 'guest_phone' not in st.session_state:
    st.session_state['guest_phone'] = None
if 'identity' not in st.session_state:
    st.session_state['identity'] = None
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 25.0
if 'fan_speed' not in st.session_state:
    st.session_state['fan_speed'] = '中风'
if 'ac_status' not in st.session_state:
    st.session_state['ac_status'] = False
if 'bill' not in st.session_state:
    st.session_state['bill'] = 0.0
if "error_flag" not in st.session_state:
    st.session_state['error_flag'] = False
if "error_info" not in st.session_state:
    st.session_state['error_info'] = ""
if "warning_flag" not in st.session_state:
    st.session_state['warning_flag'] = False
if "warning_info" not in st.session_state:
    st.session_state['warning_info'] = ""
if "info_flag" not in st.session_state:
    st.session_state['info_flag'] = False
if "info_info" not in st.session_state:
    st.session_state['info_info'] = ""
if "success_flag" not in st.session_state:
    st.session_state['success_flag'] = False
if "success_info" not in st.session_state:
    st.session_state['success_info'] = ""
if "loop" not in st.session_state:
    st.session_state['loop'] = False


st.sidebar.markdown("## 使用流程")
if st.session_state['stage'] == Stage.LOGIN.value:
    st.sidebar.warning("房客登录")
if st.session_state['stage'] == Stage.SELECT_ROOM.value:
    st.sidebar.success("房客登录")
    st.sidebar.warning("选择房间")
if st.session_state['stage'] == Stage.SET_TEMPERATURE.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.warning("设置温度")
if st.session_state['stage'] == Stage.SET_FAN_SPEED.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.success("设置温度")
    st.sidebar.warning("设置风速")
if st.session_state['stage'] == Stage.WAIT_FOR_SERVICE.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.success("设置温度")
    st.sidebar.success("设置风速")
    st.sidebar.warning("等待服务")
if st.session_state['stage'] == Stage.START_AC.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.success("设置温度")
    st.sidebar.success("设置风速")
    st.sidebar.success("等待服务")
    st.sidebar.warning("启动空调")
if st.session_state['stage'] == Stage.END_STAY.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.success("设置温度")
    st.sidebar.success("设置风速")
    st.sidebar.success("等待服务")
    st.sidebar.success("启动空调")
    st.sidebar.warning("结束住宿")
if st.session_state['stage'] == Stage.PAY.value:
    st.sidebar.success("房客登录")
    st.sidebar.success("选择房间")
    st.sidebar.success("设置温度")
    st.sidebar.success("设置风速")
    st.sidebar.success("等待服务")
    st.sidebar.success("启动空调")
    st.sidebar.success("结束住宿")
    st.sidebar.warning("结账")


def show_info():
    if st.session_state['error_flag']:
        st.error(st.session_state['error_info'])
    if st.session_state['warning_flag']:
        st.warning(st.session_state['warning_info'])
    if st.session_state['info_flag']:
        st.info(st.session_state['info_info'])
    if st.session_state['success_flag']:
        st.success(st.session_state['success_info'])
    st.session_state['error_flag'] = False
    st.session_state['warning_flag'] = False
    st.session_state['info_flag'] = False
    st.session_state['success_flag'] = False



def login():
    show_info()
    st.markdown("## 酒店房客控制空调系统 🏨❄️")
    st.markdown('---')
    st.markdown("#### 房客登录")
    room_number = st.text_input("房间号")
    guest_phone = st.text_input("房客手机号")
    identity = st.text_input("身份验证信息", type="password")

    def login_on_click(args):
        if args == "logon":
            st.session_state['stage'] = Stage.SELECT_ROOM.value
            return
        if not room_number:
            st.error("请输入房间号")
            return
        if not guest_phone:
            st.error("请输入房客手机号")
            return
        if not identity:
            st.error("请输入身份验证信息")
            return
        # 在此添加与酒店系统的身份验证逻辑
        # 如果身份验证成功，可以设置相关房客信息
        # 例如，st.session_state['room_number'] = room_number
        # 以及其他相关信息，然后将阶段切换为选择房间
        st.session_state['room_number'] = room_number
        st.session_state['guest_phone'] = guest_phone
        st.session_state['identity'] = identity
        st.session_state['stage'] = Stage.SELECT_ROOM.value

    col1, col2 = st.columns(2)
    with col1:
        st.button("登录", on_click=login_on_click, args=("login",), use_container_width=True)
    with col2:
        st.button("注册", on_click=login_on_click, args=("logon",), use_container_width=True)

if st.session_state['stage'] == Stage.LOGIN.value:
    login()

def register():
    st.markdown("## 酒店房客控制空调系统 🏨❄️")
    st.markdown('---')
    st.markdown("#### 房客注册")
    guest_phone = st.text_input("房客手机号")
    room_number = st.text_input("房间号")
    identity = st.text_input("身份验证信息", type="password")

    def register_on_click(args):
        if args == "login":
            st.session_state['stage'] = Stage.LOGIN.value
            return
        if not guest_phone:
            st.error("请输入房客手机号")
            return
        if not room_number:
            st.error("请输入房间号")
            return
        if not identity:
            st.error("请输入身份验证信息")
            return
        # 在此添加与酒店系统的注册逻辑
        # 如果注册成功，可以设置相关房客信息
        # 例如，st.session_state['room_number'] = room_number
        # 以及其他相关信息，然后将阶段切换为选择房间
        st.session_state['room_number'] = room_number
        st.session_state['guest_phone'] = guest_phone
        st.session_state['identity'] = identity
        st.session_state['stage'] = Stage.SELECT_ROOM.value

    col1, col2 = st.columns(2)
    with col1:
        st.button("登录", on_click=register_on_click, args=("login",), use_container_width=True)
    with col2:
        st.button("注册", on_click=register_on_click, args=("logon",), use_container_width=True)

if st.session_state['stage'] == Stage.REGISTER.value:
    register()

def select_room():
    st.markdown("### 选择房间")
    st.markdown("----")
    show_info()

    user_room = st.session_state['room_number']  # 从登录或注册中获取用户的房间号
    available_floors = ["1楼", "2楼", "3楼", "4楼"]  # 示例的楼层列表
    floor_to_rooms = {
        "1楼": ["101", "102", "103", "123"],
        "2楼": ["201", "202", "203"],
        "3楼": ["301", "302", "303"],
        "4楼": ["401", "402", "403"]
    }

    def confirm_on_click():
        selected_floor = st.session_state['selected_floor']
        selected_room = st.session_state['selected_room']
        if selected_floor and selected_room == user_room:
            st.success(f"您选择了{selected_floor}的{selected_room}房间")
            # 在这里添加分配房间的逻辑
            st.session_state['stage'] = Stage.SET_TEMPERATURE.value
        else:
            st.error("请正确选择您登录/注册时填写的房间号")

    selected_floor = st.selectbox("选择楼层", available_floors, key='selected_floor')
    available_rooms = floor_to_rooms[selected_floor]
    selected_room = st.selectbox("选择房间号", available_rooms, key='selected_room')

    with st.form(key='select_room'):
        st.form_submit_button("确认选择", use_container_width=True, on_click=confirm_on_click)

if st.session_state['stage'] == Stage.SELECT_ROOM.value:
    select_room()

# def select_temperature():
#     st.markdown("### 选择温度")
#     st.markdown("----")
#     show_info()
#
#     def confirm_on_click():
#         selected_temperature = st.session_state['selected_temperature']
#         if selected_temperature:
#             # 在这里添加设置温度的逻辑
#             st.success(f"温度已设置为 {selected_temperature} 度")
#         else:
#             st.error("请选择温度")
#
#     selected_temperature = st.slider('选择温度 (度)', 16, 30, 24, 1, key='selected_temperature')
#
#     with st.form(key='select_temperature'):
#         st.form_submit_button("确认选择温度", use_container_width=True, on_click=confirm_on_click)
#
# if st.session_state['stage'] == Stage.SET_TEMPERATURE.value:
#     select_temperature()