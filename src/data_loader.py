from pathlib import PosixPath

import pandas as pd

from settings import DATA_DIR


DOSAGE_TYPES = [
    "spray, metered",
    "tablet",
    "tablet, delayed release",
    "capsule",
    "capsule, extended release",
    "tablet, chewable",
    "tablet, extended release",
    "suspension",
    "powder",
    "gel",
    "troche/lozenge",
    "cream",
    "spray",
    "tablet, orally disintegrating",
    "film",
    "aerosol, foam",
    "solution",
    "aerosol, metered",
    "lotion",
    "tablet, effervescent",
    "film, extended release",
    "enema",
    "injectable",
    "ointment",
    "gel, metered",
    "patch",
    "ring",
    "tablet, for suspension",
    "capsule, delayed release",
    "for suspension, extended release",
    "tablet, orally disintegrating, delayed release",
    "for suspension",
    "suspension, extended release",
]


class DrugFilter:
    """
    Filters the dataframe by substance and dosage type.
    """

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self.drug_list = list(self._df["DrugName"].unique())
        self.substance_list = list(
            self._df.loc[
                self._df["ActiveIngredient"].str.split(";").apply(lambda x: len(x)) == 1
            ]["ActiveIngredient"].unique()
        )
        self.dosage_types = DOSAGE_TYPES

    @classmethod
    def from_df(cls, path: PosixPath):
        df = pd.read_csv(path)
        df["RecommendedStudies"] = df["RecommendedStudies"].apply(lambda x: eval(x))
        return cls(df)

    @staticmethod
    def filter_by_dosage(df: pd.DataFrame, dosage_type: str) -> pd.DataFrame:
        return df.loc[df["Dosage"] == dosage_type.upper()]

    def filter_by_substance(self, name: str) -> pd.DataFrame:
        filtered = self._df.loc[
            (self._df["ActiveIngredient"].str.contains(name))
            & (~self._df["DrugName"].str.contains(name))
            & (self._df["ActiveIngredient"].str.split(";").apply(lambda x: len(x)) == 1)
        ]
        return filtered

    @staticmethod
    def available_dosages(df: pd.DataFrame):
        return list(df["Dosage"].unique())

    def filter_drugs(self, substance: str, dosage: str = None) -> pd.DataFrame:
        filtered = self.filter_by_substance(substance)
        if dosage is not None and not filtered.empty:
            filtered = self.filter_by_dosage(filtered, dosage)
        return filtered
