import os
import csv
import re
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")

SCRIPTS_FOLDER = os.path.join(DATA_DIR, "formatted_scripts")  # input folder
OUTPUT_CSV = os.path.join(DATA_DIR, "simpsons_dialogue_cleaned.csv")
STATS_CSV = os.path.join(DATA_DIR, "character_line_counts.csv")

# Regex for a character cue
CHARACTER_RE = re.compile(
    r"""
    ^\s*                                  # optional indent
    ([A-Z][A-Z0-9\s\.'#\-]+?)             # character name
    \s*(?:\([A-Z0-9\s\.'\-]+\))?          # optional (V.O.) or (CONT'D)
    \s*$                                  # line ends
    """, re.VERBOSE
)

# Lines that are clearly not dialogue
NON_DIALOGUE_PATTERNS = [
    r"^FADE IN", r"^FADE OUT", r"^CUT TO",
    r"^INT\.", r"^EXT\.", r"^DISSOLVE TO",
    r"^SFX", r"^JINGLE", r"^MUSIC",
    r"^\(.*?\)$",
    r"^-{3,}",
    r"^\*",
    r"^REVISED",
    r"^FINAL",
    r"^TABLE DRAFT",
    r"^DELIVERY",
    r"^DRAFT",
    r"^Scene \d+",
    r"^PAGE \d+",
    r"^Sce+ne? \d+",
    r"^Seene $",
    r"\d+/\d+/\d+",  # Dates like 3/20/90
]

EPISODE_TITLE_PATTERNS = [
    r"^BART THE GENIUS$",
    r"^HOMER'S ODYSSEY$",
    r"^SOME ENCHANTED EVENING$",
    r"^THERE'S NO DISGRACE LIKE HOME$",
    r"^MOANING LISA$",
    r"^SIMPSONS ROASTING ON AN OPEN FIRE$",
    r"^THE CALL OF THE SIMPSONS$",
    r"^HOMER'S NIGHT OUT$",
    r"^BART THE GENERAL$",
    r"^THE TELLTALE HEAD$",
    r"^LIFE ON THE FAST LANE$",
    r"^KRUSTY GETS BUSTED$",
    r"^THE CREPES OF WRATH$",
    r"^TWO CARS IN EVERY GARAGE AND THREE EYES ON EVERY FISH$",
    r"^SIMPSON ANND DELILAH$",
    r"^BART GETS AN F$",
    r"^TREEHOUSE OF HORROR$",
    r"^DANCIN' HOMER$",
    r"^BART THE DAREDEVIL$",
    r"^BART VS. THANKSGIVING$",
    r"^DEAD PUTTING SOCIETY$",
    r"^ITCHY & SCRATCHY & MARGE$",
    r"^BART GETS HIT BY A CAR$",
    r"^STARK RAVING DAD$",
    r"^BART THE MURDERER$",
    r"^LIKE FATHER, LIKE CLOWN$",
    r"^LISA'S PONY$",
    r"^BURNS VERKAUFEN DER KRAFTWERK$",
    r"^RADIO BART$",
    r"^HOMER ALONE$",
    r"^SEPARATE VOCATIONS$",
    r"^A STREETCAR NAMED MARGE$",
    r"^BART'S FRIEND FALLS IN LOVE$",
    r"^BROTHER, CAN YOU SPARE TWO DIMES$",
    r"^TREEHOUSE OF HORROR III$",
    r"^NEW KID ON THE BLOCK$",
    r"^MR. PLOW$",
    r"^HOMER'S TRIPLE BYPASS$",
    r"^I LOVE LISA$",
    r"^LAST EXIT TO SPRINGFIELD$",
    r"^WHACKING DAY$",
    r"^KRUSTY GETS KANCELLED$",
    r"^HOMER'S BARBERSHOP QUARTET$",
    r"^LISA VS. MALIBU STACY$",
    r"^SWEET SEYMOUR SKINNER'S BAADASSSSS SONG$",
    r"^HOMER BADMAN$",
    r"^WHO SHOT MR. BURNS\? \(PART ONE\)$",
    r"^WHO SHOT MR. BURNS\? \(PART TWO\)$",
    r"^HOME SWEET HOMEDIDDLY-DUM-DOODILY$",
    r"^VIVA NED FLANDERS$",
    r"MAYORED TO THE MOB$",
    r"^TRASH OF THE TITANS$",
    r"^TREEHOUSE OF HORROR VI$",
    r"^BART SELLS HIS SOUL$",
    r"^THE LAST TEMPTATION OF KRUST$",
    r"^HOMER THE SMITHERS$",
    r"^MARGE GETS A JOB$",
    r"^SELMA'S CHOICE$",
    r"^MARGE IN CHAINS$",
    r"^22 SHORT FILMS ABOUT SPRINGFIELD$",
]

