---
layout: post
title: 'Dwipreproc and inter-protocol motion'
author: 'Lestropie'
date: 2017-07-21 04:36:58
categories:
discourse_id: 1046
---
Hi all,

There is an ongoing issue / discussion around the `dwipreproc` script, particularly with regards to a common use case: combination of the `-rpe_pair` and `-se_epi` options to provide reversed phase-encode spin-echo images with which to estimate the inhomogeneity field, which are then used to geometrically correct a set of DWIs that were all acquired with a fixed phase encoding (issue originally raised [here](http://community.mrtrix.org/t/dwipreproc-register-fieldmap-to-dwi-other-questions/621)). The issue is that the `dwipreproc` script fails to take into account the possibility of subject motion between acquisition of those volumes used to estimate the field, and acquisition of the DWIs to which the geometric correction is to be applied.

Although I made an attempt to provide an integrated solution to this issue within `dwipreproc` as part of the impending `3.0_RC2` tag update, that solution had to be discarded, as it did not generalise to all use cases and may therefore have led to erroneous pre-processing of some user data, without warning. So unfortunately I'm issuing a warning instead of a solution...

I've tried to provide a more user-friendly interface to `topup` and `eddy` to satisfy user requirements and simplify data pre-processing, but the `dwipreproc` script is still *not* a one-button "magic bullet" that will apply the appropriate pre-processing for all plausible acquisitions. There is therefore a certain degree of diligence required from users to ensure that the image processing algorithms they use are indeed applicable to their particular data, and are applied correctly. I cannot emphasise enough the importance of manual data checking.

With regards specifically to the issue of inter-protocol motion, there is a technique that users can employ manually in order to overcome the issue (this was additionally described somewhere on the FSL mailing list; unfortunately I can't seem to find it, if someone has the link feel free to post it here). If the first volume in the `topup` input image is the *same volume* as the first volume in the `eddy` input, then the estimated inhomogeneity field will be intrinsically aligned with the frame of reference used in `eddy` when applying that field. This can be achieved by:

- Extracting the first volume from the DWIs: `mrconvert dwi.mif first_bzero.mif -coord 3 0`

- Concatenating this volume with the reversed phase-encode images to be provided via `dwipreproc`'s `-se_epi` option, ensuring that this volume is the *first* volume in the output image: `mrcat first_bzero.mif se_epi.mif se_epi_with_bzero.mif -axis 3`.

  - If using the `-rpe_pair` or `-rpe_all` options, it is assumed that the *first half* of the volumes in this image have the same phase-encoding as that specified at the command-line using the `-pe_dir` option, and the *second half* have the *opposite* phase-encoding direction. The number of volumes in that image must therefore be a multiple of 2. If you are using one of these options, it will be necessary to also *remove* one of the original volumes from the SE-EPI series, in order to preserve this assumption.
For instance, if you have *two* volumes in the SE-EPI image, you would use:
`mrconvert se_epi.mif -coord 3 1 - | mrcat first_bzero.mif - se_epi_with_bzero.mif -axis 3`
This extracts *only* the second SE-EPI volume (the one with the reversed phase-encoding direction), and puts it *after* the first DWI *b*=0 volume in the output image.

- Running `dwipreproc` as normal, providing the `se_epi_with_bzero.mif` image using the `-se_epi` option.

**However**, there are certain assumptions within this correction that may not hold for all use cases. If *any* of these conditions do not hold, then the technique outlined above is not applicable to your data:

- Your SE-EPI images and DWIs have a different TE.

- Your SE-EPI images and DWIs have a different TR (for instance, if your DWIs are acquired using a multi-band sequence, but the reversed phase-encode images were acquired using single-band).

- Your SE-EPI images and DWIs have different effective bandwidths (for instance, if one uses GRAPPA but the other does not).

- Your SE-EPI images and DWIs do not have the same dimensions and voxel sizes in the three spatial axes.

- The first DWI volume is not a *b*=0 volume (though this can be mitigated with a bit of `mrconvert` trickery).

If this correction cannot be applied to your data, unfortunately I do not have a copy-and-paste solution for you. I would most definitely recommend checking for motion between the first SE-EPI volume and the first DWI volume of each subject to see the extent to which inter-protocol motion may be a problem for you. I do plan to try an alternative technique for automatically correcting for such inter-protocol motion within `dwipreproc`, but this will take some time to develop and validate.

Regards
Rob
            