---
layout: post
title: 'MRtrix 3.0.3 release'
author: 'Lestropie'
date: 2021-07-19 11:01:09
categories:
summary: posted by Robert Smith on Jul 19, 2021
---
We are pleased to announce the immediate release of *MRtrix* `3.0.3`.

This is a bug fix release. We recommend users upgrade as soon as practical, using the instructions provided on our [downloads pages](https://www.mrtrix.org/download/) (for precompiled packages), or the [usual procedure](https://mrtrix.readthedocs.io/en/3.0.3/installation/build_from_source.html#keeping-mrtrix3-up-to-date) for installations from source.

The [full changelog is attached below](https://community.mrtrix.org/t/mrtrix-3-0-3-release/5065/2). Noteworthy changes include:

* When loading a DICOM directory containing multiple patients and/or studies, the [order](https://github.com/MRtrix3/mrtrix3/pull/2346) in which they are presented for user selection may differ from previous behavior. Therefore, any user scripts that automatically perform such selections may need to be revised; but the updated code now ensures that these orderings are *sensible* and *reproducible*;

* We now provide official *MRtrix3* [containers]((https://mrtrix.readthedocs.io/en/3.0.3/installation/using_containers.html)), offering an alternative platform by which to utilise *MRtrix3* tools;

* Further [fixes](https://github.com/MRtrix3/mrtrix3/pull/2308) to handling of phase encoding data when stored in sidecar files, which hopefully resolves issues encountered by those with complex phase encoding acquisition strategies and/or interacting with those data directly.

All the best from the *MRtrix3* team!

---

*[View comments on the community site](https://community.mrtrix.org/t/5065)*

            