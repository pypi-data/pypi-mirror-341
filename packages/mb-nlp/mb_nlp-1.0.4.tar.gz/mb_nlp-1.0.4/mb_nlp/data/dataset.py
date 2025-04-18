from torch.utils.data import Dataset
import torch

from typing import List, Any

class TextDataset(Dataset):
    """
    PyTorch Dataset for text classification tasks.
    """
    def __init__(self, texts: List[str], labels: List[int], tokenizer: Any, max_length: int = 128) -> None:
        """
        Parameters
        ----------
        texts : list of str
            List of input texts.
        labels : list of int
            List of integer labels.
        tokenizer : Any
            HuggingFace tokenizer instance.
        max_length : int, optional
            Max sequence length for tokenization.
        """
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        """
        Returns
        -------
        int
            Number of samples in the dataset.
        """
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict:
        """
        Parameters
        ----------
        idx : int
            Index of the sample.

        Returns
        -------
        dict
            Tokenized input and label tensor.
        """
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
