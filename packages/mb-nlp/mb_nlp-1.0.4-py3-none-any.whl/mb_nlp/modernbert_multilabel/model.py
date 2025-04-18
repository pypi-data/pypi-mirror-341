from transformers import AutoTokenizer, ModernBertForSequenceClassification
from torch.optim import AdamW
import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from typing import List, Optional, Any

class ModernBertMultiLabelDataset(Dataset):
    """
    PyTorch Dataset for multi-label classification with ModernBERT.
    Each label is assumed to be a multi-hot encoded vector (list of 0/1).
    """
    def __init__(self, texts: List[str], labels: List[List[int]], tokenizer: Any, max_length: int = 128):
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
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.float)
        return item

class ModernBertMultiLabelClassifier:
    """
    Multi-label text classifier using ModernBERT.
    """
    def __init__(self, model_name: str = 'answerdotai/ModernBERT-base', num_labels: Optional[int] = None, device: Optional[str] = None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        model_kwargs = {'problem_type': 'multi_label_classification'}
        if num_labels is not None:
            model_kwargs['num_labels'] = num_labels
        self.model = ModernBertForSequenceClassification.from_pretrained(model_name, **model_kwargs)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def train(self, train_texts: List[str], train_labels: List[List[int]], val_texts: Optional[List[str]] = None, val_labels: Optional[List[List[int]]] = None, epochs: int = 3, batch_size: int = 8, lr: float = 2e-5):
        train_dataset = ModernBertMultiLabelDataset(train_texts, train_labels, self.tokenizer)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        if val_texts is not None and val_labels is not None:
            val_dataset = ModernBertMultiLabelDataset(val_texts, val_labels, self.tokenizer)
            val_loader = DataLoader(val_dataset, batch_size=batch_size)
        else:
            val_loader = None
        optimizer = AdamW(self.model.parameters(), lr=lr)
        self.model.train()
        for epoch in range(epochs):
            total_loss = 0
            for batch in train_loader:
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

    def evaluate(self, val_loader: DataLoader):
        self.model.eval()
        total = 0
        correct = 0
        with torch.no_grad():
            for batch in val_loader:
                batch = {k: v.to(self.device) for k, v in batch.items()}
                outputs = self.model(**batch)
                logits = outputs.logits
                preds = (torch.sigmoid(logits) > 0.5).int()
                labels = batch['labels'].int()
                correct += (preds == labels).sum().item()
                total += torch.numel(labels)
        acc = correct / total if total > 0 else 0
        print(f"Validation accuracy (per label): {acc:.4f}")
        self.model.train()

    def predict(self, texts: List[str]) -> List[List[int]]:
        self.model.eval()
        if isinstance(texts, str):
            texts = [texts]
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt").to(self.device)
        with torch.no_grad():
            logits = self.model(**inputs).logits
            preds = (torch.sigmoid(logits) > 0.5).int().cpu().tolist()
        return preds

    def train_from_csv(self, csv_path: str, text_col: str = 'text', label_cols: Optional[List[str]] = None, test_size: float = 0.1, epochs: int = 3, batch_size: int = 8, lr: float = 2e-5):
        df = pd.read_csv(csv_path)
        if label_cols is None:
            label_cols = [col for col in df.columns if col != text_col]
        train_df, val_df = train_test_split(df, test_size=test_size, stratify=None)
        train_texts = train_df[text_col].tolist()
        train_labels = train_df[label_cols].values.tolist()
        val_texts = val_df[text_col].tolist()
        val_labels = val_df[label_cols].values.tolist()
        self.train(train_texts, train_labels, val_texts, val_labels, epochs=epochs, batch_size=batch_size, lr=lr)
