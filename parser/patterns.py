import re

# List of (regex pattern, handler_name) tuples
PATTERNS = [

    # --- Functions ---
    (re.compile(r"inscribe ritual (\w+)(?: with (.+))?", re.IGNORECASE), "parse_function_def"),
    (re.compile(r"return (.+) to the aether", re.IGNORECASE), "parse_return"),
    (re.compile(r"invoke the ritual of (\w+)(?: offering (.+))?", re.IGNORECASE), "parse_function_call"),

    # --- Type Casting ---
    (re.compile(r"conjure the phrase\b\s+(\w+)\s+\busing\b\s+(.+)", re.IGNORECASE), "parse_join_strings"),
    (re.compile(r"let\s+(\w+)\s+\bbe the spelltext of\b\s+(.+)", re.IGNORECASE), "parse_cast_string"),
    
    # --- Length must be before let ---
    (re.compile(r"let (.+) be the length of (\w+)", re.IGNORECASE), "parse_length"),

    # --- Variable declarations ---
    (re.compile(r"let\s+(\w+)\s+be\s+(.+)", re.IGNORECASE), "parse_let"),
    (re.compile(r"speak the name of\s+(\w+)\s+to be\s+(.+)", re.IGNORECASE), "parse_let_string"),
    (re.compile(r"share (\w+) with the spirts", re.IGNORECASE), "parse_global"),

    # --- Reassignment ---
    (re.compile(r"empower\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), "parse_empower"),
    (re.compile(r"drain\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), "parse_drain"),
    (re.compile(r"transmute\s+(\w+)\s+with\s+(.+)", re.IGNORECASE), "parse_transmute"),

    # --- Output ---
    (re.compile(r"reveal the truth of (.+)", re.IGNORECASE), "parse_print"),
    (re.compile(r'let the spell echo:\s*"(.*)"', re.IGNORECASE), "parse_print_string"),

    # --- Conditionals ---
    (re.compile(r"if fate whispers (.+)", re.IGNORECASE), "parse_if"),
    (re.compile(r"else if fate shifts (.+)", re.IGNORECASE), "parse_elif"),
    (re.compile(r"else when all omens fail", re.IGNORECASE), "parse_else"),

    # --- Loops ---
    (re.compile(r"chant upon (.+) each soul called (\w+)", re.IGNORECASE), "parse_for"),
    (re.compile(r"sustain the chant while (.+) holds true", re.IGNORECASE), "parse_while"),

    # --- Lists ---
    (re.compile(r"conjure an empty tome called (\w+)", re.IGNORECASE), "parse_list_conjure"),
    (re.compile(r"add (.+) to the pages of (\w+)", re.IGNORECASE), "parse_list_add"),
    (re.compile(r"call forth the word (.+) to the pages of (\w+)", re.IGNORECASE), "parse_list_add_string"),
    (re.compile(r"call upon the phrase (.+) to the pages of (\w+)", re.IGNORECASE), "parse_list_add_string"),
    (re.compile(r"invoke the sacred phrase (.+) to the pages of (\w+)", re.IGNORECASE), "parse_list_add_string"),

    # --- Block Closures ---
    (re.compile(r"close the incantation", re.IGNORECASE), "parse_close_function"),
    (re.compile(r"let the omen pass", re.IGNORECASE), "parse_close_if"),
    (re.compile(r"complete the chant", re.IGNORECASE), "parse_close_loop"),
    (re.compile(r"seal the spell", re.IGNORECASE), "parse_close_any"),

    # --- End spell (compile trigger) ---
    (re.compile(r"(so it is written|the spell is complete|thus concludes the incantation|let it be done)\.?$", re.IGNORECASE), "parse_end"),
]