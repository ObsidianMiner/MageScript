import re

class MageScriptPreprocessor:
    def __init__(self, rawSpellLines):
        self.spellLines = rawSpellLines
        self.spellLines = self.preprocess()
    
    def preprocess(self):
        processedLines = []

        for line in self.spellLines:
            line = self.replace_thy_access(line)
            line = self.replace_arithmetic(line)
            processedLines.append(line)
        
        return processedLines
    
    def replace_thy_access(self, line):
        # Matches: drain thy health of skeleton by 2 → drain skeleton.health by 2
        pattern = r'\bthy\s+(\w+)\s+of\s+(\w+)\b'
        return re.sub(pattern, r'\2.\1', line)
    
    def replace_arithmetic(self, line):
        # Replace spell words with actual math symbols
        replacements = {
            r'\btimes\b': '*',
            r'\bplus\b': '+',
            r'\bminus\b': '-',
            r'\bdivided\s+by\b': '/',
            r'\bmodulo\b': '%',
            r'\bto\s+the\s+power\s+of\b': '**'
        }

        for pattern, symbol in replacements.items():
            line = re.sub(pattern, f' {symbol} ', line)

        return line