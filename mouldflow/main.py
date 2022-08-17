import streamlit as st
from scripts.helpers import Mqtt as mqtt
from datetime import datetime

st.write('hello friesssnd')

client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S.%f') + '_statuspush'
page_mqtt = mqtt(f'{client_id}')
page_mqtt.make_connection()

def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)

send = st.button('click')
if send:
    topic = 'test'
    payload = '111'
    send_mqtt(topic, payload=payload)
