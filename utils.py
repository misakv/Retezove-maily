"""Modul containing help functions."""
import csv
import logging
import os
import os.path
from typing import Generator

ENCODING = "utf-8"
DELIMINER = ";"
NEWLINE = "\n"


def killer(application: str) -> None:
    """Function for killing running processes."""
    os.system(f"taskkill /f /im {application}")
    logging.info(f"Application `{application}` sucessefully killed.")


def write_csv(file_name: str, input: list) -> None:
    """Function for writing into csv file."""
    with open(file_name, mode="a", encoding=ENCODING, newline=NEWLINE) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=DELIMINER)
        csv_writer.writerow([input][0])


def generate_txt(file_name: str) -> Generator:
    """Function generetes entries from csv file."""
    with open(file_name, mode="r") as file:
        rows_read = file.readlines()
        rows = rows_read[0].split(DELIMINER)
        for row in rows:
            yield row


def read_txt(file_name: str) -> str:
    """Function reads from txt file."""
    with open(file_name) as file:
        lines = file.readlines()
        return lines[0]


def write_txt(file_name: str, input: str) -> None:
    """Function appends into txt file."""
    with open(file_name, "a") as file:
        file.write(input + DELIMINER)


def remove(file_name: str) -> None:
    """Function for removing a file."""
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print(f"'{file_name}' does not exist!")
