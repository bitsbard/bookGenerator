# Book Generator Script

This Python script, `generate_book.py`, automates the generation of book content using OpenAI's GPT-3.5 Turbo model. The script interacts with the OpenAI API to produce a structured outline and detailed content for a book based on user-defined topics or categories.

## Requirements

- Python 3.x
- `openai` Python library
- `requests` Python library

## Installation

Before running the script, ensure that you have the necessary Python libraries installed. You can install these using pip:

```bash
pip install openai requests
```

## Configuration

Set your OpenAI API key in the script:

```python
OPENAI_API_KEY = 'YOUR_API_KEY_HERE'
```

Replace `'YOUR_API_KEY_HERE'` with your actual OpenAI API key.

## Usage

Run the script using Python:

```bash
python book_generate.py
```

Follow the on-screen prompts to input the category or topic for the book. The script will first generate a detailed outline for a 60,000-word book with 12 chapters, each chapter containing 5 key points. After the outline, it will proceed to generate content for each chapter following the specified style requirements.

## How It Works

1. **Input Topic**: The user inputs a category or topic for the book.
2. **Generate Outline**: The script uses the OpenAI API to generate a structured outline.
3. **Generate Content**: For each item in the outline, the script will generate detailed content ensuring each paragraph contains exactly 8 sentences.
4. **Error Handling**: Includes basic error handling for timeouts and other exceptions.
5. **Output**: The generated book content is saved to `generated_book.txt`.
