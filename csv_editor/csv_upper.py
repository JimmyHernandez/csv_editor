import csv
import tkinter as tk
from tkinter import filedialog
import chardet

def select_input_file():
    file_path = filedialog.askopenfilename()
    return file_path

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv")
    return file_path

def process_csv(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    with open(input_file_path, 'r', encoding=encoding) as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            upper_row = [cell.upper() for cell in row]
            writer.writerow(upper_row)

if __name__ == "__main__":
    input_file = select_input_file()
    output_file = select_output_file()
    process_csv(input_file, output_file)