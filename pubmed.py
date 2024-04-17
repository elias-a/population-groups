import requests


def query_pubmed(query, email)
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
    response = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
        params={
            "tool": "population-groups",
            "email": email,
            "db": "pubmed",
            "retmode": "xml",
            "id": pmids,
        },
    )
    return response.text
