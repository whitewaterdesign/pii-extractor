from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    pipeline
)
import torch
import re

# MODEL_PATH = "./sdlog_main"
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

MODEL_MAIN = "LogSensitiveResearcher/SDLog_main"
TOKENIZER_BASE = "microsoft/codebert-base"

tokenizer_main = AutoTokenizer.from_pretrained(TOKENIZER_BASE)


model_main = AutoModelForTokenClassification.from_pretrained(MODEL_MAIN)

ner_main = pipeline(
    "token-classification",
    model=model_main,
    tokenizer=tokenizer_main,
    aggregation_strategy="simple"
)

# Optional: move to GPU if available
# device = 0 if torch.cuda.is_available() else -1

# ner_main = pipeline(
#     "token-classification",
#     model=model,
#     tokenizer=tokenizer,
#     aggregation_strategy="simple",
#     device=device
# )

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
    # text = "1,Jun,14,15:16:01,combo,sshd(pam_unix),19939,authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4,E16,authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=<*>"
    # results = pii_ner(text)
    # for r in results:
    #     print(f"{r['entity_group']:12s} | {r['word']} | {r['score']:.3f}")
    # redacted = text
    # for chunk in chunk_text(text):
    #     results = pii_ner(chunk)
    #     for r in results:
    #         if r["score"] > 0.6:
    #             redacted = redacted.replace(r["word"], f"[{r['entity_group']}]")

    # with open("logs_redacted.txt", "w", encoding="utf-8") as f:
    #     f.write(redacted)

    # for chunk in chunk_text(text):
    for chunk in ['Jul 27 14:41:58 combo kernel: NET: Registered protocol Chris Cole 12 Eggles Drive London']:
        results = ner_main(chunk)

        for grp, start, end in sorted([(f'[{result['entity_group']}]', result['start'], result['end']) for result in results], reverse=True):
            chunk = chunk[:start] + grp + chunk[end:]
        print(chunk)
    # print(chunks[0], results[0])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
