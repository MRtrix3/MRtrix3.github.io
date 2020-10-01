---
layout: post
title: 'MRtrix 3.0.2 release'
author: 'jdtournier'
date: 2020-10-01 02:38:25
categories:
summary: posted by J-Donald Tournier on Oct 01, 2020
---
We are pleased to announce the immediate release of *MRtrix* `3.0.2`. 

This is primarily a bug fix release. We recommend users upgrade as soon as practical, using the instructions provided on our [downloads pages](https://www.mrtrix.org/download/) (for precompiled packages), or the [usual procedure ](https://mrtrix.readthedocs.io/en/3.0.2/installation/build_from_source.html#keeping-mrtrix3-up-to-date) for installations from source. 

The [full changelog is attached below](https://community.mrtrix.org/t/mrtrix-3-0-2-release/4142/2). Noteworthy changes include:
- fix [issue in `tckgen`](https://github.com/MRtrix3/mrtrix3/pull/2180) that caused streamlines to be erroneously discarded in some circumstances.
- fix [NIfTI qform handling](https://github.com/MRtrix3/mrtrix3/pull/2185) when writing images.
- fix [issue in `mrhistmatch` (and hence `dwicat`)](https://github.com/MRtrix3/mrtrix3/pull/2184) that would sometimes result in no change.
- fix [issues](https://github.com/MRtrix3/mrtrix3/pull/2127) in [`dwifslpreproc`](https://github.com/MRtrix3/mrtrix3/pull/2166) that precluded the integrated usage of EddyQC.

All the best from the *MRtrix3* team!

---

*[View comments on the community site](https://community.mrtrix.org/t/4142)*

            