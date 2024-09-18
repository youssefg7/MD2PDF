# MD2PDF
This is an experimental project to streamline document generation, converting from markdown files to formatted PDF files.

- Install dependencies

```shell
pip install -r requirements.txt
```

- Install `wkhtmltopdf` on your computer from [here](https://wkhtmltopdf.org/downloads.html).

- Run md2pdf.py providing input MD file path.

```shell
python md2pdf.py "input-samples/tut-README.md"
```

- You can save the intermediatry `HTML` by setting `OUTPUT_DEBUG = True` in `config.py`.