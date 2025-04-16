#initiator
#4b average precision and other metrics

from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score

# True binary labels
y_true = [0, 1, 1, 0, 1]

# Scores or predicted probabilities
y_scores = [0.1, 0.8, 0.6, 0.3, 0.9]

# Convert scores to binary predictions using a threshold (e.g., 0.5)
y_pred = [1 if score >= 0.5 else 0 for score in y_scores]

# Calculate metrics
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
avg_precision = average_precision_score(y_true, y_scores)

# Display the results
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1:.2f}")
print(f"Average Precision (AUC-PR): {avg_precision:.2f}")
