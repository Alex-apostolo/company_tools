from openai import OpenAI
import pandas as pd
import csv

client = OpenAI()


def generate_description(company_name, sic, top_5_most_frequent_words, cleaned_html):
    prompt = f"""
        ### Company Name
        {company_name}

        ### Industry Classification
        {sic}

        ### Top 5 Most Frequent Words
        {top_5_most_frequent_words}

        ### Cleaned HTML Content
        {cleaned_html}
    """
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a helpful assistant that generates company descriptions.
                    Ensure the descriptions you generate are concise yet informative, typically between 100 to 300 words. 
                    Provide a clear overview of the company's mission, products or services, target market, and unique value proposition. 

                    Input format:
                    ### Company Name
                    The name of the company.

                    ### Industry Classification
                    The industry classification codes of the company.

                    ### Top 5 Most Frequent Words
                    The top 5 most frequent words from the company's homepage.

                    ### Cleaned HTML Content
                    The cleaned HTML content of the company's homepage.

                    Output format:
                    Company Description single paragraph of 100 to 300 words.
                """,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )


df = pd.read_json("cleaned_ml_challenge_dataset.jsonl", lines=True)

with open("descriptions.csv", "a") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Description"])

    for index, row in df.iterrows():
        try:
            print(f"Generating description for {row['name']}")
            description = generate_description(
                row["name"],
                row["sic"],
                row["top_5_most_frequent_words"],
                row["cleaned_html"],
            )
            writer.writerow(
                [row["name"], description.choices[0].message.content.replace("\n", " ")]
            )
        except Exception as e:
            print(f"Error generating description for {row['name']}")
            writer.writerow([row["name"], "error"])
