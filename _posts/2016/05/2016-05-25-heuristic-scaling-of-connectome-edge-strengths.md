---
layout: post
title: 'Heuristic scaling of connectome edge strengths'
author: 'Lestropie'
date: 2016-05-25 02:07:57
categories:
discourse_id: 253
summary: posted by Robert Smith on May 25, 2016
---
Hi all,

Since this topic has arisen in a number of separate discussions recently, I thought I'd post some semi-coherent ramblings regarding the available scaling mechanisms in the `tck2connectome` command. Note that these are personal opinions and are not necessarily reflective of the general opinions of the diffusion MRI community or even the *MRtrix3* contributors, hence why this is appearing as a blog post rather than in the *MRtrix3* documentation.

The scaling mechanisms under discussion are:

1. Scaling the contribution of each streamline by the reciprocal of the streamline length. This is intended to compensate for a bias introduced by homogeneous seeding throughout the brain white matter: as longer pathways present a greater volume, streamlines are seeded within them more frequently than in shorter pathways.

2. Scaling the strength of each connectome edge by the reciprocal of the sum of the two node volumes. A larger target parcel is 'more likely' to be intersected by any particular streamline, so this mechanism attempts to directly compensate for this effect. Note that technically, for the cortex, this effect is proportional to GM-WM interface surface area rather than volume; but the same does not readily apply to sub-cortical structures, and a measure of surface area is not available in all usage scenarios, so the volume is used instead.

Both of these heuristics originate from Patric Hagmann's [2008 paper](http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.0060159), and their usage has since become ubiquitous in the field. They are also frequently applied in conjunction with one another. However, in my opinion, there has not been adequate critique or analysis of their use. Therefore here I'd like to discuss these briefly, particularly with contrast to the SIFT method.

### 1. Scaling by inverse streamline length

Firstly, I hope it is clear from the description of this scaling mechanism that it is only applicable in the specific case of homogeneous white matter seeding (whether deterministic, e.g. `tckgen -seed_grid_per_voxel`, or probabilistic, e.g. `tckgen -seed_image` or `tckgen -seed_random_per_voxel`). If *any other* seeding mechanism is used, then the mechanistic bias this heuristic is tailored to address is not present in the data in the first place, so its application would be highly erroneous.

This argument extends to the case where any tractography method that matches the tractogram to the diffusion data is applied; whether it be SIFT or comparable filtering algorithm, or global tractography. In these cases, the streamlines density is constrained to match the underlying fibre density irrespective of the length of the pathway, making the derived measure of 'connectivity' *independent of pathway length* (as it should be). Therefore in such cases, applying this scaling factor would be highly erroneous.

Another common misconception is that this effect of increased seeding density in longer pathways is the dominant source of streamlines tractography bias, and that applying this heuristic may be used as a substitute for methods such as SIFT. We have now [published results](http://www.sciencedirect.com/science/article/pii/S1053811916301677) proving that this is *not* the case.

### 2. Scaling by inverse node size

As mentioned previously, this heuristic scaling aims to directly compensate for the fact that from a given seed point, a larger target region is 'more likely' to be intersected by any one streamline, and will therefore tend to be intersected by an overall greater number of streamlines. This interpretation stems from the origins of probabilistic streamlines tractography, where the density of streamlines reaching a particular target from a particular seed was interpreted as the 'probability of connection' between those two regions. I tend to avoid such interpretation, in preference of considering each individual streamline as a plausible connection given the image data (but these are not 'additive' in terms of 'probability of connection').

In the presence of methods such as SIFT, our interpretation is redefined entirely. Streamline counts are made to be reflective of the underlying fibre density *at the local level* (i.e. per [fixel](http://mrtrix.readthedocs.io/en/latest/concepts/dixels_fixels.html)). When looking at the connection density of a particular pathway, this interpretation remains: we aim to give a meaningful measure of fibre density of the *pathway*. However, the quantified connection density between any two regions is 'blurred' by the presence of probabilistic streamlines dispersion. Nevertheless, it remains true even in this scenatio that a larger region is likely to be intersected by a greater number of streamlines as a smaller one; not because of a greater 'probability of connection', but because a physically larger area of grey matter is likely to actually have a greater physical fibre density entering / exiting the white matter.

I would strongly urge anyone using this heuristic scaling mechanism, whether by choice or as a misguided prerequisite, to reconsider its use. Node size, just like a number of other geometric parameters, will indeed influence the number of streamlines per edge; but this does not necessitate a corresponding scaling of those connection densities without careful consideration. A few points to consider:

- With SIFT (and other comparable methods), the connectivity between any pair of regions has a physically meaningful unit of cross-sectional area. With SIFT / SIFT2, the actual unit is AFD per unit length; but given that AFD is a measure of volume, this reduces to a cross-section (intra-cellular cross-sectional area in the case of high *b*-value acquisition). Other approaches contribute some magnitude of DWI intensity from each streamline point, which is a comparable parameter as signal intensity is proportional to tissue volume. By scaling these connection densities by something that is *not* dimensionless, estimated connection densities lose this direct physical meaning and interpretation.

- Many users are interested in deriving graph-theoretical measures from the connectome. Many of these measures can be thought of as a simpler version of network 'simulation', interrogating how information flows throughout the network. For such a network, the measure of 'connectivity' between nodes should be something related to 'information flow', or 'bandwidth'. Logically, the best measure for this (at least that we can access with diffusion MRI) is pathway cross-sectional area. This is precisely what methods such as SIFT provide. Deviating from this measure by introducing differential scaling of different edges in the network will therefore only deviate these network 'simulations' from the physical reality of the brain.

- Grey matter areas that are physically larger in size tend to be of a larger size not only because they require a larger number of neurons to perform their functions, but also because they require a greater density or extent of connectivity to other areas of the brain. An example that comes to mind for me is the rat barrel cortex, which apparently grew in physical size over time to support the increased complexity / density of their whiskers. Therefore the relative sizes of different regions may in fact be an *interesting feature* of the network, rather than an effect that should be 'cancelled out'; though this will depend on the particular parcellation mechanism being used.

- In the situation where the density of individual connections is to be tested, it may be preferable to include node sizes as a covariate, rather than performing a direct scaling of the connection densities themselves. This may also be beneficial in terms of hypothesis formation and reporting; e.g. "A difference in connection density was observed, taking into account differences in grey matter volume" v.s. "A difference in (connection density divided by grey matter volume) was observed".

OK, that's all from me for now. We're trialling a modification to *MRtrix3* blogging, where blog posts are made via the [community forum](http://community.mrtrix.org/c/annoucements), and some time later are pulled into the [website](http://www.mrtrix.org/blog/) (thanks to @rtabbara). This means that blog posts can be commented on by the community, and will hopefully also result in more frequent blog posts. So let us know your thoughts.

Rob
            