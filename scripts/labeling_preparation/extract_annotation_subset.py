# EthioMart_NER_Project/scripts/labeling_prep/extract_annotation_subset.py

import json
import os
import sys

# Add the project root to the Python path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config # Import configuration from config.py

INPUT_JSON_FILE = os.path.join(config.PREPROCESSED_DATA_DIR, config.PREPROCESSED_MESSAGES_FILE)
SUBSET_OUTPUT_JSON_FILE = os.path.join(config.LABELED_DATA_DIR, config.ANNOTATION_SUBSET_FILE)
NUM_MESSAGES_TO_LABEL = config.NUM_MESSAGES_TO_LABEL

# Ensure output directory exists
os.makedirs(os.path.dirname(SUBSET_OUTPUT_JSON_FILE), exist_ok=True)

def extract_subset(input_path, output_path, num_messages):
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found. Please ensure your preprocessed JSON exists.")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{input_path}': {e}")
        return

    if len(data) == 0:
        print("Error: Input JSON file is empty. Cannot extract a subset.")
        return

    # Take the first N messages, or fewer if the dataset is smaller
    subset = data[:min(num_messages, len(data))]

    # Prepare data for annotation tool (e.g., Doccano expects 'text' key)
    # We'll also keep the original 'id' for traceability
    annotation_ready_subset = []
    for msg in subset:
        annotation_ready_subset.append({
            "id": msg.get("id"), # Keep original message ID for traceability
            "text": msg.get("cleaned_text", "") # Use cleaned_text for labeling
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(annotation_ready_subset, f, ensure_ascii=False, indent=4)
    
    print(f"Extracted {len(annotation_ready_subset)} messages to '{output_path}' for annotation.")
    print("Please proceed to setting up Doccano and importing this file for manual labeling.")

if __name__ == '__main__':
    extract_subset(INPUT_JSON_FILE, SUBSET_OUTPUT_JSON_FILE, NUM_MESSAGES_TO_LABEL)