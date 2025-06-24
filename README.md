EthioMart Named Entity Recognition (NER) Project
Project Overview
The EthioMart NER Project aims to revolutionize FinTech decision-making in Ethiopia by structuring previously decentralized e-commerce data from Telegram channels. The core problem this project addresses is the inaccessibility of valuable merchant data—such as product listings, pricing, and sales locations—scattered across various informal Telegram groups. By consolidating and analyzing this data, EthioMart seeks to empower smart FinTech solutions, particularly in the realm of vendor micro-lending. The ability to accurately extract key entities will enable a data-driven "vendor scorecard" that assesses merchant activity and reliability, fostering financial inclusion for small and medium-sized e-commerce enterprises.

Project Structure
EthioMart_NER_Project/
├── .gitignore                # Specifies intentionally untracked files to ignore by Git
├── README.md                 # Project overview, setup, and usage instructions
├── requirements.txt          # Lists all Python dependencies
├── config.py                 # Stores sensitive API credentials and shared configurations
├── venv/                     # Python Virtual Environment (local to the project, recommended for dependency isolation)
├── data/                     # Centralized directory for all project data assets
│   ├── raw_telegram_data/    # Stores Telethon session files and raw, unprocessed scrape output (if any)
│   ├── preprocessed_data/    # Contains cleaned and structured textual data
│   │   ├── all_telegram_ecommerce_messages.json    # Combined raw text + metadata from scraper
│   │   └── preprocessed_amharic_ecommerce_messages.json # Fully preprocessed data ready for labeling
│   ├── labeled_data/         # Stores data specifically for labeling and its annotated output
│   │   ├── annotation_subset.json       # Subset of messages prepared for manual annotation
│   │   └── labeled_data.conll           # The final manually annotated data in CoNLL-2003 format
│   └── (optional) media/     # Placeholder for media files if downloading is enabled in the future
├── scripts/                  # Houses all Python source code for various project tasks
│   ├── scraper/              # Contains the Telegram data ingestion script
│   │   └── telegram_scraper.py
│   ├── preprocessing/        # Contains the Amharic text preprocessing script
│   │   └── amharic_preprocessing.py
│   ├── labeling_prep/        # Contains scripts to prepare data for annotation
│   │   ├── extract_annotation_subset.py
│   │   └── manual_conll_labeler.py
│   ├── model_training/       # Directory for Task 3 (model fine-tuning) scripts
│   │   └── (e.g.) train_ner_model.py
│   └── analytics/            # For Task 6 (Vendor Scorecard) and other analytics scripts
│       └── (e.g.) vendor_scorecard.py
├── docs/                     # Stores project documentation and reports
│   ├── Interim_Report_EthioMart.pdf # Comprehensive project interim report
│   └── Annotation_Guidelines.md     # Detailed rules and examples for NER entity labeling
└── notebooks/                # Optional: Jupyter notebooks for exploratory data analysis (EDA) or prototyping
    ├── Task3_FineTune_NER_Model.ipynb # Notebook for fine-tuning a single NER model
    ├── Task4_Model_Comparison.ipynb   # Notebook for comparing multiple NER models
    ├── Task5_Model_Interpretability.ipynb # Notebook for LIME and SHAP interpretability
    └── Task6_FinTech_Vendor_Scorecard.ipynb # Notebook for building the vendor scorecard

Setup Instructions
Follow these steps to set up the project environment and prepare for data processing:

Clone the repository:

git clone <your-repo-link-here> # **IMPORTANT: Replace with your actual GitHub repo URL**
cd EthioMart_NER_Project

Create a Python Virtual Environment:
It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.

python3 -m venv venv

Activate the Virtual Environment:

macOS / Linux:

source venv/bin/activate

Windows (Command Prompt):

venv\Scripts\activate.bat

Windows (PowerShell):

.\venv\Scripts\Activate.ps1

(You will need to activate this environment in each new terminal session you use for the project.)

Install Dependencies:
Install all required Python packages listed in requirements.txt.

