# UVLM DOI Namespace Policy

This file defines the canonical DOI namespace for UVLM publications.

## DOI Shape

`10.<prefix>/uvlm.<type>.<slug>.<version>`

## Allowed Type Segments

- `uvlm.paper`
- `uvlm.dataset`
- `uvlm.software`
- `uvlm.book`

## Examples

- `10.12345/uvlm.paper.echo-atlas-primer.v1`
- `10.12345/uvlm.dataset.coherence-lattice.v1`
- `10.12345/uvlm.software.sophia-ledger.v2`
- `10.12345/uvlm.book.solomons-folly.v1`

## Notes

- `<slug>` must be lowercase alphanumeric plus hyphen.
- `<version>` must follow `vN` format (for example `v1`, `v2`).
- The repository schema enforces this format for DOI suffixes.
