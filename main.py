from gliner import GLiNER

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

# ---- Scan a text file safely ----

def chunk_text(text, max_chars=2000):
    lines = text.splitlines()

    for line in lines:
        if len(line) > max_chars:
            for chunk in line.split(max_chars):
                yield chunk
        yield line
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
if __name__ == '__main__':
    with open("data/Linux_2k.log", "r", encoding="utf-8") as f:
        text = f.read()

    labels = ["work", "booking number", "personally identifiable information", "driver licence", "person", "book",
              "full address", "company", "actor", "character", "email", "passport number", "Social Security Number",
              "phone number", "ip address", "password"]


    # {'start': 72, 'end': 77, 'text': 'cyrus', 'label': 'person', 'score': 0.8641920685768127}
    chunked_text = chunk_text(text)
    for chunk in chunked_text:
        entities = model.predict_entities(
            chunk,
            labels,
            include_spans=True
        )
        for grp, start, end in sorted(
            [(f'[{entity['label']}]', entity['start'], entity['end']) for entity in entities],
        reverse=True):
            chunk = chunk[:start] + grp + chunk[end:]

        print(chunk)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
