import pytesseract
from PIL import Image
import json
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

def ocr(uploaded_file):
    if not uploaded_file:
        return None

    image = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image)

    prompt = f"""
You are analyzing text extracted from a bill using OCR (pytesseract). The text may contain OCR errors, so interpret carefully and extract only the most reliable details.

Your Task:
From the given OCR text, extract the following:

Amount — Total amount spent (include currency if mentioned)

Date — Transaction date in DD-MM-YYYY format

Category — Classify the transaction into one of the following categories:

Entertainment
Food
Transportation
Miscellaneous
Monthly Bills
Shopping

Output Format:
Return only a properly closed JSON object containing exactly three keys:
"Amount"
"Date"
"Category"

Rules:
Do not include any explanation or preamble.
Your entire output must be inside curly brackets.
No blank lines, markdown, or surrounding text—just the JSON."""

    response = llm.invoke(prompt + f"\nExtracted Text: {text}")
    print("RAW RESPONSE FROM LLM:\n", response.content)

    try:
        extracted_data = json.loads(response.content)

        from datetime import datetime

        raw_date = extracted_data.get('Date')
        formatted_date = None

        if raw_date:
            try:
                # Parse your '25-04-2025' format
                parsed_date = datetime.strptime(raw_date, "%d-%m-%Y")
                formatted_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError as e:
                print("Date parsing failed:", e)

        if formatted_date:
            extracted_data['Date'] = formatted_date
        else:
            extracted_data['Date'] = ''

        return {
            "Amount": extracted_data.get("Amount", "Not Found"),
            "Date": extracted_data.get("Date", "Not Found"),
            "Category": extracted_data.get("Category", "Not Found")
        }
    except json.JSONDecodeError:
        return {
            "Amount": "Not Found",
            "Date": "Not Found",
            "Category": "Not Found"
        }
