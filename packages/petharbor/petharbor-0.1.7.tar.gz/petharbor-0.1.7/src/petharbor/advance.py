from petharbor.utils.dataset import DatasetProcessor
from petharbor.utils.device import configure_device
from petharbor.utils.model import load_model, get_predictions_and_anonymise
from petharbor.utils.logging_setup import get_logger
from datasets import Dataset
from typing import Optional, Dict, Any
import torch
import logging
import pandas as pd

class Anonymiser:
    def __init__(
        self,
        dataset_path: str = None,
        model_path: str = "SAVSNET/PetHarbor",
        text_column: str = "text",
        cache: bool = True,
        logs: Optional[str] = None,
        device: Optional[str] = "cuda" if torch.cuda.is_available() else "cpu",
        output_dir: str = "output/",
    ):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.text_column = text_column
        self.cache = cache
        self.logs = logs
        self.device = device
        self.output_dir = output_dir

        self.logger = self._setup_logger()
        logger = logging.getLogger(__name__)
        self.device = configure_device(self.device)
        self.model, self.tokenizer = load_model(self.model_path, self.device)
        self.dataset_processor = DatasetProcessor()

    def _setup_logger(self) -> Any:
        return (
            get_logger(log_dir=self.logs, method="Advance")
            if self.logs
            else get_logger(method="Advance")
        )

    def _validate_dataset(self, dataset, empty_tag="<<EMPTY>>") -> None:
        if self.text_column not in dataset.column_names:
            raise ValueError(
                f"Text column '{self.text_column}' not found in dataset. Please add 'text_column' column to the class."
            )
        # drop missing rows 
        clean_dataset = dataset.filter(
            lambda example: example[self.text_column] is not None
        )
        # drop empty strings
        clean_dataset = clean_dataset.filter(
            lambda example: example[self.text_column].strip() != ""
        )
        logging.info(f'Dropped {len(dataset) - len(clean_dataset)} empty strings from {self.text_column} column')
        # if dataset["test"][self.text_column].str.strip().str.len().sum() == 0:
        #     # Replace empty strings with a tag
        #     dataset["test"][self.text_column] = dataset["test"][
        #         self.text_column
        #     ].str.replace("", f"{empty_tag}")
        #     self.logger.warning(
        #         f"Replaced {dataset['test'][self.text_column].str.count(f'{empty_tag}').sum()} empty strings with '{empty_tag}' in {self.text_column} column"
        #     )

    def anonymise(self, text: str = None) -> None:
        """Anonymizes the single text data or in a dataset and output/saves the results."""
        if text and self.dataset_path:
            raise ValueError(
                "Please provide either a text string or a dataset path, not both."
            )
        if text:
            text = str(text).strip()
            target_dataset = pd.DataFrame({self.text_column: [text]})
            target_dataset = Dataset.from_pandas(target_dataset)

        elif self.dataset_path:
            original_data = self.dataset_processor.load_dataset_file(self.dataset_path)
            self._validate_dataset(original_data)
            target_dataset, original_data = self.dataset_processor.load_cache(
                dataset=original_data, use_cache=self.cache
            )
        else:
            raise ValueError("Please provide either a text string or a dataset path.")
        predictions = get_predictions_and_anonymise(
            model=self.model,
            tokenizer=self.tokenizer,
            target_dataset=target_dataset,
            replaced=True,
            text_column=self.text_column,
            device=self.device,
        )
        if text:
            print(predictions)
        else:
            self.dataset_processor.save_dataset_file(
                original_data=original_data,
                target_dataset=target_dataset,
                predictions=predictions,
                text_column=self.text_column,
                output_dir=self.output_dir,
            )