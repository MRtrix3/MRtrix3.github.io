---
layout: post
title: 'Reproducible Neuroscience at Stanford University'
author: 'Lestropie'
date: 2016-08-10 01:59:19
categories:
discourse_id: 380
description: posted on 2016-08-10 01:59:19
---
Hello *MRtrix*ers,

In the spirit of increased public engagement, I thought I'd let everybody know about what's been happening in the *MRtrix3* universe of late.

Last week, myself and @Dave attended the [coding sprint](http://reproducibility.stanford.edu/coding-sprint-for-a-new-neuroimaging-data-processing-platform/) for the [Stanford Centre for Reproducible Neuroscience](http://reproducibility.stanford.edu/). This involved developing neuroimaging processing pipelines that operate on cohort data conforming to the [Brain Imaging Data Structure (BIDS)](http://bids.neuroimaging.io/) standard, and [Docker containers](https://www.docker.com/) to make the processing of those pipelines highly portable.

Long-term, we hope to produce two major pipelines, that will perform 'glass-box' diffusion MRI analysis within the ongoing expansion of the OpenfMRI platform:

- Fixel-Based Analysis (FBA)

- Connectome analysis

There's plenty of development associated with this sprint in order for us to have the prerequisite capabilities within our software:

- Native NIfTI-2 image format support

- Calculation of node-wise and global measures of connectome matrices

- Permutation-based statistical inference of:

  - Connectome-derived measures
  
  - Network-specific differences in the connectome itself using the [NBS-TFCE](https://ww4.aievolution.com/hbm1501/index.cfm?do=abs.viewAbs&abs=2741) method

- Non-linear histogram matching for [improved rigid-body registration](http://www.sciencedirect.com/science/article/pii/S1053811915002451) between DWI and T1 volumes

- Ongoing development by @rtabbara toward a completely re-designed fixel image format, that will 'unlock' the contents of fixel data to users and developers alike; this should make preparation of data for fixel-based statistical inference, and navigation of the resulting data in `mrview`, much more intuitive

I'd encourage any readers who deal with management of cohort data to take a look at the [BIDS specification document](http://bids.neuroimaging.io/bids_spec1.0.0.pdf). In addition to defining a consistent standard for neuroimaging data storage that will improve data sharing and reduce confusion when exchanging data between sites (or even individuals), there is also the potential for making your data compatibile with new and future tools developed against this standard.

Happy tracking!
Rob
            