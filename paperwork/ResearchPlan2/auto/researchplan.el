(TeX-add-style-hook
 "researchplan"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "natbib")
   (LaTeX-add-bibliographies
    "references.bib"))
 :latex)

