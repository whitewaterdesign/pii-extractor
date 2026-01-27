# GLiNER
urchade/gliner_multi_pii-v1 · Hugging Face
Total time (secs): 166.223618. Time per line (secs): 0.524365

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
