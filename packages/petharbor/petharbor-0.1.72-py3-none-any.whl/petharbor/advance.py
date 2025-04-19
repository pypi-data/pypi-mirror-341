from petharbor.utils.dataset import DatasetProcessor
from petharbor.utils.model import get_predictions_and_anonymise
from petharbor.utils.logging_setup import get_logger
from datasets import Dataset
from typing import Optional, Dict, Any
import torch
import logging
import pandas as pd

class Anonymiser:
    """Anonymises text data using a pre-trained model.
    
    Args:
        dataset (str): Path to the dataset file (CSV, Arrow, etc.).
        model (str): Path to the model.
        text_column (str): Column name in the dataset containing text data.
        cache (bool): Whether to use cache.
        cache (str): Path to save cache files.
        logs (Optional[str]): Path to save logs.
        device (Optional[str]): Device to use for computation ('cpu' or 'cuda').
        tag_map (Optional[Dict[str, str]]): Mapping of entity tags to replacement strings. Defaults to {"PER": "<<NAME>>", "LOC": "<<LOCATION>>","ORG": "<<ORG>>", "MISC": "<<MISC>>"}.
        output_dir (str): Directory to save the output files.
    """
    
    def __init__(
        self,
        dataset: str = None, # Path to the dataset file (CSV, Arrow, etc.)
        split: str = "train", # Split of the dataset to use (e.g., 'train', 'test', 'eval')
        model: str = "SAVSNET/PetHarbor", # Path to the model
        tokenizer: str = None, # Path to the tokenizer
        text_column: str = "text", # Column name in the dataset containing text data
        cache: bool = True, # Whether to use cache
        cache_path: str = "petharbor_cache/", # Path to save cache files
        logs: Optional[str] = None, # Path to save logs
        device: Optional[str] = "cuda" if torch.cuda.is_available() else "cpu",
        tag_map: Optional[Dict[str, str]] = {"PER": "<<NAME>>", "LOC": "<<LOCATION>>","TIME": "<<TIME>>", "ORG": "<<ORG>>", "MISC": "<<MISC>>"}, # Mapping of entity tags to replacement strings
        output_dir: str = None, # Directory to save the output files
    ):
        self.dataset = dataset
        self.split = split
        self.model = model
        self.tokenizer = tokenizer
        self.text_column = text_column
        self.cache = cache
        self.cache_path = cache_path
        self.logs = logs
        self.device = device
        self.tag_map = tag_map
        self.output_dir = output_dir

        self.logger = self._setup_logger()
        logger = logging.getLogger(__name__)
        self.dataset_processor = DatasetProcessor(self.cache_path)

    def _setup_logger(self) -> Any:
        return (
            get_logger(log_dir=self.logs, method="Advance")
            if self.logs
            else get_logger(method="Advance")
        )
        
        

    # def _validate_dataset(self, dataset, empty_tag="<<EMPTY>>") -> None:
    #     if self.text_column not in dataset.column_names:
    #         raise ValueError(
    #             f"Text column '{self.text_column}' not found in dataset. Please add 'text_column' column to the class."
    #         )
    #     # drop missing rows 
    #     clean_dataset = dataset.filter(
    #         lambda example: example[self.text_column] is not None
    #     )
    #     # drop empty strings
    #     clean_dataset = clean_dataset.filter(
    #         lambda example: example[self.text_column].strip() != ""
    #     )
    #     logging.info(f'Dropped {len(dataset) - len(clean_dataset)} empty strings from {self.text_column} column')
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
        if text and self.dataset:
            raise ValueError(
                "Please provide either a text string or a dataset path, not both."
            )
        if text:
            self.logger.warning(
                "Anonymizing single text. For much faster processing of datasets, initialize with 'dataset_path'."
            )            
            text = str(text).strip()
            target_dataset = pd.DataFrame({self.text_column: [text]})
            target_dataset = Dataset.from_pandas(target_dataset)

        elif self.dataset:
            original_data = self.dataset_processor.load_dataset_file(self.dataset, split=self.split)
            #self._validate_dataset(original_data)
            target_dataset, original_data = self.dataset_processor.load_cache(
                dataset=original_data, cache=self.cache
            )
        else:
            raise ValueError("Please provide either a text string or a dataset path.")
        
        predictions = get_predictions_and_anonymise(
            model=self.model,
            tokenizer=self.tokenizer,
            target_dataset=target_dataset,
            replaced=True,
            tag_map=self.tag_map,
            text_column=self.text_column,
            device=self.device,
        )
        if text:
            date_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{date_time} | SUCCESS | PetHarbor-Advance] Input: {text}")
            print(f"[{date_time} | SUCCESS | PetHarbor-Advance] Output: {predictions[0]}")
        
            
        else:
            self.dataset_processor.save_dataset_file(
                original_data=original_data,
                target_dataset=target_dataset,
                cache=self.cache,
                output_dir=self.output_dir,
            )