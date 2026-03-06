# Ultra Verba Lux Mentis Publication Registry

![Mint DOI](https://github.com/ultra-verba-lux-mentis/uvlm-publications/actions/workflows/mint_doi.yml/badge.svg)

Canonical source for UVLM scholarly publications and DOI minting.

## Repository Structure

- `papers/`: publication packages (`paper.pdf`, `metadata.yaml`, local docs).
- `schemas/`: JSON schema validation rules.
- `scripts/`: metadata validation, hash generation, Crossref XML/deposit automation.
- `registry/dois.json`: slug-based DOI state registry.
- `registry/publications.json`: global publication index keyed by DOI suffix.
- `registry/deposits/`: deposit audit logs.
- `.github/workflows/`: CI workflows.
- `DOI_NAMESPACE.md`: canonical DOI naming policy.

## DOI Namespace Policy

UVLM DOI suffixes must follow:

`uvlm.<type>.<slug>.<version>`

Examples:

- `uvlm.paper.echo-atlas-primer.v1`
- `uvlm.dataset.coherence-lattice.v1`
- `uvlm.software.sophia-ledger.v1`

Final DOI format in Crossref is:

`10.<prefix>/uvlm.<type>.<slug>.<version>`

## Metadata Format

Each `papers/<slug>/metadata.yaml` includes:

- `title`
- `type` (`paper`, `dataset`, `software`, `book`, `working-paper`)
- `authors` with required ORCID (`0000-0000-0000-0000`)
- `publisher` (explicit, e.g. `Ultra Verba Lux Mentis`)
- `series` (e.g. `UVLM Working Papers`)
- `publication_date` in ISO format `YYYY-MM-DD`
- `doi_suffix`
- `url`
- `content_hash` (SHA-256 of `paper.pdf`)
- optional `relations` entries with DOI links

Schema is enforced by `schemas/publication_schema.json`.

## DOI Generation Workflow

1. `scripts/update_content_hash.py` computes deterministic `content_hash`.
2. `scripts/validate_metadata.py` validates schema + verifies hash.
3. `scripts/generate_crossref_xml.py` creates `crossref_deposit.xml` with relation support.
4. `scripts/deposit_crossref.py --dry-run` validates payload without minting.
5. `scripts/deposit_crossref.py` deposits and updates:
   - `registry/dois.json` (`pending`, `registered`, `failed`, `updated`)
   - `registry/publications.json` global publication index
   - `registry/deposits/<date>_<slug>.json` audit logs

Required environment variables:

- `CROSSREF_USERNAME`
- `CROSSREF_PASSWORD`
- `DOI_PREFIX`

## CI Safety Policy

The workflow at `.github/workflows/mint_doi.yml` runs on `papers/**` changes:

- **Pull requests**: validates metadata, generates XML, and runs **dry-run only** deposit.
- **Pushes to `main`**: performs minting deposit, updates registries, commits audit artifacts.

This prevents accidental DOI minting before merge.
