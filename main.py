import cv2
import face_recognition
import pickle
import datetime
import csv

# Load known faces
with open('encodings.pickle', 'rb') as f:
    data = pickle.load(f)

# Initialize attendance record with current date and time for absent students
attendance = {name: {'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'attendance': 'Absent'} for name in data['names']}

def capture_and_recognize(frame):
    # Convert the frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(data['encodings'], face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(data['encodings'], face_encoding)
        if len(face_distances) > 0:
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = data['names'][best_match_index]

        # Mark attendance
        if name != "Unknown":
            attendance[name]['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            attendance[name]['attendance'] = 'Present'
            print(f"Marked {name} present at {attendance[name]['timestamp']}")

        # Draw rectangle around face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Captured Image', frame)

def save_attendance():
    # Save attendance to a CSV file
    with open('attendance.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'timestamp', 'attendance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for name, info in attendance.items():
            writer.writerow({'name': name, 'timestamp': info['timestamp'], 'attendance': info['attendance']})
    print("Attendance saved successfully.")

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'space' to capture an image and perform face recognition.")
print("Press 's' to save the attendance to a CSV file.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    # Display the live video feed
    cv2.imshow('Video', frame)

    # Wait for user input
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):  # Space key to capture image
        capture_and_recognize(frame)
    elif key == ord('s'):  # 's' key to save attendance
        save_attendance()
    elif key == ord('q'):  # 'q' key to quit
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
