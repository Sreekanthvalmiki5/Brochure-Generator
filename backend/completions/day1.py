import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
from IPython.display import Markdown, display
# openai_api_key = os.getenv('OPENAI_API_KEY')
# anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
# google_api_key = os.getenv('GOOGLE_API_KEY')
# deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
# groq_api_key = os.getenv('GROQ_API_KEY')
# grok_api_key = os.getenv('GROK_API_KEY')
# openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
ollama_api_key = os.getenv('OLLAMA_API_KEY')

ANTHROPIC_API_URL = os.getenv('ANTHROPIC_API_URL', 'https://api.anthropic.com/v1')
GEMINI_API_URL = os.getenv('GEMINI_API_URL', 'https://gemini.googleapis.com/v1')
DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/v1')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')


# if openai_api_key:
#     print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
# else:
#     print("OpenAI API Key not set")
    
# if anthropic_api_key:
#     print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
# else:
#     print("Anthropic API Key not set (and this is optional)")

# if google_api_key:
#     print(f"Google API Key exists and begins {google_api_key[:2]}")
# else:
#     print("Google API Key not set (and this is optional)")

# if deepseek_api_key:
#     print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
# else:
#     print("DeepSeek API Key not set (and this is optional)")

# if groq_api_key:
#     print(f"Groq API Key exists and begins {groq_api_key[:4]}")
# else:
#     print("Groq API Key not set (and this is optional)")

# if grok_api_key:
#     print(f"Grok API Key exists and begins {grok_api_key[:4]}")
# else:
#     print("Grok API Key not set (and this is optional)")

# if openrouter_api_key:
#     print(f"OpenRouter API Key exists and begins {openrouter_api_key[:3]}")
# else:
#     print("OpenRouter API Key not set (and this is optional)")

if ollama_api_key:
    print(f"Ollama API Key exists and begins {ollama_api_key[:3]}")
class Day1:
    
    # anthropic = OpenAI(api_key=anthropic_api_key, base_url=ANTHROPIC_API_URL)
    # gemini = OpenAI(api_key=google_api_key, base_url=GEMINI_API_URL)
    # deepseek = OpenAI(api_key=deepseek_api_key, base_url=DEEPSEEK_API_URL)
    # groq = OpenAI(api_key=groq_api_key, base_url=GROQ_API_URL)
    # grok = OpenAI(api_key=grok_api_key, base_url=GROK_API_URL)
    # openrouter = OpenAI(base_url=OPENROUTER_API_URL, api_key=openrouter_api_key)
    ollama = OpenAI(api_key="ollama", base_url=OLLAMA_API_URL)
    def __init__(self):
        self.client = OpenAI(api_key="ollama", base_url=OLLAMA_API_URL)
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.gemini=OpenAI(api_key=os.getenv("GOOGLE_API_KEY"), base_url=GEMINI_API_URL)
        self.tell_a_joke = [
            {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
        ]
        self.dilemma_prompt = """
        You and a partner are contestants on a game show. You're each taken to separate rooms and given a choice:
        Cooperate: Choose "Share" — if both of you choose this, you each win $1,000.
        Defect: Choose "Steal" — if one steals and the other shares, the stealer gets $2,000 and the sharer gets nothing.
        If both steal, you both get nothing.
        Do you choose to Steal or Share? Pick one.
        """
        
      
      
    def test_ollama(self):
        response = self.ollama.chat.completions.create(
            model="llama3.2:latest",
            # model="qwen3:4b", 
            messages=self.tell_a_joke
        )
        print(response.choices[0].message.content)
        # print(response)
        # display(Markdown(response.choices[0].message.content))
    def easy_puzzle(self):
        response = self.ollama.chat.completions.create(
            model="llama3.2:latest", 
            messages=[
                {"role":"user","content":""""
                    On a bookshelf, two volumes of Pushkin stand side by side: the first and the second.
                    The pages of each volume together have a thickness of 2 cm, and each cover is 2 mm thick.
                    A worm gnawed (perpendicular to the pages) from the first page of the first volume to the last page of the second volume.
                    What distance did it gnaw through?
"""}
                #  {"role": "user", "content": "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."},
            ]
           
        )
        print(response.choices[0].message.content)
    def easy_puzzle_openai(self):
        response = self.openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                 {"role": "user", "content": self.dilemma_prompt},
            ]
        )
    def test_gemini(self):
        response = self.gemini.chat.completions.create(
            model="gemini-2.0-flash",
            messages=self.tell_a_joke
        )
        print(response.choices[0].message.content)
if __name__ == "__main__":
    day1 = Day1()
    # day1.test_ollama()
    day1.easy_puzzle()
    # day1.easy_puzzle_openai()
    # day1.test_gemini()
