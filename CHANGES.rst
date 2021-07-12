===============
 Major changes
===============

Version 2.0
===========

- A new ``--long-line-threshold`` flag controls the line length over which Alectryon will issue “long line” warnings. [2c1f9ff]

- A new ``--cache-compression`` flag enables compression of generated cache files.  This typically yields space savings of over 95%. [GH-35]

- A new ``--html-minification`` flag enables the generation of more compact HTML files.  Minified HTML files use backreferences to refer to repeated goals and hypotheses (these backreferences are resolved at display time using Javascript).  This typically saves 70-90% of the generated file size. [GH-35]

- HTML5, XeLaTeX and LuaLaTeX outputs are now supported (``--latex-dialect``, ``--html-dialect``). [c576ae8, 08410c0]

- Caching is now supported for all documents, not just those processed through docutils (``--cache-directory``). [c3dfa6b]

- (Experimental) LaTeX export now works for full reST and Coq documents, not just snippets. [GH-47]

Breaking changes
----------------

- The HTML markup for hypothesis blocks has been simplified to save space in generated files (may affect third-party stylesheets). [de791bc]
- ``json_of_annotated`` and ``annotated_of_json`` in module ``alectryon.json`` are now ``PlainSerializer.encode`` and ``PlainSerializer.decode``. [3320896]

Version 1.1
===========

- Alectryon is now on PyPI. [GH-46]

- `alectryon.el` is now on MELPA. [https://github.com/melpa/melpa/pull/7554]

Breaking changes
----------------

- CSS classes have been renamed from ``.coq-…`` to ``.alectryon-…``.
- CSS class ``alectryon-header`` is now ``alectryon-banner``.
- The undocumented ``alectryon-header`` has been removed.
