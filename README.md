# Anonymous supporting materials

This package accompanies the anonymous submission *From Scores to Claims: Auditing Scientific Inference in AIOps Benchmarks*.

## What this package supports

The package is intentionally limited to the records needed to inspect the paper's two empirical results and their quality checks:

1. **RQ1 corpus and coding.** The corpus frame comprised 100 screened candidates: 58 from the recovered survey frame and 42 from the update search. Screening yielded the final 93-paper corpus, and the candidate-screening record shows each decision. The final coding table records the scored endpoint, primary interpretation, source quotation and locator, reported validation, and final extension class for each paper.
2. **RQ1 reliability and sensitivity.** The paired pre-adjudication records expose the independently double-coded 19-paper subset. The sensitivity tables report the corpus-composition checks used in the paper.
3. **RQ2 claim audit.** The 12-case table connects each endpoint and source-grounded claim to a compatible alternative and a discriminating observation, including assumptions and divergent expected patterns.
4. **Independent assessment.** The assessment rubric, two frozen evaluator response files, and case-level reconciliation record document how the proposed contrasts were assessed before reconciliation.

The package contains source quotations, bibliographic identifiers, URLs, and page/section/table locators. It does not redistribute the reviewed papers.

## Suggested reading order

### 1. Inspect corpus construction and final coding

- `data/corpus_candidate_screening_100.csv`
- `data/human_primary_93.csv`

The unit of analysis is one primary evaluation-backed interpretation per paper. `DIRECT` means that the interpretation remains at the scored endpoint. The six extension classes identify the broader scientific property invoked beyond that endpoint:

- `UTILITY`
- `REPRESENTATION`
- `ROBUSTNESS_GENERALIZATION`
- `CAUSAL_PROCESS`
- `REASONING_EVIDENCE`
- `ACTION_DEPLOYMENT`

An action-oriented task is not automatically `ACTION_DEPLOYMENT`. A claim that only restates scored plan validity or recovery remains `DIRECT`; the extension label applies when the interpretation invokes an operational consequence, capability, safety property, adoption, or deployment beyond the scored endpoint.

### 2. Inspect coding reliability and sensitivity

- `data/double_code_subset19_pre_adjudication.csv`
- `data/double_code_disagreements_pre_adjudication.csv`
- `data/corpus_composition_sensitivity.csv`
- `data/leave_one_method_family_out.csv`
- `data/pilot_overlap_paper_ids.csv`

The paired file contains the complete pre-adjudication labels for the 19 independently double-coded packets. The disagreement file adds the coders' ambiguity notes for packets with at least one disagreement. The sensitivity files support the full-corpus, peer-reviewed-only, no-pilot-overlap, and leave-one-method-family-out results.

### 3. Inspect the 12 claim-level contrasts

- `data/deep_audit_final_12.csv`

For each case, the file records the measured endpoint, source quotation and locator, reported validation, intended interpretation, compatible alternative, proposed discriminating observation, assumptions, expected result under each account, and final disposition. The alternatives are analyst-generated and are not attributed to the source authors.

### 4. Inspect the independent assessment

- `assessment/ASSESSMENT_RUBRIC.md`
- `assessment/validator1_raw.csv`
- `assessment/validator2_raw.csv`
- `assessment/rq2_validation_adjudicated.csv`

The two response files are the frozen pre-reconciliation responses from two additional human evaluators who were not involved in mapping generation or adjudication and did not have access to the analysts' forms. Their responses assess the proposed contrasts; they do not report outcomes of the proposed follow-up evaluations. The adjudicated file records the subsequent case-level reconciliation and wording changes. In `deep_audit_final_12.csv`, `validation_packet_version` and `pre_validation_source_sha256` are retained provenance fields. The compact package does not repeat 12 separate packet files because the source quotation, locator, reported validation, contrast, assumptions, and predictions are already present in that table.

## Verification

From the extracted package root, run:

```text
python scripts/verify_package.py
```

The script uses only the Python standard library. It verifies the manifest, file set, headline corpus and family counts, double-coding total, sensitivity rows, 12-case coverage, evaluator-response hashes, assessment totals, and final dispositions.

## Scope and anonymity

This package contains no manuscript source, repository history, local paths, submission-author names, submission-author affiliations, submission-author email addresses, author-identifying contribution notes, or superseded evaluator packets. Names that occur in paper titles, quotations, URLs, or bibliographic records refer to authors of the reviewed literature.
