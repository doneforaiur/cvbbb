import guidance
import openai
import os


if os.environ["OPENAI_API_KEY"] is None:
    print("OPENAI_API_KEY environment variable not set")
    os.exit(1)

openai.api_key = os.environ["OPENAI_API_KEY"]

guidance.llm = guidance.llms.OpenAI("text-davinci-003")

# define a guidance program that adapts proverbs
program = guidance("""Extract user's information from the text to JSON format.""")

# execute the program on a specific proverb
executed_program = program(
    user_info="Hello, my name is John, I am 25 years old.",
)

print(executed_program)

# ! TODO: Implement
def generate_pdf(text):
    return
