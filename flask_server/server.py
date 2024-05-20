from flask import Flask, json, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Chatbot API Route
# @app.route("/chatbot", methods=['GET'])
# def index():
#     #return {'result': answer_question(user_question)}
#     return {'result':True}


def extract_content(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    text_elements = soup.get_text()
    cleaned_text = re.sub('\\s+', ' ', text_elements).strip()
    #print(cleaned_text)
    #webpage_data = open("webpage_data.txt",'w')
    #webpage_data.write(cleaned_text)
    #webpage_data.close()
    return cleaned_text


def answer_question(content, user_question):
    load_dotenv()
    model = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    system_prompt = "Your name is CB bot and you have to anwer questions based on the information provided on https://www.marketrix.ai/ about Marketrix.ai, if can't find an answer to that, return \"Sorry, I don't know the answer, try asking me about Marketrix\". Information extracted from Marketrix website:  " + content
    
    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]
    chat_completion = model.chat.completions.create(
        messages=message,
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

import time
marketrix_url = "https://www.marketrix.ai/"
webdata = open("webpage_data.txt", "r")
content = webdata.read()
if not content:
    content = extract_content(marketrix_url)
webdata.close()
print(content)

@app.route("/chatbot", methods=["POST"])
def query():
    start_time = time.time()
    request_data = json.loads(request.data)
    print(request_data)
    user_question = request_data["message"]
    # return {'200':'query added successfully'}

    #webdata = open("webpage_data.txt", "r")
    #content = webdata.read()
    #if not content:
    #    content = extract_content(marketrix_url)
    #webdata.close()
    return jsonify({"result": answer_question(content, user_question)})

if __name__ == "__main__":
    app.run(debug=True)
