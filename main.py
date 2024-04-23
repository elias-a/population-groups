import os
import tomli
from pubmed import query_pubmed, parse_article_xml
from classify import classify


with open(os.path.join(os.path.dirname(__file__), "config.toml"), "rb") as f:
    config = tomli.load(f)
    email = config["AUTH"]["EMAIL"]




def run(pop, email):
    group, word = pop
    c1, total1 = get_counts(
        f'"{word}"[ti] AND 2024[dcom] AND "{group}"[mh:noexp]',
        email,
    )
    c2, total2 = get_counts(
        f'"{word}"[ti] AND 2024[dcom] NOT "{group}"[mh:noexp]',
        email,
    )
    tp = c1 + total2 - c2
    fp = c2
    fn = total1 - c1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    print(precision, recall)


def get_counts(query, email):
    xml = query_pubmed(query, email)
    articles = parse_article_xml(xml)
    labels = [classify(a) for a in articles.values()]
    return labels.count("people group"), len(labels)


pop_groups = [
    ("east asian people", "chinese"),
    ("east asian people", "japanese"),
    ("white", "white"),
]
for p in pop_groups:
    run(p, email)
