from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import os
from IPython.display import display, Markdown

class GPT:
    def __init__(self):
        self.api_key = os.getenv("CHATGPT_API_KEY"),
        self. client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key = self.api_key
        )

    def display_md(chat_completion):
        display(Markdown(chat_completion.choices[0].message.content))

    def chat(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are now a restaurant management expert.",},
                {"role": "user", "content": prompt},
            ],
            model="gpt-4",
        )
        return chat_completion

if __name__ == "__main__":
    reviews = open('./review.txt', 'r', encoding='UTF-8')
    reviews_content = reviews.read()
    prompt = "These are the reviews of one restaurant. {r} Summarize the highlights and weaknesses of this restaurant.".format(
            r=reviews_content)

    GPT = GPT()

    chat_completion = GPT.chat(prompt)

    print(chat_completion.choices[0].message.content)
