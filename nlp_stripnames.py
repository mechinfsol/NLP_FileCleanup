import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.corpus import stopwords
import os

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('stopwords')

def clean_names(input_folder, output_folder):
    # Define non-human entries for additional filtering
    non_human_names = {
        "corp", "llc", "inc", "corporation", "university", "college", "institute", "foundation", "association",
        "agency", "partnership", "society", "council", "bureau", "office", "department", "division",
        "committee", "board", "group", "business", "company", "enterprise", "organization", "agency",
        "studio", "gym", "school", "library", "church", "temple", "mosque", "synagogue", "festival", "conference",
        "seminar", "workshop", "forum", "clinic", "hospital", "bank", "museum", "gallery", "park", "garden",
        "reserve", "store", "restaurant", "cafe", "hotel", "resort", "theatre", "arena", "stadium", "mall",
        "market", "shop", "emporium", "plaza", "admin"
    }
    stop_words = set(stopwords.words('english'))

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)
            output_file_name = "processed_" + file_name
            output_path = os.path.join(output_folder, output_file_name)

            try:
                with open(file_path, "r", encoding='ISO-8859-1') as file:
                    content = file.read()
                sentences = sent_tokenize(content)
                human_names = []

                for sentence in sentences:
                    words = word_tokenize(sentence)
                    tagged_words = pos_tag(words)
                    ne_tagged_words = ne_chunk(tagged_words)
                    for entity in ne_tagged_words:
                        if hasattr(entity, 'label') and entity.label() == 'PERSON':
                            name = ' '.join(c[0] for c in entity)
                            # Further filter names to remove stopwords and non-human names
                            if name.lower() not in non_human_names and not any(word.lower() in stop_words for word in name.split()):
                                human_names.append(name)

                # Sort names alphabetically before writing to file
                human_names_sorted = sorted(set(human_names), key=str.lower)
                formatted_output = ", ".join(f"'{name}'" for name in human_names_sorted)

                with open(output_path, "w", encoding='ISO-8859-1') as output_file:
                    output_file.write(formatted_output)
                print(f"Processed {file_name} successfully.")

            except Exception as e:
                print(f"Failed to process {file_name}: {str(e)}")

# Usage
input_folder = r"Input"  # Change this to your input folder path
output_folder = r"Output"  # Change this to your output folder path
clean_names(input_folder, output_folder)
