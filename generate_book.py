import openai
import requests
import time
from typing import List, Dict, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configuration Constants
CONFIG = {
    "API_TIMEOUT": 30,
    "MAX_RETRIES": 5,
    "CHAPTERS": 12,
    "TARGET_WORDS": 60000,
    "PARAGRAPH_LENGTH": 6,  # Sentences
    "SECTION_WORDS": 1000,
    "STYLE_GUIDE": {
        "voice": "authoritative yet accessible",
        "pacing": "methodical with narrative flourishes",
        "examples": "contemporary and historical",
        "structure": "thesis-support-conclusion",
        "diversity": "include global perspectives",
        "language": "avoid jargon without explanation"
    }
}

openai.api_key = 'YOUR_API_KEY_HERE'  # Consider using environment variables in production

class LiteraryAgent:
    """Orchestrates book creation with editorial oversight"""
    
    def __init__(self):
        self.manuscript = []
        self.style_str = self._create_style_directive()
        
    def _create_style_directive(self) -> str:
        """Construct detailed style instructions for GPT"""
        return f"""Craft prose with:
        - {CONFIG['STYLE_GUIDE']['voice']} voice
        - {CONFIG['STYLE_GUIDE']['pacing']} pacing
        - {CONFIG['STYLE_GUIDE']['examples']} examples
        - {CONFIG['STYLE_GUIDE']['structure']} paragraph structure
        - {CONFIG['STYLE_GUIDE']['diversity']} references
        - {CONFIG['STYLE_GUIDE']['language']}
        - Vivid sensory descriptions
        - Rhetorical questions for engagement
        - Seamless chapter transitions
        - Each paragraph exactly {CONFIG['PARAGRAPH_LENGTH']} sentences"""
        
    @retry(stop=stop_after_attempt(CONFIG["MAX_RETRIES"]),
           wait=wait_exponential(multiplier=1, min=4, max=60),
           retry=retry_if_exception_type(requests.exceptions.Timeout))
    def generate_text(self, prompt: str) -> Optional[str]:
        """Robust content generation with enhanced error handling"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"{self.style_str}\n\n{prompt}"}],
                temperature=0.7,
                max_tokens=3000,
                request_timeout=CONFIG["API_TIMEOUT"]
            )
            return response.choices[0].message['content']
        except Exception as e:
            print(f"Critical failure: {str(e)}")
            return None

    def architect_outline(self, category: str) -> str:
        """Create complex book structure"""
        prompt = f"""Create a rigorous {category} nonfiction outline with:
        - 1 Epigraph
        - 1 Prologue (historical context)
        - {CONFIG['CHAPTERS']} chapters, each containing:
          * Chapter title with subtitle
          * 1 Conceptual framework
          * 3 Case studies (1 Western, 1 Eastern, 1 Modern)
          * 2 Controversies/debates
          * 1 Practical application section
        - 1 Epilogue (future implications)
        - 1 Author's Note
        - 1 Appendix Framework
        - 1 Annotated Bibliography"""
        return self.generate_text(prompt)

    def forge_chapter(self, prompt: str) -> str:
        """Generate deep, interconnected content"""
        enhanced_prompt = f"""Develop {CONFIG['SECTION_WORDS']} words on: {prompt}
        Include:
        - Primary source analysis
        - Counterargument refutation
        - Interdisciplinary connections
        - Real-world implementation challenges
        - Projection of future developments"""
        return self.generate_text(enhanced_prompt) or "CONTENT UNAVAILABLE"

    def compile_manuscript(self, elements: List[str]):
        """Assemble components with professional formatting"""
        self.manuscript = ["\n\n※ ※ ※\n\n".join(elements)]  # Section break convention

class ProductionStudio:
    """Handlers for user interaction and output"""
    
    @staticmethod
    def get_category() -> str:
        while True:
            category = input("Enter intellectual domain (e.g., 'Quantum Anthropology'): ")
            if len(category) > 3:
                return category
            print("Please provide substantive category")

    @staticmethod
    def save_tome(content: List[str]):
        with open("magnum_opus.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(content))
        print("\nManuscript archived in 'magnum_opus.txt'")

def main():
    print("=== AION Manuscript Forge ===")
    print("Crafting Monographs for the Discerning Intellect\n")
    
    studio = ProductionStudio()
    scribe = LiteraryAgent()
    
    category = studio.get_category()
    
    print("\nArchitecting Tome Structure...")
    outline = scribe.architect_outline(category)
    print("\nGenerated Outline:\n" + outline)
    
    print("\nCommencing Knowledge Synthesis...")
    components = []
    for section in outline.split("\n"):
        if not section.strip():
            continue
        if "Chapter" in section:
            print(f"\nForging {section}...")
            content = scribe.forge_chapter(section)
            components.append(f"{section}\n\n{content}")
            print(f"Completed {section}")
        else:
            components.append(section)
    
    scribe.compile_manuscript(components)
    studio.save_tome(scribe.manuscript)
    print("\nOpus Complete. Submit to Academic Press.")

if __name__ == "__main__":
    main()
