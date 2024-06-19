from PIL import Image
import numpy as np
import streamlit as st
import mysql.connector
import uuid
from streamlit_option_menu import option_menu
import io
import web_with_database 
import reg
import video

def register_missing_people():
    st.header("Missing People Registration")
    People_Name = st.text_input("name")
    Address = st.text_input("address")  
    Birth_date = st.date_input("birth Date")
    mark = st.text_input("identification Mark")
    country = st.text_input("country")
    photos = st.file_uploader("upload Photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if photos:
        images = []  # This will store the binary data of the images

        # Iterate through the uploaded photos
        for photo in photos:
            # Open the photo as an image
            # image = Image.open(photo)
            
            # Display the uploaded image
            # st.image(image, caption=f"Uploaded Photo: {photo.name}", use_column_width=True)
            
            # Convert the image to bytes and store in the list
            photo.seek(0)  # Reset the file pointer to the beginning of the file
            img_bytes = photo.read()
            # st.image(image, caption=f"Uploaded Photo: {photo.name}", use_column_width=True)
            images.append(img_bytes)  # Append the binary data to the list
    else:
        st.warning("Upload at least one photo")
        return  # Exit the function if no photos are uploaded

    if st.button("Register"):
        people_uuid = str(uuid.uuid4())
        people_id = people_uuid[:4]

        try:
            connection = web_with_database.connect_to_mysql()
            mydb = connection.cursor()
            
            # Create criminal_register table if not exists
            sql_create_missing_register = """
            CREATE TABLE IF NOT EXISTS missing_register (
                people_Id VARCHAR(4) PRIMARY KEY,
                people_name VARCHAR(20),
                adress VARCHAR(30),
                Birth_date DATE,
                Identification_mark VARCHAR(20),
                country VARCHAR(20),
                userid VARCHAR(10)
            )
            """
            mydb.execute(sql_create_missing_register)

            # Create photos table if not exists
            sql_create_photos_table = """
            CREATE TABLE IF NOT EXISTS photos2 (
                photo_id INT AUTO_INCREMENT PRIMARY KEY,
                people_id VARCHAR(4),
                photo longblob,
                date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (people_id) REFERENCES missing_register(people_Id)
            )
            """
            mydb.execute(sql_create_photos_table)
            connection.commit()
        except mysql.connector.Error as error:
            st.error(f"Failed to create tables: {error}")
            return  # Exit the function if table creation fails
        finally:
            if connection.is_connected():
                mydb.close()
                connection.close()

        try:
            connection = web_with_database.connect_to_mysql()
            mydb = connection.cursor()
            
            # Insert criminal data into criminal_register table
            sql_insert_people = """
            INSERT INTO missing_register (people_Id, people_name, adress, Birth_date, Identification_mark, country, userid)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val_people = (people_id, People_Name, Address, Birth_date, mark, country, st.session_state.userId)
            mydb.execute(sql_insert_people, val_people)

            # Insert photo data into photos table
            sql_insert_photo = "INSERT INTO photos2 (people_id, photo) VALUES (%s, %s)"
            for img in images:
                val_photo = (people_id, img)
                mydb.execute(sql_insert_photo, val_photo)
            connection.commit()
            st.success("Registration successfully completed")
        except mysql.connector.Error as error:
            st.error(f"Failed to register criminal: {error}")
        finally:
            if connection.is_connected():
                mydb.close()
                connection.close()