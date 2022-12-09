import sys

from utils.to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("you should provide 1-2 arguments: <input_file> <output_file>")
        exit(0)

    converter = CSVtoXMLConverter(sys.argv[1])
    output_str = converter.to_xml_str()

    if len(sys.argv) <= 2:
        print(output_str)
    else:
        file = open(sys.argv[2], "w")
        file.write(output_str)
        file.close()
