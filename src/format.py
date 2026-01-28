import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")

SCRIPTS_FOLDER = os.path.join(DATA_DIR, "raw_scripts")  # Data/scripts
OUTPUT_FOLDER = os.path.join(DATA_DIR, "formatted_scripts")  # Data/formatted_scripts

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Detect standalone CHARACTER CUE (all caps)
CHAR_RE = re.compile(r'^[A-Z][A-Z0-9 \.\'\-]{1,40}$')

# Detect CHARACTER + inline dialogue (e.g., "HOMER Oh, it was great.")
INLINE_RE = re.compile(r'^([A-Z][A-Z0-9 \.\'\-]{1,40})\s+(.*)$')


def format_script_text(text):
    lines = text.splitlines()
    formatted = []

    current_character = None

    for raw in lines:
        line = raw.strip()

        # Skip pure blank lines → add blank line to output
        if not line:
            formatted.append("")
            continue

        # CHARACTER + dialogue on same line
        inline = INLINE_RE.match(line)
        if inline:
            name, dialogue = inline.groups()
            if name.isupper() and len(name.split()) <= 4:
                current_character = name
                formatted.append(current_character)
                formatted.append(dialogue.strip())
                continue

        # Standalone character cue
        if CHAR_RE.match(line):
            current_character = line.strip()
            formatted.append(current_character)
            continue

        # Dialogue line (parentheticals or spoken text)
        # A dialogue line should only appear if we are currently in a character block
        if current_character and (
            line.startswith("(") or         # Parenthetical
            not line[0].isupper()          # Lowercase start = dialogue
        ):
            formatted.append(line)
            continue

        # Otherwise → reset character context & treat as ACTION
        current_character = None
        formatted.append(line)

    return "\n".join(formatted)


def process_all_scripts():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filename in os.listdir(SCRIPTS_FOLDER):
        if not filename.lower().endswith(".txt"):
            continue

        input_path = os.path.join(SCRIPTS_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        formatted = format_script_text(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(formatted)



if __name__ == "__main__":
    process_all_scripts()
