# EthioMart_NER_Project/scripts/preprocessing/amharic_preprocessing.py

import json
import os
import re
import unicodedata
import sys

# Add the project root to the Python path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config # Import configuration from config.py

# Input and output file paths (loaded from config.py)
COMBINED_RAW_JSON_FILE = os.path.join(config.PREPROCESSED_DATA_DIR, config.COMBINED_RAW_MESSAGES_FILE)
PREPROCESSED_JSON_FILE = os.path.join(config.PREPROCESSED_DATA_DIR, config.PREPROCESSED_MESSAGES_FILE)

# Ensure output directory exists
os.makedirs(os.path.dirname(PREPROCESSED_JSON_FILE), exist_ok=True)

# --- Amharic Preprocessing Components ---

# 1. Character Normalization Map (Comprehensive, based on common variations)
# This map normalizes interchangeable Amharic characters to a canonical form.
# You might need to expand this based on your data's specific variations.
AMHARIC_CHAR_NORM_MAP = {
    'ሀ': 'ሃ', 'ሁ': 'ሁ', 'ሂ': 'ሂ', 'ሃ': 'ሃ', 'ሄ': 'ሄ', 'ህ': 'ህ', 'ሆ': 'ሆ',
    'ሐ': 'ሃ', 'ሑ': 'ሁ', 'ሒ': 'ሂ', 'ሓ': 'ሃ', 'ሔ': 'ሄ', 'ሕ': 'ህ', 'ሖ': 'ሆ',
    'ኀ': 'ሃ', 'ኁ': 'ሁ', 'ኂ': 'ሂ', 'ኃ': 'ሃ', 'ኄ': 'ሄ', 'ኅ': 'ህ', 'ኆ': 'ሆ',
    'ኸ': 'ሃ', 'ኹ': 'ሁ', 'ኺ': 'ሂ', 'ኻ': 'ሃ', 'ኼ': 'ሄ', 'ኽ': 'ህ', 'ኾ': 'ሆ',

    'ሰ': 'ስ', 'ሠ': 'ስ', # Normalize 'ሰ' and 'ሠ' to 'ስ' (sa)

    'ጸ': 'ጽ', 'ፀ': 'ጽ', # Normalize 'ጸ' and 'ፀ' to 'ጽ' (tse)

    'አ': 'ኣ', 'ዐ': 'ኣ', # Normalize 'አ' and 'ዐ' to 'ኣ' (a)

    'ረ': 'ር', 'ሩ': 'ሩ', 'ሪ': 'ሪ', 'ራ': 'ራ', 'ሬ': 'ሬ', 'ር': 'ር', 'ሮ': 'ሮ', # Ensure consistency
    # Add more as you discover them in your data, e.g., for 'የ', 'ደ', 'ጀ', etc.
    # Example: 'የ' and 'ዬ' might be used interchangeably
}

def normalize_amharic_characters(text):
    """Normalizes interchangeable Amharic characters based on AMHARIC_CHAR_NORM_MAP."""
    normalized_text = ""
    for char in text:
        normalized_text += AMHARIC_CHAR_NORM_MAP.get(char, char)
    return normalized_text

