---
layout: "page"
title: macOS pre-compiled Anaconda install
---

These instructions are appropriate for macOS users who already have
[anaconda](https://www.anaconda.com/)
(or [miniconda](https://docs.conda.io/en/latest/miniconda.html)) installed. 

---

Instructions
============

Open a terminal configured for anaconda/miniconda, and type:
```
conda install -c mrtrix3 mrtrix3
```


---

Upgrading *MRtrix3*
===================

Once installed, you can keep *MRtrix3* up to date using the regular Anaconda
tools:
```
conda update -c mrtrix3 mrtrix3
```
Note that it is necessary to specify the `mrtrix3` channel with the `-c
mrtrix3` option when updating, otherwise the command will return indicating
that the package is up to date, without giving any indication that it hasn't
actually checked the `mrtrix3` channel.


