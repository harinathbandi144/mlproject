import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


# -------------------- CONFIG CLASS --------------------
# Stores all output file paths in one place
@dataclass
class DataIngestionConfig:
    artifacts_dir: str = "Artifacts"
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
            # ✅ Build dataset path relative to THIS file (production-safe way)
            current_dir = os.path.dirname(__file__)              # src/components
            src_dir = os.path.abspath(os.path.join(current_dir, ".."))  # src
            dataset_path = os.path.join(
                src_dir, "notebook", "data", "StudentsPerformance.csv"
            )

            print("Reading dataset from:", dataset_path)

            # Read dataset
            df = pd.read_csv(dataset_path)
            logging.info("Dataset loaded into DataFrame")

            # Create Artifacts folder
            os.makedirs(self.ingestion_config.artifacts_dir, exist_ok=True)

            # Save raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train-Test split initiated")

            # Train test split
            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42
            )

            # Save train and test
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data ingestion completed successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            print("ERROR:", e)  # temporary debug visibility
            raise CustomException(e, sys)


# -------------------- RUN AS MODULE --------------------
# Run using:
# python -m src.components.data_ingestion
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()







# import os
# import sys
# from src.exception import CustomException
# from src.logger import logging
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from dataclasses import dataclass

# @dataclass
# class DataIngestionConfig:
#     train_data_path: str = os.path.join('Artifacts', 'train.csv')
#     test_data_path: str = os.path.join('Artifacts', 'test.csv')
#     raw_data_path: str = os.path.join('Artifats', 'data.csv')

# class DataIngestion:
#     def __init__(self):
#         self.ingestion_config = DataIngestionConfig()

#     def initiate_data_ingestion(self):
#         logging.info("Entered the data ingestion method or component")

#         try:
#             df = pd.read_csv("notebook/data/StudentsPerformance.csv")
#             logging.info("Exported the red the data set as Data frame")

#             os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True) # we are creating directory/artifact of train data
            
#             df.to_csv(self.ingestion_config.raw_data_path, index= False, header=True)

#             logging.info("Train Test Split Initiated")
#             train_set, test_set = train_test_split(df, test_size= 0.2, random_state=42)

#             train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
#             test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

#             logging.info("Ingestion of the data is completed")

#             return(
#                 self.ingestion_config.train_data_path,
#                 self.ingestion_config.test_data_path
#             )
#         except Exception as e:
#             raise CustomException(e, sys)
    
# if __name__=='__main__':
#     obj = DataIngestion()
#     obj.initiate_data_ingestion()


            