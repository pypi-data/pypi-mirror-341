#initiator

#BOOLEAN

# Define the documents
documents = {
    1: "The cat chased the dog around the garden",
    2: "She was sitting in the garden last night",
    3: "I read the book the night before"
}

# Preprocess documents and build inverted index
def build_index(docs):
    index = {}
    for doc_id, text in docs.items():
        terms = set(text.lower().split())
        for term in terms:
            if term not in index:
                index[term] = {doc_id}
            else:
                index[term].add(doc_id)
    return index

# Create the index
inverted_index = build_index(documents)

# Boolean AND
def boolean_and(operands, index):
    if not operands:
        return list(range(1, len(documents) + 1))
    result = index.get(operands[0], set())
    for term in operands[1:]:
        result = result.intersection(index.get(term, set()))
    return list(result)

# Boolean OR
def boolean_or(operands, index):
    result = set()
    for term in operands:
        result = result.union(index.get(term, set()))
    return list(result)

# Boolean NOT
def boolean_not(operand, index, total_docs):
    operand_set = set(index.get(operand, set()))
    all_docs_set = set(range(1, total_docs + 1))
    return list(all_docs_set.difference(operand_set))

# Sample queries
and_query = ["garden", "night"]
or_query = ["garden", "night"]
not_query = "night"

# Run queries
and_result = boolean_and(and_query, inverted_index)
or_result = boolean_or(or_query, inverted_index)
not_result = boolean_not(not_query, inverted_index, len(documents))

# Print results
print("Documents containing BOTH 'garden' AND 'night':", and_result)
print("Documents containing 'garden' OR 'night':", or_result)
print("Documents NOT containing 'night':", not_result)

