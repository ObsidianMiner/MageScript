import re

# List of (regex pattern, handler_name) tuples
PATTERNS = [

    # --- Functions ---
    (re.compile(r"inscribe ritual (\S+)(?: with (.+))?", re.IGNORECASE), "parse_function_def"),
    (re.compile(r"return (.+) to the aether", re.IGNORECASE), "parse_return"),
    (re.compile(r"invoke the ritual of (\S+)(?: offering (.+))?", re.IGNORECASE), "parse_function_call"),
    (re.compile(r"summon (\S+) as the spirits from the ritual of (.+?)(?: offering (.+))?$", re.IGNORECASE), "parse_function_call_with_output"),
    (re.compile(r"invoke the great rite of (\S+)(?: and offer (.+) as tribute to awaken its arcane design)?", re.IGNORECASE), "parse_function_call"),

    # --- Files ---
    (re.compile(r"unseal the scroll (\S+) from (.+)", re.IGNORECASE), "parse_read_file"),
    (re.compile(r"by quill of eternity let the tome of (.+) be born etched in (\S+) and sealed in flame", re.IGNORECASE), "parse_write_file"),
    
    (re.compile(r"extend the infinite scroll of (.+) with (\S+) that its verses may never cease", re.IGNORECASE), "parse_append_file"),
    (re.compile(r"purge the chronicle of (.+) from the vault of aeons that even the gods forget it once was", re.IGNORECASE), "parse_delete_file"),
    (re.compile(r"unveil the scroll (.+) line by line and bind its verses to (\S+))", re.IGNORECASE), "parse_read_lines"),
    (re.compile(r"the aether speaks (.+) does not lie in this realm", re.IGNORECASE), "parse_file_or_path_exists"),
    (re.compile(r"by the will of creation carve the sanctum (\S+) from the bones of the world", re.IGNORECASE), "parse_create_dir"),
    (re.compile(r"chant upon the verses of (\S+) each line known as (\S+)", re.IGNORECASE), "parse_file_exists"),
    (re.compile(r"call forth the echos of the sanctum of (\S+) and seal them to (\S+)", re.IGNORECASE), "parse_for_each_line"),


    # --- Type Casting ---
    (re.compile(r"conjure the phrase\b\s+(\w+)\s+\busing\b\s+(.+)", re.IGNORECASE), "parse_join_strings"),
    (re.compile(r"let\s+(\w+)\s+\bbe the spelltext of\b\s+(.+)", re.IGNORECASE), "parse_cast_string"),
    
    # --- Length must be before let ---
    (re.compile(r"let (.+) be the length of (\w+)", re.IGNORECASE), "parse_length"),

    # --- Importing ---
    (re.compile(r"commune with the library of (.+)", re.IGNORECASE), "parse_import"),
    (re.compile(r"summon (.+) from the library of (\w+)", re.IGNORECASE), "parse_import_from_module"),

    # --- Classes (Abominations) ---
    (re.compile(r"proclaim a (\w+) abomination", re.IGNORECASE), "parse_class_def"),
    (re.compile(r"proclaim an (\w+) abomination feasting upon the bones of (\w+)", re.IGNORECASE), "parse_inherited_class_def"),
    (re.compile(r"fuel the abomination with (.+)", re.IGNORECASE), "parse_constructor_def_with_params"),
    (re.compile(r"cometh the abomination awakens", re.IGNORECASE), "parse_constructor_def"),
    (re.compile(r"birth an abomination of (.+) named (.+) fuled with (.+)", re.IGNORECASE), "parse_instantiate_class_with_params"),
    (re.compile(r"birth an abomination of (.+) named (.+)", re.IGNORECASE), "parse_instantiate_class"),

    # --- Variable declarations ---
    (re.compile(r"let\s+(\S+)\s+be\s+(.+)", re.IGNORECASE), "parse_let"),
    (re.compile(r"speak the name of\s+(\S+)\s+to be\s+(.+)", re.IGNORECASE), "parse_let_string"),
    (re.compile(r"share (\S+) with the spirts", re.IGNORECASE), "parse_global"),

    # --- Reassignment ---
    (re.compile(r"empower\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), "parse_empower"),
    (re.compile(r"drain\s+(\w+)\s+by\s+(.+)", re.IGNORECASE), "parse_drain"),
    (re.compile(r"transmute\s+(\w+)\s+with\s+(.+)", re.IGNORECASE), "parse_transmute"),
    (re.compile(r"enfold\s+(\w+)\s+with the multiplicative power of\s+(.+)", re.IGNORECASE), "parse_multiply"),
    (re.compile(r"divide the soul of\s+(\w+)\s+by the decree of\s+(.+)", re.IGNORECASE), "parse_divide"),
    (re.compile(r"mark\s+(\w+)\s+with the remainder after striking by\s+(.+)", re.IGNORECASE), "parse_modulus"),

    # --- Output ---
    (re.compile(r"reveal the truth of (.+)", re.IGNORECASE), "parse_print"),
    (re.compile(r'let the spell echo\s*"(.*)"', re.IGNORECASE), "parse_print_string"),
    (re.compile(r"whisper to the void (.+)", re.IGNORECASE), "parse_print_string"),

    # --- Input ---
    (re.compile(r"ask the stars for (\S+) saying (.+)", re.IGNORECASE), "parse_input"),
    (re.compile(r"seek the ether for (\S+) with the words (.+)", re.IGNORECASE), "parse_input"),

    # --- Conditionals ---
    (re.compile(r"if fate whispers (.+)", re.IGNORECASE), "parse_if"),
    (re.compile(r"else if fate shifts (.+)", re.IGNORECASE), "parse_elif"),
    (re.compile(r"else when all omens fail", re.IGNORECASE), "parse_else"),

    # --- Loops ---
    (re.compile(r"chant upon (.+) each soul called (\w+)", re.IGNORECASE), "parse_for"),
    (re.compile(r"sustain the chant while (.+) holds true", re.IGNORECASE), "parse_while"),
    (re.compile(r"scatter the chant to the winds of finality", re.IGNORECASE), "parse_break"),
    (re.compile(r"pass over this soul in silence", re.IGNORECASE), "parse_continue"),

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
    (re.compile(r"vanish  self", re.IGNORECASE), "parse_close_class"),
    (re.compile(r"seal the spell", re.IGNORECASE), "parse_close_any"),

    # --- End spell (compile trigger) ---
    (re.compile(r"(so it is written|the spell is complete|thus concludes the incantation|let it be done)\.?$", re.IGNORECASE), "parse_end"),
]