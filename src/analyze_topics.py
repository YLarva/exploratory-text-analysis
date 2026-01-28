import pandas as pd
import glob
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS

# Mapping of Annotation ID to Topic Name (based on chat history)
TOPIC_MAPPING = {
    1: "Characters - Themselves",
    2: "Characters - Core Simpsons Family",
    3: "Characters - Non-core Family",
    4: "Physical - Location",
    5: "Physical - Object",
    6: "Non-physical - Event",
    7: "Non-physical - Emotion",
    8: "Non-physical - Opinion/Judgement"
}

def load_data(data_dir="Data"):
    """Loads and combines annotated CSV files."""
    all_files = glob.glob(os.path.join(data_dir, "*_annotated_dialogue.csv"))
    df_list = []
    for filename in all_files:
        read_success = False
        for encoding in ['utf-8', 'cp1252', 'latin1']:
            try:
                df = pd.read_csv(filename, encoding=encoding)
                df_list.append(df)
                read_success = True
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading {filename} with {encoding}: {e}")
        
        if not read_success:
            print(f"Failed to read {filename} with any supported encoding.")
    
    if not df_list:
        raise ValueError("No CSV files found!")
        
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

def preprocess_text(text):
    """Basic text cleaning."""
    if not isinstance(text, str):
        return ""
    # Remove non-alphabetic characters (keep spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Lowercase
    text = text.lower()
    return text

def compute_tfidf_top_words(df):
    """Computes TF-IDF and returns top 10 words per topic."""
    
    # Group by annotation (topic)
    # We treat all dialogue in a topic as one big document
    topic_docs = df.groupby('annotation')['dialogue'].apply(lambda x: ' '.join(x.astype(str))).reset_index()
    
    # Preprocess
    topic_docs['clean_text'] = topic_docs['dialogue'].apply(preprocess_text)
    
    # TF-IDF Vectorization
    # Use standard english stop words, plus maybe some common conversational fillers if needed
    # For now, standard list is a good start.
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(topic_docs['clean_text'])
    feature_names = vectorizer.get_feature_names_out()
    
    results = {}
    
    for idx, row in topic_docs.iterrows():
        topic_id = row['annotation']
        
        # Get the row from the TF-IDF matrix corresponding to this topic
        # Note: idx in iterrows might not match matrix index if topics are missing, 
        # but here we reset_index so it should match the order in topic_docs
        tfidf_scores = tfidf_matrix[idx].toarray().flatten()
        
        # Get top 10 indices
        top_indices = tfidf_scores.argsort()[-10:][::-1]
        
        top_words = [(feature_names[i], tfidf_scores[i]) for i in top_indices]
        results[topic_id] = top_words
        
    return results

def main():
    try:
        df = load_data()
        print(f"Loaded {len(df)} lines of dialogue.")
    except Exception as e:
        print(f"Failed to load data: {e}")
        return

    print("\nComputing TF-IDF...")
    try:
        top_words_by_topic = compute_tfidf_top_words(df)
    except Exception as e:
        print(f"Analysis failed: {e}")
        return

    print("\nTop 10 Words per Topic:")
    print("=" * 60)
    
    # Sort by topic ID for cleaner output
    for topic_id in sorted(top_words_by_topic.keys()):
        topic_name = TOPIC_MAPPING.get(topic_id, f"Topic {topic_id}")
        words = top_words_by_topic[topic_id]
        
        print(f"\n[{topic_id}] {topic_name}")
        print("-" * 30)
        for word, score in words:
            print(f"  {word:<15} ({score:.4f})")

if __name__ == "__main__":
    main()
