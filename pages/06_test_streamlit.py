import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

dictionnaire = {"text" : "test"}

st.write(dictionnaire["text"])

copy_button = Button(label="Copier l'article")
copy_button.js_on_event("button_click", CustomJS(args={"text" : "test"}, code="""
    navigator.clipboard.writeText(text);
    """))

no_event = streamlit_bokeh_events(
    copy_button,
    events="GET_TEXT",
    key="get_text",
    refresh_on_update=True,
    override_height=75,
    debounce_time=0)