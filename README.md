# doclint

A tool that runs automated heuristic evaluations for online documentation and
course material.

The heuristics are based on a number of sources on education and technical
writing:

- [SUNY Online Course Quality Review Rubrics](https://oscqr.suny.edu/)
- Literature on Learning and Teaching in Higher Education, such as:
  - Pokorny, H. and Warren, D. *Enhancing Teaching Practice in Higher
    Education*. Sage, 2016. First edition. (TODO: 2nd edition is out)
  - Barkley, E.F. and Howell Major, C. *Engaged Teaching: A Handbook for College
    Faculty*. SocialGood/K. Patricia Cross Academy, 2022.


## The competition / collaboration?

While developing this tool, it is a good idea to keep in view competitors
with similar functionality.

### Website markup and style checkers

There are plenty of website style checkers but they tend to focus on certain
aspects such as responsiveness, accessibility, markup validity, or

Notable ones are:

- [The Nu Html Checker] is the W3C's tool for checking correct usage of HTML
markup. Definitely worth running as part of a larger suite of tests. There is a
[Python wrapper for it], though it does not seem to be acively maintained?

[Python wrapper for it]:https://github.com/sveetch/py-html-checker
[The Nu Html Checker]:https://github.com/validator/validator

-

### MkDocs Plugins

- [mkdocs-spellcheck](https://github.com/pawamoy/mkdocs-spellcheck):
  an MkDocs plugin that runs a spell-checker over the rendered HTML.

- [linkchecker-mkdocs](https://github.com/byrnereese/linkchecker-mkdocs):
  an MkDocs plugin that checks for broken links.

- [mktestdocs](https://github.com/koaning/mktestdocs)
  an MkDocs plugin that runs code examples through `pytest`.

## Other documentation linters

These tend to be written in other languages (Ruby, JS, Java) or have
other features that make them less than ideal for the use cases I have
in mind. Many of them are from https://earthly.dev/blog/markdown-lint/

- **markdownlint**:

- [vnu]()
