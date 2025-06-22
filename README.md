# EthioMart Named Entity Recognition (NER) Project

This project aims to consolidate and structure decentralized Ethiopian e-commerce data from Telegram channels to support FinTech decisions, particularly vendor micro-lending. It involves data ingestion, Amharic text preprocessing, manual data labeling for NER, model fine-tuning, and performance comparison.

## Project Structure
EthioMart_NER_Project/
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── venv/
├── data/
│   ├── raw_telegram_data/
│   ├── preprocessed_data/
│   ├── labeled_data/
│   └── (optional) media/
├── scripts/
│   ├── scraper/
│   ├── preprocessing/
│   ├── labeling_prep/
│   └── (future) model_training/
├── docs/
│   ├── Interim_Report_EthioMart.pdf
│   └── Annotation_Guidelines.md
└── (future) notebooks/

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd EthioMart_NER_Project
    ```
2.  **Create a Python Virtual Environment:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the Virtual Environment:**
    * macOS/Linux: `source venv/bin/activate`
    * Windows CMD: `venv\Scripts\activate.bat`
    * Windows PowerShell: `.\venv\Scripts\Activate.ps1`
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Configure API Credentials:**
    * Obtain `api_id` and `api_hash` from [my.telegram.org/apps](https://my.telegram.org/apps).
    * Create `config.py` in the root directory and add your credentials (see `config.py` example below).
    * Replace `YOUR_PHONE_NUMBER` with your actual Telegram phone number.

## Running the Project

### Task 1: Data Ingestion and Preprocessing

1.  **Run the Telegram Scraper:**
    * Before running, update `CHANNELS` list in `scripts/scraper/telegram_scraper.py` with your chosen Telegram channel usernames/links.
    * Ensure your `config.py` is set up.
    ```bash
    python scripts/scraper/telegram_scraper.py
    ```
    This will generate `data/preprocessed_data/all_telegram_ecommerce_messages.json`.

2.  **Run the Amharic Preprocessing Script:**
    * Review `scripts/preprocessing/amharic_preprocessing.py` and ensure the `AMHARIC_STOP_WORDS` and `remove_numbers()` function are configured correctly for NER (i.e., `ብር` and numbers are NOT removed).
    ```bash
    python scripts/preprocessing/amharic_preprocessing.py
    ```
    This will generate `data/preprocessed_data/preprocessed_amharic_ecommerce_messages.json`.

### Task 2: Data Labeling Preparation

1.  **Extract Annotation Subset:**
    ```bash
    python scripts/labeling_prep/extract_annotation_subset.py
    ```
    This will create `data/labeled_data/annotation_subset.json` with 30-50 messages for labeling.

2.  **Set up Doccano for Labeling:**
    * Install Doccano (refer to Doccano documentation or previous instructions).
    * Start Doccano server: `doccano webserver --port 8000`
    * Create a "Sequence Labeling" project, define `PRODUCT`, `LOC`, `PRICE` labels.
    * Import `data/labeled_data/annotation_subset.json` into Doccano.# EthioMart-amharic-ecommerce-entity-extractor
