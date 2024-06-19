import face_recognition
import cv2
import streamlit as st
import database_missing  # Import the database module
import winsound



def face_recog():
    
    st.empty()
  
    # Load sample images and encode known faces
    known_face_encodings, known_face_names = database_missing.fetch_known_faces()  # Call fetch_known_faces from the database module

    # Initialize variables
    face_locations = []
    face_encodings = []
    face_names = []

    st.title("Finding Missing People..")
    stframe = st.empty()
    
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
                
                
        # Display the resulting image
        # cv2.imshow('Face Recognition', frame)
        stframe.image(frame,channels="BGR")
        

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()