pip install -r requirements.txt

Troubleshooting TimeoutError during pip install doccano (or other large packages):
If you encounter ReadTimeoutError (especially for numpy or pandas dependencies of Doccano), try increasing pip's timeout:

pip install doccano --timeout 1000
# If it still fails, try installing numpy/pandas separately first:
# pip install numpy --timeout 1000
# pip install pandas --timeout 1000
# pip install doccano --timeout 1000

You can also try clearing pip's cache: pip cache purge.

Configure Telegram API Credentials:

Obtain API Credentials:

Go to my.telegram.org/apps.

Log in with your Telegram phone number.

Click on "API development tools".

Fill in the "App title" and "Short name" (e.g., "EthioMart Scraper").

You will receive your api_id (an integer) and api_hash (a string). Keep these confidential.

Create/Edit config.py:

Open the config.py file located in the root directory (EthioMart_NER_Project/config.py).

Replace the placeholder values for API_ID, API_HASH, and PHONE_NUMBER with your actual credentials.

Ensure your PHONE_NUMBER is in international format (e.g., '+251912345678').

Running the Project Scripts
Ensure your virtual environment is activated before running any scripts.

Task 1: Data Ingestion and Preprocessing
Run the Telegram Scraper (scripts/scraper/telegram_scraper.py):

Purpose: Fetches messages and metadata from specified Telegram e-commerce channels.

Before running: Open scripts/scraper/telegram_scraper.py and update the CHANNELS list with the specific Telegram channel usernames or links you wish to scrape (e.g., @helloomarketethiopia).

Execution:

python scripts/scraper/telegram_scraper.py

Output: This script will create a session file in data/raw_telegram_data/ and save all collected text messages and their metadata (including media presence, but no actual media files) into a single JSON file: data/preprocessed_data/all_telegram_ecommerce_messages.json.

Run the Amharic Preprocessing Script (scripts/preprocessing/amharic_preprocessing.py):

Purpose: Cleans and normalizes the raw Amharic text collected by the scraper.

Before running: Open scripts/preprocessing/amharic_preprocessing.py.

Review the AMHARIC_STOP_WORDS set: For NER, words like "ብር" (Birr) and numbers are crucial entities for PRICE and PRODUCT_NAME. Ensure "ብር" is NOT included in the AMHARIC_STOP_WORDS list (it is commented out by default in the provided list).

Confirm that the remove_numbers(text) function call within clean_amharic_text is commented out if you want to retain numbers for PRICE or PRODUCT_NAME entities (recommended for e-commerce NER).

Execution:

python scripts/preprocessing/amharic_preprocessing.py

Output: This script reads data/preprocessed_data/all_telegram_ecommerce_messages.json, applies the defined preprocessing steps to the message field, and adds a new cleaned_text field to each message entry. The enhanced data is saved to data/preprocessed_data/preprocessed_amharic_ecommerce_messages.json.

Task 2: Data Labeling Preparation
Extract Annotation Subset (scripts/labeling_prep/extract_annotation_subset.py):

Purpose: Prepares a smaller, manageable subset of preprocessed messages specifically for manual annotation.

Execution:

python scripts/labeling_prep/extract_annotation_subset.py

Output: This will create data/labeled_data/annotation_subset.json containing the first 30-50 messages (or fewer if the dataset is smaller) from your preprocessed_amharic_ecommerce_messages.json, with only id and text (cleaned text) fields.

Perform Manual Labeling (scripts/labeling_prep/manual_conll_labeler.py):

Purpose: Manually label the extracted subset of messages directly in the terminal, outputting to CoNLL format. This bypasses web-based annotation tools for simplicity.

Before running: Ensure your data/labeled_data/annotation_subset.json file exists.

Execution:

python scripts/labeling_prep/manual_conll_labeler.py

Usage:

The script will display each token from a message and prompt you to enter its label (e.g., B-PRODUCT, I-PRODUCT, O).

