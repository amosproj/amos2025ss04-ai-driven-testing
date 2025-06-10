from modules.base import ModuleBase
from llm_manager import LLMManager
from keybert import KeyBERT
import requests
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate

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

    def process_prompt(self, prompt_data: dict) -> dict:
        prompt = prompt_data["prompt"]

        # Keyword extraction
        kw_model = KeyBERT()
        extracted_keywords = kw_model.extract_keywords(
            prompt,
            keyphrase_ngram_range=(1, 2),
            top_n=5
        )
        keywords = [keyword[0] for keyword in extracted_keywords]
        search_query = keywords if keywords else prompt

        # Get URLs and scrape them
        urls = get_duckduckgo_urls(search_query)
        all_text = ""
        for url in urls:
            try:
                soup = scrape_url(url)
                clean_text = extract_clean_text(soup)
                all_text += clean_text + "\n"
            except Exception as e:
                print(f"[Warning] Skipping URL {url}: {e}")

        # Compose prompt
        context = all_text.strip()
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        final_prompt = prompt_template.format(
            context=context,
            question=prompt
        )

        prompt_data["prompt"] = final_prompt
        return prompt_data

    def process_response(self, response_data: dict, prompt_data: dict) -> dict:
        return response_data


def get_duckduckgo_urls(query, max_results=5):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    params = {
        "q": query,
        "kl": "us-en"
    }
    url = "https://html.duckduckgo.com/html/"

    response = requests.post(url, data=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for result in soup.find_all("a", class_="result__a", href=True):
        links.append(result['href'])
        if len(links) == max_results:
            break

    return links


def scrape_url(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding or 'utf-8'
    return BeautifulSoup(response.text, "html.parser")


def extract_clean_text(soup: BeautifulSoup) -> str:
    elements = soup.find_all(['p', 'h1', 'h2', 'h3'])
    texts = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]
    return "\n".join(texts)
