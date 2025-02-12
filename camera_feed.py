from pathlib import Path

import cv2
from ultralytics import YOLO

from detect import LicensePlateDetectorYolo
from ocr import EasyOcrStrategy


class VideoFeedProvider:
    def __init__(self, assets_file_path: Path):
        self._cap = cv2.VideoCapture((assets_file_path / "test_video.mp4").as_posix())
        self._license_plate_detector = LicensePlateDetectorYolo(
            YOLO(assets_file_path / "license_plate_detector.pt"))
        self._ocr_strategy = EasyOcrStrategy()
        self._face_cascade_front = cv2.CascadeClassifier(
            (assets_file_path / 'haarcascade_frontalface_default.xml').as_posix())
        self._face_cascade_profile = cv2.CascadeClassifier(
            (assets_file_path / "haarcascade_profileface.xml").as_posix())

    def get_frame(self):
        if not self._cap.isOpened():
            raise FileNotFoundError()

        ret, frame = self._cap.read()

        if not ret:
            return None

        frame = cv2.cvtColor(frame, code=cv2.COLOR_BGR2RGB)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        ocr = self.label_frame_with_license_number_if_any(frame)
        # self.label_frame_with_faces_if_any(frame)
        return frame, ocr

    def release(self):
        self._cap.release()

    def label_frame_with_license_number_if_any(self, frame):
        detections = self._license_plate_detector.get_licence_place_numbers(frame)
        if detections is None or len(detections) == 0:
            return

        for detection in detections:
            x1, y1, x2, y2, score = detection

            cropped = frame[y1:y2, x1:x2, :]
            ocr = self._ocr_strategy.get_text(cropped)
            if ocr is None:
                continue
            
            if len(ocr) < 10:
                continue
            ocr_new = ocr[-10:]
            
            ocr_new = self.transform_vehicle_number(ocr_new)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 8)
            cv2.putText(frame, "License Number: {}".format(ocr_new), (x1, y1 - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            return ocr_new

    def label_frame_with_faces_if_any(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces1 = self._face_cascade_front.detectMultiScale(gray, scaleFactor=1.1,
                                                           minNeighbors=5,
                                                           minSize=(100, 100))

        for (x, y, w, h) in faces1:
            print("FACE")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 144),
                          2)
    
    def transform_vehicle_number(self, ocr_res: str) -> str:
        # ddcddddddc
        chars = []
        for i in range(len(ocr_res)):
            if i == 2 or i == 9:
                chars.append(self.get_alphabet(ocr_res[i]))
            else:
                chars.append(self.get_digit(ocr_res[i]))
        return "".join(chars)

    def get_alphabet(self, chr: str):
        if chr in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return chr
        
        if chr == "1":
            return "I"
        if chr == "4":
            return "A"
        if chr == "5":
            return "S"
        if chr == "6":
            return "G"
        if chr == "0":
            return "O"
        if chr == "8":
            return "B"
        if chr == "2":
            return "Z"
        
        return "."
    
    def get_digit(self, chr: str):
        if chr in "0123456789":
            return chr
        
        if chr == "I":
            return "1"
        if chr == "A":
            return "4"
        if chr == "S":
            return "5"
        if chr == "G":
            return "6"
        if chr == "O":
            return "0"
        if chr == "B":
            return "8"
        if chr == "Z":
            return "2"
        
        return "."