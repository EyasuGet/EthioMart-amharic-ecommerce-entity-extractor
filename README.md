# EthioMart Named Entity Recognition (NER) Project

This project aims to consolidate and structure decentralized Ethiopian e-commerce data from Telegram channels to support FinTech decisions, particularly vendor micro-lending. It involves data ingestion, Amharic text preprocessing, manual data labeling for NER, model fine-tuning, and performance comparison.

## Project Structure
```
ethiomart-amharic-ecommerce-ner/
├── .gitignore
├── README.md
├── requirements.txt
├── config.py
├── data/
│   ├── raw/                  # Raw Telegram data as collected
│   ├── interim/              # Preprocessed but not yet labeled
│   ├── labeled/              # Labeled data (CoNLL, Doccano, etc.)
│   └── media/                # (Optional) Downloaded images, etc.
├── scripts/
│   ├── scraper/              # Telegram scraping scripts
│   ├── preprocessing/        # Amharic text preprocessing scripts
│   ├── labeling/             # Scripts for annotation prep/conversion
│   ├── training/             # (Future) Model training/fine-tuning scripts
│   └── analysis/             # (Future) Vendor analytics, scoring, etc.
├── notebooks/                # (Future) Exploration, modeling, analysis notebooks
├── docs/
│   ├── Interim_Report_EthioMart.pdf
│   └── Annotation_Guidelines.md
└── venv/                     # Local Python virtual environment (not tracked)
```

## Setup Instructions

