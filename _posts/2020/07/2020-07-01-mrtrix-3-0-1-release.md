---
layout: post
title: 'MRtrix 3.0.1 release'
author: 'jdtournier'
date: 2020-07-01 11:32:22
categories:
summary: posted by J-Donald Tournier on Jul 01, 2020
---
We are pleased to announce the immediate release of *MRtrix* `3.0.1`. 

This is primarily a bug fix release. We recommend users upgrade as soon as practical, using the instructions provided on our [downloads pages](https://www.mrtrix.org/download/) (for precompiled packages), or the [usual procedure ](https://mrtrix.readthedocs.io/en/3.0.0/installation/build_from_source.html#keeping-mrtrix3-up-to-date) for installations from source. 

The [full changelog is attached below](https://community.mrtrix.org/t/mrtrix-3-0-1-release/3854/2?u=jdtournier). Noteworthy changes include:
- fix [issue in `fixelcfestats`](https://github.com/MRtrix3/mrtrix3/pull/2057) when importing data
- fix [issue in `dwifslpreproc`](https://github.com/MRtrix3/mrtrix3/pull/2067) that prevented the gradient table from being properly updated
- fix [compatibility issue with FreeSurfer 7 lookup table](https://github.com/MRtrix3/mrtrix3/pull/2076) in `labelconvert`
- [installation instructions for precompiled packages on Windows via MSYS2](https://www.mrtrix.org/download/windows-msys2/) have changed

All the best from the *MRtrix3* team!

---

*[View comments on the community site](https://community.mrtrix.org/t/3854)*

            