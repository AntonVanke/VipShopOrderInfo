from tinydb import TinyDB, where

import streamlit as st

# 屏蔽掉默认组件
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

db = TinyDB("database.json")
# 用户数据表
users_table = db.table("users")


def login():
    # 密码输入
    password_input = st.empty()
    # 密码确认
    password_button = st.empty()

    password = password_input.text_input("请输入鉴权Key")
    if password_button.button("登入"):
        if password == "8D8735985D2054ACB4B2F93365DE4124A1F3F3FFE19E6B9C897A40E0EDC6C90D":
            password_button.empty()
            password_input.empty()
        else:
            st.error("密码错误")

