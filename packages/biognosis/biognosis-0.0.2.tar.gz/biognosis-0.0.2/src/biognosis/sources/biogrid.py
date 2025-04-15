"""Source for BioGRID."""

import contextlib
import csv
import zipfile
from collections.abc import Generator, Iterable
from pathlib import Path
from typing import IO, Literal, overload

import bioversions
from bioregistry import NormalizedReference
from curies import Triple
from tqdm import tqdm

from biognosis.sources.constants import get_module

__all__ = [
    "ensure_biogrid",
    "ensure_open_biogrid",
]

MODULE = get_module("biogrid")
EXT = "mitab"
FORMAT_URL = "https://downloads.thebiogrid.org/Download/BioGRID/Release-Archive/BIOGRID-{version}/BIOGRID-ALL-{version}.{extension}.zip"

#: molecularly interacts with
MIW = NormalizedReference(prefix="ro", identifier="0002436")

# TODO get these in RO?

"""
  151,772 psi-mi:"MI:0403"(colocalization)
  376,637 psi-mi:"MI:0407"(direct interaction)
   13,622 psi-mi:"MI:0914"(association)
1,327,679 psi-mi:"MI:0915"(physical association)
   19,486 psi-mi:"MI:2368"("phenotypic enhancement (sensu biogrid)")
   33,145 psi-mi:"MI:2369"("synthetic growth defect (sensu biogrid)")
   21,633 psi-mi:"MI:2370"("synthetic lethality (sensu biogrid)")
  195,182 psi-mi:"MI:2371"("positive genetic interaction (sensu biogrid)")
      379 psi-mi:"MI:2372"("synthetic haploinsufficiency (sensu biogrid)")
  568,282 psi-mi:"MI:2373"("negative genetic interaction (sensu biogrid)")
   21,831 psi-mi:"MI:2374"("phenotypic suppression (sensu biogrid)")
   12,038 psi-mi:"MI:2375"("synthetic rescue (sensu biogrid)")
    8,718 psi-mi:"MI:2376"("dosage rescue (sensu biogrid)")
    2,506 psi-mi:"MI:2377"("dosage lethality (sensu biogrid)")
    2,417 psi-mi:"MI:2378"("dosage growth defect (sensu biogrid)")
"""


# docstr-coverage:excused `overload`
@overload
def ensure_biogrid(
    *, force: bool = ..., version: str | None = ..., return_version: Literal[True] = True
) -> tuple[Path, str]: ...


# docstr-coverage:excused `overload`
@overload
def ensure_biogrid(
    *, force: bool = ..., version: str | None = ..., return_version: Literal[False] = False
) -> Path: ...


def ensure_biogrid(
    *, force: bool = False, version: str | None = None, return_version: bool = False
) -> Path | tuple[Path, str]:
    """Get BioGRID."""
    if version is None:
        version = bioversions.get_version("biogrid", strict=True)
    module = get_module("biogrid")
    url = FORMAT_URL.format(version=version, extension=EXT)
    path = module.ensure(url=url, version=version, force=force)
    if return_version:
        return path, version
    return path


@contextlib.contextmanager
def ensure_open_biogrid(
    *, force: bool = False, version: str | None = None
) -> Generator[IO[bytes], None, None]:
    """Download and open BioGRID."""
    path, version = ensure_biogrid(version=version, force=force, return_version=True)
    with zipfile.ZipFile(path) as zip_file:
        with zip_file.open(f"BIOGRID-ALL-{version}.{EXT}.txt") as file:
            yield file


P1 = "uniprot/swiss-prot:"
P1_LEN = len(P1)
P2 = "entrez gene/locuslink:"
P2_LEN = len(P2)

XXXX = set()


def _get_uniprot(y: str, x: str) -> NormalizedReference | None:
    for curie in x.split("|"):
        if curie.startswith(P1):
            return NormalizedReference(prefix="uniprot", identifier=curie[P1_LEN:])

    if y.startswith(P2):
        return NormalizedReference(prefix="ncbigene", identifier=y[P2_LEN:])

    if y not in XXXX:
        tqdm.write(f"could not deal with {y} / {x}")
        XXXX.add(y)
    return None


def _get_relation(x: str) -> NormalizedReference:
    # psi-mi:"MI:0407"(direct interaction)
    x = x.removeprefix('psi-mi:"')
    x = x.split('"')[0]
    if x == "MI:0407":
        return MIW
    return NormalizedReference.from_curie(x)


def get_biogrid_triples() -> Iterable[Triple]:
    """Get BioGRID triples."""
    with ensure_open_biogrid() as file:
        lines = (
            line.decode("utf-8")
            for line in tqdm(file, unit_scale=True, unit="interaction", desc="Preparing graph")
        )
        for record in csv.DictReader(lines, delimiter="\t"):
            left = _get_uniprot(record["#ID Interactor A"], record["Alt IDs Interactor A"])
            right = _get_uniprot(record["ID Interactor B"], record["Alt IDs Interactor B"])
            if left is None or right is None:
                continue
            relation = _get_relation(record["Interaction Types"])

            yield Triple(left, relation, right)


def _main() -> None:
    from curies.triples import write_triples

    write_triples(get_biogrid_triples(), get_module("biogrid").join(name="triples.tsv"))


if __name__ == "__main__":
    _main()
