import os, re
from pathlib import Path


# Clear the screen and enable colors for highlighting matched words
os.system("cls")


# Highlight matched keywords in the email text in yellow
def highlight_matches(email, keywords):
    for word in keywords:
        pattern = re.compile(rf"({re.escape(word)})", re.IGNORECASE)
        email = pattern.sub("\033[93m" + r"\1" + "\033[0m", email)
    return email


def main():
    # Ask where their email(s) are located and store it
    folder_path = input("Enter folder path containing your .txt emails: ").strip()
    folder = Path(folder_path)

    # If it doesn't exist, exit program
    if not folder.is_dir():
        print(f"Error: '{folder}' does not exist or is not a valid directory.")
        return


    # Let user input a word they want to find and separate it with commas
    keywords_input = input("Enter keyword(s) to search for (separated with commas): ")
    keywords = [word.strip() for word in keywords_input.split(",") if word.strip()]


    # Declaration / Get files that end in .txt and put them in a list
    total_matches = 0
    keyword_totals = {word: 0 for word in keywords}
    files = sorted(folder.glob("**/*.txt"))


    # Find the index and loop through each file starting at index 1
    for i, filename in enumerate(files, start = 1):
        # Open the file in read mode with UTF-8 encoding (able to read special characters)
        # Read the entire content of the email and convert it into a string
        email = filename.read_text(encoding = 'utf-8')

        # Create empty list to hold matched words every loop to reset it
        keyword_counts = {}
        current_loop_match = 0

        # Check if (each) keyword(s) exists in email(s) and add them to the list
        for word in keywords:
            matches = re.findall(re.escape(word), email, re.IGNORECASE)
            # If there is a match...
            if matches:
                keyword_counts[word] = len(matches)
                keyword_totals[word] += len(matches)

        # If at least one word is found...
        if keyword_counts:
            total_matches += 1

            print("=" * 60)
            # Print the filename and the keywords that were matched
            print(f"File: {filename.name} - Matches found for: {keywords}")
            # Find how many times that word appeared in an email
            for word, count in keyword_counts.items():
                print(f"\t'{word}' found {count} time(s)")
            print("-" * 60 + "\n")
            # Print the entire email contents with matched words highlighted
            print(highlight_matches(email.strip(), keywords))
            print("\n" + "=" * 60 + "\n")

    print(f"\nTotal files matched: {total_matches} out of {len(files)}")
    for word, total in keyword_totals.items():
        print(f"'{word}' appeared {total} time(s) across all files.")

if __name__ == "__main__":
    main()