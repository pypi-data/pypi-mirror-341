# mb_nlp

A simple package for text classification using the latest BERT models via Hugging Face Transformers.

## Installation

```bash
pip install mb_nlp
```

## Usage

```python
from mb_nlp import BertTextClassifier

classifier = BertTextClassifier(model_name='bert-base-uncased', num_labels=2)
prediction = classifier.predict("Your text here")
```

See `examples/example_usage.py` for more examples.

## Testing

Run the tests:

```bash
python tests/test_inputs.py
```
