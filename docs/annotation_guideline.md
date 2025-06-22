# EthioMart NER Project: Annotation Guidelines

These guidelines define the entity types and rules for annotating Amharic e-commerce messages in the CoNLL format. Consistent and accurate labeling is crucial for training a high-performing Named Entity Recognition (NER) model.

## 1. Annotation Format: CoNLL-2003

* Each token (word) is labeled on its own line.
* The token is followed by a tab or space, and then its entity label.
* Blank lines (`\n`) separate individual sentences or messages.

**Example Structure:**

Token1 Label1
Token2 Label2
...
TokenN LabelN

TokenA LabelA
TokenB LabelB
...


## 2. Entity Types and Definitions

The following entity types are used, with `B-` (Beginning) and `I-` (Inside) prefixes for multi-token entities, and `O` (Outside) for non-entity tokens.

* **`PRODUCT`**: Refers to the specific name or description of the item being sold or discussed.
    * **Scope:** Include brand names, model numbers, and descriptive adjectives that are integral to identifying the unique product.
    * **Examples:**
        * `**iPhone 15 Pro Max**`
        * `**Samsung Galaxy S24 Ultra**`
        * `**የሴቶች ቦርሳ**` (women's bag)
        * `**አነሶላ**` (bedsheet)
        * `**የልጆች ቀሚስ**` (children's dress)
    * **Exclusions:** Generic terms like "ምርት" (product), "እቃ" (item) if not followed by a specific descriptor.

* **`LOC` (Location)**: Refers to specific geographical places, cities, districts, or notable landmarks mentioned as points of sale, pickup, or delivery.
    * **Scope:** City names, neighborhood names, specific building names if used as a location.
    * **Examples:**
        * `**አዲስ አበባ**` (Addis Ababa)
        * `**ቦሌ**` (Bole - a district in Addis Ababa)
        * `**ፒያሳ**` (Piazza - a specific area in Addis Ababa)
        * `**መገናኛ**` (Megenagna - a specific area)
    * **Exclusions:** General directions (e.g., "እዚህ" - here, "በዛ" - there) unless they are part of a named location.

* **`PRICE`**: Refers to the monetary value of a product, including both the numerical amount and the currency unit.
    * **Scope:** The numeric value and the currency word.
    * **Examples:**
        * `**25000 ብር**` (25000 Birr)
        * `**1000 ብር**` (1000 Birr)
        * `**5000ETB**` (if "ETB" is present)
        * `**ዋጋው 500 ብር**` (label only "**500 ብር**", "ዋጋው" is O)
    * **Crucial Note:** Numbers (digits) and currency terms (like "ብር") are critical for this entity. Ensure they are **NOT** removed during preprocessing. If "ብር" or numbers were removed from your `cleaned_text` during preprocessing, go back and adjust the `amharic_preprocessing.py` script.
    * **Exclusions:** Just a number if it's not clearly a price (e.g., a phone number, a date, a quantity without context).

* **`O` (Outside)**: Denotes any token that is not part of a `PRODUCT`, `LOC`, or `PRICE` entity.

## 3. General Annotation Principles

* **Be Consistent:** This is the most important rule. If you label a certain type of phrase one way, always label similar phrases the same way throughout the dataset.
* **Exact Spans:** Select the exact words that form the entity. Do not include leading/trailing punctuation or unnecessary words.
* **Contiguous Entities:** Entities should be contiguous (no gaps). If parts of an entity are separated by non-entity words, treat them as separate entities or only label the contiguous part.
* **Ambiguity:** If a word or phrase could belong to multiple entity types, choose the most specific or most common entity type for your domain. If still ambiguous, prioritize the most important entity type for your project's goals (e.g., PRICE and PRODUCT are likely higher priority for FinTech micro-lending).
* **Case Sensitivity:** While Amharic doesn't have true "case" like English (upper/lower), proper nouns often start with capitalized characters in Latin transcriptions or are simply distinct words. Annotation should respect the tokens provided by the preprocessor. Your `cleaned_text` from preprocessing should be the source.

## 4. Annotation Process with Doccano

1.  **Prepare Data:** Use `scripts/labeling_prep/extract_annotation_subset.py` to create `annotation_subset.json`.
2.  **Setup Doccano:** Install and run Doccano server locally (`doccano webserver --port 8000`).
3.  **Create Project:** In Doccano UI, create a "Sequence Labeling" project and define `PRODUCT`, `LOC`, `PRICE` as labels.
4.  **Import Data:** Import `annotation_subset.json` into your Doccano project.
5.  **Annotate:** Go through each document, select text spans, and assign the appropriate labels. Doccano will automatically apply B-/I- prefixes.
6.  **Export:** After labeling 30-50 messages, export the dataset from Doccano in "CoNLL 2003" format and save it as `data/labeled_data/labeled_data.conll`.

