import numpy as np
import cv2


class FacialRecognition:
    def __init__(self, ):
        self.face_detection = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.settings = {
            'scaleFactor': 1.3,
            'minNeighbors': 5,
            'minSize': (50, 50)
        }

        # we can change this to whatever the dataset is scaled to
        self.face_scale = (48, 48) 
    
    def run_detection_bytes(self, imgdata):
        as_array = np.frombuffer(imgdata, dtype=np.uint8)

        img = cv2.imdecode(as_array, flags=cv2.IMREAD_GRAYSCALE)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = self.face_detection.detectMultiScale(
            img, **self.settings)

        for x, y, w, h in detected:
            cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
            cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
            face = img[y+5:y+h-5, x+20:x+w-20]
            face = cv2.resize(face, self.face_scale)
            face = face/255.0
            
            # save output for testing
            cv2.imwrite('test.jpg', img)
            return face
        
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
    recognizer = FacialRecognition()
    recognizer.run_loop()
