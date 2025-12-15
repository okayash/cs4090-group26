import os
import mysql.connector
import streamlit as st


def get_conn():
    '''
    db connection for 
    1. planetscale
    2. local env
    '''
    if "connections" in st.secrets:
        conn = mysql.connector.connect(
            host=st.secrets["connections"]["mysql"]["host"],
            database=st.secrets["connections"]["mysql"]["database"],
            user=st.secrets["connections"]["mysql"]["username"],
            password=st.secrets["connections"]["mysql"]["password"],
            ssl_disabled=False,
            autocommit=True
        )
        return conn

    return mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", 3306),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "clio"),
    )