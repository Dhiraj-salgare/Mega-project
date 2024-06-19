import face_recognition
import cv2
import streamlit as st
import tempfile  # For temporary file handling

# Assuming fetch_known_faces is defined in the database module
import database  # Import the database module


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
            known_face_encodings, known_face_names = database.fetch_known_faces()  # Call fetch_known_faces from the database module

            # Initialize variables
            face_locations = []
            face_encodings = []
            face_names = []

            st.title("Finding criminal..")
            stframe = st.empty()
            
            # Open video capture
            video_capture = cv2.VideoCapture(video_path)
            
            if not video_capture.isOpened():
                st.write("Error: Could not open video file.")
                return

            process_frame = True  # Variable to control frame skipping
            skip_frames = 2  # Process every nth frame
            
            while True:
                # Read video frame
                ret, frame = video_capture.read()
                if not ret:
                    st.write("Video processing complete.")
                    break

                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                if process_frame:
                    # Convert the image from BGR color (OpenCV default) to RGB color
                    try:
                        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                    except cv2.error as e:
                        st.write(f"Error converting frame to RGB: {e}")
                        break

                    # Find all the faces and their encodings in the current frame
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

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
                        top *= 2
                        right *= 2
                        bottom *= 2
                        left *= 2

                        if name == "Unknown":
                            # Draw a box around the face
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                            # Draw a label with the name below the face
                            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
                        else:
                            # Draw a box around the face
                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                            # Draw a label with the name below the face
                            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

                        # Display the resulting image
                        stframe.image(frame, channels="BGR")

                        # Skip frames
                    for _ in range(skip_frames):
                        ret, frame = video_capture.read()
                        if not ret:
                             break

                        # Toggle frame processing
                        process_frame = not process_frame

            # Release video capture and close windows
            video_capture.release()
            cv2.destroyAllWindows()

        else:
            st.write("Video surveillance stopped.")