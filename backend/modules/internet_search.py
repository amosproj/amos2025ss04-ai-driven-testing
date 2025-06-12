from modules.base import ModuleBase
from schemas import PromptData
from keybert import KeyBERT
import requests
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
import random

PROMPT_TEMPLATE = """
Answer the query based on the above context: {question}
---
Answer the query based only on the following context:
{context}
"""


class InternetSearch(ModuleBase):
    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return False

    def process_prompt(self, prompt_data: PromptData) -> dict:
        print(prompt_data)
        prompt = prompt_data.input.user_message

        # Keyword extraction
        kw_model = KeyBERT()
        extracted_keywords = kw_model.extract_keywords(
            prompt, keyphrase_ngram_range=(1, 2), top_n=5
        )
        keywords = [keyword[0] for keyword in extracted_keywords]
        search_query = keywords if keywords else prompt

        # Get URLs and scrape them
        urls = get_duckduckgo_urls(search_query)
        all_text = ""
        for url in urls:
            print(f"Scraping {url}")
            try:
                soup = scrape_url(url)
                if soup:
                    text = extract_clean_text(soup)
                    print(text[:500])  # print first 500 chars
                    all_text += text
            except Exception as e:
                print(e)
            print("=" * 80)

        # Compose prompt
        context = all_text.strip()
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        final_prompt = prompt_template.format(context=context, question=prompt)

        prompt_data.input.user_message = final_prompt
        prompt_data.rag_sources = urls
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: PromptData):
        pass


def get_random_headers():
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/113.0",
    ]
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }


def get_duckduckgo_urls(query, max_results=5):
    params = {"q": query, "kl": "us-en"}
    url = "https://html.duckduckgo.com/html/"

    response = requests.post(url, data=params, headers=get_random_headers())
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for result in soup.find_all("a", class_="result__a", href=True):
        links.append(result["href"])
        if len(links) == max_results:
            break
    print(links)
    return links


def scrape_url(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def extract_clean_text(soup):
    elements = soup.find_all(["p", "h1", "h2", "h3"])
    texts = [
        el.get_text(strip=True) for el in elements if el.get_text(strip=True)
    ]
    return "\n".join(texts)
