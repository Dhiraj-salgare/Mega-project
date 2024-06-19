import mysql.connector
from PIL import Image
import io
import numpy as np
import face_recognition

# Function to connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        port='3305',
        password='',
        database='criminal_recognition'
    )

# Function to fetch known face encodings and names from MySQL database
def fetch_known_faces():
    known_face_encodings = []
    known_face_names = []

    try:
        connection = connect_to_mysql()
        cursor = connection.cursor()

        # Fetch known faces from the database
        # cursor.execute("SELECT photo, criminal_name FROM criminal_register")
        cursor.execute("SELECT missing_register.people_name,photos2.photo FROM missing_register Join photos2 on missing_register.people_id = photos2.people_id")
        rows = cursor.fetchall()

        for row in rows:
            # Convert binary image data to numpy array
            image_data = row[1]
            image = Image.open(io.BytesIO(image_data))
            image_np = np.array(image)

            # Detect face encoding
            face_encoding = face_recognition.face_encodings(image_np)[0]

            known_face_encodings.append(face_encoding)
            known_face_names.append(row[0])

    except mysql.connector.Error as error:
        print(f"Error fetching known faces from MySQL database: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return known_face_encodings, known_face_names
