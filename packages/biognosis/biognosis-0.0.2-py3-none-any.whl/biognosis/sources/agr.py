"""Alliance of Genome Resources."""

from collections.abc import Iterable

import pandas as pd
from bioregistry import NormalizedNamedReference, NormalizedReference
from curies import Triple
from curies import vocabulary as v

from biognosis.sources.constants import get_mod_to_uniprot, get_module

KEY = "agr"
MODULE = get_module(KEY)
URL = "https://fms.alliancegenome.org/download/DISEASE-ALLIANCE_COMBINED.tsv.gz"
IMPLICATED = NormalizedNamedReference(
    prefix="obo", identifier="agr#implicated", name="is implicated in"
)
MAPPING = {
    "is_model_of": NormalizedNamedReference.from_reference(v.is_model_of),  # 12,340
    "is_marker_for": NormalizedNamedReference.from_reference(v.is_marker_for),  # 17,077
    "biomarker_via_orthology": NormalizedNamedReference.from_reference(v.is_marker_for),  # 105,704
    # UNMAPPED
    "implicated_via_orthology": IMPLICATED,  # 190,479
    "is_implicated_in": IMPLICATED,  # 55,195
    # NEGATIVE
    "is_not_implicated_in": None,  # 1,428
}


def get_agr_triples() -> Iterable[Triple]:
    """Get triples from the Alliance of Genome Resources."""
    df = MODULE.ensure_csv(
        url=URL,
        read_csv_kwargs={
            "comment": "#",
        },
    )
    mod_to_uniprot = get_mod_to_uniprot()
    # TODO need to convert to UniProt or Entrez
    for subject_curie, association, disease_curie in df[
        ["DBObjectID", "AssociationType", "DOID"]
    ].values:
        subject = NormalizedReference.from_curie(subject_curie)
        uniprot_id = mod_to_uniprot.get(subject)
        if uniprot_id is None:
            continue
        if pd.isna(disease_curie):
            continue
        pred = MAPPING[association]
        if not pred:
            continue
        disease = NormalizedReference.from_curie(disease_curie)
        yield Triple(NormalizedReference(prefix="uniprot", identifier=uniprot_id), pred, disease)


def _main() -> None:
    from curies.triples import write_triples

    write_triples(get_agr_triples(), MODULE.join(name="triples.tsv"))


if __name__ == "__main__":
    _main()
