import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser.patterns import PATTERNS
import re

def extract_literal_phrases_from_regex(pattern: str):
    # 1. Remove all capturing groups (e.g., (.+), (\S+), etc.)
    pattern = re.sub(r'\([^)]*\)', '', pattern)

    # 2. Replace escaped whitespace (e.g., \s+) with a space
    pattern = re.sub(r'\\s\+?', ' ', pattern)

    # 3. Remove other escaped characters (e.g., \w, \d, etc.)
    pattern = re.sub(r'\\[a-zA-Z]', '', pattern)

    # 4. Remove regex symbols and punctuation
    pattern = re.sub(r'[^\w\s]', '', pattern)  # removes anything not word or space

    # 5. Collapse multiple spaces into one
    pattern = re.sub(r'\s+', ' ', pattern)

    # 6. Trim leading/trailing spaces
    cleaned = pattern.strip()

    # 7. Return words or fragments
    return cleaned.split()

def get_keywords():
    keywords = []
    for pattern, _ in PATTERNS:
        literals = extract_literal_phrases_from_regex(pattern.pattern)
        if literals:
            keywords.extend(literals)
    keywords = set(keywords)
    return keywords
def get_phrases():
    phrases = []
    for pattern, _ in PATTERNS:
        literals = extract_literal_phrases_from_regex(pattern.pattern)
        if literals:
            phrases.append(literals)
    print(phrases)

if __name__ == "__main__":
    print(get_phrases())