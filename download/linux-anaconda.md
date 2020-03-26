---
layout: "page"
title: GNU/Linux pre-compiled Anaconda install
---

These instructions are appropriate for GNU/Linux users who already have
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
conda update mrtrix3
```
or to update all packages:
```
conda update --all
```



