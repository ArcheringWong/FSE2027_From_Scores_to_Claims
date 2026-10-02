from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def agreement_statistics(
    records: list[dict[str, str]],
    coder1_field: str,
    coder2_field: str,
    categories: list[str],
) -> tuple[float, float, float]:
    n = len(records)
    observed = sum(
        row[coder1_field] == row[coder2_field] for row in records
    ) / n
    coder1_counts = Counter(row[coder1_field] for row in records)
    coder2_counts = Counter(row[coder2_field] for row in records)
    cohen_expected = sum(
        (coder1_counts[category] / n) * (coder2_counts[category] / n)
        for category in categories
    )
    cohen_kappa = (observed - cohen_expected) / (1 - cohen_expected)
    pooled = {
        category: (coder1_counts[category] + coder2_counts[category]) / (2 * n)
        for category in categories
    }
    ac1_expected = sum(
        probability * (1 - probability) for probability in pooled.values()
    ) / (len(categories) - 1)
    gwet_ac1 = (observed - ac1_expected) / (1 - ac1_expected)
    return observed, cohen_kappa, gwet_ac1


manifest_path = ROOT / "MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
expected_files = {entry["path"] for entry in manifest["files"]} | {"MANIFEST.json"}
actual_files = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file()
}
assert actual_files == expected_files, {
    "missing": sorted(expected_files - actual_files),
    "unexpected": sorted(actual_files - expected_files),
}
for entry in manifest["files"]:
    path = ROOT / entry["path"]
    assert path.stat().st_size == entry["bytes"], entry["path"]
    assert sha256(path) == entry["sha256"], entry["path"]

screening = rows("data/corpus_candidate_screening_100.csv")
corpus = rows("data/human_primary_93.csv")
assert len(screening) == 100
assert len(corpus) == 93
assert sum(row["inclusion_status"].strip().upper() == "INCLUDED" for row in screening) == 93
assert Counter(row["publication_status"] for row in corpus) == Counter(
    {"peer_reviewed": 78, "preprint": 15}
)
assert Counter(row["final_extension_class"] for row in corpus) == Counter(
    {
        "DIRECT": 47,
        "UTILITY": 7,
        "REPRESENTATION": 3,
        "ROBUSTNESS_GENERALIZATION": 12,
        "CAUSAL_PROCESS": 5,
        "REASONING_EVIDENCE": 8,
        "ACTION_DEPLOYMENT": 11,
    }
)

paired = rows("data/double_code_subset19_pre_adjudication.csv")
disagreements = rows("data/double_code_disagreements_pre_adjudication.csv")
assert len(paired) == 19
assert sum(row["extension_agree"].strip().upper() in {"TRUE", "YES", "1"} for row in paired) == 14
assert len(disagreements) == 10
extension_statistics = agreement_statistics(
    paired,
    "coder1_extension",
    "coder2_extension",
    [
        "DIRECT",
        "UTILITY",
        "REPRESENTATION",
        "ROBUSTNESS_GENERALIZATION",
        "CAUSAL_PROCESS",
        "REASONING_EVIDENCE",
        "ACTION_DEPLOYMENT",
    ],
)
relation_statistics = agreement_statistics(
    paired,
    "coder1_relation",
    "coder2_relation",
    [
        "DIRECTLY_TARGETS_CONSTRUCT",
        "PARTIALLY_TARGETS_CONSTRUCT",
        "INDIRECT_PROXY",
        "UNCLEAR",
    ],
)
for actual, expected in zip(
    extension_statistics,
    (0.736842, 0.592275, 0.706261),
):
    assert math.isclose(actual, expected, abs_tol=0.0000005), (actual, expected)
for actual, expected in zip(
    relation_statistics,
    (0.473684, 0.116279, 0.361345),
):
    assert math.isclose(actual, expected, abs_tol=0.0000005), (actual, expected)

composition = rows("data/corpus_composition_sensitivity.csv")
assert {
    row["subset"]: (int(row["N"]), int(row["DIRECT"]), int(row["NON_DIRECT"]))
    for row in composition
} == {
    "FULL_CORPUS": (93, 47, 46),
    "PEER_REVIEWED_ONLY": (78, 42, 36),
    "NO_PILOT_OVERLAP": (56, 34, 22),
}
leave_one_out = rows("data/leave_one_method_family_out.csv")
assert len(leave_one_out) == 9
assert all(row["all_six_non_direct_classes_present"].strip().upper() == "YES" for row in leave_one_out)
pilot_overlap = rows("data/pilot_overlap_paper_ids.csv")
assert len(pilot_overlap) == 93
assert sum(row["pilot_overlap"].strip().upper() == "NO" for row in pilot_overlap) == 56

cases = rows("data/deep_audit_final_12.csv")
assert len(cases) == 12
assert Counter(row["extension_family"] for row in cases) == Counter(
    {
        "UTILITY": 2,
        "REPRESENTATION": 2,
        "ROBUSTNESS_GENERALIZATION": 2,
        "CAUSAL_PROCESS": 2,
        "REASONING_EVIDENCE": 2,
        "ACTION_DEPLOYMENT": 2,
    }
)
assert Counter(row["validation_final_disposition"] for row in cases) == Counter(
    {
        "RETAIN AS WRITTEN": 6,
        "RETAIN WITH MINOR CLARIFICATION": 4,
        "REVISE CONTRAST": 2,
    }
)

validator_hashes = {
    "assessment/validator1_raw.csv": "4fe566b937bbe3e002cdf571bda73fa7f824fe5b4ca1fd98179a90df929b846a",
    "assessment/validator2_raw.csv": "a7da154e9361677333584561183295a763bfda6da8083af61811c14555a43997",
}
for relative, expected in validator_hashes.items():
    assert sha256(ROOT / relative) == expected, relative
    response_rows = rows(relative)
    assert len(response_rows) == 12
    assert all(row["q2_alternative_compatibility"].strip().upper() == "YES" for row in response_rows)
    assert all(row["q3_predictive_discrimination"].strip().upper() == "YES" for row in response_rows)

adjudicated = rows("assessment/rq2_validation_adjudicated.csv")
assert len(adjudicated) == 12
assert {row["case_id"] for row in adjudicated} == {row["case_id"] for row in cases}

print("Anonymous supporting package verification passed.")
print("Corpus: 100 screened; 93 included = 47 DIRECT + 46 extended.")
print("Families: 7 / 3 / 12 / 5 / 8 / 11.")
print(
    "Reliability: Extension agreement 14/19, kappa 0.592275, AC1 0.706261; "
    "Evidence Relation agreement 9/19, kappa 0.116279, AC1 0.361345."
)
print("Sensitivity: 3 corpus slices and 9 leave-one-method-family-out rows verified.")
print("RQ2: 12 cases; 24/24 compatibility; 24/24 discrimination; dispositions 6 / 4 / 2 / 0.")
