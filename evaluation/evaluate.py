import re
from typing import List, TypedDict, Optional
import copy
import numpy as np
import pandas as pd
import json

class Label(TypedDict):
    label: str
    text: str
    score: Optional[float]

LABEL_SET  = {"PASSWORD",
    "PERSON",
    "NAME",
    "DATE_OF_BIRTH",
    "NINO",
    "NHS_NUMBER",
    "NATIONAL_INSURANCE_NUMBER",
    "PHONE_NUMBER",
    "BANK_SORT_CODE",
    "BANK_ACCOUNT_NUMBER",
    "CREDIT_CARD_NUMBER",
    "ADDRESS",
    "POSTCODE",
    "VEHICLE_REGISTRATION",
    "EMAIL_ADDRESS",}

class LabelDictionary(TypedDict):
    PASSWORD: str
    PERSON: str
    NAME: str
    DATE_OF_BIRTH: str
    NINO: str
    NHS_NUMBER: str
    NATIONAL_INSURANCE_NUMBER: str
    PHONE_NUMBER: str
    BANK_SORT_CODE: str
    BANK_ACCOUNT_NUMBER: str
    CREDIT_CARD_NUMBER: str
    ADDRESS: str
    POSTCODE: str
    VEHICLE_REGISTRATION: str
    EMAIL_ADDRESS: str

label_dictionary: LabelDictionary = {
    'PASSWORD': 'PASSWORD',
    'PERSON': 'PERSON',
    'NAME': 'NAME',
    'DATE_OF_BIRTH': 'DATE_OF_BIRTH',
    'NINO': 'NINO',
    'NHS_NUMBER': 'NHS_NUMBER',
    'NATIONAL_INSURANCE_NUMBER': 'NATIONAL_INSURANCE_NUMBER',
    'PHONE_NUMBER': 'PHONE_NUMBER',
    'BANK_SORT_CODE': 'BANK_SORT_CODE',
    'BANK_ACCOUNT_NUMBER': 'BANK_ACCOUNT_NUMBER',
    'CREDIT_CARD_NUMBER': 'CREDIT_CARD_NUMBER',
    'ADDRESS': 'ADDRESS',
    'POSTCODE': 'POSTCODE',
    'VEHICLE_REGISTRATION': 'VEHICLE_REGISTRATION',
    'EMAIL_ADDRESS': 'EMAIL_ADDRESS',
}

from typing import List, TypedDict, Optional
import copy
import numpy as np

class Label(TypedDict):
    label: str
    text: str
    score: Optional[float]

class LabelSets(TypedDict):
    labels: List[set[str]]

label_dict = {label: {} for label in sorted(LABEL_SET)}
label_dict_set = {label: set() for label in sorted(LABEL_SET)}

def word_set(text: str):
    return set(re.findall(r"\w+", str(text).lower()))

class BaseLabels:
    _items: List[Label]
    _sets: List[set[str]]
    _labels: set[str]
    LABEL_SET = {"PASSWORD",
                 "PERSON",
                 "NAME",
                 "DATE_OF_BIRTH",
                 "NINO",
                 "NHS_NUMBER",
                 "NATIONAL_INSURANCE_NUMBER",
                 "PHONE_NUMBER",
                 "BANK_SORT_CODE",
                 "BANK_ACCOUNT_NUMBER",
                 "CREDIT_CARD_NUMBER",
                 "ADDRESS",
                 "POSTCODE",
                 "VEHICLE_REGISTRATION",
                 "EMAIL_ADDRESS", }

    def __init__(self, items: List[Label]):
        self._items = items
        self._labels = { label['label'] for label in items }
        self._sets = [word_set(label['text']) for label in items]

    @property
    def labels(self) -> set[str]:
        return self._labels

    def __len__(self):
        return len(self._items)

    @property
    def items(self) -> List[Label]:
        return self._items

class Y(BaseLabels):
    _tree: dict[str, set[str]] # TODO: note this doesn't account for multiple entities per label

    def __init__(self, items: List[Label]):
        super().__init__(items)
        self._items = items
        self._tree = copy.deepcopy(label_dict_set)

        for label in items:
            self._tree[label['label']].add(label['text'])

class Predictions(BaseLabels):
    _pred_tree: dict[str, dict[str, float]]
    threshold: float = 0.5
    pred_to_base_labels: dict[str, str]
    _dict: dict[str, str]

    def __init__(self, predictions: List[Label], dictionary: dict[str, str] = label_dictionary):
        super().__init__(predictions)
        self._pred_tree = {k:{} for k in dictionary.values()}
        self.pred_to_base_labels = {v:k for k,v in dictionary.items()}
        self._dict = dictionary
        for label in predictions:
            self._pred_tree[label['label']][label['text']] = label['score']

    def __len__(self):
        return len(self._items)

    def has_entity(self, gt_label: Label, translation_dict: dict[str,str]) -> bool:
        translated_label = self._dict[gt_label['label']]
        if gt_label['text'] not in self._pred_tree[translated_label]:
            return False

        score = self._pred_tree[translated_label][gt_label['text']]
        return score >= self.threshold

    def has_entity_np(self, label: Label, translation_dict: dict[str,str]) -> np.int64:
        return np.int64(self.has_entity(label, translation_dict))

