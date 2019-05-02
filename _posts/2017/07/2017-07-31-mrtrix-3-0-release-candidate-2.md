---
layout: post
title: 'MRtrix 3.0 (release candidate 2)'
author: 'thijsdhollander'
date: 2017-07-31 05:50:46
categories:
discourse_id: 1065
summary: posted on Jul 31, 2017
---
The last few months of work have resulted in another batch of updated features. The most important changes motivating this second release candidate relate to the bias field correction and intensity normalisation process previously performed by the `mtbin` command, which affects the fixel-based analysis pipeline in particular.  Users who are in the process of performing a fixel-based analysis on their data should pay special attention to the changes this update brings to the bias field and intensity normalisation and other steps (and documentation) of the fixel-based analysis pipeline (see below for details). 

This release candidate introduces a number of bug fixes and enhancements, but also other changes that you will need to know about, in particular:

- [the `mtbin` command is now deprecated](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/2); users are urged to use the new `mtnormalise` command instead.
- [`dwipreproc` has been updated](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/3) to better handle acquisitions with repeated DWIs.
- [`mrview` now supports displaying multiple volumes](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/4) in lightbox mode.
- [new `-mask` option to `fixelcfestats`](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/5)
- [ `mrdegibbs`: a new command](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/6) to remove Gibbs ringing artefacts.
- changes to [voxel size handling in `population_template`](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/7)
- the [energy term used in `dirgen`](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/8) and associated commands has been corrected.
- [improved DICOM handling](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/9) for series containing multiple image types
- support for [reading TIFF images](http://community.mrtrix.org/t/mrtrix-3-0-release-candidate-2/1065/10)

#### Other more minor enhancements:

- support for exporting tracks to PLY format via `tckconvert` (courtesy of Daniel Blezek)
- improved handling of MGH/NGZ images
- fix handling of large files on Windows
- fix of the `-shell` option for `dwi2fod msmt_csd` (thanks to @isAarya for reporting!) 

As always, you can update your install by performing a `git pull` followed by `./build` at the command line (while in your MRtrix installation folder).
            