# Scene direction patterns that shouldn't be treated as characters
SCENE_PATTERNS = [
    r"^INT\.",
    r"^EXT\.",
    r"^CLOSE UP",
    r"^CLOSEUP",
    r"^CLOSE-UP",
    r"^MONTAGE$",
    r"^NEW ANGLE$",
    r"^ON COUCH$",
    r"^ON TV$",
    r"^STAGE$",
    r"^BACK TO",
    r"^THE SIMPSONS$",
    r"P\.O\.V\.",
    r"- CONTINUOUS$",
    r"- MORNING$",
    r"- NIGHT$",
    r"- DAY$",
    r"- LATER$",
    r"^ACT (ONE|TWO|THREE|FOUR)",
    r"^ON ",
    r"^WIDE SHOT",
    r"^LONG SHOT",
    r"^CAMERA ",
    r"^PULL BACK",
    r"^PULL IN",
    r"^CUT WIDE",
    r"^REVERSE ANGLE",
    r"^FREEZE FRAME",
    r"^RIPPLE DISSOLVE",
    r"^DISSOLVE BACK",
    r"^SLOW MOTION",
    r"^TRAINING MONTAGE",
    r"^BY$",
    r"^BEHIND ",
    r"^ENTRANCE TO",
    r"^IN ANOTHER",
    r"^WE CUT",
    r"^DURING THE FOLLOWING$",
]

# Script metadata patterns to filter from dialogue
SCRIPT_METADATA_PATTERNS = [
    r"REVISED.*?DRAFT",
    r"FINAL.*?DRAFT",
    r"TABLE.*?DRAFT",
    r"DELIVERY.*?DRAFT",
    r"^DRAFT\b",
    r"Scene \d+",
    r"PAGE \d+",
    r"\d+/\d+/\d+",  # Dates
    r"^(REVISED|FINAL|TABLE|DELIVERY)\b",
]

# Manual character mapping: maps variant names to canonical names
CHARACTER_MAPPING = {
    "MONROE": "MARVIN MONROE",
    "MARVIN MONROE": "MARVIN MONROE",
    "PRYOR": "PRYOR",
    "KRABAPPEL": "KRABAPPEL",
    "KRABAPPLE": "KRABAPPEL",
    "SKINNER": "SKINNER",
    "PRINCIPAL SKINNER": "SKINNER",
    "SEYMOUR SKINNER": "SKINNER",
    "Flanders": "NED FLANDERS",
    "BURNS": "BURNS",
    "BOB": "SIDESHOW BOB",
    "SIDESHOW BOB": "SIDESHOW BOB",
    "SISDESHOW BOB": "SIDESHOW BOB",
    "BOTZ": "BOTZ",
    "COTZ": "BOTZ",
    "MELON": "MELON",
    "WIGGUM": "CHIEF WIGGUM",
    "POLICE CHIEF WIGGUM": "CHIEF WIGGUM",
    "CHIEF WIGGUM": "CHIEF WIGGUM",
    "BROCKMAN": "KENT BROCKMAN",
    "KENT BROCKMAN": "KENT BROCKMAN",
    "GRAMPA": "GRANDPA",
    "GRANDPA": "GRANDPA",
    "HIBBERT": "HIBBERT",
    "DOCTOR HIBBERT": "HIBBERT",
    "LOVEJOY": "LOVEJOY",
    "REV. LOVEJOY": "LOVEJOY",
    "REVEREND LOVEJOY": "LOVEJOY",
    "HELEN LOVEJOY": "HELEN LOVEJOY",
    "CRUSTY": "KRUSTY",
    "KRUSTY": "KRUSTY",
    "WINFIELD": "OLD MAN WINFIELD",
    "OLD MAN WINFIELD": "OLD MAN WINFIELD",
    "QUIMBY": "MAYOR QUIMBY",
    "MAYOR QUIMBY": "MAYOR QUIMBY",
    "NED": "NED FLANDERS",
    "FLANDERS": "NED FLANDERS",

}

def is_scene_direction(line):
    stripped = line.strip()
    for pat in NON_DIALOGUE_PATTERNS:
        if re.match(pat, stripped):
            return True
    if stripped.isupper() and len(stripped.split()) <= 4 and not stripped.endswith('.'):
        return True
    return False

def is_script_metadata(line):
    stripped = line.strip()
    for pat in SCRIPT_METADATA_PATTERNS:
        if re.search(pat, stripped, re.IGNORECASE):
            return True
    return False

def is_episode_title_line(name):
    for pat in EPISODE_TITLE_PATTERNS:
        if re.match(pat, name):
            return True
    words = name.split()
    if len(words) >= 4:
        return True
    return False

def is_scene_annotation(name):
    for pat in SCENE_PATTERNS:
        if re.search(pat, name):
            return True
    return False

