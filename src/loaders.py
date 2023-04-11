import re
import urllib.parse
from urllib.parse import urljoin

from langchain.document_loaders import WebBaseLoader
from langchain.docstore.document import Document
from bs4 import BeautifulSoup


class DocsLoader(WebBaseLoader):
    known_pages = set()

    def load(self) -> list[Document]:
        docs = []
        for path in self.web_paths:
            docs.extend(self._load(path))
        return docs

    def _load(self, path):
        docs = []
        soup: BeautifulSoup = self._scrape(path)
        self.process_page(soup, path)
        text = soup.find(class_="markdown").get_text("\n", strip=True)
        metadata = {"source": path, "html": soup.decode(),
                    "title": soup.find("h1").text}
        docs.append(Document(page_content=text, metadata=metadata))
        print("Parse page", path)

        next_page = soup.find(class_="pagination-nav__item--next")
        while True:
            if next_page.find(href=True) is None:
                break
            next_page_link = urljoin(path, next_page.find(href=True)["href"])
            if next_page_link in self.known_pages:
                break
            print("Parse page", next_page_link)
            soup: BeautifulSoup = self._scrape(next_page_link)
            self.process_page(soup, next_page_link)
            self.known_pages.add(next_page_link)

            text = soup.find(class_="markdown").get_text(
                separator="\n", strip=True)
            metadata = {"source": next_page_link,
                        "html": soup.decode(), "title": soup.find("h1").text}
            docs.append(Document(page_content=text, metadata=metadata))

            next_page = soup.find(class_="pagination-nav__item--next")
        return docs

    @staticmethod
    def process_page(soup: BeautifulSoup, path):
        if path == "https://docs.lido.fi/integrations/wallets":
            print("Remove example code from page", path)
            soup.find(string="Example code,").find_next().decompose()
            soup.find(string="Preview,").find_next().decompose()
        return soup


def parse_addresses(texts: dict):
    address_pattern = r'([a-zA-Z0-9\(\) ]+):\s*(0x[a-fA-F0-9]{40})(?:\s*\(([^)]+)\))?'
    address_dict = {}

    for url, text in texts.items():
        matches = re.finditer(address_pattern, text)
        for match in matches:
            alias = match.group(1)
            address = match.group(2).lower()
            postfix = match.group(3)
            if postfix:
                alias = alias + "_" + postfix
            if alias not in address_dict:
                address_dict[urllib.parse.urlsplit(
                    url).path + "_" + alias] = address

    return address_dict


def replace_addresses_with_aliases(text, address_dict, replace_template="$[{}]"):
    address_pattern = r'(0x[a-fA-F0-9]{40})'

    def replace_address(match):
        address = match.group(1).lower()
        for alias, known_address in address_dict.items():
            if address == known_address.lower():
                return replace_template.format(alias)
        return address

    replaced_text = re.sub(address_pattern, replace_address, text)
    return replaced_text


def replace_aliases_with_addresses(text, address_dict, replace_template="{}"):
    print("Called replace_aliases_with_addresses", text)
    alias_pattern = r'\$\[(.*)\]'
    address_pattern = re.compile(r"0x[a-fA-F0-9]{40}")

    def replace_alias(match):
        alias = match.group(1)
        if alias in address_dict:
            value = replace_template.format(address_dict[alias])
        else:
            value = "unknown"
        print("Replace alias", alias, value)
        return value

    def replace_address(match):
        address = match.group()
        print("Replace address", address, "unknown")
        return "unknown"

    replaced_text = re.sub(address_pattern, replace_address, text)
    replaced_text = re.sub(alias_pattern, replace_alias, replaced_text)
    return replaced_text


def parse_addresses_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    prefix = soup.find("h1").text
    address_pattern = re.compile(r"0x[a-fA-F0-9]{40}")
    address_dict = {}

    # Find all the list items (bullets)
    items = soup.find_all('li')

    for item in items:
        parent_key = ""
        if item.find_parent('li'):
            parent_key = ''.join([content.text for content in item.find_parent(
                "li").contents if content.name != 'ul']).strip()

        # Get the current item text without children's text
        item_text = ''.join(
            [content.text for content in item.contents if content.name != 'ul']).strip()

        # Find the address in the current item text
        address_match = address_pattern.search(item_text)

        # If an address is found, store it in the dictionary
        if address_match:
            address = address_match.group()

            # Join parent key and subkey if a parent key exists
            if parent_key:
                key = f"{prefix} -> {parent_key} -> {item_text}"
            else:
                key = f"{prefix} -> {item_text}"
            key = re.sub(address_pattern, '', key).strip().rstrip(":")
            key = re.sub(r' +', ' ', key)
            address_dict[key] = address
    return address_dict


def get_addresses_from_docs(docs):
    addresses = {}
    for doc in docs:
        if "deployed-contracts" in doc.metadata["source"]:
            addresses = {**addresses, **
                         (parse_addresses_from_html(doc.metadata["html"]))}
    return addresses


def replace_addresses_with_aliases_in_docs(docs, addresses):
    for doc in docs:
        doc.page_content = replace_addresses_with_aliases(
            doc.page_content, addresses)
    return docs


if __name__ == '__main__':
    loader = DocsLoader(
        ["https://docs.lido.fi", "https://docs.lido.fi/deployed-contracts/goerli/"])
    docs = loader.load()
    addresses = get_addresses_from_docs(docs)
    docs = replace_addresses_with_aliases_in_docs(docs, addresses)
