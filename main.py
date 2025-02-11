from pathlib import Path

from ultralytics import YOLO

from camera_feed import VideoFeedProvider
from detect import LicensePlateDetectorOpenCvGeeksForGeeks, LicensePlateDetectorYolo
from ocr import OCR, EasyOcrStrategy


def main():
    video_feed_provider = VideoFeedProvider(
        Path("/home/anmol/Downloads/fauji_gaadi.jpeg"))
    ocr_strategy = EasyOcrStrategy()
    # license_plate_detector = LicensePlateDetectorOpenCvGeeksForGeeks(4100, 15000)
    # model = OCR(modelFile="./assets/binary_128_0.50_ver3.pb",
    #             labelFile="./assets/binary_128_0.50_labels_ver2.txt")

    license_plate_detector = YOLO('./assets/license_plate_detector.pt')
    license_plate_detector_2 = LicensePlateDetectorYolo(license_plate_detector)

    while video_feed_provider.has_next_frame():
        frame = video_feed_provider.get_frame()

        detections = license_plate_detector_2.get_licence_place_numbers(frame)

        if detections is None:
            continue

        if len(detections) == 0:
            continue
        
        for detection in detections:
            ocr = ocr_strategy.get_text(detection[1])
            print("Detected vehicle number: {}, confidence: {}".format(ocr, detection[0]))

        # for i, p in enumerate(license_numbers):
        #     chars_on_plate = license_plate_detector.char_on_plate[i]
        #     recognized_plate, _ = model.label_image_list(chars_on_plate,
        #                                                  imageSizeOuput=128)
        #     
        #     print(recognized_plate)


if __name__ == "__main__":
    main()