# 2. Amharic Punctuation and English Punctuation
# Amharic specific punctuation
AMHARIC_PUNCTUATION = ['።', '፡', '፣', '፤', '፥', '፦', '፨', '፠', '«', '»', '‹', '›', '“', '”', '‘', '’', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', '@', '#', '$', '%', '^', '&', '*', '+', '=', '~', '`']
# Common English punctuation that might appear in Amharic text
ENGLISH_PUNCTUATION = r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'

def remove_punctuation(text):
    """Removes both Amharic and common English punctuation."""
    # Remove common English punctuation first
    text = re.sub(ENGLISH_PUNCTUATION, '', text)
    # Remove Amharic punctuation
    for p in AMHARIC_PUNCTUATION:
        text = text.replace(p, '')
    return text

# 3. Number Removal/Normalization (CAUTION for NER)
def remove_numbers(text):
    """Removes numeric digits (Arabic numerals).
       CAUTION: For NER, numbers are often crucial for PRICE or PRODUCT_NAME entities.
       Consider if you want to remove them or keep them based on your specific entity types."""
    return re.sub(r'\d+', '', text)

# You can add logic to convert Amharic numerals (፩, ፪) to Arabic numerals if you encounter them
# Example: text = text.replace('፩', '1').replace('፪', '2') etc.

# 4. Abbreviation Expansion (Requires a custom dictionary, for future enhancement)
AMHARIC_ABBREVIATIONS = {
    "ት/ቤት": "ትምህርት ቤት",
    "አ.አ": "አዲስ አበባ",
    "ብ/ር": "ብር", # Birr
    "ቁ.": "ቁጥር", # Number
    "ማ/ት": "ማስታወቂያ", # Advertisement (example)
    # Add more as you find them in your e-commerce data
}

def expand_abbreviations(text, abbr_dict):
    """Expands common Amharic abbreviations using a dictionary.
       This is a simple word-based replacement and might need more
       sophisticated logic for complex abbreviations."""
    words = text.split()
    expanded_words = []
    for word in words:
        expanded_words.append(abbr_dict.get(word, word))
    return ' '.join(expanded_words)

# 5. Tokenization
def tokenize_amharic(text):
    """Simple tokenization based on whitespace."""
    # Replace any multiple spaces with a single space before splitting
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split(' ')
    return [token for token in tokens if token] # Remove empty tokens

# 6. Stop Word Removal (Expanded List)
# IMPORTANT for NER: Carefully curate this list. Words that are part of entity names
# or are strong indicators of entities (like "ብር" for price) should NOT be stop words.
AMHARIC_STOP_WORDS = set([
    "አሉ", "ሀገር", "ሁሉ", "ሁሉም", "ሁሉንም", "ሁል", "ሁኔታ", "ህዝብ", "ሆነ", "ሆኑ", "ሆኖም",
    "ሆይ", "ኋላ", "ለማለት", "ለምን", "ለዘላለም", "ለድርጊቶችዎ", "ላይ", "ሌላ", "ሌሎች", "ልክ",
    "ልጅ", "መሆኑ", "መሆን", "መልካም", "መቸ", "መቸም", "መንግስት", "መካከል", "መግለጹን",
    "ማለት", "ማነው", "ማን", "ማንም", "ማንኛውም", "ማድረግ", "ምነው", "ምን", "ምንም", "ምንድን",
    "ምክንያቱም", "ምክንያት", "ሰሞኑን", "ሰአት", "ሰው", "ሰዎች", "ሲሆን", "ሲሉ", "ሲል",
    "ሲናገር", "ሳይሆን", "ሴት", "ስለ", "ስለሆነ", "ስም", "ስራ", "ቀን",
    "ቁጥር", # CAUTION: "ቁጥር" (number) can be part of CONTACT_INFO or refer to a product number. Consider for NER.
    "በኋላ", "በለው", "በላይ", "በል", "በሰላም", "በሰሞኑ", "በርካታ", "በቃ", "በተለይ", "በተመለከተ",
    "በተመሳሳይ", "በታች", "በአል", "በኢትዮጵያ", "በኩል", "በውስጥ", "በዚህ", "በይ", "በጣም",
    "በፊት", "ቢሆን", "ቢቢሲ", "ቤተሰቦችዎ", "ቤት", "ብለህ", "ብለዋል", "ብላ", "ብሎ",
    # "ብር", # CAUTION: "ብር" (Birr) is a currency. Keep this line commented out if you want to extract PRICE entities.
    "ብቸኛው", "ብቻ", "ብቻውን", "ብዙ", "ብዛት", "ቦታ", "ተማሪዎች", "ተባለ", "ተናግረዋል",
    "ተከናውኗል", "ተው", "ተገለጸ", "ተገልጿል", "ተጠናቅቋል", "ተጨማሪ", "ቲም", "ታላቅ",
    "ታች", "ታዲያ", "ትልቅ", "ትናንት", "ትክክል", "ችግር", "ነህ", "ነሽ", "ነበረ", "ነበረች",
    "ነበሩ", "ነበር", "ነች", "ነን", "ነኝ", "ነዋ", "ነው", "ነይ", "ነገር", "ነገሮች", "ነገሮችን",
    "ናት", "ናቸው", "አሁን", "አለ", "አላውቅም", "አልነበረም", "አመልክተዋል", "አመሰግናለሁ",
    "አሜን", "አሳሰበ", "አሳስበዋል", "አስረድተዋል", "አስታወቀ", "አስታውሰዋል", "አስታውቀዋል",
    "አስገነዘቡ", "አስገንዝበዋል", "አስፈላጊ", "አረ", "አበራራ", "አብራርተዋል", "አታውቅም",
    "አቶ", "አንተ", "አንች", "አንድ", "አንጻር", "አዎ", "አይ", "አይነት", "አይደለም", "አይደል",
    "ኢትዮጵያ", "እሱ", "እስቲ", "እስከ", "እስኪደርስ", "እስካሁን", "እሷ", "እረ", "እርስዎ",
    "እሽ", "እባክህ", "እባክሸ", "እባክዎ", "እና", "እናመሰግናለን", "እናም", "እኔ", "እኔም",
    "እንኳ", "እንደ", "እንደተናገሩት", "እንደተገለጸው", "እንደት", "እንደአስረዱት", "እንደገለጹት",
    "እንደገና", "እንዲሁም", "እንዴ", "እንድህ", "እንጂ", "እንግድህ", "እኛ", "እኮ", "እውነት",
    "እዚሁ", "እዚህ", "እዚያ", "እያንዳንዱ", "እያንዳንዳችው", "እያንዳንዷ", "እግር", "ኧረ",
    "ከ", "ከሆነ", "ከኋላ", "ከላይ", "ከመካከል", "ከሰሞኑ", "ከተማ", "ከታች", "ከቶ", "ከውስጥ",
    "ከጋራ", "ከፊት", "ክልል", "ክፍል", "ወቅት", "ወንድ", "ወዘተ", "ወይ", "ወይም", "ወይኔ",
    "ወደ", "ወደፊት", "ዋና", "ውስጥ", "ውይ", "ውጪ", "ዛሬ", "ዜና", "ዝም", "የኋላ",
    "የለም", "የለውም", "የሚገኙ", "የሚገኝ", "የሰሞኑ", "የሰው", "የተለያየ", "የተለያዩ", "የታች",
    "የት", "የኔ", "የኢትዮጵያ", "የወደፊቱ", "የውስጥ", "የዘላለም", "የገለጹት", "ያለ", "ያለው",
    "ያሉ", "ያሳዝናል", "ያፈሳሉ", "ይሁን", "ይሄ", "ይህ", "ይህን", "ይሆናል", "ይሆን", "ይሞታል",
    "ይሰማቸዋል", "ይታወሳል", "ይችላል", "ይቿ", "ይናገራሉ", "ይገልጻል", "ይገባል", "ደህና",
    "ደሞ", "ደስ", "ደግሞ", "ድረስ", "ድርጊቶች", "ድጋፍ", "ዶክተር", "ገልጸዋል", "ገልጿል",
    "ገና", "ጉዳይ", "ጉድ", "ጊዜ", "ጋራ", "ጋር", "ግን", "ግዜ", "ጥሩ", "ጥቂት", "ፈጣሪ",
    "ፊት", "፣", "፤", "ቤት", "በ", "ም", "፡", "ዓ", "የ", "ሆኖ", "አሉ", "አንዱ"
])

def remove_stopwords(tokens, stopwords_list):
    """Removes stop words from a list of tokens (case-insensitive)."""
    return [word for word in tokens if word.lower() not in stopwords_list]

# 7. Overall Text Cleaning Function
def clean_amharic_text(text):
    """Applies a sequence of preprocessing steps to Amharic text."""
    if not text: # Handle empty or None text
        return ""

    text = text.strip()
    text = normalize_amharic_characters(text)
    
    # Remove emojis
    text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', '', text)
    
    # Expand abbreviations before removing punctuation or numbers if abbreviations contain them
    # Uncomment if you have a robust abbr_dict that's proven useful
    # text = expand_abbreviations(text, AMHARIC_ABBREVIATIONS) 

    text = remove_punctuation(text)
    
    # IMPORTANT FOR NER: Decide if you want to keep numbers for prices, quantities, model numbers etc.
    # For e-commerce NER, numbers are often crucial (e.g., "iPhone 15", "500 ብር").
    # If you need numbers as part of entities, you should SKIP the `remove_numbers(text)` step.
    # For now, this is COMMENTED OUT to RETAIN NUMBERS for NER purposes.
    # text = remove_numbers(text) 

    tokens = tokenize_amharic(text)
    tokens = remove_stopwords(tokens, AMHARIC_STOP_WORDS)
    
    # Rejoin tokens to a string
    cleaned_text = ' '.join(tokens)
    
    # Final cleaning of extra spaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text

# --- Main Preprocessing Script ---
def preprocess_telegram_data(input_file, output_file):
    print(f"Loading raw data from {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        print(f"Successfully loaded {len(raw_data)} messages.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please ensure your combined raw JSON exists.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{input_file}': {e}")
        return

    preprocessed_data = []
    for i, message_entry in enumerate(raw_data):
        if (i + 1) % 1000 == 0:
            print(f"Processing message {i+1}/{len(raw_data)}...")

        original_text = message_entry.get('message', '') # Use .get to handle missing 'message' key
        
        # Apply cleaning
        cleaned_text = clean_amharic_text(original_text)
        
        # Add the cleaned text to the message entry
        message_entry['cleaned_text'] = cleaned_text
        
        preprocessed_data.append(message_entry)

    print(f"Finished preprocessing {len(preprocessed_data)} messages.")

    print(f"Saving preprocessed data to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(preprocessed_data, f, ensure_ascii=False, indent=4)
        print(f"Preprocessed data saved to {output_file}")
    except Exception as e:
        print(f"Error saving preprocessed JSON file: {e}")

if __name__ == '__main__':
    preprocess_telegram_data(COMBINED_RAW_JSON_FILE, PREPROCESSED_JSON_FILE)