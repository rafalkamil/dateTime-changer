from datetime import datetime
import os
from tkinter import Tk, filedialog

def fix_date_format(date_str, time_str):
    """
        Function takes two strings, date and time in potentially wrong formats, parse them using date in 'm/d/y' format
        and time in 'h:m:s AM/PM' format. If failed, tries an alt format with date in 'd/m/y' format and time in
        'h:m:s' format.
        If parsing succeeded in both formats, then formats date to 'd/m/y' and time to 'h:m:s', other-ways strings
        are returned without modification.
    """
    try:
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        time_obj = datetime.strptime(time_str, '%I:%M:%S %p').time()
    except ValueError:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        time_obj = datetime.strptime(time_str, '%H:%M:%S').time()

    formatted_date = date_obj.strftime('%d/%m/%Y')
    formatted_time = time_obj.strftime('%H:%M:%S')

    return formatted_date, formatted_time

def process_records(records):
    """
        Function takes a list of string records as input, where values are separated by tabs.
        It processes each record by extracting the date and time from first two values, formatting
        them using `fix_date_format` function.
        Processed records are stored in list, where date and time have been formatted, other values are unchanged.
        """
    processed_records = []

    for record in records:
        parts = record.strip().split('\t')
        date_str, time_str = parts[0], parts[1]
        formatted_date, formatted_time = fix_date_format(date_str, time_str)
        formatted_record = f"{formatted_date}\t{formatted_time}\t" + '\t'.join(parts[2:])
        processed_records.append(formatted_record)

    return processed_records

def read_text_file(file_path):
    """
    Reads content of file and returns it as list of lines.
    """
    with open(file_path, 'r') as file:
        text_content = file.readlines()
    return text_content

def write_text_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content[0].strip() + '\n')
        file.write('\n'.join(content[1:]))


def process_and_write_file(input_file_path, output_file_path):
    """
        Function reads content of the input file.
        It processes records by extracting date and time, then formats them.
        Processed records are then written to output file.
        The function assumes that first line is header, and rest are data records.
    """
    text_content = read_text_file(input_file_path)

    header = text_content[0]
    records = text_content[1:]
    processed_records = process_records(records)

    formatted_content = [header] + processed_records
    write_text_file(output_file_path, formatted_content)

def process_multiple_files(input_directory, output_directory):
    """
        Processes multiple files in input directory, writes formatted results to output directory.
        For each file in input directory with a '.bin' extension, calls 'process_and_write_file' function.
    """
    if not os.path.exists(input_directory) or not os.path.exists(output_directory):
        print("Directories not exist!.")
        return

    for filename in os.listdir(input_directory):
        if filename.endswith(".bin"):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, f"Formatted_{filename}")
            process_and_write_file(input_file_path, output_file_path)


def ask_directory(title):
    root = Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(title=title)

    return folder_path


def main():
    input_directory = ask_directory("Select Input Directory")
    output_directory = ask_directory("Select Output Directory")

    if not input_directory or not output_directory:
        print("Please select both input and output directories.")
        return

    process_multiple_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
