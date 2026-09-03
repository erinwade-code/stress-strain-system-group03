from datetime import datetime
import json
import csv
from pathlib import Path

class StressStrainTest:
    def __init__(self, material_name: str, force: float, area: float, orig_len: float, delta_len: float):
        self.material_name = material_name
        self.force = force
        self.area = area
        self.orig_len = orig_len
        self.delta_len = delta_len
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TestCollection:
    def __init__(self):
        self.tests = []

    def add_test(self, test: StressStrainTest):
        self.tests.append(test)

    def save_to_json(self, filename="results.json"):
        data = [t.__dict__ for t in self.tests]
        Path(filename).write_text(json.dumps(data, indent=4))

    def export_to_csv(self, filename="results.csv"):
        if not self.tests:
            return
        keys = self.tests[0].__dict__.keys()
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows([t.__dict__ for t in self.tests])
        