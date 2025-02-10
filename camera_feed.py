from pathlib import Path

import cv2


class VideoFeedProvider:
    def __init__(self, video_file_path: Path):
        self._video_file_path = video_file_path
        self._total_frame_count = 1
        self._curr_frame_idx = 0

    def has_next_frame(self):
        return self._curr_frame_idx < self._total_frame_count

    def get_frame(self):
        self._curr_frame_idx += 1
        return cv2.imread(self._video_file_path.as_posix())
