#!/bin/bash

# Check if all required command line arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: cTAKES_HOME INPUT_DIR (of .txt files) TARGET_DIR api_key"
    exit 1
fi

# Assign command line arguments to variables
cTAKES_HOME=$1
INPUT_DIR=$2
TARGET_DIR=$3
API_KEY=$4

# Step 1: Change directory to $CTAKES_HOME/desc/ctakes-clinical-pipeline/desc/collection_processing_engine/
cd "$cTAKES_HOME/bin"

# Step 2: run clinical pipeline, replace with your own API KEY
sh runClinicalPipeline.sh -i $INPUT_DIR  --xmiOut $TARGET_DIR --key $API_KEY

echo "The resulting file will be generated in the output directory ($TARGET_DIR)."