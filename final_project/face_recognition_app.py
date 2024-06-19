import face_recognition
import cv2
import streamlit as st
import database  # Import the database module
import winsound


def face_recog():
    st.empty()
  
    # Load sample images and encode known faces
    known_face_encodings, known_face_names = database.fetch_known_faces()  # Call fetch_known_faces from the database module

    # Initialize variables
    face_locations = []
    face_encodings = []
    face_names = []
    recognized_faces = set()


    st.title("Finding criminal..")
    stframe = st.empty()
    col_info, col_photo = st.columns([3, 1])

    
    # Open video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        # Read video frame
        ret, frame = video_capture.read()

        # Convert the image from BGR color (OpenCV default) to RGB color
        # rgb_frame = frame[:, :, ::-1]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compare face encoding with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=0.5)
            name = "Unknown"

            # If a match is found, use the known face name
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

        # Clear the information columns
        col_info.empty()
        col_photo.empty()
        
        # Display results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if(name == "Unknown"):
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                # Draw a label with the name below the face
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
            else:
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with the name below the face
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
                # Play the beep
                winsound.Beep(2000, 1000)
                
            if name != "Unknown" and name not in recognized_faces:
                recognized_faces.add(name)
                # Fetch criminal data from the database
                criminal_data = database.fetch_criminal_data(name)
                if criminal_data:
                    # Display criminal information
                    
                    col_info.write("Criminal Data:")
                    col_info.write(f"Name: {criminal_data['name']}")
                    col_info.write(f"ID: {criminal_data['id']}")
                    col_info.write(f"Address: {criminal_data['adress']}")
                    col_info.write(f"Birth Date: {criminal_data['birth_date']}")
                    col_info.write(f"Country: {criminal_data['country']}")

                    # Display matched face image
                    col_photo.image(criminal_data['photo'], caption=f"Matched Face: {criminal_data['name']}", width=150)
                    st.write("-----------------------------------------------------")
                        
                
        # Display the resulting image
        # cv2.imshow('Face Recognition', frame)
        stframe.image(frame,channels="BGR")
        

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()
