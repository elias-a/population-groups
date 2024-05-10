import requests
from lxml import etree


def query_pubmed(query, email):
    response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        params={
            "tool": "population-groups",
            "email": email,
            "db": "pubmed",
            "retmode": "json",
            "retmax": 10000,
            "term": query,
        },
    )
    pmids = response.json().get("esearchresult", {}).get("idlist", [])
    response = requests.post(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        params={
            "tool": "population-groups",
            "email": email,
            "db": "pubmed",
            "retmode": "xml",
        },
        data={ "id": pmids },
    )
    return response.text


def parse_article_xml(xml):
    articles = {}
    for article in etree.XML(xml).findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = " ".join(article.find(".//ArticleTitle").itertext())
        abstract_node = article.find(".//Abstract")
        abstract = " ".join(
            abstract_node.itertext()
        ) if abstract_node is not None else ""
        articles[pmid] = { "title": title, "abstract": abstract }
    return articles
