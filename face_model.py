import cv2
import streamlit as st

def main():
    st.title("autometic attendence")
    
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    cap.release()

if __name__ == "__main__":
    main()
