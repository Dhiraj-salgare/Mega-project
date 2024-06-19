from PIL import Image
import numpy as np
import streamlit as st
import mysql.connector
import uuid
from streamlit_option_menu import option_menu
import io

def connect_to_mysql():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        port='3305',
        password='',
        database='criminal_recognition'
)

# Function to register criminal with multiple photos
def register_criminal():
    st.header("Criminal Registration")
    Criminal_Name = st.text_input("Name")
    Address = st.text_input("Address")  
    Birth_date = st.date_input("Birth Date")
    mark = st.text_input("Identification Mark")
    country = st.text_input("Country")
    photos = st.file_uploader("Upload Photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
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

    if st.button("Register Criminal"):
        crim_uuid = str(uuid.uuid4())
        criminal_id = crim_uuid[:4]

        try:
            connection = connect_to_mysql()
            mydb = connection.cursor()
            
            # Create criminal_register table if not exists
            sql_create_criminal_register = """
            CREATE TABLE IF NOT EXISTS criminal_register (
                criminal_Id VARCHAR(4) PRIMARY KEY,
                criminal_name VARCHAR(20),
                adress VARCHAR(30),
                Birth_date DATE,
                Identification_mark VARCHAR(20),
                country VARCHAR(20),
                userid VARCHAR(10)
            )
            """
            mydb.execute(sql_create_criminal_register)

            # Create photos table if not exists
            sql_create_photos_table = """
            CREATE TABLE IF NOT EXISTS photos (
                photo_id INT AUTO_INCREMENT PRIMARY KEY,
                criminal_id VARCHAR(4),
                photo longblob,
                date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (criminal_id) REFERENCES criminal_register(criminal_Id)
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
            connection = connect_to_mysql()
            mydb = connection.cursor()
            
            # Insert criminal data into criminal_register table
            sql_insert_criminal = """
            INSERT INTO criminal_register (criminal_Id, criminal_name, adress, Birth_date, Identification_mark, country, userid)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val_criminal = (criminal_id, Criminal_Name, Address, Birth_date, mark, country, st.session_state.userId)
            mydb.execute(sql_insert_criminal, val_criminal)

            # Insert photo data into photos table
            sql_insert_photo = "INSERT INTO photos (criminal_id, photo) VALUES (%s, %s)"
            for img in images:
                val_photo = (criminal_id, img)
                mydb.execute(sql_insert_photo, val_photo)
            connection.commit()
            st.success("Registration successfully completed")
        except mysql.connector.Error as error:
            st.error(f"Failed to register criminal: {error}")
        finally:
            if connection.is_connected():
                mydb.close()
                connection.close()

if __name__ == "__main__":
    st.title("Criminal Registration System")
    register_criminal()
