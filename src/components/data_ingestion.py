import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging
from src.components.data_tranformation import DataTranformations


# -------------------- CONFIG CLASS --------------------
@dataclass
class DataIngestionConfig:
    artifacts_dir: str = "artifacts"
    train_data_path: str = os.path.join(artifacts_dir, "train.csv")
    test_data_path: str = os.path.join(artifacts_dir, "test.csv")
    raw_data_path: str = os.path.join(artifacts_dir, "data.csv")


# -------------------- DATA INGESTION CLASS --------------------
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion component")

        try:
            current_dir = os.path.dirname(__file__)
            src_dir = os.path.abspath(os.path.join(current_dir, ".."))
            dataset_path = os.path.join(
                src_dir, "notebook", "data", "StudentsPerformance.csv"
            )

            print("Reading dataset from:", dataset_path)

            df = pd.read_csv(dataset_path)
            logging.info("Dataset loaded into DataFrame")

            os.makedirs(self.ingestion_config.artifacts_dir, exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42
            )

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            print("ERROR:", e)
            raise CustomException(e, sys)


# -------------------- RUN AS MODULE --------------------
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_tranformation = DataTranformations()
    data_tranformation.initiate_data_tranformations(train_data, test_data)