---
layout: default
---

# Documentation

There are several sources of information to help you get the most out of *MRtrix3*:

- [The official *MRtrix3* reference documentation](https://mrtrix.readthedocs.io/en/latest/). Note that you can access the documentation for specific versions of *MRtrix3* using the green button at the bottom of the sidebar (by default, this will be set to `v:latest`).

- The [*MRtrix3* wiki](https://community.mrtrix.org/c/wiki/12), hosted as a category on the [community forum](https://community.mrtrix.org/categories). This contains user-contributed information covering topics that might not fit well within the reference documentation. Users are encouraged to contribute to the wiki if they come across solutions to thorny or interesting problems, etc.

  Note that wiki posts can be browsed using the following tags: {% for tag in site.data.wiki_tags %} {% if forloop.last %}and{% else %}{% endif %} <a href="https://community.mrtrix.org/tags/c/wiki/12/{{ tag.name }}">{{ tag.name }}</a>{% if forloop.last %}{% else %},{% endif %}{% endfor %}.

- The [*MRtrix3* community forum](https://community.mrtrix.org/categories) is very active, and many of your questions may have already been answered there. You should of course feel free to start a new topic if you can't find the answers you're looking for!

- The [B.A.T.M.A.N. tutorial](https://osf.io/fkyht/), authored by [Marlene Tahedl](https://community.mrtrix.org/u/martahedl/summary), provides an excellent overview of a full analysis pipeline using *MRtrix3*, with plenty of examples, helpful strategies and advice about common pitfalls.

- [Andy's Brain Blog](https://www.andysbrainblog.com/), written by [Andrew Jahn](https://www.andysbrainblog.com/about), contains a wealth of information on various topics, including:
  - a [course on *MRtrix3*](https://andysbrainbook.readthedocs.io/en/latest/MRtrix/MRtrix_Introduction.html)
  - a [video series on Youtube](https://www.youtube.com/playlist?list=PLIQIswOrUH68Zi9SVDAdcUExpq2i6A2eD).

- The [*MRtrix3* youtube channel](/videos), which showcases key functionalities of *mrview*.


