# encode_faces.py
import face_recognition
import os
import pickle

dataset_path = '/home/arham/Desktop/arham/dataset'
encodings_path = './encodings.pickle'
face_encodings = []
labels = []

for person_name in sorted(os.listdir(dataset_path)):
    person_path = os.path.join(dataset_path, person_name)
    image_path = os.path.join(person_path, os.listdir(person_path)[0])  # Assume one image per person

    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0]

    face_encodings.append(encoding)
    labels.append(person_name)

data = {'encodings': face_encodings, 'names': labels}
print(data)
with open(encodings_path, 'wb') as f:
    f.write(pickle.dumps(data))
