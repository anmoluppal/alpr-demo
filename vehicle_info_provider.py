import csv
from pathlib import Path


class VehicleInfoProvider:
    def __init__(self, file_path: Path):
        self._self_vehicle_details = {}
        self._load(file_path)

    def get_details(self, ocr: str):
        if ocr not in self._self_vehicle_details:
            return None

        return self._self_vehicle_details.get(ocr)

    def _load(self, path: Path):
        with open(path, "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:

                self._self_vehicle_details[row["vehicle_number"]] = {
                    "driver_name": row["driver_name"],
                    "make_and_type": row["make_and_type"],
                    "unit": row["unit"],
                    "color": row["color"]
                }
        
