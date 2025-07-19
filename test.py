from spacy.lang.en import English
from spacy.kb import KnowledgeBase, InMemoryLookupKB
from spacy.tokens import Span
import spacy

nlp = spacy.load("en_core_web_lg")
kb = InMemoryLookupKB(vocab=nlp.vocab, entity_vector_length=300)
name = "Ada Lovelace"
qid = "Q7259"
kb.add_entity(entity=qid, entity_vector=nlp(name).vector, freq=342)
kb.add_alias(entities=[qid], alias="Lovelace", probabilities=[0.3])
kb.add_alias(entities=[qid], alias="James", probabilities=[0.3])
kb.add_alias(entities=[qid], alias="Ada", probabilities=[0.3])
doc = nlp("Ada Lovelace was born in London")
# Document level
ents = [(e.text, e.label_, e.kb_id_) for e in doc.ents]
print(kb.get_entity_strings())
print(kb.get_alias_strings())
# Process "Ada" through spaCy to get a token
ada_doc = nlp("Ada Lovelace")
ada_token = ada_doc[0]
print([c.entity_ for c in kb.get_candidates(ada_token)])
# Token level
# ent_ada_0 = [doc[0].text, doc[0].ent_type_, doc[0].ent_kb_id_]
# ent_ada_1 = [doc[1].text, doc[1].ent_type_, doc[1].ent_kb_id_]
# ent_london_5 = [doc[5].text, doc[5].ent_type_, doc[5].ent_kb_id_]
# print(ent_ada_0)  # ['Ada', 'PERSON', 'Q7259']
# print(ent_ada_1)  # ['Lovelace', 'PERSON', 'Q7259']
# print(ent_london_5)  # ['London', 'GPE', 'Q84']