Valid Labels: B-PRODUCT, I-PRODUCT, B-LOC, I-LOC, B-PRICE, I-PRICE, O. (Labels are case-insensitive when entered, but will be converted to uppercase for consistency).

Type s and press Enter to skip the rest of the current message (all remaining tokens will be labeled O).

Type r and press Enter to re-label the current message from the beginning.

Press Ctrl+C at any time to exit the labeling process and save the labels collected so far.

Output: The script will save your manually labeled data to data/labeled_data/labeled_data.conll in the CoNLL-2003 format. This file is your gold-standard labeled dataset for NER model training.

Running Jupyter Notebooks for Tasks 3-6
For the following tasks, it is recommended to use Google Colab with GPU support for faster training and processing.

Upload data/labeled_data/labeled_data.conll to your Google Drive (e.g., within the colab_projects/EthioMart_NER/data/labeled_data/ path).

Upload data/preprocessed_data/preprocessed_amharic_ecommerce_messages.json to your Google Drive (e.g., within the colab_projects/EthioMart_NER/data/preprocessed_data/ path).

Open the respective .ipynb file in Google Colab (from your EthioMart_NER_Project/notebooks/ folder in Drive).

Ensure GPU runtime is enabled (Runtime -> Change runtime type -> GPU).

Run the Google Drive mounting cell at the beginning of each notebook.

Run all cells in the notebook.

Task 3: Fine-Tune NER Model (notebooks/Task3_FineTune_NER_Model.ipynb)
Purpose: Fine-tune a single, best-performing pre-trained NER model (XLM-R-Amharic-NER) using your labeled dataset.

Input: data/labeled_data/labeled_data.conll

Output: Saves the fine-tuned model and tokenizer to XLM-R-Amharic-NER_ner_output/final_model within your Google Drive project path.

Task 4: Model Comparison (notebooks/Task4_Model_Comparison.ipynb)
Purpose: Fine-tune and evaluate multiple NER models (XLM-R-Amharic-NER, BERT-Medium-Amharic-NER, mBERT-Base-Cased) and compare their performance metrics (F1-score, Precision, Recall, Accuracy).

Input: data/labeled_data/labeled_data.conll

Output: Prints a comparison table and saves individual fine-tuned models to their respective output directories within your Google Drive. It also identifies and prints the path to the best-performing model.

Task 5: Model Interpretability (notebooks/Task5_Model_Interpretability.ipynb)
Purpose: Use LIME and SHAP to understand how the best-performing NER model makes its predictions on example sentences.

Input: The final_model saved from Task 3/4.

Output: Prints LIME and SHAP explanations (feature importances) for example sentences, demonstrating model transparency.

Task 6: FinTech Vendor Scorecard (notebooks/Task6_FinTech_Vendor_Scorecard.ipynb)
Purpose: Combine NER extractions from all preprocessed Telegram messages with engagement metadata to create a vendor scorecard and calculate a "Lending Score" for micro-lending decisions.

Inputs:

data/preprocessed_data/preprocessed_amharic_ecommerce_messages.json (all messages)

The final_model from Task 3/4 (for NER inference).

Output: Prints a summary table (Vendor Scorecard) comparing vendors based on calculated metrics and their Lending Score.

Coding Standards and Contribution Guidelines
To ensure code quality, readability, and maintainability in a collaborative environment, please adhere to the following guidelines:

PEP 8 Compliance: All Python code should follow PEP 8 style guidelines (e.g., naming conventions, line length, whitespace).

Docstrings: Every function, class, and module should have a clear and concise docstring explaining its purpose, arguments, and return values. Use Sphinx-style or Google-style docstrings for consistency.

Inline Comments: Use inline comments (#) to explain complex logic, non-obvious steps, or design decisions within functions.

Type Hinting: Use type hints for function parameters and return values to improve code clarity and enable static analysis.

Automated Formatting/Linting:

Consider using Black for automated code formatting (pip install black).

Use Flake8 for linting (pip install flake8).

These can be integrated into your IDE (e.g., VS Code) or run as pre-commit hooks.

