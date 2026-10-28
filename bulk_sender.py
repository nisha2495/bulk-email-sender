import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

st.set_page_config(page_title="Bulk Email Sender - shanza", page_icon="📧")

st.title("📧 Python Bulk Email Sender - Pro")
with st.sidebar:
    smtp_server = st.text_input("SMTP Server", "smtp.gmail.com")
    smtp_port = st.number_input("Port", value=587)
    email_user = st.text_input("Your Email")
    email_pass = st.text_input("App Password", type="password")
    delay = st.slider("Delay (sec)", 1, 10, 2)

subject = st.text_input("Subject", "Hello from Shanza")
uploaded_file = st.file_uploader("Upload Excel/CSV (column: email)", type=["xlsx","csv"])
body = st.text_area("Body (HTML)", value="<h3>Hello {email},</h3><p>Test email</p>", height=200)
attachment = st.file_uploader("Attachment", type=["pdf","jpg","png"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
    emails = df['email'].tolist()
else:
    emails = []

if st.button("📤 Start Sending", type="primary"):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_user, email_pass)
    for to_email in emails:
        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = email_user, to_email, subject
        msg.attach(MIMEText(body, 'html'))
        server.send_message(msg)
        time.sleep(delay)
    st.success("Done!")