def match_greedy(s: np.ndarray, threshold=0.3):
    y, y_hat = s.shape
    matched_pred = set()
    matched_gold = set()
    matches = []

    pairs = [
        (i, j, s[i, j])
        for i in range(y)
        for j in range(y_hat)
        if s[i, j] >= threshold
    ]

    # Sort by similarity descending
    pairs.sort(key=lambda x: x[2], reverse=True)

    for i, j, score in pairs:
        if i not in matched_gold and j not in matched_pred:
            matched_pred.add(i)
            matched_gold.add(j)
            matches.append((i, j, score))

    tp = len(matches)
    fp = y_hat - tp
    fn = y - tp

    return tp, fp, fn, matches

class Evaluator(Y):
    confusion_matrix: np.ndarray = np.zeros(3).astype(np.int64)
    _to_base_labels: dict[str, str]
    _label_dictionary: dict[str, str]

    def __init__(self, items: List[Label], dictionary: LabelDictionary = label_dictionary):
        super().__init__(items)
        self._to_base_labels = {v:k for k,v in dictionary.items()}
        self._label_dictionary = dict(dictionary)

    def jaccard_similarity_matrix(self, predictions: List[Label]) -> np.ndarray:
        prediction_sets = [word_set(prediction['text']) for prediction in predictions]
        label_sets = self._sets

        S = np.zeros((len(label_sets), len(prediction_sets)))

        for i, gt in enumerate(label_sets):
            for j, pred in enumerate(prediction_sets):
                inter = len(gt & pred)
                union = len(gt | pred)
                S[i, j] = inter / union if union else 0.0

        return S

    def evaluate(self, predictions: List[Label]) -> 'Evaluator':
        matrix = self.jaccard_similarity_matrix(predictions)

        tp, fp, fn, _matches = match_greedy(matrix)

        self.confusion_matrix = np.array([tp, fp, fn]).astype(np.int64)

        return self

    def predict(self, predictions_list: List[Label]):
        predictions = Predictions(predictions_list, self._label_dictionary)

        tp = np.array([predictions.has_entity(gt_entity, self._label_dictionary) for gt_entity in self._items]).astype(np.int64)
        fn = 1 - tp
        fp = max(np.int64(0), len(predictions) - tp.sum())

        self.confusion_matrix = np.array([tp.sum(), fp.sum(), fn.sum()]).astype(np.int64)

        return self

    def metrics(self):
        return self.calculate_metrics(self.confusion_matrix)

    @classmethod
    def calculate_metrics(cls, confusion_matrix: np.ndarray):
        tp, fp, fn = confusion_matrix
        accuracy = tp.sum() / (tp.sum() + fp.sum() + fn.sum()) if tp.sum() > 0 else np.float64(0)
        precision = tp.sum() / (tp.sum() + fp.sum()) if tp.sum() > 0 else np.float64(0)
        recall = tp.sum() / (tp.sum() + fn.sum()) if tp.sum() > 0 else np.float64(0)
        f1 = 2 * ((precision * recall) / (precision + recall)) if tp.sum() > 0 else np.float64(0)

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }


class AggEvaluator:
    _base_truth_predictors: List[Evaluator]
    _metrics: List[dict]
    _pred_df: pd.DataFrame

    def __init__(self, base_truth_labels: List[List[Label]], dictionary: LabelDictionary | None = None):
        self._base_truth_predictors = [Evaluator(gt) for gt in base_truth_labels] if dictionary is None else [Evaluator(gt, dictionary) for gt in base_truth_labels]

    def __len__(self):
        return len(self._base_truth_predictors)

    def __iter__(self):
        for x in self._base_truth_predictors:
            yield x

    def predict(self, predictions: pd.DataFrame) -> pd.DataFrame:
        zipped_preds = zip(predictions['labels'], self)
        predictions['results'] = [eval.evaluate(pred).confusion_matrix for pred, eval in zipped_preds]

        return predictions['results']

    @classmethod
    def get_predictions(cls, preds_path: str):
        with open(preds_path) as f:
            predictions = pd.DataFrame({"labels": [json.loads(line.rstrip("\n")) for line in f]})

        return predictions

    @classmethod
    def instance(cls, dictionary: LabelDictionary | None = None, labels_path: str = '../data/labels.jsonl'):
        with open(labels_path) as f:
            logs_df = pd.DataFrame({"labels": [json.loads(line.rstrip("\n")) for line in f]})

            return cls(logs_df['labels'], dictionary)

    @classmethod
    def calculate_metrics(cls, confusion_matrix: np.ndarray):
        return Evaluator.calculate_metrics(confusion_matrix)


if __name__ == "__main__":
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
    evaluator = AggEvaluator.instance(
        dictionary=label_dictionary,
        labels_path='../data/labels.jsonl'
    )
    predictions = evaluator.get_predictions('../data/gliner/results.jsonl')
    prediction_scores = evaluator.predict(predictions)

    print(evaluator.calculate_metrics(prediction_scores.sum()))