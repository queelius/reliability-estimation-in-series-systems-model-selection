all: manuscript.pdf cover-letter.pdf

manuscript.pdf: manuscript.tex refs.bib
	latexmk -pdf manuscript.tex

cover-letter.pdf: cover-letter.tex
	latexmk -pdf cover-letter.tex

clean:
	latexmk -C
	rm -f *.bbl *.blg *.out *.toc *.fls *.fdb_latexmk *.log *.aux

.PHONY: all clean
