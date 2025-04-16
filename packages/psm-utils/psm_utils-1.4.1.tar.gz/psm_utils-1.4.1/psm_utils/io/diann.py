"""
Reader for PSM files from DIA-NN

Reads the '.tsv' file as defined on the
`DIA-NN documentation page <https://github.com/vdemichev/DiaNN/tree/1.8.1?tab=readme-ov-file#main-output-reference>`_.

Notes
-----

- DIA-NN calculates q-values at both the run and library level. The run-level q-value is used as
  the PSM q-value.
- DIA-NN currently does not return precursor m/z values.
- DIA-NN currently does not support C-terminal modifications in its searches.

"""

from __future__ import annotations

import csv
import re
from typing import Iterable, Optional

from psm_utils.io._base_classes import ReaderBase
from psm_utils.io._utils import set_csv_field_size_limit
from psm_utils.psm import PSM
from psm_utils.psm_list import PSMList

set_csv_field_size_limit()

RESCORING_FEATURES = [
    "RT",
    "Predicted.RT",
    "iRT",
    "Predicted.iRT",
    "Ms1.Profile.Corr",
    "Ms1.Area",
    "IM",
    "iIM",
    "Predicted.IM",
    "Predicted.iIM",
]


class DIANNTSVReader(ReaderBase):
    def __init__(self, filename, *args, **kwargs) -> None:
        """
        Reader for DIA-NN '.tsv' file.

        Parameters
        ----------
        filename : str or Path
            Path to PSM file.

        """
        super().__init__(filename, *args, **kwargs)
        self.filename = filename

    def __iter__(self) -> Iterable[PSM]:
        """Iterate over file and return PSMs one-by-one."""
        with open(self.filename) as msms_in:
            reader = csv.DictReader(msms_in, delimiter="\t")
            for row in reader:
                yield self._get_peptide_spectrum_match(row)

    def _get_peptide_spectrum_match(self, psm_dict) -> PSM:
        """Parse a single PSM from a DIA-NN PSM file."""
        rescoring_features = {}
        for ft in RESCORING_FEATURES:
            try:
                rescoring_features[ft] = psm_dict[ft]
            except KeyError:
                continue

        return PSM(
            peptidoform=self._parse_peptidoform(
                psm_dict["Modified.Sequence"], psm_dict["Precursor.Charge"]
            ),
            spectrum_id=psm_dict["MS2.Scan"],
            run=psm_dict["Run"],
            is_decoy=False,
            qvalue=psm_dict["Q.Value"],
            pep=float(psm_dict["PEP"]),
            score=float(psm_dict["CScore"]),
            precursor_mz=None,  # Not returned by DIA-NN :(
            retention_time=float(psm_dict["RT"]),
            ion_mobility=float(psm_dict["IM"]),
            protein_list=psm_dict["Protein.Ids"].split(";"),
            source="diann",
            rank=None,
            provenance_data=({"diann_filename": str(self.filename)}),
            rescoring_features=rescoring_features,
            metadata={},
        )

    @staticmethod
    def _parse_peptidoform(peptide: str, charge: Optional[str]) -> str:
        # Add charge
        if charge:
            peptide += f"/{int(float(charge))}"

        # Replace parentheses with square brackets and capitalize UniMod prefix
        pattern = r"\(UniMod:(\d+)\)"
        replacement = r"[UNIMOD:\1]"
        peptide = re.sub(pattern, replacement, peptide)

        # Add hyphen for N-terminal modifications
        # If [UNIMOD:n] occurs before the first amino acid, a hyphen is added before the first
        # amino acid
        if peptide[0] == "[":
            # Hyphen after the closing bracket
            peptide = peptide.replace("]", "]-", 1)

        # C-terminal modifications are currently not supported in DIA-NN

        return peptide

    @classmethod
    def from_dataframe(cls, dataframe) -> PSMList:
        """Create a PSMList from a DIA-NN Pandas DataFrame."""
        return PSMList(
            ptm_list=[
                cls._get_peptide_spectrum_match(cls(""), entry)
                for entry in dataframe.to_dict(orient="records")
            ]
        )
