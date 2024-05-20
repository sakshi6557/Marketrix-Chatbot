import requests
from bs4 import BeautifulSoup
import os
from groq import Groq
from dotenv import load_dotenv
import re

# Function to extract content from Marketrix website
def extract_content(url):
    header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant content from the webpage
    #content = soup.find('div', class_='content').text
    #return content
    result = ''

    text_elements = soup.get_text()
    cleaned_text = re.sub('\\s+', ' ', text_elements).strip()
    #print(cleaned_text)

    for data in soup.find_all("p"): 
         result += data.get_text()
    #print(data.get_text())  
    return cleaned_text

# Function to provide answers using Llama3 70B model
def answer_question(question):
    # Add code to interact with Llama3 70B model here
    # For simplicity, let's just return a dummy answer
    load_dotenv()
    model = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    user_message = "What is Live Meeting feature"
    system_prompt = "Your name is CB bot and you have to anwer questions based on the information provided on https://www.marketrix.ai/ about Marketrix.ai, if can't find an answer to that, return \"Sorry, I don't know the answer, try asking me about Marketrix\". Information extracted from Marketrix website:  " + content
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    chat_completion = model.chat.completions.create(
        messages= message,
        model="llama3-70b-8192",
    )

    #print(chat_completion.choices[0].message.content)


    return chat_completion.choices[0].message.content

# Example usage
marketrix_url = "https://www.marketrix.ai/"
content = extract_content(marketrix_url)
#print("Content from Marketrix website:", content)
# webdata = open("webpage_data.txt", "r")
# content = webdata.read()
# #if not content:
# #    content = extract_content(marketrix_url)
# webdata.close()

user_question = input("Ask a question about Marketrix: ")
answer = answer_question(user_question)
print("Answer:", answer)
