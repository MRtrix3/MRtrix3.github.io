---
layout: post
title: 'Scripts: Help pages and algoritms'
author: 'Lestropie'
date: 2016-07-05 07:24:40
categories:
discourse_id: 335
---
Hi all,

I've just pushed some more changes to the Python scripts and scripting library provided with *MRtrix3*. I thought that in addition to highlighting those changes, I'd also take the chance to draw attention to some of the work I've done in the past related to script *algorithms*, which may interest some users looking to implement their own processing scripts or integrate their own personalized approaches into *MRtrix3* workflows.

## Script help pages

Apart from fixing a few bugs here and there, the main change I've made to the scripts that users will notice is the inline documentation: the help page that is provided by the script within the terminal, whenever you either type the name of the script without any command-line arguments, or use the `-help` option. Previously, this help page was provided by the [argparse](https://docs.python.org/3/library/argparse.html) library, which is also responsible for parsing the arguments and options that you provide at the command-line when running these scripts. Unfortunately these help pages could be quite confusing. So as of today, the scripts now provide help pages that are very similar to those provided by the *MRtrix3* binary commands; they are also piped to `less` by default, which allows you to navigate up and down the help page contents more easily.

Contrast this old help page for `dwipreproc`:

```

Error: the following arguments are required: pe_dir, input, output

usage: dwipreproc [-continue <TempDir> <LastFile>] [-force] [-help]
                  [-nocleanup] [-nthreads number] [-tempdir /path/to/tmp/]
                  [-quiet | -verbose] [-cuda]
                  (-rpe_none | -rpe_pair forward reverse | -rpe_all input_revpe)
                  [-grad GRAD | -fslgrad bvecs bvals]
                  [-export_grad_mrtrix grad | -export_grad_fsl bvecs bvals]
                  pe_dir input output

Perform diffusion image pre-processing using FSL's eddy tool; including inhomogeneity distortion correction using FSL's topup tool if possible

positional arguments:
  pe_dir                The phase encode direction; can be a signed axis
                        number (e.g. -0, 1, +2) or a code (e.g. AP, LR, IS)
  input                 The input DWI series to be corrected
  output                The output corrected image series

optional arguments:
  -cuda                 Use the CUDA version of eddy
  -grad GRAD            Provide a gradient table in MRtrix format
  -fslgrad bvecs bvals  Provide a gradient table in FSL bvecs/bvals format
  -export_grad_mrtrix grad
                        Export the final gradient table in MRtrix format
  -export_grad_fsl bvecs bvals
                        Export the final gradient table in FSL bvecs/bvals
                        format

standard options:
  -continue <TempDir> <LastFile>
                        Continue the script from a previous execution; must
                        provide the temporary directory path, and the name of
                        the last successfully-generated file
  -force                Force overwrite of output files if pre-existing
  -help                 Display help information for the script
  -nocleanup            Do not delete temporary directory at script completion
  -nthreads number      Use this number of threads in MRtrix multi-threaded
                        applications (0 disables multi-threading)
  -tempdir /path/to/tmp/
                        Manually specify the path in which to generate the
                        temporary directory
  -quiet                Suppress all console output during script execution
  -verbose              Display additional information for every command
                        invoked

Options for passing reversed phase-encode data:
  -rpe_none             Specify explicitly that no reversed phase-encoding
                        image data is provided; eddy will perform eddy current
                        and motion correction only
  -rpe_pair forward reverse
                        Provide a pair of images to use for inhomogeneity
                        field estimation; note that the FIRST of these two
                        images must have the same phase-encode direction as
                        the input DWIs
  -rpe_all input_revpe  Provide a second DWI series identical to the input
                        series, that has the opposite phase encoding; these
                        will be combined in the output image

Relevant citations for tools / algorithms used in this script:

eddy:
Andersson, J. L. & Sotiropoulos, S. N. An integrated approach to correction for off-resonance effects and subject movement in diffusion MR imaging. NeuroImage, 2015, 125, 1063-1078

FSL:
Smith, S. M.; Jenkinson, M.; Woolrich, M. W.; Beckmann, C. F.; Behrens, T. E.; Johansen-Berg, H.; Bannister, P. R.; De Luca, M.; Drobnjak, I.; Flitney, D. E.; Niazy, R. K.; Saunders, J.; Vickers, J.; Zhang, Y.; De Stefano, N.; Brady, J. M. & Matthews, P. M. Advances in functional and structural MR image analysis and implementation as FSL. NeuroImage, 2004, 23, S208-S219

Skare2010:
Skare, S. & Bammer, R. Jacobian weighting of distortion corrected EPI data. Proceedings of the International Society for Magnetic Resonance in Medicine, 2010, 5063

topup:
Andersson, J. L.; Skare, S. & Ashburner, J. How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. NeuroImage, 2003, 20, 870-888

Author:
Robert E. Smith (robert.smith@florey.edu.au)

Copyright (C) 2008-2016 The MRtrix3 contributors. This is free software; see the source for copying conditions. There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

```

