import face_recognition
import cv2
import streamlit as st
import tempfile  # For temporary file handling

# Assuming fetch_known_faces is defined in the database module
import database_missing  # Import the database module


def video_surveillance():
    st.header("Video Surveillance")
    if 'running' not in st.session_state:
        st.session_state['running'] = False

    st.empty()
    stvideo = st.empty()
    video_file = st.file_uploader("Upload Video", type=["mp4"])

    video_path = None
    if video_file is not None:
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            temp_video_file.write(video_file.read())
            video_path = temp_video_file.name

        

    if st.button("Start/Stop"):
        if not video_path:
            st.error("Please upload a video file first.")
            return

        # Toggle the running state
        st.session_state['running'] = not st.session_state['running']

        if st.session_state['running']:
            # Load sample images and encode known faces
            known_face_encodings, known_face_names = database_missing.fetch_known_faces()  # Call fetch_known_faces from the database module

            # Initialize variables
            face_locations = []
            face_encodings = []
            face_names = []

            st.title("Finding Missing People..")
            stframe = st.empty()

            # Open video capture
            video_capture = cv2.VideoCapture(video_path)

            if not video_capture.isOpened():
                st.error("Error: Could not open video file.")
                return

            while st.session_state['running']:
                # Read video frame
                ret, frame = video_capture.read()
                if not ret:
                    st.write("End of video or failed to read frame.")
                    break

                # Convert the image from BGR color (OpenCV default) to RGB color
                try:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except cv2.error as e:
                    st.error(f"Error converting frame to RGB: {e}")
                    break

                # Find all the faces and their encodings in the current frame
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # Compare face encoding with known faces
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # If a match is found, use the known face name
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    face_names.append(name)

                # Display results
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Draw a box around the face
                    color = (0, 255, 0) if name == "Unknown" else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    # Draw a label with the name below the face
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

                # Display the resulting image
                stframe.image(frame, channels="BGR")

                # Exit loop if 'q' is pressed (for local debugging)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release video capture and close windows
            video_capture.release()
            cv2.destroyAllWindows()
        else:
            st.write("Video surveillance stopped.")