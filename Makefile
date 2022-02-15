
all: input.pdf output.pdf output_P.pdf

output.tex: input.tex unicode2latex Makefile
	rm -f output.tex
	./unicode2latex -i input.tex -o output.tex
	chmod -w output.tex

output_P.tex: input.tex unicode2latex Makefile
	rm -f output_P.tex
	./unicode2latex -P -i input.tex -o output_P.tex
	chmod -w output_P.tex

%.pdf : %.tex Makefile
	xelatex -interaction=batchmode  $<

clean:
	rm -f  input.pdf output.tex output.pdf output_P.tex  output_P.pdf
