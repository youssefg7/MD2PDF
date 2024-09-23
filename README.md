# Sales Document Generator
This is an experimental project to streamline document generation.

- Install dependencies

```shell
pip install -r requirements.txt
```

## Markdown MD to PDF Script Tool

- Install `wkhtmltopdf` on your computer from [here](https://wkhtmltopdf.org/downloads.html).

- Run `scripts/md2pdf.py` providing input MD file path.

```shell
python scripts/md2pdf.py "input-samples/tut-README.md"
```

## AI Generated plots from structured data (CSV, XLSX)
- Run `scripts/xlsx2png.py` providing input xlsx or csv file path, and input prompt.

```shell
python scripts/xlsx2png.py "input-samples/Sale Data.xlsx" "Any suitable plot of the data"
```

- You can save the intermediatry results by setting `OUTPUT_DEBUG = True` in `config.py`.
