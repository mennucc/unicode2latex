
all: input.pdf output.pdf output_P.pdf

output.tex: input.tex unicode2latex Makefile
	./unicode2latex -i input.tex -o output.tex

output_P.tex: input.tex unicode2latex Makefile
	./unicode2latex -P -i input.tex -o output_P.tex

%.pdf : %.tex Makefile
	xelatex -interaction=batchmode  $<
