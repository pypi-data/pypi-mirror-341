from transformers import BertTokenizer, BertForSequenceClassification, AdamW
import torch
from torch.utils.data import DataLoader
from mb_nlp.data.dataset import TextDataset
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm

from typing import List, Optional, Union

__all__ = ['BertTextClassifier']

class BertTextClassifier:
    """
    BERT-based text classifier supporting training and inference.
    """
    def __init__(self, model_name: str = 'bert-base-uncased', num_labels: int = 2, device: Optional[str] = None) -> None:
        """
        Initialize the BERT text classifier.

        Parameters
        ----------
        model_name : str, optional
            Name of the BERT model to use.
        num_labels : int, optional
            Number of target classes.
        device : str or None, optional
            Device to use ('cuda', 'cpu'). If None, auto-detect.
        """
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def predict(self, texts: Union[str, List[str]]) -> List[int]:
        """
        Predict class labels for input texts.

        Parameters
        ----------
        texts : str or list of str
            Input text(s) to classify.

        Returns
        -------
        list of int
            Predicted class indices.
        """
        if isinstance(texts, str):
            texts = [texts]
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)
        return preds.cpu().tolist()

    def train(
        self,
        train_texts: List[str],
        train_labels: List[int],
        val_texts: Optional[List[str]] = None,
        val_labels: Optional[List[int]] = None,
        epochs: int = 3,
        batch_size: int = 8,
        lr: float = 2e-5
    ) -> None:
        """
        Fine-tune the BERT classifier on provided data.

        Parameters
        ----------
        train_texts : list of str
            Training texts.
        train_labels : list of int
            Training labels.
        val_texts : list of str, optional
            Validation texts.
        val_labels : list of int, optional
            Validation labels.
        epochs : int, optional
            Number of epochs.
        batch_size : int, optional
            Batch size.
        lr : float, optional
            Learning rate.
        """
        train_dataset = TextDataset(train_texts, train_labels, self.tokenizer)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        if val_texts is not None and val_labels is not None:
            val_dataset = TextDataset(val_texts, val_labels, self.tokenizer)
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

    def evaluate(self, val_loader: DataLoader) -> None:
        """
        Evaluate the model on a validation DataLoader.

        Parameters
        ----------
        val_loader : DataLoader
            Validation data loader.
        """
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

    def train_from_csv(
        self,
        csv_path: str,
        text_col: str = 'text',
        label_col: str = 'label',
        test_size: float = 0.1,
        epochs: int = 3,
        batch_size: int = 8,
        lr: float = 2e-5
    ) -> None:
        """
        Fine-tune the classifier using a CSV file.

        Parameters
        ----------
        csv_path : str
            Path to the CSV file.
        text_col : str, optional
            Name of the text column.
        label_col : str, optional
            Name of the label column.
        test_size : float, optional
            Fraction of data to use for validation.
        epochs : int, optional
            Number of epochs.
        batch_size : int, optional
            Batch size.
        lr : float, optional
            Learning rate.
        """
        df = pd.read_csv(csv_path)
        train_df, val_df = train_test_split(df, test_size=test_size, stratify=df[label_col])
        train_texts = train_df[text_col].tolist()
        train_labels = train_df[label_col].tolist()
        val_texts = val_df[text_col].tolist()
        val_labels = val_df[label_col].tolist()
        self.train(train_texts, train_labels, val_texts, val_labels, epochs=epochs, batch_size=batch_size, lr=lr)
