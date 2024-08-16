import csv

class ExtractionService:
    @staticmethod
    def extract_from_file(file_path):
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                data.append(row)
        return data