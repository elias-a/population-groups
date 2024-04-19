from transformers import pipeline


def classify(article):
    classifier = pipeline(model="facebook/bart-large-mnli")
    classification = classifier(
        article["title"],
        candidate_labels=[
            "people group",
            "plants",
            "animals",
            "medicine",
            "food",
            "beverages",
            "exercise",
            "culture",
            "health",
        ],
    )
    label, _ = max(
        zip(classification["labels"], classification["scores"]),
        key=lambda c: c[1],
    )
    return label
