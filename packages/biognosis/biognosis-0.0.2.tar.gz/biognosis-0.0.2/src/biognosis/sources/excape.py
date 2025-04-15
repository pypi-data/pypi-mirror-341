"""Source for ExcapeDB."""

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import pystow
from bioregistry import NormalizedNamableReference, NormalizedReference
from curies import Triple, vocabulary
from tqdm import tqdm

from biognosis.sources.constants import get_module

KEY = "excape"
EXCAPE_URL = "https://zenodo.org/record/2543724/files/pubchem.chembl.dataset4publication_inchi_smiles_v2.tsv.xz"
ID_MAPPINGS = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz"
REGULATOR_OF = NormalizedNamableReference.from_reference(vocabulary.regulator_of)


def ensure_excape(*, force: bool = False) -> Path:
    """Download ExcapeDB."""
    module = get_module(KEY)
    path = module.ensure(url=EXCAPE_URL, force=force)
    return path


KWARGS = {
    "sep": "\t",
    "compression": "xz",
    "usecols": ["DB", "Original_Entry_ID", "Entrez_ID", "Activity_Flag", "Tax_ID"],
    "dtype": str,
}


def get_entrez_to_uniprot() -> dict[str, str]:
    """Get a mapping of NCBI Gene (Entrez) gene identifiers to UniProt."""
    path = pystow.join("bio", "uniprot", name="entrez_to_uniprot.tsv.gz")
    path_sample = pystow.join("bio", "uniprot", name="entrez_to_uniprot.example.tsv")
    if path.exists():
        df = pd.read_csv(path, sep="\t", dtype=str)
        return dict(df.values)

    df = pystow.ensure_csv(
        "bio",
        "uniprot",
        url=ID_MAPPINGS,
        read_csv_kwargs={
            "usecols": [0, 2],
            "header": None,
        },
    )
    df = df[[2, 0]]
    df.columns = ["ncbigene", "uniprot"]
    df.to_csv(path, sep="\t", index=False)
    df.head().to_csv(path_sample, sep="\t", index=False)
    return dict(df.values)


def get_excape_df(*, force: bool = False) -> pd.DataFrame:
    """Get the ExCAPe database as a dataframe (unprocessed)."""
    path = ensure_excape(force=force)
    return pd.read_csv(path, **KWARGS)


def get_excape_triples(*, force: bool = False) -> Iterable[Triple]:
    """Get triples from ExcapeDB with chemicals as subjects and proteins as objects."""
    entrez_to_uniprot = get_entrez_to_uniprot()

    def _uniprot_curie_from_entrez(s: str | None) -> NormalizedReference | None:
        if pd.isna(s) or s is None:
            return None
        uniprot_id: str | None = entrez_to_uniprot.get(s)
        if not uniprot_id:
            return None
        return NormalizedReference(prefix="uniprot", identifier=uniprot_id)

    df = get_excape_df(force=force)

    # keep only active relationships
    df = df[df["Activity_Flag"] == "A"]

    df["subject"] = [_get_object_curie(db, i) for i, db in df[["Original_Entry_ID", "DB"]].values]
    df["object"] = df["Entrez_ID"].map(_uniprot_curie_from_entrez)

    # throw away anything that can't be mapped to human uniprot
    df = df[df["subject"].notna() & df["object"].notna()]

    df = df[["subject", "object"]].drop_duplicates()
    for s, o in df.values:
        yield Triple(s, REGULATOR_OF, o)


PC_ = {"pubchem_screening", "pubchem"}


def _get_object_curie(prefix: str, identifier: str) -> NormalizedReference | None:
    if prefix == "chembl20":
        return NormalizedReference(prefix="chembl.compound", identifier=identifier)
    if prefix in PC_:
        return NormalizedReference(prefix="pubchem.compound", identifier=identifier)
    tqdm.write(f"unknown DB: {prefix}")
    return None


def _main() -> None:
    from curies.triples import write_triples

    write_triples(get_excape_triples(), get_module(KEY).join(name="triples.tsv"))


if __name__ == "__main__":
    _main()
