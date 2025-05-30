# Minimal makefile for Sphinx documentation

# These variables can be set from the command line or environment
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Default target: show help
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Main Sphinx build targets (html, latexpdf, etc.)
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom target to generate API .rst files automatically
.PHONY: apidoc
apidoc:
	@echo "Current directory is: $$(pwd)"
	@ls generated/pyrsgis*
	@rm -v generated/pyrsgis.rst generated/pyrsgis.raster.rst generated/pyrsgis.convert.rst generated/pyrsgis.ml.rst generated/pyrsgis.utils.rst || true
	@sphinx-apidoc -o generated ../pyrsgis --module-first --separate --no-toc ../pyrsgis/tests/*
