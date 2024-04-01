"""
SciSpaCy symptom extractor.
"""
from dataloader import DataLoader
import scispacy
import spacy
import json
import re
import os

class LinkerNotInitialized(Exception):
    "Raised when ScispaCy linker is not intialized and user performs action that requires linker."
    def __init__(self, message="ScispaCy linker not initialized."):
        self.message = message
        super().__init__(self.message)

class SciSpacyExtractor():
    def __init__(self, model_name):
        # Initialize the SciSpacyEntityExtractor with a specified SpaCy model and a data_arranger instance
        self.nlp = spacy.load(model_name)  # Load the specified SpaCy model
        self.model_name = model_name
        self.is_linker_initalized = False
    
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
    
    def initalize_umls_pipeline(self):
        self.nlp.add_pipe("scispacy_linker", config={"linker_name": "umls"})
        self.is_linker_initalized = True

    def return_as_json_filter(self, json_object, types, file_to_write):
        if not self.is_linker_initalized:
            raise LinkerNotInitialized()
        list_of_attributes = {}
        linker = self.nlp.get_pipe("scispacy_linker")
        for (disease, text) in json_object.items():
            filtered_ents = []  # Initialize inside the loop
            doc = self.nlp(text)
            for ent in doc.ents:
                if (ent._.kb_ents):
                    umls_ent = ent._.kb_ents[0]
                    list_of_types = linker.kb.cui_to_entity[umls_ent[0]].types
                    for umls_type in list_of_types:
                        if umls_type in types:
                            filtered_ents.append(ent)
            list_of_attributes[disease] = list({re.sub(r'[^\w\s]', '', ent.text).lower() for ent in filtered_ents})
        # Write to file
        with open(file_to_write, "w") as f:
            json.dump(list_of_attributes, f)
 