import streamlit as st
import mysql.connector
import uuid
from streamlit_option_menu import option_menu
import face_recognition
import face_recognition_app
import pandas as pd
import cv2
from PIL import Image
from io import BytesIO
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import web_with_database 
import reg
import video
import criminal_data

def crimnal_menu():
    
    with st.sidebar:
       criminal_menu_option = option_menu("Criminal Options", ["Register Criminal", "Realtime Surveillance", "Video Surveillance", "Criminal Data"])
       
    if criminal_menu_option == "Register Criminal":
                        reg.register_criminal()
                        st.empty()
    elif criminal_menu_option  == "Realtime Surveillance":
                        st.header("Realtime Surveillance")
                        if st.button("Start/Stop", on_click=web_with_database.start_stop_process):
                            if st.session_state.button_state:
                                # Call your function to start the process
                                face_recognition_app.face_recog()
                                st.write("Process started")
                            else:
                                # Call your function to stop the process
                                st.write("Process stopped")
    elif criminal_menu_option  == "Video Surveillance":
                        
                        video.video_surveillance()
    elif criminal_menu_option  == "Criminal Data":
                        st.header("Criminal Data")
                        st.write("-----------------------------------------------------")
                        criminal_data.criminal_data(st.session_state.userId)
                        # grouped = df.groupby(['criminal_Id', 'criminal_name', 'adress', 'Birth_date', 'Identification_mark', 'country'])
                    
                        # for (criminal_id, name, address, birth_date, mark, country), group in grouped:
                        #     left_column, right_column = st.columns([3, 1])  # Ratio of 3:1

                        #     # Display text data in the left column
                        #     left_column.write(f"Criminal Id: {criminal_id}")
                        #     left_column.write(f"Criminal Name: {name}")
                        #     left_column.write(f"Adress: {address}")
                        #     left_column.write(f"Birth Date: {birth_date}")
                        #     left_column.write(f"Identification Mark: {mark}")
                        #     left_column.write(f"Country: {country}")

                        #     # Display images in the right column
                        #     with right_column:
                        #         web_with_database.display_image(group['photo'].tolist())
                        #     st.write("-----------------------------------------------------")