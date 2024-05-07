import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import re
import os

# Download the required NLTK resources if not already available
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def clean_names(input_folder, output_folder):
    # Define non-name entries, business-related keywords, and character filters
    non_names = [
        "Corp", "Counseling", "Creative", "Country", "County", "Development", "Direction", "Discovering", "Discovery",
        "Divine", "Dream", "Elite", "Embrace", "Embracing", "Enhancement", "Enterprises", "Essential", "Everyday",
        "Family", "Financial", "Fiscal", "For", "Future", "Generations", "Global", "Good", "Graciously", "Guardian",
        "Guardians", "Hard", "Healing", "Healthy", "Helping", "Honest", "Human", "Inc.", "Intensive", "Ideal",
        "LLC", "Corporation", "Group", "Services", "Solutions", "Systems", "Management", "Enterprise", "Technologies",
        "Agency", "Consulting", "Partners", "Studio"
    ]

    # Pronoun POS tags to filter out
    pronoun_tags = {'PRP', 'PRP$'}

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)
            # Construct output path with 'processed_' prefix
            output_file_name = "processed_" + file_name
            output_path = os.path.join(output_folder, output_file_name)

            # Read the original file with a specified encoding to handle non-standard characters
            with open(file_path, "r", encoding='ISO-8859-1') as file:
                content = file.read()
                # Extract names using regex, splitting by ', and removing any trailing characters
                original_names = re.findall(r"'([^']*)'", content)

            # Filter and format the output
            refined_names = [
                name for name in original_names 
                if not any(non_name.lower() in name.lower() for non_name in non_names)
                and "_" not in name and "@" not in name and "." not in name
                and len(name.strip()) > 2  # Excludes 1 or 2 character names
                and not any(tag in pronoun_tags for _, tag in pos_tag(word_tokenize(name)))
                and name.strip() != ""
            ]

            # Format the output as comma-separated values enclosed in single quotes
            formatted_output = ", ".join(f"'{name}'" for name in refined_names)

            # Write the filtered and formatted list to a new file
            with open(output_path, "w", encoding='ISO-8859-1') as output_file:
                output_file.write(formatted_output)

# Usage
input_folder = r"C:\Users\ashdi\Downloads\output_1-20240506T193128Z-001\Input"  # Change this to your input folder path
output_folder = r"C:\Users\ashdi\Downloads\output_1-20240506T193128Z-001\Output"  # Change this to your output folder path
clean_names(input_folder, output_folder)
