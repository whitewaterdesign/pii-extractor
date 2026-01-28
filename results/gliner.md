# GLiNER
urchade/gliner_multi_pii-v1 · Hugging Face
Total time (secs): 166.223618. Time per line (secs): 0.524365

## Metrics

We can define the precision and recall as follows:

$$Recall = \frac{TP}{TP + FN}$$

$$Precision = \frac{TP}{TP + FP}$$

$$Accuracy = \frac{TP}{TP + FP + FN}$$

$$F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$$

## Strict Evaluation

| Metric | Percentage |
|--------|------------|
| Accuracy  | 28.77%         | 
| Precision    | 36.40%         |
| Recall    | 57.85%         |
| F1    | 44.68%    |



The main problem is that we only count it as a positive if it's an exact match.
GLiNER seems to find people before it finds emails.
So it is categorising:
joe.bloggs@example.com as joe.bloggs -> Person (edited) 

## Looser Evaluation

| Metric | Percentage |
|--------|------------|
| Accuracy  | 47.57%        | 
| Precision    | 52.51%       |
| Recall    | 83.47%        |
| F1    | 64.47%    |

These metrics are less useful than they could be.
What we care about is 

## Relaxed (Jaccard-based) Evaluation

| Metric    | Value   | Interpretation (PII in Logs)                         |
|------------|---------|--------------------------------------------------------|
| Accuracy   | 47.57%  | Not very meaningful for span detection                |
| Precision  | 52.51%  | Moderate over-detection, common for PII systems       |
| Recall     | 83.47%  | Strong PII catch rate on unseen data                  |
| F1-score   | 64.47%  | Solid overall relaxed performance                     |

Both the strict and the loose evaluation use exact string matching, which does not show the usefulness of the model.
We can use Jaccard similarity instead, which is a more relaxed measure of overlap.

$$J(A,B) = \frac{|A \cap B|}{|A \cup B|}$$

Jaccard similarity is defined as the size of the intersection divided by the size of the union 
of the sets of words included in the predicted and gold spans
We've set the threshold for a match (TP) to be 0.3.





