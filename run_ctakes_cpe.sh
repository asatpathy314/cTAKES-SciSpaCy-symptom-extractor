#!/bin/bash

# Check if all required command line arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: cTAKES_HOME INPUT_JSON_FILE TARGET_DIR API_KEY"
    exit 1
fi

# Assign command line arguments to variables
cTAKES_HOME=$1
INPUT_FILE=$2
TARGET_DIR=$3
API_KEY=$4
CURRENT_DIR=$(pwd)

#Step 1: Generate intermediates
rm -r cTAKES_intermediate
python symptom_extractor_cTAKES.py $INPUT_FILE

# Step 2: Change directory to $CTAKES_HOME/desc/ctakes-clinical-pipeline/desc/collection_processing_engine/
cd "$cTAKES_HOME/bin"

# Step 3: run clinical pipeline, replace with your own API KEY
sh runClinicalPipeline.sh -i "$CURRENT_DIR/cTAKES_intermediate"  --xmiOut $TARGET_DIR --key $API_KEY

cd $CURRENT_DIR

rm -r cTAKES_intermediate

echo "The resulting file will be generated in the output directory ($TARGET_DIR)."

