from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
)
import torch
import gc
from .func import compute_metrics_multi_labels, compute_metrics_multi_class
from .config import Config


class Pipeline:
    def __init__(
            self,
            pretrained_model: str,
            task_type: str = "multi_classes",
            hub_model_id: str = None,
            use_bf16: bool = False,
            **kwargs
    ):
        # config
        self.pretrained_model = pretrained_model
        self.id2label = kwargs.get("id2label", {})
        self.label2id = kwargs.get("label2id", {})
        self.use_bf16 = use_bf16
        self.flash_attention_2 = kwargs.get("flash_attention_2", False)
        self.hub_model_id = hub_model_id

        # problem type
        self.task_type = "multi_labels" if task_type != "multi_classes" else None
        self.metrics = (
            compute_metrics_multi_labels
            if task_type != "multi_classes"
            else compute_metrics_multi_class
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_model()
        self._print_summary()

    def _print_summary(self):
        gpu_info = (
            (
                f"CUDA: {torch.cuda.get_device_properties(0).name}, "
                f"Flash Attention: {torch.backends.cuda.flash_sdp_enabled()}"
            )
            if self.device.type == "cuda"
            else "CPU only"
        )
        print(f"""
*** [Configuration] ***
- Torch version: {torch.__version__}
- Device: {self.device}, {gpu_info}
- Model: {self.pretrained_model}
- Precision: {'BF16' if self.use_bf16 else 'FP32'}
- Task type: {self.task_type}
""")

    def _load_model(self):
        print(f"Pretrain: {self.pretrained_model}")

        config = {
            "pretrained_model_name_or_path": self.pretrained_model,
            "num_labels": len(self.id2label),
            "id2label": self.id2label,
            "label2id": self.label2id,
            "problem_type": self.task_type,
        }
        if self.use_bf16:
            config["torch_dtype"] = torch.bfloat16
        if self.flash_attention_2:
            config["attn_implementation"] = "flash_attention_2"

        self.tokenizer = AutoTokenizer.from_pretrained(self.pretrained_model)
        self.data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        self.model = AutoModelForSequenceClassification.from_pretrained(**config)

    def train(self, folder: str, train, val, **kwargs):
        log_step = kwargs.get("log_step", 50)
        training_args = TrainingArguments(
            output_dir=folder,
            warmup_ratio=0.1,
            lr_scheduler_type="cosine",
            weight_decay=0.001,
            learning_rate=kwargs.get("learning_rate", 1e-4),
            per_device_train_batch_size=kwargs.get("per_device_train_batch_size", 512),
            per_device_eval_batch_size=kwargs.get("per_device_eval_batch_size", 64),
            bf16=self.use_bf16,
            logging_strategy="steps",
            save_strategy="steps",
            eval_strategy="steps",
            save_steps=log_step,
            eval_steps=log_step,
            logging_steps=log_step,
            save_total_limit=2,
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            report_to="none",
            num_train_epochs=kwargs.get("num_train_epochs", 3),
            optim="adamw_torch_fused",
        )
        if self.hub_model_id:
            config = Config()
            training_args.hub_token = config.hub_token
            training_args.push_to_hub = config.push_to_hub
            training_args.hub_private_repo = config.hub_private_repo
            training_args.hub_model_id = self.hub_model_id

        # train
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train,
            eval_dataset=val,
            data_collator=self.data_collator,
            compute_metrics=self.metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
        )
        train_results = trainer.train()

        # save model
        trainer.save_model()
        trainer.log_metrics("train", train_results.metrics)
        trainer.save_metrics("train", train_results.metrics)
        trainer.save_state()
        trainer.create_model_card()
        self.tokenizer.save_pretrained(folder)

        # clean cache
        torch.cuda.empty_cache()
        gc.collect()

        return trainer
