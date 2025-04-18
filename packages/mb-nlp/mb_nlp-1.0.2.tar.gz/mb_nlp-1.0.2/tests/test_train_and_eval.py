from mb_bert_classifier.classifier import BertTextClassifier

# Use the synthetic CSV for training
csv_path = 'tests/synthetic_train.csv'

if __name__ == '__main__':
    clf = BertTextClassifier(model_name='bert-base-uncased', num_labels=2)
    print('Training on synthetic data...')
    clf.train_from_csv(csv_path, text_col='text', label_col='label', epochs=1, batch_size=2, test_size=0.2)
    print('Testing predictions:')
    test_texts = [
        'I am very happy!',
        'This is bad.',
        'Excellent quality and service.',
        'I will never buy again.'
    ]
    preds = clf.predict(test_texts)
    for text, pred in zip(test_texts, preds):
        print(f'Input: {text!r} => Predicted label: {pred}')