Follow these steps to set up the project environment and prepare for data processing:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link-here> # **IMPORTANT: Replace with your actual GitHub repo URL**
    cd EthioMart_NER_Project
    ```
2.  **Create a Python Virtual Environment:**
    It is highly recommended to use a virtual environment to manage project dependencies and avoid conflicts with other Python projects.
    ```bash
    python3 -m venv venv
    ```
3.  **Activate the Virtual Environment:**
    * **macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    (You will need to activate this environment in each new terminal session you use for the project.)

4.  **Install Dependencies:**
    Install all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    * **Troubleshooting `TimeoutError` during `pip install doccano` (or other large packages):**
        If you encounter `ReadTimeoutError` (especially for `numpy` or `pandas` dependencies of Doccano), try increasing pip's timeout:
        ```bash
        pip install doccano --timeout 1000
        # If it still fails, try installing numpy/pandas separately first:
        # pip install numpy --timeout 1000
        # pip install pandas --timeout 1000
        # pip install doccano --timeout 1000
        ```
        You can also try clearing pip's cache: `pip cache purge`.

5.  **Configure Telegram API Credentials:**
    * **Obtain API Credentials:**
        1.  Go to [my.telegram.org/apps](https://my.telegram.org/apps).
        2.  Log in with your Telegram phone number.
        3.  Click on "API development tools".
        4.  Fill in the "App title" and "Short name" (e.g., "EthioMart Scraper").
        5.  You will receive your `api_id` (an integer) and `api_hash` (a string). Keep these confidential.
    * **Create/Edit `config.py`:**
        * Open the `config.py` file located in the root directory (`EthioMart_NER_Project/config.py`).
        * Replace the placeholder values for `API_ID`, `API_HASH`, and `PHONE_NUMBER` with your actual credentials.
        * Ensure your `PHONE_NUMBER` is in international format (e.g., `'+251912345678'`).

## Running the Project Scripts

Ensure your virtual environment is activated before running any scripts.

### Task 1: Data Ingestion and Preprocessing

1.  **Run the Telegram Scraper (`scripts/scraper/telegram_scraper.py`):**
    * **Purpose:** Fetches messages and metadata from specified Telegram e-commerce channels.
    * **Before running:** Open `scripts/scraper/telegram_scraper.py` and update the `CHANNELS` list with the specific Telegram channel usernames or links you wish to scrape (e.g., `@helloomarketethiopia`, `@ethio_brand_collection`).
    * **Execution:**
        ```bash
        python scripts/scraper/telegram_scraper.py
        ```
    * **Output:** This script will create a session file in `data/raw_telegram_data/` and save all collected text messages and their metadata (including media presence, but no actual media files) into a single JSON file: `data/preprocessed_data/all_telegram_ecommerce_messages.json`.

2.  **Run the Amharic Preprocessing Script (`scripts/preprocessing/amharic_preprocessing.py`):**
    * **Purpose:** Cleans and normalizes the raw Amharic text collected by the scraper.
    * **Before running:** Open `scripts/preprocessing/amharic_preprocessing.py`.
        * Review the `AMHARIC_STOP_WORDS` set: For NER, words like "ብር" (Birr) and numbers are crucial entities for `PRICE` and `PRODUCT_NAME`. Ensure "ብር" is **NOT** included in the `AMHARIC_STOP_WORDS` list (it is commented out by default in the provided list).
        * Confirm that the `remove_numbers(text)` function call within `clean_amharic_text` is **commented out** if you want to retain numbers for `PRICE` or `PRODUCT_NAME` entities (recommended for e-commerce NER).
    * **Execution:**
        ```bash
        python scripts/preprocessing/amharic_preprocessing.py
        ```
    * **Output:** This script reads `data/preprocessed_data/all_telegram_ecommerce_messages.json`, applies the defined preprocessing steps to the `message` field, and adds a new `cleaned_text` field to each message entry. The enhanced data is saved to `data/preprocessed_data/preprocessed_amharic_ecommerce_messages.json`.

### Task 2: Data Labeling Preparation

1.  **Extract Annotation Subset (`scripts/labeling_prep/extract_annotation_subset.py`):**
    * **Purpose:** Prepares a smaller, manageable subset of preprocessed messages specifically for manual annotation.
    * **Execution:**
        ```bash
        python scripts/labeling_prep/extract_annotation_subset.py
        ```
    * **Output:** This will create `data/labeled_data/annotation_subset.json` containing the first 30-50 messages (or fewer if the dataset is smaller) from your `preprocessed_amharic_ecommerce_messages.json`, with only `id` and `text` (cleaned text) fields, formatted for easy import into annotation tools like Doccano.

2.  **Set up and Use Doccano for Manual Labeling:**
    * **Install Doccano (if not already):**
        * Activate your `venv` (or a fresh `doccano_env` if your main `venv` had issues with Doccano).
        * `pip install doccano`
    * **Initialize Doccano Database:**
        ```bash
        doccano init
        ```
    * **Create Doccano Superuser Account:**
        ```bash
        doccano createuser --username admin --password admin # Choose a strong password!
        ```
    * **Start Doccano Server:** Keep this terminal session open.
        ```bash
        doccano webserver --port 8000
        ```
    * **Access Doccano UI:** Open your web browser and navigate to `http://127.0.0.1:8000`. Log in with your admin credentials.
    * **Create Project:**
        * Click "Create project".
        * Set `Project Type` to "**Sequence Labeling**".
        * Define labels: Add `PRODUCT`, `LOC`, `PRICE`. (Doccano automatically handles `B-`/`I-` prefixes).
    * **Import Data:**
        * Within your project in Doccano, go to "Import Dataset".
        * Select "JSON" format and upload `data/labeled_data/annotation_subset.json`.
    * **Perform Manual Labeling:**
        * Go through each document in the Doccano interface.
        * Select text spans that correspond to `PRODUCT`, `LOC`, or `PRICE` entities.
        * Assign the appropriate label using the pop-up.
        * Refer to `docs/Annotation_Guidelines.md` for detailed labeling rules and examples.
    * **Export Labeled Data:**
        * After labeling your 30-50 messages, navigate to the "Export Dataset" tab in Doccano.
        * Select "**CoNLL 2003**" format.
        * Save the downloaded `.txt` file as `data/labeled_data/labeled_data.conll`. This file is your gold-standard labeled dataset for NER model training.

## Coding Standards and Contribution Guidelines

To ensure code quality, readability, and maintainability in a collaborative environment, please adhere to the following guidelines:

* **PEP 8 Compliance:** All Python code should follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines (e.g., naming conventions, line length, whitespace).
* **Docstrings:** Every function, class, and module should have a clear and concise docstring explaining its purpose, arguments, and return values. Use [Sphinx-style](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html) or [Google-style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) docstrings for consistency.
* **Inline Comments:** Use inline comments (`#`) to explain complex logic, non-obvious steps, or design decisions within functions.
* **Type Hinting:** Use [type hints](https://docs.python.org/3/library/typing.html) for function parameters and return values to improve code clarity and enable static analysis.
* **Automated Formatting/Linting:**
    * Consider using `Black` for automated code formatting (`pip install black`).
    * Use `Flake8` for linting (`pip install flake8`).
    * These can be integrated into your IDE (e.g., VS Code) or run as pre-commit hooks.
* **Commit Messages:** Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
    * **Format:** `<type>(<scope>): <subject>`
    * **Body (optional):** More detailed explanation.
    * **Examples:**
        * `feat: Implement X feature`
        * `fix(scraper): Resolve API timeout issue`
        * `docs: Update README with setup instructions`
        * `refactor(preprocessing): Improve Amharic normalization logic`
        * `chore: Update dependencies`
