.PHONY: help update-tex-files test lint clean build install

help:
	@echo "unicode2latex - Makefile targets:"
	@echo ""
	@echo "  make update-tex-files  - Update backup TeX files from system (requires TeX Live)"
	@echo "  make test              - Run all unit tests"
	@echo "  make lint              - Run flake8 linter"
	@echo "  make clean             - Remove build artifacts"
	@echo "  make build             - Build wheel and sdist"
	@echo "  make install           - Install package in development mode"
	@echo ""

# Update backup TeX files from system installation
# This should be run when unicode-math package is updated in TeX Live
update-tex-files:
	@echo "Updating backup TeX files from system..."
	@command -v kpsewhich >/dev/null 2>&1 || { echo "Error: kpsewhich not found. Please install TeX Live."; exit 1; }
	@mkdir -p unicode2latex/tex
	cp -a -u -v -t unicode2latex/tex \
		$$(kpsewhich unicode-math-xetex.sty) \
		$$(kpsewhich unicode-math-table.tex)
	@echo ""
	@echo "Backup files updated. File info:"
	@ls -lh unicode2latex/tex/
	@echo ""
	@echo "To check unicode-math version:"
	@grep -m1 "ProvidesExelatexPackage\|ProvidesPackage" unicode2latex/tex/unicode-math-xetex.sty || echo "(version not found in file)"

# Run all tests
test:
	python3 -m unittest discover unittests -v

# Run linter
lint:
	python3 -m flake8 unicode2latex/ unittests/ --max-line-length=127

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Build distribution packages
build: clean
	python3 -m pip install --upgrade build
	python3 -m build

# Install in development mode
install:
	python3 -m pip install -e .
