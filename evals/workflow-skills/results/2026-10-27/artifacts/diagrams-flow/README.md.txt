# Example project

Local checks: `python3 -m unittest discover -s tests -v`.

Entry point is app/api.py::submit; the supplied store is an in-memory list.
compose.yaml is a proposed local deployment configuration. No deployment state is recorded.

See [submit flow and configured deployment](docs/architecture/submit-and-deployment.md)
for Mermaid diagrams, source references, and verification limits.
