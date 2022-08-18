import streamlit as st
from scripts.helpers import Mqtt as mqtt
from datetime import datetime
# import pandas as pd

st.set_page_config(
    page_title="Orac MouldFlow",
    page_icon="⭕",
    layout="wide",
    initial_sidebar_state='auto'
)

client_id = datetime.now().strftime('%d/%b/%Y %H:%M:%S.%f') + '_statuspush'
page_mqtt = mqtt(f'{client_id}')
page_mqtt.make_connection()

def send_mqtt(topic, payload):
    page_mqtt.client.publish(topic=topic, payload=str(payload), qos=1, retain=True)

m = st.markdown("""
<style>
div.stButton > button:first-child {
    box-shadow: 0px 15px 14px -7px #276873;
	background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);
	background-color:#599bb3;
	border-radius:9px;
	border:4px solid #29668f;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:28px;
	font-weight:bold;
	padding:13px 60px;
	text-decoration:none;
	text-shadow:0px 9px 5px #3d768a;
}
</style>""", unsafe_allow_html=True)

# st.sidebar.write(st.session_state)
data = {}

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'history' not in st.session_state:
    st.session_state.history = []

c1, c2, c3, c4, c5, c6 = st.columns(6)
insert_button = c1.empty()
issue_button = c2.empty()
out_button = c4.empty()
reset_button = c6.empty()
st.markdown('***')

m1, m2 = st.columns([3, 2])
pl = m1.empty()
with m2.expander('Matrijsonderhoud'):
    st.markdown('***')
    clean_button = st.empty()
    st.markdown('***')
    extern_button = st.empty()
    st.markdown('***')

def mqttprep(num, command):
    # st.write(num)
    # st.sidebar.write(st.session_state[str(num)])
    data['DateTime'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data['die'] = st.session_state[str(num)]
    data['status'] = command
    topic = 'MATRIJSONDERHOUD'
    send_mqtt(topic, payload=data)
    st.session_state.history.append(data)
    if len(st.session_state.history) > 3:
        st.session_state.history = st.session_state.history[-3:]
    m1.write(st.session_state.history)

hist = m1.button('show_history')
if hist:
    m1.write(st.session_state.history)

while True:
    num = st.session_state.num
    if reset_button.button('reset', key=f'reset_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        # send_mqtt(num)
        st.session_state.num += 1

    elif insert_button.button('IN', key=f'insert_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        mqttprep(num, 'IN')
        st.session_state.num += 1

    elif issue_button.button('ISSUE', key=f'issue_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        mqttprep(num, 'ISSUE')
        st.session_state.num += 1

    elif out_button.button('OUT', key=f'out_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        mqttprep(num, 'OUT')
        st.session_state.num += 1

    elif extern_button.button('EXTERN', key=f'extern_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        mqttprep(num, 'EXTERN')
        st.session_state.num += 1

    elif clean_button.button('CLEAN', key=f'clean_{num}'):
        pl.empty()
        pl.text_input('Scan hier je matrijs', key=num)
        mqttprep(num, 'CLEAN')
        st.session_state.num += 1
    else:
        pl.text_input('Scan hier je matrijs', key=num)
        st.stop()

