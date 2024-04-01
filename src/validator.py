"""
Validation Scripts

"""

from dataloader import DataLoader
import json
import os

class Validator:
    def __init__(self, gold_label_json, test_json, tool): #tool is a temporary stopgap for bugs with cTAKES
        # Initialize the DataArranger for loading data
        self.data = DataLoader()
        self.tool = tool
        # Load and preprocess data
        with open(gold_label_json, "r") as f:
            self.gold_label = json.load(f)
        
        with open(test_json, "r") as f:
            self.data = json.load(f)

        # Scores
        # Phrase Level
        self.phrase_level_precision = []
        self.phrase_level_recall = []
        self.phrase_level_f_measure = []

        # Token Level
        self.token_level_precision = []
        self.token_level_recall = []
        self.token_level_f_measure = []

        # Attributes
        self.correctly_returned_tokens = []
        self.tokens_in_output = []
        self.tokens_in_gold_standard = []
        self.correctly_returned_phrases = []
        self.phrases_in_output = []
        self.phrases_in_gold_standard = []

        # Analyze the data
        self.iterate()

    def find_matches(self, symptoms_gold_label, symptoms_test):
        # Extract phrases from the data and ground truth
        gold_label_phrases = [phrase.strip().lower() for phrase in symptoms_gold_label]
        output_phrases = [phrase.strip() for phrase in symptoms_test]
        print(gold_label_phrases)
        print(output_phrases)
        # Count the number of phrases in the output and gold standard
        self.phrases_in_output.append(len(output_phrases))
        self.phrases_in_gold_standard.append(len(gold_label_phrases))

        # Extract words from the phrases
        output_words = [word for phrase in output_phrases for word in phrase.split()]
        gold_label_words = [word for phrase in gold_label_phrases for word in phrase.split()]

        # Count the number of tokens in the output and gold standard
        self.tokens_in_output.append(len(output_words))
        self.tokens_in_gold_standard.append(len(gold_label_words))

        # Find common words between output and gold standard
        common_words = set(output_words) & set(gold_label_words)
        self.correctly_returned_tokens.append(len(common_words))

        # Find common phrases between output and gold standard
        common_phrases = set(output_phrases) & set(gold_label_phrases)
        self.correctly_returned_phrases.append(len(common_phrases))

    def iterate(self):
        # Iterate through the data to find matches
        for key in self.gold_label.keys():
            if self.tool=="cTAKES":
                self.find_matches(self.gold_label.get(key, []), self.data.get(key.replace("/", ""), []))
            else:
                self.find_matches(self.gold_label.get(key, []), self.data.get(key, [])) #result of cTAKES breaking with "/"

        # Calculate precision, recall, f1 score at both phrase and token levels
        for index in range(len(self.gold_label)):
            self.phrase_level_precision.append((self.correctly_returned_phrases[index] / self.phrases_in_output[index]))
            self.phrase_level_recall.append((self.correctly_returned_phrases[index] / self.phrases_in_gold_standard[index]))
            
            # Calculate F1 score for phrase level
            if self.phrase_level_precision[-1] + self.phrase_level_recall[-1] == 0:
                self.phrase_level_f_measure.append(0.0)
            else:
                self.phrase_level_f_measure.append((2 * self.phrase_level_precision[-1] * self.phrase_level_recall[-1]) /
                                                   (self.phrase_level_precision[-1] + self.phrase_level_recall[-1]))
           
            self.token_level_precision.append((self.correctly_returned_tokens[index] / self.tokens_in_output[index]))
            self.token_level_recall.append((self.correctly_returned_tokens[index] / self.tokens_in_gold_standard[index]))
           
            # Calculate F1 score for token level
            if self.token_level_precision[-1] + self.token_level_recall[-1] == 0:
                self.token_level_f_measure.append(0.0)
            else:
                self.token_level_f_measure.append((2 * self.token_level_precision[-1] * self.token_level_recall[-1]) /
                                                  (self.token_level_precision[-1] + self.token_level_recall[-1]))

    def print_debug(self):
        # Print debug information
        print(
            self.correctly_returned_tokens,
            self.tokens_in_output,
            self.tokens_in_gold_standard,
            self.correctly_returned_phrases,
            self.phrases_in_output,
            self.phrases_in_gold_standard
        )
    def return_scores(self):
        # Print the calculated scores
        return_string = ""
        return_string += "Phrase Level Precision:"+ format(sum(self.phrase_level_precision) / len(self.phrase_level_precision), ".3f")+"\n"
        return_string += "Phrase Level Recall:"+ format(sum(self.phrase_level_recall) / len(self.phrase_level_recall), ".3f")+"\n"
        return_string += "Token Level Precision:"+ format(sum(self.token_level_precision) / len(self.token_level_precision), ".3f")+"\n"
        return_string += "Token Level Recall:"+ format(sum(self.token_level_recall) / len(self.token_level_recall), ".3f")+"\n"
        return_string += "Phrase Level F1:"+ format(sum(self.phrase_level_f_measure) / len(self.phrase_level_f_measure), ".3f")+"\n"
        return_string += "Token Level F1:"+ format(sum(self.token_level_f_measure) / len(self.token_level_f_measure), ".3f")+"\n"
        return return_string


    def print_scores(self):
        # Print the calculated scores
        print("Phrase Level Precision:", format(sum(self.phrase_level_precision) / len(self.phrase_level_precision), ".3f"))
        print("Phrase Level Recall:", format(sum(self.phrase_level_recall) / len(self.phrase_level_recall), ".3f"))
        print("Token Level Precision:", format(sum(self.token_level_precision) / len(self.token_level_precision), ".3f"))
        print("Token Level Recall:", format(sum(self.token_level_recall) / len(self.token_level_recall), ".3f"))
        print("Phrase Level F1:", format(sum(self.phrase_level_f_measure) / len(self.phrase_level_f_measure), ".3f"))
        print("Token Level F1:", format(sum(self.token_level_f_measure) / len(self.token_level_f_measure), ".3f"))

def return_final_results():
    return_string = ""
    list_of_tools = ["cTAKES", "SciSpaCy"]
    list_of_websites = ["MayoClinic", "ODEMSA", "Wikipedia"]
    for tool in list_of_tools:
        for website in list_of_websites:
            print((tool, website))
            return_string += f"{tool} {website}\n"
            validate = Validator(f"KB_evaluation/{website}/disease_symptom_gt.json", f"KB_results/{tool}/Processed/{website}/disease_symptoms.json", tool)
            return_string += validate.return_scores() + "\n"
            print(return_string)
    print(return_string)


if __name__ == "__main__":
    return_final_results()
