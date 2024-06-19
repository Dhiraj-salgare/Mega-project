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
import reg
import video
import crimnal_menu
import missing_people_menu


hello1 = st.container()
header = st.container()

def connect_to_mysql():
    return mysql.connector.connect(
    host='localhost',
    user='root',
    port='3305',
    password='',
    database='criminal_recognition'
)

if 'button_state' not in st.session_state:
    st.session_state.button_state = False

# Function to simulate login
def login_btn(username, password):
    try:
        connection = connect_to_mysql()
        mydb = connection.cursor()
        sql = "select * from user_register where username=%s AND password=%s"
        val = (username, password)
        mydb.execute(sql, val)
        user = mydb.fetchone()
        if user:
            st.success("Login successful")
            st.session_state['loggedIn'] = True
            st.session_state.userId = user[0]
        else:
            st.error("Invalid username and password")
    except mysql.connector.Error as error:
        st.error(f"Failed to login: {error}")
    finally:
        if connection.is_connected():
            mydb.close()
            connection.close()

def login():
    st.header(" CRIMINAL AND MISSING PEOPLE DETECTION SYSTEM")
    st.image("D:\mega_python\wr.jpeg")
    
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    st.button("login", on_click=login_btn, args=(username, password))

# Register criminal
def register_criminal():
    st.header("Register Criminal")
    reg.register_criminal()

# Video surveillance
def video_surveillance():
    video.video_surveillance()

# # Code for criminal data
# def criminal_data(user_id):
#     st.header("Criminal Data")
#     connection = connect_to_mysql()
#     cursor = connection.cursor()
#     sql = "SELECT r.criminal_Id, r.criminal_name, r.adress, r.Birth_date, r.Identification_mark, r.country, p.photo FROM criminal_register r Join photos p on r.criminal_id = p.criminal_id WHERE userid = %s"
#     cursor.execute(sql, (user_id,))
#     data = cursor.fetchall()
#     columns = [i[0] for i in cursor.description]
    
#     # Close cursor and connection
#     cursor.close()
#     connection.close()
    
#     # Create DataFrame
#     df = pd.DataFrame(data, columns=columns)
    
#     return df

def display_image(image_data):
    for img_data in image_data:
        image = Image.open(BytesIO(img_data))
        st.image(image, caption="Criminal Photo", width=150)

def start_stop_process():
    if st.session_state.button_state:
        st.session_state.button_state = False
    else:
        st.session_state.button_state = True
        
# def start_stop_process1():
#     if st.session_state.button_state:
#         st.session_state.button_state = False
#     else:
#         st.session_state.button_state = True

# Function to register missing people
# def register_missing_people():
#     st.header("Register Missing People")
#     register_missing_people.register_missing_people()
    # Implement the registration form and logic similar to the register_criminal function

# missing people data
# def missing_people_data(user_id):
    
#     st.header("Missing People Data")
#     connection = connect_to_mysql()
#     cursor = connection.cursor()
#     sql = "SELECT m.people_id, m.people_name, m.adress, m.birth_date, m.identification_mark, m.country, p.photo FROM missing_register m Join photos2 p on m.people_id = p.people_id WHERE userid = %s"
#     cursor.execute(sql, (user_id,))
#     data = cursor.fetchall()
#     columns = [i[0] for i in cursor.description]
    
#     # Close cursor and connection
#     cursor.close()
#     connection.close()
    
#     # Create DataFrame
#     df = pd.DataFrame(data, columns=columns)
    
#     return df

def hello():
    with hello1:
        with st.sidebar:
            selected_option = option_menu("Menu", ["Criminal Menu", "Missing People Menu"],key="main_menu")
            # criminal_menu_option = option_menu("Criminal Options", ["Register Criminal", "Realtime Surveillance", "Video Surveillance", "Criminal Data"])
            # missing_people_menu_option = option_menu("Missing People Options", ["Register Missing People", "Missing People Data"])
            
        if selected_option == "Criminal Menu":
            
            crimnal_menu.crimnal_menu()
                # criminal_menu_option = option_menu("Criminal Options", ["Register Criminal", "Realtime Surveillance", "Video Surveillance", "Criminal Data"])

                # options = option_menu("Criminal Menu", options=["Register Criminal", "Realtime Surveillance", "Video Surveillance", "Criminal Data"])
                # missing_options = option_menu("Missing People Menu", options=["Register Missing People", "Missing People Data"])

            # if criminal_menu_option == "Register Criminal":
            #         register_criminal()
            #         st.empty()
            # elif criminal_menu_option  == "Realtime Surveillance":
            #         if st.button("Start/Stop", on_click=start_stop_process):
            #             if st.session_state.button_state:
            #                 # Call your function to start the process
            #                 face_recognition_app.face_recog()
            #                 st.write("Process started")
            #             else:
            #                 # Call your function to stop the process
            #                 st.write("Process stopped")
            # elif criminal_menu_option  == "Video Surveillance":
            #         st.write("Video Surveillance")
            #         video_surveillance()
            # elif criminal_menu_option  == "Criminal Data":
            #         df = criminal_data(st.session_state.userId)
            #         grouped = df.groupby(['criminal_Id', 'criminal_name', 'adress', 'Birth_date', 'Identification_mark', 'country'])
                
            #         for (criminal_id, name, address, birth_date, mark, country), group in grouped:
            #             left_column, right_column = st.columns([3, 1])  # Ratio of 3:1

            #             # Display text data in the left column
            #             left_column.write(f"Criminal Id: {criminal_id}")
            #             left_column.write(f"Criminal Name: {name}")
            #             left_column.write(f"Adress: {address}")
            #             left_column.write(f"Birth Date: {birth_date}")
            #             left_column.write(f"Identification Mark: {mark}")
            #             left_column.write(f"Country: {country}")

            #             # Display images in the right column
            #             with right_column:
            #                 display_image(group['photo'].tolist())
            #             st.write("-----------------------------------------------------")

        elif selected_option == "Missing People Menu":
            
            missing_people_menu.missing_people_menu()
                
                # missing_people_menu_option = option_menu("Missing People Options", ["Register Missing People", "Missing People Data"])
                
            # if missing_people_menu_option == "Register Missing People":
            #         register_missing_people()
                    
            # elif missing_people_menu_option == "Missing People Data":
            #         df = missing_people_data(st.session_state.userId)
            #         grouped = df.groupby(['missing_id', 'name', 'address', 'birth_date', 'identification_mark', 'country'])
                
            #         for (missing_id, name, address, birth_date, mark, country), group in grouped:
            #             left_column, right_column = st.columns([3, 1])  # Ratio of 3:1

            #             # Display text data in the left column
            #             left_column.write(f"Missing Id: {missing_id}")
            #             left_column.write(f"Name: {name}")
            #             left_column.write(f"Adress: {address}")
            #             left_column.write(f"Birth Date: {birth_date}")
            #             left_column.write(f"Identification Mark: {mark}")
            #             left_column.write(f"Country: {country}")

            #             # Display images in the right column
            #             with right_column:
            #                 display_image(group['photo'].tolist())
            #             st.write("-----------------------------------------------------")

with header:
    with st.sidebar:
        optionmain = option_menu("Login", options=["Login"],key="login_menu")

    if optionmain == "Login":
        if 'loggedIn' not in st.session_state:
            st.session_state['loggedIn'] = False
            login()
        else:
            if st.session_state['loggedIn']:
                hello()
            else:
                login()
