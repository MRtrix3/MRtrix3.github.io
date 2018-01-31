---
layout: post
title: 'Announcing the first MRtrix3 workshop: Paris, June 22-24'
author: 'jdtournier'
date: 2018-01-30 23:14:56
categories:
discourse_id: 1438
---
![workshop2018](http://community.mrtrix.org/uploads/default/original/2X/4/48694c5a817089ceca44a54d30a40d6fa99a0c5e.png)

We are very excited to announce that the first official _MRtrix3_ workshop will be held this year in Paris, France (June 22-24), immediately after the main ISMRM meeting. 

This 2½ day hands-on workshop will cover the theory and practice of diffusion analysis, covering the range of techniques available within _MRtrix3_. 

Participants will each be provided with a laptop, pre-installed with the relevant software and data. Participants that wish to bring their own laptops or data are of course welcome to do so, and we will do our best to accommodate them. 

**After completing this _MRtrix3_ course, participants should be able to process, analyze, and visualize their own diffusion MRI data sets using _MRtrix3_ tools.**

This course is aimed at both new and existing users of _MRtrix3_, covering basic functionality as well as the latest analysis methods. The topics covered are intended for researchers in basic science and/or clinical research, and will include: 

- Data pre-processing and quality assessment
  - [MP-PCA denoising](https://www.ncbi.nlm.nih.gov/pubmed/27523449)
  - [Gibbs ringing artefact removal](https://www.ncbi.nlm.nih.gov/pubmed/26745823)
  - [motion, eddy- and susceptibility-induced artefact removal](https://www.ncbi.nlm.nih.gov/pubmed/26481672) 
  - [bias field correction & intensity normalisation](https://www.researchgate.net/publication/315836355_Bias_Field_Correction_and_Intensity_Normalisation_for_Quantitative_Analysis_of_Apparent_Fibre_Density)
- Diffusion modelling:
   - [diffusion tensor imaging](https://www.ncbi.nlm.nih.gov/pubmed/12489095)
   - [spherical deconvolution](https://www.ncbi.nlm.nih.gov/pubmed/17379540)
   - [multi-tissue constrained spherical deconvolution](https://www.ncbi.nlm.nih.gov/pubmed/25109526)
   - [response function estimation for single-shell and multi-shell dMRI](http://mrtrix.readthedocs.io/en/doctest/constrained_spherical_deconvolution/response_function_estimation.html)
   - [multi-tissue CSD in presence of pathology](https://www.researchgate.net/publication/315836029_Towards_interpretation_of_3-tissue_constrained_spherical_deconvolution_results_in_pathology)
- Tractography:
  - [probabilistic & deterministic streamlines](http://onlinelibrary.wiley.com/doi/10.1002/ima.22005/abstract)
  - [global tractography](https://www.ncbi.nlm.nih.gov/pubmed/26272729) 
  - [anatomically-constrained tractography](https://www.ncbi.nlm.nih.gov/pubmed/22705374)
  - [track density imaging](https://www.ncbi.nlm.nih.gov/pubmed/20643215) & [track orientation density imaging](https://www.ncbi.nlm.nih.gov/pubmed/24389015)
- Connectomics:
  - connectome construction and related issues
  - [quantification of connectivity](https://www.ncbi.nlm.nih.gov/pubmed/25312774) via spherical deconvolution informed filtering of tracrograms ([SIFT](https://www.ncbi.nlm.nih.gov/pubmed/23238430) & [SIFT2](https://www.ncbi.nlm.nih.gov/pubmed/26163802))
  - [network based statistics](https://www.ncbi.nlm.nih.gov/pubmed/20600983)
- Group analysis of diffusion MRI data:
  - [fibre ODF based registration](https://www.ncbi.nlm.nih.gov/pubmed/21316463)
  - [fixel-based analysis](https://www.ncbi.nlm.nih.gov/pubmed/27639350)
  - statistical analysis via [connectivity-based fixel enhancement](https://www.ncbi.nlm.nih.gov/pubmed/26004503)
- Data visualisation:
  - using _MRView_ to display images, overlays, ODF glyphs, tractograms, etc.
  - [FOD-based DEC maps](https://www.researchgate.net/publication/276412466_Time_to_move_on_an_FOD-based_DEC_map_to_replace_DTI%27s_trademark_DEC_FA) & [panchromatic sharpening](https://www.researchgate.net/publication/276412176_Panchromatic_sharpening_of_FOD-based_DEC_maps_by_structural_T1_information)

--- 

#### Registration

The registration fee (in AU$) is:
- AU$ 750 for MSc/MD/PhD students _(approx. €490 / US$ 600)_ 
- AU$ 900 for other academic attendees _(approx. €590 / US$ 730)_
- AU$ 1,500 for commercial attendees _(approx.  €980 / US$ 1210)_

Registration includes all sessions, coffee/tea breaks and lunch for each day. Accommodation is _not_ included. All course materials, including lecture slides, tutorial instructions, and example data sets will be made available after the course.

The registration page will be open from **Tuesday 13 February** at **10pm (CET)**, and will close once the maximum of 80 participants has been reached. A further announcement will be made nearer the time with further details. 

---

#### Venue & accommodation

The _MRtrix3_ workshop will be held the [Hotel Mercure Paris Expo Porte de Versailles](http://www.mercure.com/gb/hotel-0375-mercure-paris-porte-de-versailles-expo-hotel/index.shtml), 36-38 rue du moulin, 92170 Vanves, France. 

<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2626.645493746547!2d2.2890146152365918!3d48.82682507928453!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47e67068aabf589b%3A0x37c908c3bb39dddb!2sHotel+Mercure+Paris+Porte+de+Versailles+Expo!5e0!3m2!1sen!2suk!4v1517244818305" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>

You will need to organise your own accommodation for the duration of the workshop. Those attending the ISMRM meeting may wish to use the same accommodation for both meeting and workshop. Alternatively, accommodation is available in the hotel hosting the workshop, or in the many hotels servicing the area.

---

#### Recommended prior reading

We strongly recommend attendees familiarise themselves with the **Unix command line**, as introduced in [this tutorial](http://command-line-tutorial.readthedocs.io/).

Recommended review papers on diffusion MRI:
- [Diffusion tensor imaging and beyond](https://www.ncbi.nlm.nih.gov/pubmed/21469191)
- [Diffusion MRI fiber tractography of the  brain](http://onlinelibrary.wiley.com/doi/10.1002/nbm.3785/full)

Further introductory material can be found in these books:
- [Diffusion Tensor Imaging: A Practical Handbook](http://www.springer.com/gp/book/9781493931170)
- [Introduction to Diffusion Tensor Imaging And Higher Order Models](https://www.elsevier.com/books/introduction-to-diffusion-tensor-imaging/mori/978-0-12-398398-5)

For details of the methods covered, please refer to the articles linked to in the outline above. 

---

#### Organisers & Speakers

[J-Donald Tournier](https://kclpure.kcl.ac.uk/portal/jacques-donald.tournier.html)<sup>1,2</sup>,  [Robert Smith](https://www.florey.edu.au/user/5819)<sup>3</sup>, [Max Pietsch](https://kclpure.kcl.ac.uk/portal/en/persons/maximilian-pietsch(211dfcc7-1906-4d55-ab52-1a0e5d9fc7fc).html)<sup>1,2</sup>, [Thijs Dhollander](https://www.florey.edu.au/user/5276)<sup>3</sup>, [Daan Christiaens](https://kclpure.kcl.ac.uk/portal/daan.christiaens.html)<sup>1,2</sup>, [Ben Jeurissen](https://visielab.uantwerpen.be/people/ben-jeurissen)<sup>4</sup>, [Chun-Hung Jimmy Yeh](https://www.florey.edu.au/user/5595)<sup>3</sup>, [Alan Connelly](https://www.florey.edu.au/user/5256)<sup>3,5</sup>

<sup>1</sup>[School of biomedical engineering and imaging sciences](https://www.kcl.ac.uk/lsm/research/divisions/imaging/Research.aspx), King's College London, London, UK
<sup>2</sup>[Centre for the Developing Brain](https://www.developingbrain.co.uk/), King's College London, London, UK
<sup>3</sup>[Florey Institute of Neuroscience & Mental Health](https://www.florey.edu.au/), Melbourne, Australia
<sup>4</sup>[Imec-Vision Lab](https://visielab.uantwerpen.be/), Department of Physics, University of Antwerp, Belgium
<sup>5</sup>[University of Melbourne](https://www.unimelb.edu.au/), Melbourne, Australia

----

#### Programme

|  | Fri 22 June | Sat 23 June | Sun 24 June |
| :---: | --- | --- | --- |
| 9:00&nbsp;&#8209;&nbsp;10:00 | Introduction to diffusion MRI | Quantitative metrics in dMRI | Group-level fixel-based analysis |
| 10:15&nbsp;&#8209;&nbsp;11:15 | Introduction to _MRtrix3_ & mrview | Apparent fibre density & required preprocessing | Connectivity-based fixel enhancement |
| 11:30&nbsp;&#8209;&nbsp;12:30 | Handling dMRI data | Registration in diffusion MRI | Visualisation of fixel-based analysis |
|  | _lunch_ | _lunch_ | _lunch_ |
| 14:00&nbsp;&#8209;&nbsp;15:00 | dMRI preprocessing | Quantitative whole-brain tractography | | 
| 15:15&nbsp;&#8209;&nbsp;16:15 | Voxel-level modelling | Generating the connectome | |
| 16:30&nbsp;&#8209;&nbsp;17:30 | Tractography | Group-level connectomics | | 

---

#### Contact

If you have any queries related to this workshop, please [contact us](http://community.mrtrix.org/new-message?groupname=workshop&title=workshop%20inquiry) via the @workshop group on the _MRtrix3_ community forum.
            