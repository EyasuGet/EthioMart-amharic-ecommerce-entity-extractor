# EthioMart Named Entity Recognition (NER) Project

## Overview

EthioMart NER is designed to transform FinTech decision-making in Ethiopia by structuring decentralized e-commerce data from Telegram channels. The project addresses the challenge of inaccessible merchant data—such as product listings, prices, and sales locations—scattered across informal Telegram groups. By consolidating and analyzing this data, EthioMart enables data-driven "vendor scorecards" for micro-lending, supporting financial inclusion for small and medium e-commerce businesses.

---

## Project Structure

```
EthioMart_NER_Project/
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── venv/
├── data/
│   ├── raw_telegram_data/
│   ├── preprocessed_data/
│   │   ├── all_telegram_ecommerce_messages.json
│   │   └── preprocessed_amharic_ecommerce_messages.json
│   ├── labeled_data/
│   │   ├── annotation_subset.json
│   │   └── labeled_data.conll
│   └── (optional) media/
├── scripts/
│   ├── scraper/
│   │   └── telegram_scraper.py
│   ├── preprocessing/
│   │   └── amharic_preprocessing.py
│   ├── labeling_prep/
│   │   ├── extract_annotation_subset.py
│   │   └── manual_conll_labeler.py
│   ├── model_training/
│   │   └── train_ner_model.py
│   └── analytics/
│       └── vendor_scorecard.py
├── docs/
│   ├── Interim_Report_EthioMart.pdf
│   └── Annotation_Guidelines.md
└── notebooks/
    ├── Task3_FineTune_NER_Model.ipynb
    ├── Task4_Model_Comparison.ipynb
    ├── Task5_Model_Interpretability.ipynb
    └── Task6_FinTech_Vendor_Scorecard.ipynb
```

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <your-repo-link-here>
   cd EthioMart_NER_Project
   ```

2. **Create and Activate a Python Virtual Environment**
   ```bash
   python3 -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows (CMD)
   venv\Scripts\activate.bat
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   - If you encounter `ReadTimeoutError` (e.g., with `doccano`, `numpy`, or `pandas`), increase the timeout:
     ```bash
     pip install doccano --timeout 1000
     # Or install numpy/pandas separately first
     pip install numpy --timeout 1000
     pip install pandas --timeout 1000
     pip install doccano --timeout 1000
     ```
   - Clear pip cache if needed: `pip cache purge`

4. **Configure Telegram API Credentials**
   - Obtain `api_id` and `api_hash` from [my.telegram.org/apps](https://my.telegram.org/apps).
   - Edit `config.py` and set `API_ID`, `API_HASH`, and `PHONE_NUMBER` (in international format, e.g., `+251912345678`).

---

## Running Project Scripts

**Activate your virtual environment before running scripts.**

### 1. Data Ingestion & Preprocessing

- **Scrape Telegram Data**
  - Edit `scripts/scraper/telegram_scraper.py` to set your target channels.
  - Run:
    ```bash
    python scripts/scraper/telegram_scraper.py
    ```
  - Output: `data/preprocessed_data/all_telegram_ecommerce_messages.json`

- **Preprocess Amharic Text**
  - Review `AMHARIC_STOP_WORDS` in `scripts/preprocessing/amharic_preprocessing.py` (ensure "ብር" is not removed).
  - Ensure numbers are retained for PRICE/PRODUCT_NAME entities.
  - Run:
    ```bash
    python scripts/preprocessing/amharic_preprocessing.py
    ```
