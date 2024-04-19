import openai
import requests

OPENAI_API_KEY = 'PLACEHOLDER FOR YOUR API KEY'
openai.api_key = OPENAI_API_KEY

def generate_content(prompt):
    try:
        # Generate content using OpenAI API in a chat-based approach.
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message['content']
    except requests.exceptions.ReadTimeout:
        print("Timeout error. Retrying...")
        return generate_content(prompt)  # Retry the same prompt
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string in case of other errors

def main():
    category = input("Enter a category or topic for the book: ")

    # Initial conversation history
    conversation_history = [
        {
            "role": "user",
            "content": ""
        }
    ]

    outline_prompt = f"Generate a book outline for a {category} book that is 60,000 words in total. Make each chapter have 5 bullet points after the chapter title. There must be 12 chapters. Do not write anything in the response after the last bullet point of the last chapter is written."
    outline = generate_content(outline_prompt)
    conversation_history.append({"role": "user", "content": outline_prompt})

    # Print the generated book outline
    print("\nGenerated Book Outline:\n", outline)

    # Split the outline into lines
    lines = outline.split("\n")

    book_content = []
    style_instruction = "I want each paragraph to be exactly 8 sentences long. Please ensure this style throughout the content."

    for idx, line in enumerate(lines):
        if not line.strip():  # Skip empty lines or lines with only whitespace
            continue
        elif "Chapter" in line:
            book_content.append(line)
        elif "Epilogue" in line or "Outline" in line or "Conclusion" in line or "Title" in line:
            # Store the line in the conversation history but do not generate content for it
            conversation_history.append({"role": "user", "content": line})
        else:
            print(f"\nGenerating content for line {idx+1} based on: {line}")
            prompt = f"{style_instruction} Now, write 1000 words based on: {line}."
            section_content = generate_content(prompt)
            conversation_history.append({"role": "user", "content": prompt})
            book_content.append(section_content)
            print(f"Completed content for line {idx+1}")

    # Save the entire content
    with open("generated_book.txt", "w") as file:
        file.write("\n\n".join(book_content))
    print("\nBook content saved to 'generated_book.txt'")
    print("Program completed. Exiting...")
    exit()

if __name__ == "__main__":
    main()
