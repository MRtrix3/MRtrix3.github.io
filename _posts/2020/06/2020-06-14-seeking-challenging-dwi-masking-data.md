---
layout: post
title: 'Seeking challenging DWI masking data'
author: 'Lestropie'
date: 2020-06-14 01:18:55
categories:
summary: posted by Robert Smith on Jun 14, 2020
---
Hi all,

As part of the 2020 OHBM Hackathon, I'm intending to run a [project](https://github.com/ohbm/hackathon2020/issues/195) where we will re-implement `dwi2mask` using an "algorithm"-based interface (i.e. like `5ttgen` and `dwi2response`), so that different possibilities for deriving a brain mask from DWI data will be made available from a common *MRtrix3*-style command-line interface.

What would *really* assist this project would be if members of the community were to provide a **wide range of DWI data**, particularly including those where **brain masking has proven difficult** using one or more methods (`dwi2mask` or otherwise). This could include both pre-processed and raw DWI data. Availability of such data would allow us to demonstrate how different approaches perform in different scenarios, hopefully establish an assessment pipeline to quantify how different approaches perform, and potentially also inform the development of future algorithms.

-----

Since these data will be shared among team members (and hopefully in time incorporated in a public repository), any images provided by community members should ideally be anonymised. One way this can be done reasonably reliably is to convert to NIfTI, including command-line options for `mrconvert` to strip out fields where potential identifying information can appear:

```
mrconvert DWI.mif sub-01_dwi.nii.gz \
-export_grad_fsl sub-01_dwi.bvec sub-01_dwi.bval \
-json_export sub-01_dwi.json \
-clear_property comments \
-clear_property command_history
```

Any data where manually defined / refined masks could also be provided would be particularly valuable.

-----

For anybody interested in contributing, data can be shared through Dropbox or Google Drive (`r.smith <at> brain.org.au`), OneDrive (`robert.smith <at> florey.edu.au`), or any other convenient mechanism, where a link can be forwarded via PM on this forum or one of the email addresses above.

Any contributions would be greatly appreciated! :hugs: 

Best regards
Rob

---

*[View comments on the community site](https://community.mrtrix.org/t/3783)*

            