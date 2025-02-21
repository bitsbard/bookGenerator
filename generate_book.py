import openai
import requests

# Replace with your actual OpenAI API key
OPENAI_API_KEY = 'YOUR_API_KEY_HERE'
openai.api_key = OPENAI_API_KEY

def generate_content(prompt, max_retries=3):
    """
    Generate content using the OpenAI API with a retry mechanism for timeouts.
    
    Args:
        prompt (str): The prompt to send to the API.
        max_retries (int): Maximum number of retries for timeout errors.
    
    Returns:
        str: Generated content or an empty string if generation fails.
    """
    retries = 0
    while retries < max_retries:
        try:
            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message['content']
        except requests.exceptions.ReadTimeout:
            print("Timeout error occurred. Retrying...")
            retries += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""  # Return empty string for other errors
    print("Maximum retries exceeded. Skipping this section.")
    return ""

def parse_outline(outline):
    """
    Parse the book outline into a list of chapters with titles and bullet points.
    
    Args:
        outline (str): The raw outline text from the API.
    
    Returns:
        list: List of dictionaries, each containing 'title' and 'bullet_points'.
    """
    chapters = []
    lines = outline.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("Chapter"):
            title = line
            bullet_points = []
            # Collect the next 5 bullet points
            for j in range(1, 6):
                if i + j < len(lines):
                    bullet_line = lines[i + j].strip()
                    if bullet_line.startswith("-"):
                        # Remove the '-' prefix and extra whitespace
                        bullet_points.append(bullet_line[1:].strip())
            if len(bullet_points) == 5:  # Ensure exactly 5 bullet points
                chapters.append({"title": title, "bullet_points": bullet_points})
            i += 6  # Skip to the next chapter (title + 5 bullets)
        else:
            i += 1  # Skip non-chapter lines
    return chapters

def main():
    """Main function to generate a sophisticated book."""
    # Get the book category from the user
    category = input("Enter a category or topic for the book: ")

    # Define the style instruction
    style_instruction = "Each paragraph must be exactly 8 sentences long. Write in a formal, book-like style."

    # Generate the book outline
    outline_prompt = (
        f"Generate a book outline for a {category} book that is 60,000 words in total. "
        "Make each chapter have 5 bullet points after the chapter title. There must be 12 chapters. "
        "Do not write anything in the response after the last bullet point of the last chapter is written."
    )
    print("Generating book outline...")
    outline = generate_content(outline_prompt)
    if not outline:
        print("Failed to generate outline. Exiting...")
        exit()
    
    print("\nGenerated Book Outline:\n", outline)

    # Parse the outline into chapters
    chapters = parse_outline(outline)
    if len(chapters) != 12:
        print(f"Warning: Expected 12 chapters, but found {len(chapters)}. Proceeding anyway.")

    # Create the table of contents
    toc = "Table of Contents\n\n" + "\n".join([chapter['title'] for chapter in chapters]) + "\n"
    
    # Open the file in write mode and write content progressively
    with open("generated_book.txt", "w") as file:
        # Write the table of contents
        file.write(toc)
        file.write("\n")

        print("\nStarting book content generation. This may take a while...")
        
        # Generate content for each chapter
        for chapter_idx, chapter in enumerate(chapters, 1):
            # Write chapter separator and title
            file.write("\n*****\n\n")
            file.write(f"{chapter['title']}\n\n")
            print(f"Generating content for {chapter['title']} ({chapter_idx}/12)...")

            # Generate sections for each bullet point
            for bullet_idx, bullet in enumerate(chapter['bullet_points'], 1):
                prompt = (
                    f"{style_instruction} "
                    f"Write a section for the chapter titled '{chapter['title']}' in a book about {category}, "
                    f"based on the point: {bullet}. Aim for approximately 1,000 words."
                )
                print(f"  Generating section {bullet_idx}/5: {bullet[:50]}...")
                section_content = generate_content(prompt)
                if section_content:
                    file.write(section_content + "\n\n")
                else:
                    file.write("Section could not be generated due to errors.\n\n")
    
    print("\nBook content saved to 'generated_book.txt'")
    print("Program completed successfully.")

if __name__ == "__main__":
    main()
