import smtplib, ssl
from email.message import EmailMessage
import streamlit as st

def _smtp_settings():
    try:
        e = st.secrets["email"]
        return dict(
            sender=e["sender_email"],
            server=e["smtp_server"],
            port=int(e.get("smtp_port", 465)),
            username=e["smtp_username"],
            password=e["smtp_password"],
            use_ssl=bool(e.get("use_ssl", True)),
        )
    except Exception:
        return None

def send_email(to: str, subject: str, body: str) -> bool:
    cfg = _smtp_settings()
    if not cfg:
        return False
    msg = EmailMessage()
    msg["From"] = cfg["sender"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    if cfg["use_ssl"]:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(cfg["server"], cfg["port"], context=context) as server:
            server.login(cfg["username"], cfg["password"])
            server.send_message(msg)
    else:
        with smtplib.SMTP(cfg["server"], cfg["port"]) as server:
            server.starttls(context=ssl.create_default_context())
            server.login(cfg["username"], cfg["password"])
            server.send_message(msg)
    return True
