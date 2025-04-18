SPHINXBUILD = sphinx-build
SOURCEDIR = .
BUILDDIR = _build

.PHONY: html clean

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html --fail-on-warning

clean:
	rm -rf $(BUILDDIR)