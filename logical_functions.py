import os
import re
import json
from groq import Groq
from dotenv import load_dotenv
import google.generativeai as genai



# LOAD DOTENV FUNCTION TO ACCESS ENV FILES
load_dotenv()

# CONFIGURE GOOGLE(GEMINI) API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# CREATE FUNCTION TO INTEGRATE LLM MODEL USING GEMINI(1.5 FLASH) TO USE IN RESUME
def google_llm_model(prompt):
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"Error occurred {e}"


# CREATE FUNCTION FOR LLM MODEL TO USE IN ATS AND INTERVIEW QUESTIONS
def groq_llm_model(prompt):
    prompts = json.dumps(prompt)
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompts}],
        # model="mixtral-8x7b-32768"
        model="llama3-70b-8192"
    )
    llm_response = chat_completion.choices[0].message.content.encode('utf-8').decode('utf-8-sig').strip()
    return llm_response


def clean_json_string(s):
    return s.replace('\n', '').replace('\r', '').replace('\t', '').strip()

    content = clean_json_string(llm_response)
    content = content.lstrip('\ufeff').lstrip()
    return content


# FUNCTION TO GET SPECIFIC DATA BETWEEN '{' & '}'.
def extract_json_data_from_response(response_with_extra_data):
    json_data = re.search(r'\{.*\}', response_with_extra_data, re.DOTALL)

    if json_data:
        try:
            json_content = json.loads(json_data.group()) # string to json
            json_content_str = json.dumps(json_content) # json to string
            return json_content_str

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return response_with_extra_data
    else:
        print("No valid JSON found. Please check the input.")
        return response_with_extra_data


# # SPLITS LIST INTO N CHUNKS AS EVENLY AS POSSIBLE
def split_list(input_list, n):
    avg = len(input_list) // n
    remainder = len(input_list) % n
    split_list = []
    start = 0

    for i in range(n):
        length = avg + (1 if i < remainder else 0)
        split_list.append(input_list[start:start + length])
        start += length

    return split_list