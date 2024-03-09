"""
Uses a variety of command line tools to perform batch processing of 
clinical text documents for the purpose of symptom extraction. 
"""
import os
import subprocess
from dataloader import DataLoader

class cTAKESExtractor:
    def __init__(self, cTAKES_home, target_directory, input_file_path):
        self.cTAKES_home = cTAKES_home
        self.target_directory = target_directory
        self.input_file_path = input_file_path
        self.dataloader = DataLoader()
    
    def process_file(self):
        try:
            cTAKES_intermediate = os.mkdir("cTAKES_intermediate")
        except FileExistsError:
            print("Warning: File already Exists")
        self.dataloader.json_to_text(input_file_path=self.input_file_path, output_file_directory="cTAKES_intermediate")
        subprocess.run(f"sh /Users/asatpathy/Documents/Code/cTAKES-SciSpacy-symptom-extractor/run_ctakes_cpe.sh {self.cTAKES_home} {self.target_directory} cTAKES_intermediate", shell=True)

ctakes = cTAKESExtractor(cTAKES_home="/Users/asatpathy/apache-ctakes-4.0.0.1",
                         target_directory="/Users/asatpathy/Documents/Code/cTAKES-SciSpacy-symptom-extractor/KB_results/cTAKES",
                         input_file_path="/Users/asatpathy/Documents/Code/cTAKES-SciSpacy-symptom-extractor/KB_evaluation/Wikipedia/disease_content.json")     
    
ctakes.process_file()
