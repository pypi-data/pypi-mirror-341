from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from torch.utils.data import Dataset, DataLoader
from torch.amp import autocast
from tqdm.auto import tqdm
from accelerate import Accelerator


class TextDataset(Dataset):
    def __init__(self, texts: list[str]):
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx: int) -> str:
        return self.texts[idx]


class FastTextClassifier:
    def __init__(
        self,
        model_name: str,
        bf16: bool = True,
        use_torch_compile: bool = True,
        max_length: int = 50,
    ):
        """
        Super‑fast text classifier:
          - Batches raw lists of strings
          - Mixed‑precision & pinned memory
          - TorchCompile / TorchScript
          - (Optional) dynamic quantization for CPU

        :param model_name: HuggingFace model ID or local path
        :param bf16: run in bfloat16 on GPU
        :param use_torch_compile: wrap in torch.compile (PyTorch >=2.0)
        :param max_length: tokenizer max length
        """
        self.device = Accelerator().device
        self.bf16 = bf16
        self.max_length = max_length

        # 1) load tokenizer & model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype=(torch.bfloat16 if self.bf16 else None),
        ).to(self.device)

        # 2) compile / script for extra speed
        if use_torch_compile and hasattr(torch, "compile"):
            self.model = torch.compile(self.model)

        self.model.eval()
        self.id2label = list(self.model.config.id2label.values())


    def _collate_fn(self, batch_texts: list[str]):
        enc = self.tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        return enc

    def predict_with_dataloader(
        self,
        texts: list[str],
        multi_label: bool = False,
        num_workers: int = 8,
        prefetch_factor: int = 2,
        batch_size: int = 512,
    ) -> dict[str, list]:
        """
        Inference over a list of texts via DataLoader.
        """
        ds = TextDataset(texts)
        loader = DataLoader(
            ds,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            pin_memory=True,
            prefetch_factor=prefetch_factor,
            collate_fn=self._collate_fn,
        )

        all_labels = []
        all_scores = []
        with torch.inference_mode():
            for batch_enc in tqdm(loader, desc="Inference"):
                # move to device
                batch_enc = {
                    k: v.to(self.device, non_blocking=True)
                    for k, v in batch_enc.items()
                }

                # mixed‑precision on GPU
                if self.bf16:
                    with autocast(self.device.type, dtype=torch.bfloat16):
                        logits = self.model(**batch_enc).logits
                else:
                    logits = self.model(**batch_enc).logits

                probs = logits.softmax(dim=-1)
                if multi_label:
                    scores = probs.half().cpu().detach().numpy().tolist()
                    all_scores.extend(scores)
                    all_labels = [self.id2label] * len(texts)
                else:
                    scores, indices = torch.max(probs, dim=1)
                    scores = scores.half().cpu().detach().numpy().tolist()
                    labels = [
                        self.id2label[idx]
                        for idx in indices.cpu().detach().numpy().tolist()
                    ]
                    all_scores.extend(scores)
                    all_labels.extend(labels)

        return {"labels": all_labels, "scores": all_scores}