def normalize_character_name(name):
    name = re.sub(r"'S\s.*$", "", name)
    name = re.sub(r"\s+VOICE$", "", name)
    name = re.sub(r"-ISH\s.*$", "", name)
    name = re.sub(r"^(DR|MR|MRS|MS|MISS|REV|PROF)\.?\s+", "", name)
    name = re.sub(r"\.+\s*-+.*$", "", name)
    name = re.sub(r"\s+", " ", name).strip()
    
    if name in CHARACTER_MAPPING:
        name = CHARACTER_MAPPING[name]
    
    return name

def should_keep_character(name):
    if is_episode_title_line(name):
        return False
    if is_scene_annotation(name):
        return False
    if len(name) <= 1:
        return False
    return True

def clean_dialogue(text):
    text = re.sub(r"\([^)]*\)", "", text).strip()
    return text

def save_dialogue_block(dialogues, character, dialogue_lines):
    if character and dialogue_lines:
        combined_dialogue = " ".join(dialogue_lines)
        if combined_dialogue:
            dialogues.append((character, combined_dialogue))

def extract_episode_title(path):
    filename = os.path.basename(path)
    title = os.path.splitext(filename)[0]
    
    # Try to read the first few lines to find the episode title
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i > 20:
                    break
                stripped = line.strip()
                for pat in EPISODE_TITLE_PATTERNS:
                    if re.match(pat, stripped):
                        return stripped
    except:
        pass
    
    # Clean up filename to make it more readable
    title = re.sub(r"[_-]", " ", title)
    title = title.upper()
    
    return title

def extract_dialogue_from_file(path):
    dialogues = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    
    current_character = None
    current_dialogue_lines = []
    
    for line in lines:
        raw = line.rstrip("\n")
        
        # Skip script metadata lines
        if is_script_metadata(raw):
            continue
        
        # Check if line is a character cue
        m = CHARACTER_RE.match(raw)
        if m:
            # ALWAYS save previous dialogue block when we see a character name
            save_dialogue_block(dialogues, current_character, current_dialogue_lines)
            
            # Start new character block
            name = m.group(1).strip()
            if len(name.split()) <= 5:
                current_character = name
                current_dialogue_lines = []
            else:
                current_character = None
                current_dialogue_lines = []
            continue
        # Check for blank line → end of dialogue block
        if not raw.strip():
            # Save the current dialogue block and reset
            save_dialogue_block(dialogues, current_character, current_dialogue_lines)
            current_character = None
            current_dialogue_lines = []
            continue
        
        # Check if this is dialogue from the current character
        if current_character and not is_scene_direction(raw):
            text = clean_dialogue(raw)
            if text:
                current_dialogue_lines.append(text)
    
    # Don't forget the last dialogue block
    save_dialogue_block(dialogues, current_character, current_dialogue_lines)
    
    return dialogues

def main():
    # Extract all dialogue from script files
    all_dialogue = []
    for filename in os.listdir(SCRIPTS_FOLDER):
        if filename.lower().endswith((".txt", ".script")):
            fullpath = os.path.join(SCRIPTS_FOLDER, filename)
            
            # Extract episode title
            episode_title = extract_episode_title(fullpath)
            
            # Extract dialogues
            dialogues = extract_dialogue_from_file(fullpath)
            
            # Add episode title to each dialogue entry
            for character, dialogue in dialogues:
                all_dialogue.append((character, dialogue, episode_title))
    
    # Clean and normalize character names
    cleaned_data = []
    character_stats = defaultdict(int)
    
    for character, dialogue, episode in all_dialogue:
        # Check if we should keep this entry
        if not should_keep_character(character):
            continue
        
        # Normalize the character name
        normalized_character = normalize_character_name(character)
        
        # Track statistics
        character_stats[normalized_character] += 1
        
        # Add to cleaned data
        cleaned_data.append({
            "character": normalized_character,
            "dialogue": dialogue,
            "episode": episode
        })
    
    # Filter out characters with only 1 dialogue block
    cleaned_data = [
        entry for entry in cleaned_data
        if character_stats[entry["character"]] > 9
    ]
    character_stats = {char: count for char, count in character_stats.items() if count > 9}
    
    # Sort by episode title
    cleaned_data.sort(key=lambda x: x["episode"])
    
    # Write cleaned dialogue CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["character", "dialogue", "episode"])
        writer.writeheader()
        writer.writerows(cleaned_data)
    
    # Write character line counts to a separate CSV
    sorted_characters = sorted(character_stats.items(), key=lambda x: x[1], reverse=True)
    
    with open(STATS_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["character", "dialogue_blocks"])
        for character, count in sorted_characters:
            writer.writerow([character, count])
    
    print(f"\nCharacter dialogue block counts saved to {STATS_CSV}")
    print(f"Total unique characters: {len(sorted_characters)}")


if __name__ == "__main__":
    main()