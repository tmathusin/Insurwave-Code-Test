from __future__ import annotations
import json
import sys
from typing import Optional
import click
from .pipeline import extract_dates
from .logging_conf import setup_logging

@click.command()
@click.option("--text", type=str, help="Input text to parse for dates.")
@click.option("--file", "file_path", type=click.Path(exists=True, dir_okay=False), help="Path to a UTF-8 text file to parse.")
def main(text: Optional[str], file_path: Optional[str]) -> None:
    """CLI wrapper that prints JSON to stdout."""
    setup_logging()
    if not text and not file_path:
        click.echo("Provide --text or --file", err=True)
        sys.exit(2)
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    assert text is not None
    result = extract_dates(text)
    # Structured JSON for API layer
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
