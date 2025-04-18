from mb_bert_classifier.classifier import BertTextClassifier

def test_various_inputs():
    classifier = BertTextClassifier(model_name='bert-base-uncased', num_labels=2)
    test_cases = [
        "Normal sentence.",
        "",
        "1234567890",
        "!@#$%^&*()",
        "A" * 512,
        ["First", "Second", "", "Third"]
    ]
    for case in test_cases:
        try:
            result = classifier.predict(case)
            print(f"Input: {repr(case)} => Output: {result}")
        except Exception as e:
            print(f"Input: {repr(case)} => Exception: {e}")

if __name__ == "__main__":
    test_various_inputs()
