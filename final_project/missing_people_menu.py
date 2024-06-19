import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import web_with_database 
import reg
import video
import missing_reg
import missing_recog
import missing_video

def start_stop_process1():
    if st.session_state.button_state:
        st.session_state.button_state = False
    else:
        st.session_state.button_state = True
        
def missing_people_menu():
    
    with st.sidebar:
       missing_people_menu_option = option_menu("Missing People Options", ["Register Missing People","Realtime Surveillance", "Video Surveillance", "Missing People Data"])
       
    if missing_people_menu_option == "Register Missing People":
                    
                    missing_reg.register_missing_people()
    elif missing_people_menu_option  == "Realtime Surveillance":
                        st.header("Realtime Surveillance")
                        if st.button("Start/Stop", on_click = start_stop_process1):
                            if st.session_state.button_state:
                                # Call your function to start the process
                                missing_recog.face_recog()
                                st.write("Process started")
                            else:
                                # Call your function to stop the process
                                st.write("Process stopped") 
    elif missing_people_menu_option  == "Video Surveillance":
                        
                        missing_video.video_surveillance()              
                    
    elif missing_people_menu_option == "Missing People Data":
                    st.header("Missing People Data")
                    st.write("-----------------------------------------------------")
                    df = web_with_database.missing_people_data(st.session_state.userId)
                    grouped = df.groupby(['people_id', 'people_name', 'adress', 'birth_date', 'identification_mark', 'country'])
                
                    for (people_id, name, address, birth_date, mark, country), group in grouped:
                        left_column, right_column = st.columns([3, 1])  # Ratio of 3:1

                        # Display text data in the left column
                        left_column.write(f"Missing Id: {people_id}")
                        left_column.write(f"Name: {name}")
                        left_column.write(f"Adress: {address}")
                        left_column.write(f"Birth Date: {birth_date}")
                        left_column.write(f"Identification Mark: {mark}")
                        left_column.write(f"Country: {country}")

                        # Display images in the right column
                        with right_column:
                            web_with_database.display_image(group['photo'].tolist())
                        st.write("-----------------------------------------------------")
