import csv


class getCSVdata():
    def get_data(file_name):
        rows = []
        data_file = open(file_name, 'r')
        reader = csv.reader(data_file)
        next(reader, None)
        for row in reader:
            rows.append(row)
        return rows
