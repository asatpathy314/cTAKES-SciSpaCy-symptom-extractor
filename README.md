# cTAKES-SciSpaCy-symptom-extractor 

**Description**: This program is designed to extract and analyze symptoms from clinical text documents using two different tools: cTAKES and SciSpaCy. The program includes scripts for data loading, processing, extraction, and validation. It currently supports three different websites' datasets: MayoClinic, ODEMSA, and Wikipedia.

## Table of Contents

- [Files](#files)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Instructions](#instructions)
- [Contributing](#contributing)
- [License](#license)

## Files

### 1. run_ctakes_cpe.sh
A shell script to run the cTAKES clinical pipeline on a specified input directory of text files. It requires cTAKES_HOME, INPUT_DIR, TARGET_DIR, and an API_KEY as command line arguments.

### 2. dataloader.py
A Python script containing a `DataLoader` class with methods for converting various data formats, such as JSON and XMI. It also includes functionality for organizing data into specific directories.

### 3. symptom_extract_cTAKES.py
A Python script attempting to use the cTAKES pipeline for symptom extraction. Currently disabled due to an issue with the shell command.

### 4. symptom_extractor_scispacy.py
A Python script using SciSpaCy to extract symptoms. It converts JSON data to text and then extracts symptoms using a specified SciSpaCy model.

### 5. validator.py
A Python script containing a `Validator` class to compare the output of the symptom extraction tools (cTAKES and SciSpaCy) against gold standard labels. It calculates precision, recall, and F1 scores at both the phrase and token levels.

## Usage

1. Ensure that cTAKES is properly installed and configured.
2. Install required Python dependencies using `pip install -r requirements.txt`.
3. Run the `run_ctakes_cpe.sh` script to process the input clinical text files using cTAKES. Provide the required command line arguments: cTAKES_HOME, INPUT_DIR, TARGET_DIR, and API_KEY.
4. Run the `symptom_extractor_scispacy.py` script to extract symptoms using SciSpaCy. Adjust the input file path and output file path as needed.
5. Run the `validator.py` script to compare the output of cTAKES and SciSpaCy against gold standard labels. Provide the paths to the gold label JSON, test JSON, and the tool being validated (either "cTAKES" or "SciSpaCy").

## Dependencies

- cTAKES (clinical Text Analysis and Knowledge Extraction System)
- Python 3.x
- [SciSpaCy](https://allenai.github.io/scispacy/)

## Instructions

1. Ensure cTAKES is correctly installed and configured.
2. Install Python dependencies using `pip install -r requirements.txt`.
3. Execute the `run_ctakes_cpe.sh` script to process clinical text files with cTAKES.
4. Run the `symptom_extractor_scispacy.py` script to extract symptoms using SciSpaCy.
5. Validate the results using the `validator.py` script, providing the necessary input paths.

## Contributing

Feel free to contribute to the project by submitting bug reports, feature requests, or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).


