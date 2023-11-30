from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import os
from IPython.display import display, Markdown

reviews = open( './review.txt', 'r')
reviews_content = reviews.read()

def display_md(chat_completion):
    display(Markdown(chat_completion.choices[0].message.content))

def chat(prompt):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=os.getenv("CHATGPT_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are now a restaurant management expert.",},
            {"role": "user", "content": prompt},
        ],
        model="gpt-4",
    )

    return chat_completion

if __name__ == "__main__":
    prompt = "These are the reviews of one restaurant. {r} Summarize the highlights and weaknesses of this restaurant.".format(
            r=reviews_content)

    chat_completion = chat(prompt)

    print(chat_completion.choices[0].message.content)
