from transformers import BertTokenizer, BertForSequenceClassification, AdamW
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

class BertTextClassifier:
    def __init__(self, model_name='bert-base-uncased', num_labels=2, device=None):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def predict(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)
        return preds.cpu().tolist()

    class TextDataset(Dataset):
        def __init__(self, texts, labels, tokenizer, max_length=128):
            self.texts = texts
            self.labels = labels
            self.tokenizer = tokenizer
            self.max_length = max_length

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, idx):
            item = self.tokenizer(
                self.texts[idx],
                padding='max_length',
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            )
            item = {k: v.squeeze(0) for k, v in item.items()}
            item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
            return item

    def train(self, train_texts, train_labels, val_texts=None, val_labels=None, epochs=3, batch_size=8, lr=2e-5):
        train_dataset = self.TextDataset(train_texts, train_labels, self.tokenizer)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        if val_texts is not None and val_labels is not None:
            val_dataset = self.TextDataset(val_texts, val_labels, self.tokenizer)
            val_loader = DataLoader(val_dataset, batch_size=batch_size)
        else:
            val_loader = None
        optimizer = AdamW(self.model.parameters(), lr=lr)
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
                batch = {k: v.to(self.device) for k, v in batch.items()}
                outputs = self.model(**batch)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                total_loss += loss.item()
            print(f"Epoch {epoch+1} training loss: {total_loss / len(train_loader):.4f}")
            if val_loader:
                self.evaluate(val_loader)
        self.model.eval()

    def evaluate(self, val_loader):
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                batch = {k: v.to(self.device) for k, v in batch.items()}
                outputs = self.model(**batch)
                preds = torch.argmax(outputs.logits, dim=1)
                correct += (preds == batch['labels']).sum().item()
                total += batch['labels'].size(0)
        acc = correct / total if total > 0 else 0
        print(f"Validation accuracy: {acc:.4f}")
        self.model.train()

    def train_from_csv(self, csv_path, text_col='text', label_col='label', test_size=0.1, epochs=3, batch_size=8, lr=2e-5):
        df = pd.read_csv(csv_path)
        train_df, val_df = train_test_split(df, test_size=test_size, stratify=df[label_col])
        train_texts = train_df[text_col].tolist()
        train_labels = train_df[label_col].tolist()
        val_texts = val_df[text_col].tolist()
        val_labels = val_df[label_col].tolist()
        self.train(train_texts, train_labels, val_texts, val_labels, epochs=epochs, batch_size=batch_size, lr=lr)
