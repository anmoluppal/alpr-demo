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
        self.label_frame_with_license_number_if_any(frame)
        self.label_frame_with_faces_if_any(frame)
        return frame

    def release(self):
        self._cap.release()

    def label_frame_with_license_number_if_any(self, frame):
        detections = self._license_plate_detector.get_licence_place_numbers(frame)
        if detections is None or len(detections) == 0:
            return

        for detection in detections:
            x1, y1, x2, y2, score = detection
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 8)

            cropped = frame[y1:y2, x1:x2, :]
            ocr = self._ocr_strategy.get_text(cropped)
            if ocr is None:
                continue

            cv2.putText(frame, "License Number: {}".format(ocr), (x1, y1 - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def label_frame_with_faces_if_any(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces1 = self._face_cascade_front.detectMultiScale(gray, scaleFactor=1.1,
                                                           minNeighbors=5,
                                                           minSize=(100, 100))

        for (x, y, w, h) in faces1:
            print("FACE")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 144),
                          2)
