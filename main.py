import os
import time

print("print 1")
import pandas as pd

print("print 2")

from google import genai

print()
import pandas as pd

API_KEY = "AIzaSyBEI72sxtV6Omsrj2B_W1iRwiwkit-e8Fw"
INPUT_FILE = "Book1.xlsx"
COLUMN_NAME = "title"
OUTPUT_FILE = "queries_normalized.xlsx"
MODEL_NAME = "gemini-3-flash-preview"

client = genai.Client(api_key=API_KEY)


def normalize_query(raw_query):
    prompt = f"""
    به عنوان یک متخصص سئو و جستجو، عبارت جستجوی زیر را نرمال کن.
    هدف: حذف جزئیات اضافی (رنگ، سایز، صفات، کلمات مدل‌وار طولانی) و نگه داشتن هسته اصلی محصول.
    قانون: فقط و فقط عبارت نهایی را برگردان و هیچ توضیحی نده.

    مثال: "کفش دویدن نایک مدل ایرمکس ۲۰۲۴ رنگ قرمز سایز ۴۲" -> "کفش نایک ایرمکس"
    مثال: "گوشی موبایل سامسونگ گلکسی اس ۲۴ الترا ظرفیت ۲۵۶ گیگ" -> "سامسونگ گلکسی S24 Ultra"

    عبارت: "{raw_query}"
    """
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error processing '{raw_query}': {e}")
        return None


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"error: {INPUT_FILE} not found.")
        return

    df = pd.read_excel(INPUT_FILE)

    if "normalized_query" not in df.columns:
        df["normalized_query"] = ""

    print(f"start processing {len(df)} rows...")

    for index, row in df.iterrows():
        if pd.notna(row["normalized_query"]) and row["normalized_query"] != "":
            continue

        raw_q = str(row[COLUMN_NAME])
        print(f"Processing ({index + 1}/{len(df)}): {raw_q}")

        normalized_q = normalize_query(raw_q)

        if normalized_q:
            df.at[index, "normalized_query"] = normalized_q

            df.to_excel(OUTPUT_FILE, index=False)
            print(f"Saved: {normalized_q}")

        time.sleep(4)


if __name__ == "__main__":
    main()
