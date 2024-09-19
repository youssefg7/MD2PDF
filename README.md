# MD2PDF
This is an experimental project to streamline document generation, converting from markdown files to formatted PDF files.

- Install dependencies

```shell
pip install -r requirements.txt
```

## Markdown MD to PDF tool

- Install `wkhtmltopdf` on your computer from [here](https://wkhtmltopdf.org/downloads.html).

- Run `md2pdf.py` providing input MD file path.

```shell
python md2pdf.py "input-samples/tut-README.md"
```

## AI Generated plots from structured data (CSV, XLSX)
- Run `xlsx2png.py` providing input xlsx or csv file path, and input prompt.

```shell
python xlsx2png.py "input-samples/Sale Data.xlsx" "Any suitable plot of the data"
```

- You can save the intermediatry results by setting `OUTPUT_DEBUG = True` in `config.py`.