With the new help page (which also includes bold and underlined characters when viewed in the terminal):

```

     dwipreproc: Script using the MRtrix3 Python libraries

SYNOPSIS

     dwipreproc [ options ] pe_dir input output

        pe_dir       The phase encode direction; can be a signed axis number
                     (e.g. -0, 1, +2) or a code (e.g. AP, LR, IS)

        input        The input DWI series to be corrected

        output       The output corrected image series

DESCRIPTION

     Perform diffusion image pre-processing using FSL's eddy tool; including
     inhomogeneity distortion correction using FSL's topup tool if possible

Options for passing reversed phase-encode data; one of these options MUST be provided

  -rpe_none
     Specify explicitly that no reversed phase-encoding image data is provided;
     eddy will perform eddy current and motion correction only

  -rpe_pair forward reverse
     Provide a pair of images to use for inhomogeneity field estimation; note
     that the FIRST of these two images must have the same phase-encode
     direction as the input DWIs

  -rpe_all input_revpe
     Provide a second DWI series identical to the input series, that has the
     opposite phase encoding; these will be combined in the output image

Options for the dwipreproc script

  -cuda
     Use the CUDA version of eddy

  -grad GRAD
     Provide a gradient table in MRtrix format

  -fslgrad bvecs bvals
     Provide a gradient table in FSL bvecs/bvals format

  -export_grad_mrtrix grad
     Export the final gradient table in MRtrix format

  -export_grad_fsl bvecs bvals
     Export the final gradient table in FSL bvecs/bvals format

Standard options

  -continue <TempDir> <LastFile>
     Continue the script from a previous execution; must provide the temporary
     directory path, and the name of the last successfully-generated file

  -force
     Force overwrite of output files if pre-existing

  -help
     Display help information for the script

  -nocleanup
     Do not delete temporary files during script, or temporary directory at
     script completion

  -nthreads number
     Use this number of threads in MRtrix multi-threaded applications (0
     disables multi-threading)

  -tempdir /path/to/tmp/
     Manually specify the path in which to generate the temporary directory

  -quiet
     Suppress all console output during script execution

  -verbose
     Display additional information for every command invoked

AUTHOR
     Robert E. Smith (robert.smith@florey.edu.au)

COPYRIGHT
     Copyright (c) 2008-2016 the MRtrix3 contributors  This Source Code Form is
     subject to the terms of the Mozilla Public  License, v. 2.0. If a copy of
     the MPL was not distributed with this  file, You can obtain one at
     http://mozilla.org/MPL/2.0/  MRtrix is distributed in the hope that it will
     be useful,  but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  For more details, see
     www.mrtrix.org

REFERENCES

     Andersson, J. L. & Sotiropoulos, S. N. An integrated approach to correction
     for off-resonance effects and subject movement in diffusion MR imaging.
     NeuroImage, 2015, 125, 1063-1078

     Smith, S. M.; Jenkinson, M.; Woolrich, M. W.; Beckmann, C. F.; Behrens, T.
     E.; Johansen-Berg, H.; Bannister, P. R.; De Luca, M.; Drobnjak, I.;
     Flitney, D. E.; Niazy, R. K.; Saunders, J.; Vickers, J.; Zhang, Y.; De
     Stefano, N.; Brady, J. M. & Matthews, P. M. Advances in functional and
     structural MR image analysis and implementation as FSL. NeuroImage, 2004,
     23, S208-S219

     * If using -rpe_all option:
     Skare, S. & Bammer, R. Jacobian weighting of distortion corrected EPI data.
     Proceedings of the International Society for Magnetic Resonance in
     Medicine, 2010, 5063

     * If using -rpe_pair or -rpe_all options:
     Andersson, J. L.; Skare, S. & Ashburner, J. How to correct susceptibility
     distortions in spin-echo echo-planar images: application to diffusion
     tensor imaging. NeuroImage, 2003, 20, 870-888
     
```

