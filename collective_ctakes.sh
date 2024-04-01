UMLS_API_KEY = #INSERT UMLS API KEY HERE

declare -a arr1=("Wikipedia" "MayoClinic" "ODEMSA")
declare -a arr2=("disease_treatment_content.json")

for file in "${arr2[@]}"; 
do 
    for dir in "${arr1[@]}" 
    do
    sh "run_ctakes_cpe.sh" "/Users/as314159265/Code/apache-ctakes-4.0.0.1" "Data/${dir}/${file}" "/Users/as314159265/Code/repos/link-lab/cTAKES-SciSpaCy-symptom-extractor/KB_Treatment_Results/raw/cTAKES_treatment/${dir}" $UMLS_API_KEY
    done
    #sh ../run_ctakes_cpe.sh /Users/as314159265/Code/apache-ctakes-4.0.0.1 $i
done

