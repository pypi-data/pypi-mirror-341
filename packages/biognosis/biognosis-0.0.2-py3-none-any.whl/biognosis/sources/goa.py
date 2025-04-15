"""Source for Gene Ontology Annotations."""

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from bioregistry import NormalizedReference
from curies import Triple
from curies import vocabulary as v
from tqdm import tqdm

from biognosis.sources.constants import get_module

__all__ = [
    "get_go_annotations",
]

BASE_URL = "https://current.geneontology.org/annotations"
URLS = [
    f"{BASE_URL}/goa_human.gpad.gz",
    f"{BASE_URL}/reactome.gpad.gz",
    f"{BASE_URL}/ecocyc.gpad.gz",
    "https://ftp.ebi.ac.uk/pub/databases/intact/complex/current/various/go/complex_portal.v2.gpad",
]
RELATIONS = {
    "located_in": v.located_in,
    "is_active_in": v.is_active_in,
    "contributes_to": v.contributes_to,
    "acts_upstream_of_or_within_positive_effect": v.acts_upstream_of_or_within_positive_effect,
    "part_of": v.part_of,
    "acts_upstream_of_positive_effect": v.acts_upstream_of_positive_effect,
    "acts_upstream_of": v.acts_upstream_of,
    "colocalizes_with": v.colocalizes_with,
    "involved_in": v.involved_in,
    "acts_upstream_of_or_within_negative_effect": v.acts_upstream_of_or_within_negative_effect,
    "acts_upstream_of_or_within": v.acts_upstream_of_or_within,
    "acts_upstream_of_negative_effect": v.acts_upstream_of_negative_effect,
    "enables": v.enables,
}


def get_go_annotations(*, force: bool = False) -> Iterable[Triple]:
    """Get triples Gene Ontology terms as the objects."""
    module = get_module("go")
    for url in URLS:
        path = module.ensure(url=url, force=force)
        yield from _read_gpad(path)


def _read_gpad(path: Path) -> Iterable[Triple]:
    # see https://geneontology.org/docs/gene-product-association-data-gpad-format-2.0/
    df = pd.read_csv(
        path,
        sep="\t",
        comment="!",
        usecols=[0, 1, 2, 3],
        names=["object", "negation", "relation", "go"],
    )
    # TODO other filters, such as evidence code?
    df = df[~df["relation"].str.startswith("NOT")]
    df.drop_duplicates(inplace=True)
    for subject_curie, _b, relation_curie, go_curie in df.values:
        if subject_curie.startswith("UniProtKB") and "-" in subject_curie:
            subject_curie = subject_curie.replace("UniProtKB", "uniprot.isoform")

        if "PRO_" in subject_curie:
            continue  # TODO
        if "VAR_" in subject_curie:
            continue  # TODO

        try:
            subject = NormalizedReference.from_curie(subject_curie)
        except ValueError:
            tqdm.write(f"failed to parse subject: {subject_curie}")
            continue

        yield Triple(
            subject,
            NormalizedReference.from_curie(relation_curie),
            NormalizedReference.from_curie(go_curie),
        )


def _main() -> None:
    from curies.triples import write_triples

    write_triples(get_go_annotations(), get_module("go").join(name="triples.tsv"))


if __name__ == "__main__":
    _main()
