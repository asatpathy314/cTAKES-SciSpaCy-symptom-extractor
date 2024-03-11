"""
Uses a variety of command line tools to perform batch processing of 
clinical text documents for the purpose of symptom extraction. 

Usage of the file is:
python symptom_extractor_cTAKES.py path/to/input/file
"""
import os
import sys
from dataloader import DataLoader

class cTAKESExtractor:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.dataloader = DataLoader()
        print(input_file_path)
    
    def generate_intermediate(self):
        try:
            cTAKES_intermediate = os.mkdir("cTAKES_intermediate")
        except FileExistsError:
            print("Warning: File already Exists")
        self.dataloader.json_to_text(input_file_path=self.input_file_path, output_file_directory="cTAKES_intermediate")

if __name__ == "__main__":
    ctakes = cTAKESExtractor(input_file_path=sys.argv[1])     
    ctakes.generate_intermediate()