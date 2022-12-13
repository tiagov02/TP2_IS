import os
import time
import uuid

import os
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from utils.to_xml_converter import CSVtoXMLConverter

CSV_INPUT_PATH = "/csv"
XML_OUTPUT_PATH = "/shared/output"


def get_converted_files():
    # !TODO: you should retrieve from the database the files that were already converted before
    return []

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name():
    return f"/shared/output/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())


class CSVHandler(FileSystemEventHandler):
    def __init__(self):
        self._converted_files = get_converted_files()

    def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in self._converted_files:
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate an unique file name for the XML file
        xml_path = generate_unique_file_name()

        # we do the conversion
        # !TODO: once the conversion is done, we should updated the converted_documents tables
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # !TODO: we should store the XML document into the imported_documents table
        # !FIXME: instead of updating the local cache for converted files, we should reload them from the database
        # !FIXME: in the next iteration
        self._converted_files.append(csv_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            self.convert_csv(event.src_path)


if __name__ == "__main__":
    print("main")
    observer = Observer()
    event_handler = CSVHandler()
    observer.schedule(event_handler, path=CSV_INPUT_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
