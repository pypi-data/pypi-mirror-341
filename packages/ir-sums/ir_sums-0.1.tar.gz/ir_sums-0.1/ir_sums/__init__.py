#initiator
#Calculating precision,recall,f1 positive
# Given values
true_positive = 60
false_positive = 30
false_negative = 20

precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f_measure = 2 * (precision * recall) / (precision + recall)

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F-measure: {f_measure:.2f}")
