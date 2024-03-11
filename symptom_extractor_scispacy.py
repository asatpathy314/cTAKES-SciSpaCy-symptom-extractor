"""
SciSpaCy symptom extractor.
"""

from dataloader import DataLoader
import scispacy
import spacy
import json
import re

class SciSpacyExtractor():
    def __init__(self, model_name):
        # Initialize the SciSpacyEntityExtractor with a specified SpaCy model and a data_arranger instance
        self.nlp = spacy.load(model_name)  # Load the specified SpaCy model
        self.model_name = model_name
    def return_symptoms_as_list(self, json_object):
        docs = []
        for note in json_object.values():
            doc = self.nlp(note)
            docs.append(doc)
             
    def return_symptoms_as_json(self, json_object, file_to_write):
        list_of_disease_symptoms = {}
        for (disease, text) in json_object.items():
            doc = self.nlp(text)
            list_of_disease_symptoms |= {disease: list({re.sub(r'[^\w\s]', '', ent.text).lower() for ent in doc.ents})}
        #Write to file
        with open(file_to_write, "w") as file:
            json.dump(list_of_disease_symptoms, file)


data = DataLoader()
scispacy_extractor = SciSpacyExtractor("en_ner_bc5cdr_md")
scispacy_extractor.return_symptoms_as_json(data.return_json_object("/Users/as314159265/Code/repos/cTAKES-SciSpaCy-symptom-extractor/KB_evaluation/ODEMSA/disease_content.json"), 
                                           file_to_write="/Users/as314159265/Code/repos/cTAKES-SciSpaCy-symptom-extractor/KB_results/SciSpaCy/ODEMSA/disease_symptoms.json")
