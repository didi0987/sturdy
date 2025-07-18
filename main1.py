import spacy, re
from spacy.tokens import Span


def remove_headers_footers(text):
    lines = text.split("\n")
    remaining_lines = lines[93:13336]
    text = "\n".join(remaining_lines)
    return text


def pre_process():
    print("Pre-processing text...")
    with open("42671.txt", "r", encoding="utf-8") as file:
        text = file.read()
    text = remove_headers_footers(text)
    text = re.sub(
        r"^CHAPTER\s+[IVXLC\d]+\.", "", text, flags=re.IGNORECASE | re.MULTILINE
    )
    with open("clean_book.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Pre-processing complete.")


def get_person_title(span):
    if span.label_ == "PERSON" and span.start != 0:
        prev_token = span.doc[span.start - 1]
        if prev_token.text in ("Dr", "Dr.", "Mr", "Mr.", "Ms", "Ms."):
            return prev_token.text


def extend_person_entity(doc):

    # Create list to store new entities with extended boundaries
    new_entities = []

    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent._.person_title:
            # Extend entity to include the title (one token before)
            extended_start = ent.start - 1
            extended_span = Span(doc, extended_start, ent.end, label="PERSON")
            new_entities.append(extended_span)
        else:
            # Keep all non-person entities unchanged
            new_entities.append(ent)

    # Update the document's entities with the extended boundaries
    doc.ents = new_entities

    # Verify the changes
    print("\nFinal entities:")
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            print(f"PERSON: {ent.text.replace("\n", " ")}")


def main():
    # load text from file
    text = ""
    print("Loading text from file...")
    with open("clean_book.txt", "r", encoding="utf-8") as file:
        text = file.read()

    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    # Register the Span extension as 'person_title'
    Span.set_extension("person_title", getter=get_person_title)
    extend_person_entity(doc)


if __name__ == "__main__":
    # pre_process()
    main()
