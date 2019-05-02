---
layout: post
title: 'MRtrix 3.0 (release candidate 3)'
author: 'jdtournier'
date: 2018-05-11 14:02:33
categories:
discourse_id: 1624
description: posted on 2018-05-11 14:02:33
---
We are pleased to announce the immediate release of our third release candidate, tagged as `3.0_RC3`, which brings a large number of improvements and bug fixes. We recommend users upgrade as soon as practical, using the [usual procedure](http://mrtrix.readthedocs.io/en/3.0_rc3/installation/linux_install.html#keeping-mrtrix3-up-to-date), with an additional call to `configure`:
```ShellSession
git pull
./configure
./build
``` 

Of the many changes introduced in this release, one is particularly important, and described in detail below. See subsequent sections for the full changelog.

## Important changes in `tckgen`

The most important bug fix, and primary motivation for pushing out this candidate release now, concerns a [mistake in our handling of spherical harmonics](https://github.com/MRtrix3/mrtrix3/commit/2ee2ed7ad027cfa0135a5c0d8b6a53f263be371b#diff-7f1548d07227925d6d884cbb25e8970aR453), introduced in version 0.3.11 (originally released on 12 Feb 2014). The good news is only one _MRtrix3_ command is affected by this bug. The bad news is that the command affected is [tckgen](http://mrtrix.readthedocs.io/en/3.0_rc2/reference/commands/tckgen.html), a prominent component of any tractography analysis. 

Since uncovering this bug, we have spent some time investigating its likely impact in various practical situations, and trying to get a feel for the severity of the issue -- (see full discussion on GitHub in issues [1204](https://github.com/MRtrix3/mrtrix3/pull/1204) and [1206](https://github.com/MRtrix3/mrtrix3/pull/1206)). While it's difficult to quantify its effect on tractography output, we feel that the impact, while undeniable, is likely to be minor, and likely to be countered by the subsequent application of SIFT/SIFT2. We are therefore confident that this bug is unlikely to introduce any detectable biases in quantitative tractography analyses, and is also unlikely to lead to any observable differences in other applications (e.g. targeted tractography studies).  

However, fixing this bug also prompted us to revisit the fODF threshold used during tracking (the `-cutoff` option in `tckgen`). The primary impact of this bug consisted of an overestimation of the fODF amplitude, which in effect means that tractography was performed with a lower cutoff than specified. The optimal value for the cutoff is somewhat subjective and context-dependent: there are differences in output between regular single-shell CSD and its more recent multi-shell multi-tissue variant (respectively, the `csd` and `msmt_csd` algorithms in `dwi2fod`), and different requirements for anatomically-constrained tractography. Based on a [comprehensive comparison](https://github.com/MRtrix3/mrtrix3/pull/1228#issuecomment-381514370) of the output of `tckgen` under the various relevant conditions, we came to the conclusion that a reduction of the default cutoff value to 0.05 was warranted (from its previous value of 0.1). Note that while manually specified thresholds will not be affected by the change in the default value, the output produced will nonetheless differ somewhat due to the bug itself. 

All the best from the _MRtrix3_ team!
            