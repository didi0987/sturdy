import spacy, re, csv
from spacy.tokens import Span
from spacy.kb import KnowledgeBase, InMemoryLookupKB


def load_entities():
    entities_path = "characters.csv"
    names = dict()
    aliases = dict()
    with open(entities_path, "r", encoding="utf-8") as file:
        csvreader = csv.reader(file, delimiter=",")
        for row in csvreader:
            qid = row[0]
            name = row[1]
            alias = [
                alias.replace(" ", "").replace(".", "").replace("\n", "")
                for alias in row[2:]
            ]  # Remove empty aliases
            names[qid] = name.replace(" ", "").replace("\n", "").replace(".", "")
            aliases[qid] = alias

    return names, aliases


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


def build_entitylink_by_kb(doc, nlp):
    kb = InMemoryLookupKB(vocab=nlp.vocab, entity_vector_length=300)
    names_dict, aliases_dict = load_entities()
    entity_link = dict()
    print(aliases_dict)
    for qid, name in names_dict.items():
        # Add entity to the knowledge base
        print(f"Adding entity: {qid} - {name}")
        kb.add_entity(entity=qid, entity_vector=nlp(name).vector, freq=342)
        # Add aliases for the entity
        for alias in aliases_dict[qid]:
            if alias:
                kb.add_alias(entities=[qid], alias=alias, probabilities=[1])
    print(kb.get_entity_strings())
    print(kb.get_alias_strings())
    print("\nFinal entities:")
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Remove spaces from entity text
            clean_name = ent.text.replace(" ", "").replace("\n", "").replace(".", "")
            # If the cleaned name is in the knowledge base, get its ID
            for qid, name in names_dict.items():
                if name == clean_name:
                    kb_id = qid
                    if kb_id in entity_link:
                        entity_link[kb_id].append(ent)
                    else:
                        entity_link[kb_id] = [ent]
                    break
                # get entity ID for alias
                elif kb.get_alias_candidates(clean_name):
                    kb_id = kb.get_alias_candidates(clean_name)[0].entity_
                    print(f"Alias found for {clean_name}, using ID: {kb_id}")
                    if kb_id in entity_link:
                        entity_link[kb_id].append(ent)
                    else:
                        entity_link[kb_id] = [ent]
                    break
                else:
                    kb_id = "N/A"
            print(f"PERSON: {clean_name}, KB ID: {kb_id}")
    print(entity_link)
    return entity_link


def cluster_name_entities(doc, kb):
    pass
    # Verify the changes


def divide_text_into_chunks(doc, chunk_size=1000):
    """
    Divide the document into chunks of specified size.
    """
    chunks = []
    for i in range(0, len(doc), chunk_size):
        chunk = doc[i : i + chunk_size]
        chunks.append(chunk)
    return chunks


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
    my_el = build_entitylink_by_kb(doc, nlp)
    ada_doc = nlp("MrDarcy")
    ada_token = ada_doc[0]
    print([c.entity_ for c in kb.get_candidates(ada_token)])
    # kb=KnowledgeBase(nlp.vocab, entity_vector_length=300)
    # names_dict,aliaes_dict = load_entities()
    # for qid,name in names_dict.items():
    #     kb.add_alias(entiqid, name, aliases=[name])


if __name__ == "__main__":
    # names,aliases=load_entities()
    # print("Loaded entities:", names)
    # print("Loaded alias:", aliases)
    # pre_process()
    main()
