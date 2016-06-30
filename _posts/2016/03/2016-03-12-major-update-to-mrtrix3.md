---
layout: post
title: 'Major update to MRtrix3'
author: 'jdtournier'
date: 2016-03-12 12:09:20
categories:
discourse_id: 110
---
We have just pushed a major update for MRtrix3, constituting over a year's work from the developers in preparation for the official software release. Most of these changes will in fact be transparent to users: invoking commands, processing data etc. are more-or-less unaffected by the changes. The only major changes from a user's point of view relate to installation of the software. See [below for details](#changes-to-the-installation-process).

For the sake of clarity, and to encourage people to update and test the newest code prior to the official software release, we are listing here both the [major modifications](#major-updates) that have occurred within the code, as well as [minor updates](#minor-updates) that have been added within this code branch and are now available to users.

While we firmly believe these updates will prove advantageous for users in the long run, some of these changes will affect the outcome and/or usage of some of the commands. This is the case notably for `dwi2response`, `dwi2tensor`, and `tckgen` (see [below for details](#minor-updates)). For users who wish to prevent this upgrade (for example to ensure the same version of the software is
used for their study), it may be preferably to checkout the last version of master before this upgrade (see [here for instructions](#preventing-the-upgrade)). 

If there are any issues encountered with the changes listed below, or indeed any aspect of MRtrix3, please report it. You can either use the [GitHub issue tracking page](https://github.com/MRtrix3/mrtrix3/issues) for issues that you are confident are software glitches, or create a new topic in this community forum for more general questions or inquiries.

----

# Changes to the installation process

There are two major changes related to the installation:

- MRtrix3 now relies on the [Eigen3](http://eigen.tuxfamily.org/) library for its linear algebra handling. The [GNU Scientific Library](http://www.gnu.org/software/gsl/) is no longer required. 

- By default, the executables now reside in the `release/bin` folder rather than `bin/`.


### Instructions for upgrading

To upgrade cleanly from the current version of MRtrix3, we recommend the following steps:

- Install the [Eigen3](http://eigen.tuxfamily.org/) library. This will depend on your distribution. See the [updated instructions in the documentation](http://mrtrix.readthedocs.org/) for details.

- Before upgrading, clean out your current installation of any temporary files and executables: 

```
  $ ./build clean
```

- Update the code:

```
  $ git pull
```

- Run the configure script:

```
  $ ./configure
```

- Build the executables:

```
  $ ./build
```

- Update your `PATH`. This depends on how you set your `PATH` originally. Assuming you followed our original recommendations, you will most likely have added a line similar to the following to your `./~bashrc` file:

```
  export PATH=/home/user/mrtrix3/bin:/home/user/mrtrix3/scripts:$PATH
```
 
  This line will depend on your exact setup. You will need to modify it to include the `release` folder between `mrtrix3/` and `bin`. Using the example above, this would change to:

```
  export PATH=/home/user/mrtrix3/release/bin:/home/user/mrtrix3/scripts:$PATH
```

----

# Preventing the upgrade

Some users may wish to prevent this upgrade to ensure their studies are unaffected by the changes entailed. In this case, it may be better to lock the code to the last version before this upgrade: `0.3.13`. This can be done with the following instructions:

```
$ git fetch
$ git checkout 0.3.13
$ ./build
```
 

----

# Major updates

- *Image handling code*: We have almost completely overhauled the C++ classes responsible for opening, creating and navigating both image header information, and image data contents, both on disk and within RAM. This has greatly reduced the number of different code classes required to perform such operations, and will hopefully ease the learning curve for researchers choosing to make use of the MRtrix3 libraries for their own developmental research. It also makes our own lives easier by reducing unnecessary code duplication.

- *Mathematics library*: We have completely removed the dependence of MRtrix3 on the [GNU Scientific Library (GSL)](http://www.gnu.org/software/gsl/), in favour of the C++ template library [Eigen](http://eigen.tuxfamily.org/). This library provides highly-optimised code for performing linear algebra, and is quite actively developed. In addition to the performance benefits we have observed (a factor of 3 speedup in some instances), it has also made redundant a large fraction of the custom classes and algorithms that were written as part of MRtrix3's own mathematics library component.

  A side-effect of this change is that MRtrix3 is no longer constrained to use the GNU Public License due to a dependence on GSL. Instead, MRtrix3 is now distributed under the [Mozilla Public License](http://mozilla.org/MPL/2.0/).

- *Automated testing*: We now automatically compile and test various components of MRtrix3 in a fully automated fashion using [TravisCI](https://travis-ci.org/). This means that any proposed changes to the code must be proven to compile and run on a set of testing platforms before the changes can be pushed to users. We also get a little green 'passing' logo on the main GitHub page.

- *Documentation*: This will no longer be managed using the [GitHub wiki](https://github.com/MRtrix3/mrtrix3/wiki); instead, this documentation will be included as part of the downloaded package (compiled into a PDF document), and made available through [readthedocs](http://mrtrix.readthedocs.org/).

----

# Minor updates

The merge of the `updated_syntax` branch pushed a total of 761 code updates to the main code repository branch. Below is a summary of the little updates that have happened along the way, that are tangible for the end user. We will try to group these in a semi-sensible manner...

### Implementation changes

- `tckgen`: A few little tractography tweaks, with respect to Anatomically-Constrained Tractography (ACT):

  - Slightly modified how iFOD2 handles the image edges. This should prevent streamlines from being erroneously rejected by ACT as they attempt to leave the inferior edge of the diffusion images due to iFOD2's calibration mechanism.
  
  - Streamlines can now be seeded from _within_ sub-cortical grey matter. The ACT priors are still applied, they are just slightly reformulated to be applicable in this context: each streamline must traverse white matter when tracking from _only one_ direction from the seed point. Hopefully this is useful for e.g. connectivity-based parcellation.
  
  - The back-tracking algorithm has been modified from that presented in the ACT NeuroImage article. There, a simple integer counter was incremented, and the track was truncated according to the value of that counter at each back-tracking event. This meant that if back-tracking was successfully used to traverse one difficult area, but a new difficult area was later encountered, the initial back-tracking step would already be very large. The new algorithm progressively increases the length of back-tracking when attempting to traverse a region, but the counter is _reset_ if the track successfully extends beyond the initial back-tracking event. This should enhance the effectiveness of the approach at improving tracking in difficult areas.

- `dwi2tensor`: Now uses an iteratively-reweighted linear least-squares solver for estimating tensor components.

- `dwi2response`: This command has been _deleted_, and replaced by a _script_ (see below).

- `5ttgen`: This (effectively unused) command has been deleted; the functionality is instead performed explicitly in the corresponding Python script.

### Script changes

The provided Python scripts have all been renamed, and undergone significant implementation changes. Apart from making the naming convention more consistent with the binary commands, hopefully it will also enable expansion of their capabilities, rather than having many scripts with subtle differences.

- `dwi2response` is no longer a binary command, but a _script_. Furthermore, it provides access to a number of different algorithms for estimating the response function from image data, and parameters for each. The discussion on [response function estimation](http://mrtrix.readthedocs.org/en/updated_syntax/concepts/response_function_estimation.html) has been updated accordingly.

- `act_anat_prepare_fsl` and `act_anat_prepare_freesurfer` have been combined into a single script, `5ttgen`.

- `revpe_distcorr` and `revpe_dwicombine` have been combined into a single script, `dwipreproc`. The command-line options for this script are used to indicate what type of reversed phase-encoding data are to be provided; it also works in the absence of any reversed phase-encode data. In addition, the script will now make use of the rotated diffusion gradient vectors provided by `eddy` in the latest version of FSL.

- `fs_parc_replace_sgm_first` has been renamed to `labelsgmfix`.

- Script `dwibiascorrect` can use either FSL's FAST, or the N4 algorithm provided with ANTS to estimate the inhomogeneity field.

### New commands

- `msdwi2fod`: Performs Multi-Shell Multi-Tissue (MSMT) CSD. The necessary response function files will most typically be generated using the new ``dwi2response`` script with the ``msmt_5tt`` algorithm; alternative approaches are still in development.

- `tckconvert`: Commands `tckimport` and `tck2vtk` have been removed, and replaced with this more general command, which can perform conversion of track data both to and from a number of file formats, as well as apply transformations between spatial conventions.

- `dwinormalise`: This is used for performing inter-subject DWI intensity normalisation.

- `fod2dec`: For generating Directionally-Encoded Colour images based on FOD data rather than the tensor model. Includes options for panchromatic sharpening, and luminance/perception correction.

- `tckglobal`: For performing global tractography (see [this paper for details](http://www.sciencedirect.com/science/article/pii/S1053811915007168)).

### New features

- `tckgen`: Null distribution tracking algorithms for both 1st- and 2nd-order tractography algorithms (the latter provides the null case of the default iFOD2 algorithm).

- `dwi2tensor`: Now capable of estimating diffusion kurtosis tensor (DKI) components.

- Bash completion. After compilation, execute the file `scripts/mrtrix_bash_completion` as part of your Bash profile startup. Then, hitting the TAB key while writing out an MRtrix command will auto-complete options; and, when searching for an input file, prompt only those files within the directory that are relevant (e.g. image files only when the command expects an input image).

- Additional tensor metrics available in the `tensor2metric` command.

- Job counter during the `build` script, to give an indication of likely duration of compilation.

- The ODF tool in `mrview` is now capable of displaying, in addition to spherical harmonic data:

- Amplitudes as defined based on a set of directions on the hemisphere. Note that this includes single- and multi-shell diffusion data, allowing direct visualisation of the diffusion signal on the half-sphere (rather than mapping to spherical harmonics, which may obscure features or artefacts).
  
- Diffusion Tensor glyphs (visualized as mean particle displacement).

- Integer postfixes at the command-line. Tired of running `tckgen -number 10000000`, and questioning whether you've accidentally got an extra zero in there? Just use `tckgen -number 10M` instead.

As always, please report any issues you encounter with this.
Cheers!

Donald.
            