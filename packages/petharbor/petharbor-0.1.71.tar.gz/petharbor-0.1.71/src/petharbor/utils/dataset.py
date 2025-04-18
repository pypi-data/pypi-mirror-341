import logging
import pandas as pd
from datasets import load_from_disk, load_dataset

logger = logging.getLogger(__name__)


class DatasetProcessor:

    def load_dataset_file(self, file_path: str) -> dict:
        """
        Attempt to load a dataset using multiple strategies:
        1. As a HuggingFace Arrow dataset from disk.
        2. As a CSV file via HuggingFace `load_dataset`.
        3. As a generic dataset via HuggingFace `load_dataset`.

        Returns:
            A dictionary with keys as split names (e.g., 'train', 'test') and values as datasets.
        """ 
        # Try loading from disk
        if file_path.endswith("csv"):
            try:
                dataset = load_dataset("csv", data_files=file_path)
                logger.info(f"Loaded dataset from {file_path}")
            except Exception as e:
                logger.error(f"Failed to load dataset from {file_path}: {e}.")
                raise
        else:
            try:
                dataset = load_from_disk(file_path)
                logger.info(f"Loaded dataset from {file_path}")
            except Exception as e:
                logger.error(f"Failed to load dataset from {file_path}: {e}")
                raise 
        # Check if dataset is empty
        if not dataset:
            logger.error(f"Dataset is empty or not found at {file_path}")
            raise ValueError(f"Dataset is empty or not found at {file_path}")
        else:
            return dataset

    def load_cache(self, dataset, use_cache: bool = False) -> tuple:
        """
        Filter out anonymized data and check if the dataset contains non-anonymized records.
        """
        if use_cache:
            try:
                target_dataset = dataset.filter(
                    lambda example: example["annonymised"] == 0
                )
                logger.info(
                    f"Cache enabled | skipping anonymization for {len(dataset)} rows | Running on {len(target_dataset)} rows"
                )
            except:
                target_dataset = dataset

            if len(target_dataset) == 0:
                logger.info("All data has been anonymized, exiting...")
                exit()
            else:
                logger.info(f"Anonymizing {len(target_dataset)} rows")
        else:
            target_dataset = dataset

        return target_dataset, dataset

    def save_dataset_file(
        self,
        original_data,
        target_dataset,
        predictions: list = None,
        text_column: str = "text",
        output_dir: str = "predictions.csv",
        cache=False,
    ):
        """
        Save dataset predictions to a file.
        """
        logger.info(f"Saving predictions to {output_dir}")
        df_new = target_dataset.to_pandas()
        if predictions:
            df_new[text_column] = predictions
        df_new["annonymised"] = 1

        if cache:
            df_old = original_data.to_pandas()
            df_new = pd.concat([df_old, df_new], ignore_index=True)

        output_path = (
            output_dir
            if output_dir.endswith(".csv")
            else f"{output_dir}/predictions.csv"
        )
        df_new.to_csv(output_path, index=False)
