from dataclasses import dataclass
from pubmed import query_pubmed, parse_article_xml
from classify import classify


@dataclass(kw_only)
class Accuracy:
    correct: int
    total: int


@dataclass(kw_only=True)
class PopGroup:
    mesh: str
    entry_term: str


def count_correct(yes, no):
    return Accuracy(
        correct=yes.count("people group") + len(no) - no.count("people group"),
        total=len(yes) + len(no),
    )


def get_labels(query, email):
    xml = query_pubmed(query, email)
    articles = parse_article_xml(xml)
    return [classify(a) for a in articles.values()]


def process_group(group, email):
    yes = get_labels(
        f'"{group.entry_term}"[ti] AND 2024[dcom] AND "{group.mesh}"[mh:noexp]',
        email,
    )
    no = get_labels(
        f'"{group.entry_term}"[ti] AND 2024[dcom] NOT "{group.mesh}"[mh:noexp]',
        email,
    )
    return count_correct(yes, no)


def run_pipeline(email):
    [process_group(p, email) for p in [
        PopGroup(mesh="east asian people", entry_term="chinese"),
        PopGroup(mesh="east asian people", entry_term="japanese"),
        PopGroup(mesh="white", entry_term="white"),
    ]]
