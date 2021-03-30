"""Modul containing help functions."""
import csv
import os
import logging

ENCODING = "utf-8"
DELIMINER = ";"
NEWLINE = ""


def killer(application: str) -> None:
    """Function for killing running processes."""
    os.system(f"taskkill /f /im {application}")
    logging.info(f"Application {application} sucessefully killed.")


def write_csv(file_name: str, input: list) -> None:
    """Function for writing into csv file."""
    with open(file_name, mode="a", encoding=ENCODING, newline=NEWLINE) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=DELIMINER)
        csv_writer.writerow(input)


def read_txt(file: str) -> str:
    """Function reads from txt file."""
    with open(file) as f:
        lines = f.readlines()
        return lines[0]