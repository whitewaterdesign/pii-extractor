import json
import time
from pathlib import Path
from gliner import GLiNER

from evaluation.evaluate import LabelDictionary

MODEL_PATH = "./gliner_multi_pii-v1"
#
# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(
#     MODEL_PATH,
#     local_files_only=True
# )
#
# # Load model (PyTorch + safetensors)
# model = AutoModelForTokenClassification.from_pretrained(
#     MODEL_PATH,
#     local_files_only=True,
#     use_safetensors=True
# )
# model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
model = GLiNER.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

logs_path = Path("data/gliner/results.jsonl")

with logs_path.open("w", encoding="utf-8") as f:
    f.write("")

# ---- Scan a text file safely ----


    # for i in range(0, len(text), max_chars):
    #     yield text[i:i+max_chars]


# def split_net_token(token):
#     # split on common separators like : /
#     return re.split(r'[:/]', token)
#
# split_tokens = []
# for tok in net_tokens:
#     split_tokens.extend(split_net_token(tok))


# Press the green button in the gutter to run the script.

MAX_CHARS = 384

if __name__ == '__main__':
    label_dictionary: LabelDictionary = {
        'PASSWORD': 'password',
        'PERSON': 'person',
        'NAME': 'person',
        'DATE_OF_BIRTH': 'date of birth',
        'NINO': 'national insurance number',
        'NHS_NUMBER': 'nhs number',
        'NATIONAL_INSURANCE_NUMBER': 'national insurance number',
        'PHONE_NUMBER': 'phone number',
        'BANK_SORT_CODE': 'bank sort code',
        'BANK_ACCOUNT_NUMBER': 'bank account number',
        'CREDIT_CARD_NUMBER': 'credit card number',
        'ADDRESS': 'full address',
        'POSTCODE': 'postcode',
        'VEHICLE_REGISTRATION': 'vehicle registration',
        'EMAIL_ADDRESS': 'email',
    }

    with open("data/logs.jsonl", "r", encoding="utf-8") as f:
        text = f.read()

    labels = ["email", "driver licence",
              "full address", "postcode", "passport number", "Social Security Number", "bank sort code",
              "phone number", "password", "vehicle registration", "credit card number", "bank account number",
              "national insurance number", "nhs number", "person", "date of birth"]

    lines = text.splitlines()
    chunked_lines = []

    for line in lines:
        chunked_line = [line]
        if len(line) > MAX_CHARS:
            chunked_line = []
            for chunk in [line[i:i + MAX_CHARS] for i in range(0, len(line), MAX_CHARS)]:
                chunked_line.append(chunk)

        chunked_lines.append(chunked_line)
    # {'start': 72, 'end': 77, 'text': 'cyrus', 'label': 'person', 'score': 0.8641920685768127}

    lines_extracted = []
    results = []
    times = []
    for line in chunked_lines:
        time_start = time.perf_counter()

        line_results = []
        line_chunks = []

        for chunk in line:
            entities = model.predict_entities(
                chunk,
                labels,
                include_spans=True
            )
            line_results.extend(entities)
            for grp, start, end in sorted(
                [(f'[{entity['label']}]', entity['start'], entity['end']) for entity in entities],
            reverse=True):
                chunk = chunk[:start] + grp + chunk[end:]
            line_chunks.append(chunk)
        line_str = "".join(line_chunks)
        lines_extracted.append(line_str)
        print(line_str)
        results.append(line_results)
        print(line_results)

        elapsed = time.perf_counter() - time_start
        print(f"Elapsed time (secs): {elapsed:.6f}")

        with logs_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line_results) + "\n")

        times.append(elapsed)
    print(times)
    total_time = sum(times)
    print(f"Total time (secs): {total_time:.6f}. Time per line (secs): {total_time/len(lines):.6f}")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
