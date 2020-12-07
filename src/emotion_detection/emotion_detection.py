import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

class EmotionDetector:
    def __init__(self, ):
        self.model = Sequential()

        self.model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        self.model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(7, activation='softmax'))
        self.model.load_weights('./src/emotion_detection/model.h5')

        self.face_detection = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.settings = {
            'scaleFactor': 1.3,
            'minNeighbors': 5,
            'minSize': (50, 50)
        }

        self.emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

        self.face_scale = (48, 48) 
    
    def run_detection_bytes(self, imgdata):
        as_array = np.frombuffer(imgdata, dtype=np.uint8)

        img = cv2.imdecode(as_array, flags=cv2.IMREAD_GRAYSCALE)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = self.face_detection.detectMultiScale(
            img, **self.settings)

        for x, y, w, h in detected:
            cv2.rectangle(img, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = img[y:y + h, x:x + w]
            face = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            
            prediction = self.model.predict(face)
            maxindex = int(np.argmax(prediction))

            # test
            cv2.putText(img, self.emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # save output for testing
            cv2.imwrite('test.jpg', img)

            return self.emotion_dict[maxindex], prediction[0][maxindex].item()
        
        return None


    def run_detection_loop(self):
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

        while True:
            _, img = camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            detected = self.face_detection.detectMultiScale(
                gray, **self.settings)

            for x, y, w, h in detected:
                cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
                cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
                face = gray[y+5:y+h-5, x+20:x+w-20]
                face = cv2.resize(face, self.face_scale)
                face = face/255.0

                yield face

            cv2.imshow('Facial Expression', img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            if cv2.waitKey(5) != -1:
                break

        camera.release()
        cv2.destroyAllWindows()


# some tests
if __name__ == "__main__":
    recognizer = EmotionDetector()
    recognizer.run_loop()
