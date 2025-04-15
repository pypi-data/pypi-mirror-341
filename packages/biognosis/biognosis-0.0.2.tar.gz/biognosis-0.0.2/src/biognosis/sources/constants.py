"""Constants for sources."""

import csv
import gzip
import pickle
from typing import cast

import bioregistry
import pystow
from bioregistry import NormalizedReference
from tqdm import tqdm

__all__ = [
    "MODULE",
    "get_module",
]

MODULE = pystow.module("bio", "biognosis")
UNIPROT_MODULE = pystow.module("bio", "uniprot")
UNIPROT_MAPPING_URL = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping.dat.gz"
MODEL_ORGANISM_DATABASE_PREFIXES = {
    "hgnc",
    "sgd",
    "mgi",
    "flybase",
    "fb",
    "rgd",
    "zfin",
    "wormbase",
    "wb",
    "xenbase",
}


def get_module(key: str, *, version: str | None = None) -> pystow.Module:
    """Get the module."""
    rv = MODULE.module(key)
    if version is not None:
        rv = rv.module(version)
    return rv


def get_mod_to_uniprot(*, force: bool = False) -> dict[NormalizedReference, str]:
    """Get a mapping of NCBI Gene (Entrez) gene identifiers to UniProt."""
    cache_path = UNIPROT_MODULE.join(name="mod-cache.pkl")
    if cache_path.is_file():
        with cache_path.open("rb") as file:
            return cast(dict[NormalizedReference, str], pickle.load(file))  # noqa:S301

    rv: dict[NormalizedReference, str] = {}

    missing: set[str] = set()

    path = UNIPROT_MODULE.ensure(url=UNIPROT_MAPPING_URL, force=force)
    with gzip.open(path, "rt") as file:
        it = tqdm(file, desc="Processing UniProt Mappings", unit="mapping", unit_scale=True)
        for uniprot_id, prefix, identifier in csv.reader(it, delimiter="\t"):
            norm_prefix = bioregistry.normalize_prefix(prefix)
            if prefix is None:
                if prefix not in missing:
                    tqdm.write(f"did not normalize prefix: {prefix}")
                continue
            if norm_prefix not in MODEL_ORGANISM_DATABASE_PREFIXES:
                continue
            try:
                ref = NormalizedReference(prefix=norm_prefix, identifier=identifier)
            except ValueError:
                tqdm.write(f"could not normalize: {norm_prefix}:{identifier}")
                continue

            rv[ref] = uniprot_id

    with cache_path.open("wb") as file:
        pickle.dump(rv, file, protocol=pickle.HIGHEST_PROTOCOL)

    return rv
