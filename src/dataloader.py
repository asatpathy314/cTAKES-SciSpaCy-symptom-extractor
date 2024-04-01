import re
import json
import os

class DataLoader():
    def __init__(self):
        pass
   
    def return_json_object(self, input_file_path):
        try:
            with open(input_file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error: {e}")
    
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
            output_file_path = output_file_directory+ dataset+ (disease).replace("/", "")
            with open(output_file_path, "a") as f:
                f.write(re.sub(r'[^\x00-\x7F"]', '', description))
        
    def json_to_text(self, input_file_path, output_file_directory):
        json_object = self.return_json_object(input_file_path)
        for (disease, description) in json_object.items():
            output_file_path = os.path.join(output_file_directory, (disease).replace("/", ""))
            with open(output_file_path, "a") as f:
                description = description.replace("\n", "").replace('"', "").strip()
                f.write(re.sub(r'[^\x00-\x7F"]', '', description))
    
    def xmi_to_json_sign_symptom(self, input_file):
        with open(input_file, "r") as f:
            text = f.read()
            name = f.name
        text_match = re.findall(r'sofaString="(.*?)"', text)[0]
        pattern = re.compile(r'&amp;|&lt;|&gt;|&apos;|&quot;')
        text_match = re.sub(pattern, ' ', text_match)
        symptom_matches = re.findall(r'<textsem:SignSymptomMention (.*?)>', text)
        list_of_symptom_indexes = [(re.findall(r'begin="(.*?)"', item)[0], re.findall(r'end="(.*?)"', item)[0]) for item in symptom_matches] 
        list_of_symptoms = []
        for begin, end in list_of_symptom_indexes:
            list_of_symptoms.append(text_match[int(begin):int(end)])
        
        list_of_symptoms = list(set(map(str.lower, list_of_symptoms)))
        
        return {name.split("/")[-1].replace(".xmi", ""): list_of_symptoms}

    def xmi_to_json_filter(self, input_file, types):
        with open(input_file, "r") as f:
            text = f.read()
            name = f.name
        #regex magic
        text_match = re.findall(r'sofaString="(.*?)"', text)[0]
        pattern = re.compile(r'&amp;|&lt;|&gt;|&apos;|&quot;')
        text_match = re.sub(pattern, ' ', text_match)
        matches = re.findall(r'<textsem:.*?Mention (.*?)>', text)
        umls_concepts = re.findall(r'refsem:UmlsConcept (.*?)>', text)
        print(umls_concepts)
        list_of_indexes = [(re.findall(r'begin="(.*?)"', item)[0], re.findall(r'end="(.*?)"', item)[0], re.findall(r'ontologyConceptArr="(.*?)"', item)[0].split(" ")) for item in matches] 
        list_of_umls = [(re.findall(r'tui="(.*?)"', item)[0], re.findall(r'xmi:id="(.*?)"', item)) for item in umls_concepts]
        print(list_of_indexes)
        print(list_of_umls)
        list_of_entities = []
        
        for begin, end, ont_arr in list_of_indexes:
            for tui, xmi_id in list_of_umls: 
                if xmi_id[0] in ont_arr and tui in types:
                    list_of_entities.append(text_match[int(begin):int(end)])
        
        list_of_entities = list(set(map(str.lower, list_of_entities)))
    
        return {name.split("/")[-1].replace(".xmi", ""): list_of_entities}
    
    def ctakes_to_json(self, input_dir, output_file):
        output_json_dictionary = {}
        for file in os.scandir(input_dir):
            if file.path.endswith(".xmi"):
                output_json_dictionary |= self.xmi_to_json(file.path)
        with open(output_file, "w") as f:
            json.dump(output_json_dictionary, f)
        
    def ctakes_to_json_filtered(self, input_dir, output_file, types):
        output_json_dictionary = {}
        for file in os.scandir(input_dir):
            if file.path.endswith(".xmi"):
                output_json_dictionary |= self.xmi_to_json_filter(file.path, types=types)
        with open(output_file, "w") as f:
            json.dump(output_json_dictionary, f)


if __name__ == "__main__":
    data = DataLoader()
    print(data.xmi_to_json_filter("/Users/as314159265/Code/repos/link-lab/cTAKES-SciSpaCy-symptom-extractor/test/416.9: Chronic obstructive pulmonary disease.xmi"))
    def directory_iterator(input_directory_path, output_directory_path):
        for directory in os.scandir(input_directory_path):
            data.ctakes_to_json(directory.path, os.path.join(output_directory_path, directory.path.split("/")[-1], "disease_symptoms.json"))


