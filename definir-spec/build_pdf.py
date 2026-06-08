#!/usr/bin/env python
"""Construye el PDF de una spec: antepone la intro para el usuario final y luego
el spec técnico. La intro NO vive en el .md del spec; se pasa como archivo aparte.

Uso:
    python build_pdf.py <intro.md> <spec.md> <salida.pdf>

Requiere: markdown + xhtml2pdf (presentes, p. ej., en el venv del proyecto).
Si no están disponibles, ver fallbacks en SKILL.md (pandoc / npx md-to-pdf).
"""
import sys
from pathlib import Path

import markdown  # type: ignore
from xhtml2pdf import pisa  # type: ignore

CSS = """
@page { size: A4; margin: 2.2cm 2cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; color: #1a1a1a; line-height: 1.4; }
h1 { font-size: 17pt; border-bottom: 2px solid #444; padding-bottom: 4px; }
h2 { font-size: 13pt; margin-top: 16px; }
h3 { font-size: 11.5pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; }
th, td { border: 1px solid #bbb; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 8px; font-family: Courier, monospace; font-size: 9pt; white-space: pre-wrap; }
code { font-family: Courier, monospace; }
.pagebreak { page-break-after: always; }
"""

MD_EXTS = ["tables", "fenced_code", "sane_lists", "toc"]


def render(intro_md: str, spec_md: str, out_pdf: str) -> None:
    intro_html = markdown.markdown(Path(intro_md).read_text(encoding="utf-8"), extensions=MD_EXTS)
    spec_html = markdown.markdown(Path(spec_md).read_text(encoding="utf-8"), extensions=MD_EXTS)
    html = (
        f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
        f"{intro_html}"
        f"<div class='pagebreak'></div>"
        f"{spec_html}"
        f"</body></html>"
    )
    with open(out_pdf, "wb") as fh:
        result = pisa.CreatePDF(html, dest=fh, encoding="utf-8")
    if result.err:
        raise SystemExit(f"xhtml2pdf reportó {result.err} error(es) al generar {out_pdf}")
    print(f"PDF generado: {out_pdf}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    render(sys.argv[1], sys.argv[2], sys.argv[3])
