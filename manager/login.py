import streamlit as st
import requests
import json
from utils import utils

st.set_page_config(
    page_title="管理员客户端",
    page_icon="👋",
)

# 设置全局变量
if 'stage' not in st.session_state:
    st.session_state['stage'] = 'login'
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
    def exit():
        headers = {
            "Authorization": st.session_state['token']
        }
        data = 1
        if data == 1:
            st.session_state['stage'] = "login"
        else:
            st.error('unable to logout')


    st.title("管理员退出")
    img = 'https://img.mjj.today/2023/05/27/47d01dd60f3f5e83da821f40d829fe7c.png'
    st.image(img, caption='您现在处于登录状态')
    st.button("退出", on_click=exit)
