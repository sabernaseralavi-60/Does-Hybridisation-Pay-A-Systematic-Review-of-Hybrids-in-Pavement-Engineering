.PHONY: render pdf docx html bib figures clean setup

render: bib figures
	quarto render manuscript.qmd

pdf: bib figures
	quarto render manuscript.qmd --to elsevier-pdf

docx: bib figures
	quarto render manuscript.qmd --to docx

html: bib figures
	quarto render manuscript.qmd --to html

bib:
	python3 analysis/make_bib.py

figures:
	cd figures && python3 ../analysis/fig_coverage_gap.py

setup:
	quarto add quarto-journals/elsevier --no-prompt
	pip install jupyter matplotlib numpy --break-system-packages

clean:
	rm -rf output .quarto manuscript.tex manuscript_files
