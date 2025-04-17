def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score
relevant_documents = [1, 2, 3, 4, 5]
retrieved_documents = [1, 2, 3, 6, 7]
precision = len(set(relevant_documents).intersection(retrieved_documents)) / len(retrieved_documents)
recall = len(set(relevant_documents).intersection(retrieved_documents)) / len(relevant_documents)
f_measure = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print("Manual Calculation:")
print("Precision:", precision)
print("Recall:", recall)
print("F-measure:", f_measure)
y_true = [1 if doc in relevant_documents else 0 for doc in retrieved_documents]
y_pred = y_true.copy()
print("\nEvaluation Toolkit:")
print("Average Precision:", average_precision_score(y_true, y_pred))

    '''
    print(code)