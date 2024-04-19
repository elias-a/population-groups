import os
import tomli
from pubmed import query_pubmed, parse_article_xml
from classify import classify


with open(os.path.join(os.path.dirname(__file__), "config.toml"), "rb") as f:
    config = tomli.load(f)
    email = config["AUTH"]["EMAIL"]
query = '"east asian people"[mh:noexp] AND 2024[dcom]'
xml = query_pubmed(query, email)
articles = parse_article_xml(xml)
labels = [classify(a) for a in articles.values()]
print(labels.count("people"))
print(len(labels))
