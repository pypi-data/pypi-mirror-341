from unittest.mock import patch
import sys
from duckdbmcp.config import Config
from duckdbmcp.server import DuckDBDatabase

def test_smart_load_multiple_csv_files():
    test_args = [
        "--db-in-memory",
    ]
    with patch.object(sys, "argv", ["prog"] + test_args):
        config = Config.from_arguments()
        assert config.db_in_memory is True

        db = DuckDBDatabase(config)
        handler  = db.handler
        handler.smart_load_multiple_csv_files(
            [
                "https://c72gdackzgkn7zoa.public.blob.vercel-storage.com/personal-investments-sLlshHSlqYTkCx57n867K4f5KcSoS2.csv",
                "https://raw.githubusercontent.com/scikit-learn/examples-data/refs/heads/master/financial-data/GE.csv",
                "https://raw.githubusercontent.com/scikit-learn/examples-data/refs/heads/master/financial-data/AMZN.csv",
                "https://storage.googleapis.com/kagglesdsdata/datasets/435/896/sales_data_sample.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250415%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250415T074309Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=18e9bdc95aec525b3acb5451a0928fb1e11953f70965d142ed659f9523de14dad86094db2a4b98abb6b28732093b7aa1f4afe6b30b4602c02467a857d6180eabf30e2c5010847d291092e9f87f28c6681d5b3a331cc57ce8679357e58d9612ec4f289941ec2742b26c2f1e08459118934fd015a4362b1ea3c7946d4e07d77a3810e64be6a8e5580f4655d7fc1e028523bf243170d3c35b96c69619ace3e755c31f388d630623c71a2ed9f92331968d127dfdb239d8978f434141b69cd85938e99e7e5e9199cf9e514ec0c1bf0e1e1b26508b5b506075c4dc784bbb1904911ca8db37f7c4b5faa4bd6c40e3f5c0327b26d3a022160dc7eb75fdebdbba332d7dd4"
            ],
        )

def main():
    test_smart_load_multiple_csv_files()

if __name__ == "__main__":
    main()