I think the biggest issue with the default `argparse` help page is that the 'usage' field becomes entirely congested with command-line options, and fails to adequately highlight the command-line arguments that are actually required. So hopefully these new help pages are much easier when first learning how to use a new script, or looking for available command-line options.

Some other little changes that will hopefully make script usage more seamless:

- Less picky about the order in which you provide options (e.g. previously to use `-force` it had to appear *before* the algorithm name; that's no longer the case)

- Scripts will now print the terminal output of any command that fails, and also write that output to a text file in the temporary directory.

## Script algorithms

For scripts `5ttgen` and `dwi2response`, the first compulsory command-line argument is the name of the *algorithm* to be used: e.g. `5ttgen fsl` to use the 'default' approach for generating the ACT 5TT image using FSL tools BET / FAST / FIRST, and `dwi2response tournier` to use Donald's response function estimation algorithm from [this paper](http://onlinelibrary.wiley.com/doi/10.1002/nbm.3017/abstract).

These two scripts are unique in that they provide solutions to a particular *computational task* (i.e. generating the 5TT image / estimating the response function), but there is *no single unique way* of achieving those tasks; therefore a *range of algorithms* are provided, which can be selected at the command line. Furthermore, each individual algorithm may have its own set of different command-line arguments or options associated with them.

What many may not have realised is that the algorithm choices made available by these scripts are *not actually hard-coded* into the main script itself. Rather, the master script (i.e. `5ttgen` / `dwi2response`) looks for appropriate source files within the relevant `scripts/src/` sub-directory, and makes those algorithms available for selection by the user at the command-line:

```
rob@Three MINGW64 /c/Users/rob/mrtrix3
$ ls scripts/src/dwi2response/ | grep -v "__"
fa.py
manual.py
msmt_5tt.py
tax.py
tournier.py

rob@Three MINGW64 /c/Users/rob/mrtrix3
$ dwi2response
 dwi2response: Script using the MRtrix3 Python libraries

SYNOPSIS

     dwi2response [ options ] algorithm ...

        algorithm    Select the algorithm to be used to derive the response function;
                     additional details and options become available once an
                     algorithm is nominated. Options are: fa, manual, msmt_5tt,
                     tax, tournier

```

Note how the list of algorithms made available by `dwi2response` matches the contents of the `scripts/src/dwi2response` directory. Furthermore, if a particular algorithm is selected when invoking the help page, the script will additionally present any arguments and options specific to the chosen algorithm within the generated help page.

This therefore presents an opportunity for anybody interested in, for instance, using an alternative software package for performing anatomical image segmentation and providing the 5TT image, or an alternative sequence of processing steps for generating a response function for spherical deconvolution. It is possible to provide a *new* source file within the relevant `scripts/src/` sub-directory, and the main script will *automatically* detect the presence of that file, and make that algorithm available at the command-line. This doesn't require *any modification* to *MRtrix3* files, yet allows you to take full advantage of the command-line parsing and provided library functions. So people are free to experiment with new algorithm designs for these tasks, by using one of the existing algorithms as a starting point and modifying from there. 

I hope somebody out there other than myself manages to have a bit of fun mucking about with these :grin:

Cheers
Rob
            