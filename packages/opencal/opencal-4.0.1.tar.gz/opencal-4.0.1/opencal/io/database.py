import json
import logging
import os
from pathlib import Path
import sqlmodel

import opencal
import opencal.models

OPENCAL_DB_PATH: Path = Path(opencal.cfg["opencal"]["db_path"]).expanduser().absolute()    # Replace '~' with the user's home directory
SQLITE_DATABASE_URL = os.getenv("OPENCAL_DATABASE_URL", f"sqlite:///{OPENCAL_DB_PATH}")    # TODO: use the environment variable in production?

logging.info(f"Open {SQLITE_DATABASE_URL}")

# Create the database engine
engine = sqlmodel.create_engine(
    url=SQLITE_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}   # TODO ?
)


def create_db_and_tables() -> None:
    """
    Create the database and tables.

    Returns
    -------
    None
    """
    sqlmodel.SQLModel.metadata.create_all(engine)


def db_to_json(tables_to_dump: list[str]|None = None, json_file_path: Path|None = None) -> str:
    data: dict[str, dict[str, dict[str, int|str|bool]]] = {
        "acquisitionreview": {},
        "consolidationreview": {}
    }

    # Create a session
    with sqlmodel.Session(engine) as session:
        if (tables_to_dump is None) or ("acquisitionreview" in tables_to_dump):
            acquisition_reviews = session.exec(sqlmodel.select(opencal.models.AcquisitionReview))
            for acquisition_review in acquisition_reviews:
                acquisition_review_dict = json.loads(acquisition_review.model_dump_json())
                acquisition_review_uuid = acquisition_review_dict.pop("uuid")
                data["acquisitionreview"][acquisition_review_uuid] = acquisition_review_dict
        
        if (tables_to_dump is None) or ("consolidationreview" in tables_to_dump):
            consolidation_reviews = session.exec(sqlmodel.select(opencal.models.ConsolidationReview))
            for consolidation_review in consolidation_reviews:
                consolidation_review_dict = json.loads(consolidation_review.model_dump_json())
                consolidation_review_uuid = consolidation_review_dict.pop("uuid")
                data["consolidationreview"][consolidation_review_uuid] = consolidation_review_dict

        json_str = json.dumps(data, sort_keys=True, indent=4, default=str)

    if json_file_path is not None:
        # Write the list of dictionaries to the JSON file
        json_file_path.write_text(json_str)

    return json_str
