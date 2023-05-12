from tinydb import TinyDB, where

import streamlit as st
from streamlit_elements import elements, mui, html, dashboard

st.set_page_config(page_title="VIPShop订单整理系统", layout="wide")
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
orders_table = db.table("orders")

st.table([{
    "id": "533372022",
    "token": "E2AF37CD0987B4CF9B6650BDA75F7F04ECBA6B79"
}, {
    "id": "654654664",
    "token": "E2AF37CD0987B4CF9B6650BDA75F7F04ECBA6B79"
}
])
