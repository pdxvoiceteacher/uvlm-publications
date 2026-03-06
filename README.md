# Ultra Verba Lux Mentis Publication Registry

This repository serves as the canonical metadata source for UVLM scholarly publications and DOI minting.

## Repository Structure

- `papers/`: publication packages (`paper.pdf`, `metadata.yaml`, and local publication docs).
- `schemas/`: JSON schemas used to validate publication metadata.
- `scripts/`: automation tools for validation, Crossref XML generation, and DOI deposit.
- `registry/`: DOI tracking registry (`dois.json`).
- `.github/workflows/`: CI pipelines for metadata validation and DOI minting.

## How to Add a Paper

1. Create a new directory under `papers/<paper-slug>/`.
2. Add:
   - `paper.pdf`
   - `metadata.yaml`
   - `README.md`
3. Choose a unique `doi_suffix` and include all required metadata fields.
4. Commit and push.

## Metadata Format

Metadata lives in `metadata.yaml` and is validated by `schemas/publication_schema.json`.

Required keys:

- `title`
- `authors`
- `publication_date`
- `doi_suffix`
- `url`

Example publication is available at `papers/echo-atlas-primer/metadata.yaml`.

## DOI Generation Workflow

1. Validate metadata via `scripts/validate_metadata.py`.
2. Generate Crossref XML via `scripts/generate_crossref_xml.py`.
3. Deposit XML and update `registry/dois.json` via `scripts/deposit_crossref.py`.

Required environment variables:

- `CROSSREF_USERNAME`
- `CROSSREF_PASSWORD`
- `DOI_PREFIX`

## CI Pipeline

The workflow at `.github/workflows/mint_doi.yml` triggers on changes under `papers/**`.

It performs:

1. dependency install
2. metadata validation
3. Crossref XML generation
4. DOI deposit and registry update

## Versioning Strategy

Use semantic publication IDs with version information in metadata:

- `echo-atlas-primer` + `version: v1`
- future updates can add `version: v2` and `previous_doi`

This supports Crossref version linking over time.
