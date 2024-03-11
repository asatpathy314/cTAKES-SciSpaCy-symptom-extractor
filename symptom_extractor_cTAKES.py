"""
Uses a variety of command line tools to perform batch processing of 
clinical text documents for the purpose of symptom extraction. 

The usage of this file is to generate intermediates, the shell script
must be run from a shell utilizing the provided arguments in the commented
section of script of run_ctakes_cpe.sh.
"""
import os
import subprocess
from dataloader import DataLoader

class cTAKESExtractor:
    def __init__(self, cTAKES_home, input_file_path): #add target_dir for future developers
        self.cTAKES_home = cTAKES_home
        #self.target_directory = target_directory
        self.input_file_path = input_file_path
        self.dataloader = DataLoader()
    
    def generate_intermediate(self):
        try:
            cTAKES_intermediate = os.mkdir("cTAKES_intermediate")
        except FileExistsError:
            print("Warning: File already Exists")
        self.dataloader.json_to_text(input_file_path=self.input_file_path, output_file_directory="cTAKES_intermediate")
"""
This command doesn't work despite the .sh file functioning perfectly fine on its own. If anyone can figure it out I would be 
very thankful.

    def process_file(self):
        self.generate_intermediate()
        #print(f"sh run_ctakes_cpe.sh {self.cTAKES_home} {self.target_directory} cTAKES_intermediate")
        os.system(f"sh run_ctakes_cpe.sh {self.cTAKES_home} {self.target_directory} cTAKES_intermediate")
        subprocess.run(f"rm -r cTAKES_intermediate", shell=True)

"""

if __name__ == "__main__":
    ctakes = cTAKESExtractor(cTAKES_home="",
                            input_file_path="")     
    ctakes.generate_intermediate()