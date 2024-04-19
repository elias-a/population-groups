from transformers import pipeline


def classify(article):
    classifier = pipeline(model="facebook/bart-large-mnli")
    classification = classifier(
        article["title"] + article["abstract"],
        candidate_labels=["people", "food", "drink", "animals"],
    )
    label, _ = max(
        zip(classification["labels"], classification["scores"]),
        key=lambda c: c[1],
    )
    return label
