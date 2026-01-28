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

An example of a match:

Log
```json
{"timestamp": "2026-01-25T14:18:42.917000Z", "level": "WARN", "service": {"name": "notification-worker", "version": "2.8.3", "environment": "prod"}, "host": {"hostname": "ip-10-42-7-19", "ip": "10.42.7.19"}, "log": {"logger": "com.acme.notify.AlertDispatcher", "thread": "worker-3"}, "trace": {"trace_id": "7f8a6f0e2b8f4c1e9a4b0fd2c6c1a3f2", "span_id": "3b2c1d0e9f8a7b6c", "parent_span_id": "a1b2c3d4e5f60718"}, "correlation_id": "c3b7d2b0-4a8a-4b55-9f3e-1d6f2f1f6a5a", "http": null, "user": null, "event": {"type": "alert_dispatch", "outcome": "deferred", "entity": "email_recipient", "entity_id": null}, "security": {"auth_method": null, "mfa": null}, "data_classification": "confidential", "message": "Alert dispatch deferred due to transient SMTP error; will retry delivery to d.harrington+alerts@proton.me", "extra": null}
```

Gold standard spans
```json
[{"label": "EMAIL_ADDRESS", "text": "d.harrington+alerts@proton.me"}]
```

Predicted spans
```json
[{"text": "email_recipient", "label": "email", "score": 0.9511743187904358}, {"text": "d.harrington", "label": "person", "score": 0.9549511671066284}]
```

Gold standard set:

$$\{d, harrington, alerts, proton, me\}$$

Predicted set:

$$\{d, harrington\}$$

Jaccard similarity:

$$J(A,B) = \frac{|\{d, harrington\}|}{|\{d, harrington, alerts, proton, me\}|} = 0.4$$



