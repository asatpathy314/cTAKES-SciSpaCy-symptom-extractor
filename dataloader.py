import re
import json
import os

class DataLoader():
    def __init__(self):
        pass
   
    def return_json_object(self, input_file_path):
        try:
            with open(input_file_path, "r") as file:
                text = file.read()
        except Exception as e:
            print(f"Error: {e}")
        json_object = json.loads(text)
        return json_object
    
    def json_to_text_in_dir(self, input_file_path, output_file_directory):
        """
        Creates a new directory within existing output directory with a dataset subfolder
        containing all disease descriptions with the file names as the disease name
        """
        try:
            dataset = input_file_path.split("/")[-2]
            dir = os.path.join(output_file_directory, dataset)
            os.mkdir(dir)
        except FileExistsError as e:
            print("Error: Directory already exists")
        
        json_object = self.return_json_object(input_file_path)
        
        for (disease, description) in json_object.items():
            output_file_path = os.path.join(output_file_directory, dataset, (disease + ".txt").replace("/", ""))
            with open(output_file_path, "a") as f:
                f.write(description)
        
    def json_to_text(self, input_file_path, output_file_directory):
        json_object = self.return_json_object(input_file_path)
        for (disease, description) in json_object.items():
            output_file_path = os.path.join(output_file_directory, (disease + ".txt").replace("/", ""))
            with open(output_file_path, "a") as f:
                f.write(description)

