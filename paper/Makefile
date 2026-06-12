TEX      := paper
DOCS_DIR := ../docs

.PHONY: all clean distclean docs watch

all: $(TEX).pdf

$(TEX).pdf: $(TEX).tex refs.bib $(wildcard image/*.pdf image/**/*.pdf)
	latexmk -pdf $(TEX).tex

watch:
	latexmk -pdf -pvc $(TEX).tex

docs: $(TEX).pdf
	cp $(TEX).pdf $(DOCS_DIR)/

clean:
	latexmk -c

distclean:
	latexmk -C
