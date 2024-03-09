#!/bin/bash

# Check if all required command line arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: cTAKES_home target_directory input_directory"
    exit 1
fi

# Assign command line arguments to variables
cTAKES_HOME=$1
TARGET_DIR=$2
INPUT_DIR=$3

# Step 1: Change directory to $CTAKES_HOME/desc/ctakes-clinical-pipeline/desc/collection_processing_engine/
cd $cTAKES_HOME/desc/ctakes-clinical-pipeline/desc/collection_processing_engine/

# Step 2: Copy test_plaintext.xml to another file (e.g., "test_plaintext_test.xml").
cp test_plaintext.xml test_plaintext_test.xml

# Step 3: Edit "test_plaintext_test.xml" to set the input directory
sed -e "s|<name>InputDirectory</name><value>.*</value>|<name>InputDirectory</name><value>$INPUT_DIR</value|" test_plaintext_test.xml > test_plaintext_test.xml

# Step 4: Edit "test_plaintext_test.xml" to set the output directory
sed '' -e "s|<name>OutputDir</name><value>.*</value>|<name>OutputDir</name><value>$OUTPUT_DIR</value>|" test_plaintext_test.xml > test_plaintext_test.xml


# Step 5: Save "test_plaintext_test.xml" and change directory to $CTAKES_HOME/bin
cd $cTAKES_HOME/bin

# Step 6: Copy runctakesCPE.sh to another file (e.g., "runctakesCPE_CLI.sh").
cp runctakesCPE.sh runctakesCPE_CLI.sh

# Step 7: Edit "runctakesCPE_CLI.sh"; replace the last line ("java ...") with the provided line
sed -i "s|java.*|java -Dctakes.umls_apikey=b3874b4b-173f-4744-b984-bfc20f07c643  -cp $CTAKES_HOME/lib/*:$CTAKES_HOME/desc/:$CTAKES_HOME/resources/ -Dlog4j.configuration=file:$CTAKES_HOME/config/log4j.xml -Xms2g -Xmx3g org.apache.uima.examples.cpe.SimpleRunCPE $CTAKES_HOME/desc/ctakes-clinical-pipeline/desc/collection_processing_engine/test_plaintext_test.xml"

# Step 10: Run "runctakesCPE_CLI.sh"
sh runctakesCPE_CLI.sh

cd ..

echo "cTAKES CPE has started running under command line mode."
echo "The resulting file will be generated in the output directory ($TARGET_DIR/note.txt.xml)."
