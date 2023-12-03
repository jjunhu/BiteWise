from openai import OpenAI
from dotenv import load_dotenv
import os
from IPython.display import display, Markdown
load_dotenv()

class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key = os.getenv("CHATGPT_API_KEY"))
        self.memory = []

    def push_mem(self, role, msg):
        self.memory.append({"role": role, "content": msg})

    def chat(self, file_content, prompt):
        file_prompt  = ""
        if file_content:
            file_prompt = "The file content is {f}".format(f=file_content)
        prompt = file_prompt + prompt

        self.push_mem("user", prompt)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are now a restaurant management expert.",},
                {"role": "user", "content": str(self.memory) + prompt},
            ],
            model="gpt-4-1106-preview",
        )
        self.push_mem("assistant", chat_completion.choices[0].message.content)
        return chat_completion

    def display_md(chat_completion):
        display(Markdown(chat_completion.choices[0].message.content))



if __name__ == "__main__":
    reviews = open('./review.txt', 'r', encoding='UTF-8')
    reviews_content = reviews.read()
    reviews.close()
    # prompt = "These are the reviews of one restaurant. {r} Summarize the highlights and weaknesses of this restaurant.".format(
    #         r=reviews_content)

    GPT = ChatBot()
    while 1:
        prompt = input()

        chat_completion = GPT.chat(prompt)
        print(chat_completion)
        # print(chat_completion.choices[0].message.content)
