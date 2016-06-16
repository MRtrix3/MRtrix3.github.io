---
layout: post
title: MRtrix3 version incremented to 0.3.15
author: Lestropie
date: 2016-06-16 00:43:50
categories:
discourse_id: 300
---
Hi *MRtrix*ers,

I've just pushed a whole load of changes to the master branch of the GitHub repository. Since there's quite a few things in there that influence either the interfaces to commands, or the default behaviour of certain operations, I'm also incrementing the software version number from 0.3.14 to 0.3.15. We plan for this to be the *final version update* before *MRtrix3* is officially released. So our focus will shift to fixing the last few remaining bugs and critical missing features that are required to bundle up the software for a wider range of distribution mechanisms.

To show what's been happening with the software since the [last major update](http://community.mrtrix.org/t/major-update-to-mrtrix3/110), I've compiled below a list of important changes that have occurred during that time. Changes that are part of today's specific code merge are highlighted in bold, but all noteworthy changes in the 3 months since the last major update are included.

We highly recommend that users upgrade to this latest version, due to the range of bugs that have been fixed, as well as to ensure that the latest additions to the software are adequately tested before its release. We do however also recommend that users scroll through the list below, in case there have been changes to the software that may influence your particular experiments. The upgrade process itself should be hassle-free, as there are not any changes to software dependencies / binary file locations / etc.. It is however preferable to run: `./build clean`, in order to remove the binaries of deprecated commands.

Thanks to all who have provided feedback during this period; please continue to do so!

Best regards
Rob




# *MRtrix3* changelog: 0.3.13 to 0.3.15

(Note that tag 0.3.14 was used to indicate fixing of [FSL bvecs handling](http://community.mrtrix.org/t/bug-in-fsl-bvecs-handling/165))

## Major updates:

* **`dwidenoise`**: New command. This command uses the method described in [this paper](http://onlinelibrary.wiley.com/doi/10.1002/mrm.26059/abstract) to selectively filter noise from diffusion-weighted image volumes. We have made this command available to the research community as quickly as we could; so although we have not tested its influence on our own group studies, we are excited about the results we've seen.

* **`tcksample`**: Major changes. The existing functionality has been split between two commands, with enhanced functionalities added to both.

  * `tcksample`:
This command will now be wholly responsible for _sampling an underlying image_ along streamlines. Functionalities include:
    * Ability to export samples per streamline point to ASCII or `.tsf`.
    * Ability to calculate a statistic from the values per streamline, to produce a vector data file (one value per streamline).
    * Ability to use the precise streamline-to-voxel mapping mechanism: instead of getting a trilinear-interpolated value at each point, use the length through each voxel traversed when calculating the relevant statistic.
    * Ability to pre-calculate a Track Density Image, and subsequently divide the quantitative image value in each voxel appropriately amongst the streamlines traversing each voxel. This mechanism is only applicable for images where it is appropriate for the quantitative value considered to be the summation of contributions from individual fibres.

  * `tckresample`:
New command, responsible for _resampling a streamline to new vertices_. The previous `tcksample` functionality of re-sampling each streamline to vertices according to a specified line or arc in scanner space is now provided here, along with added capabilities (all of which exactly preserve the endpoints of every streamline):
    * Upsample streamline by an integer factor.
    * Downsample streamline by an integer factor.
    * Set a new fixed step size.
    * Obtain a fixed number of vertices for each streamline, regardless of length.
    * Extract the streamline endpoints.

  * `tckmap`:
    * Ability to import a vector file (e.g. from `tcksample`) as the primary source of image contrast (ie. the TWI 'factor' for each streamline).

  * `tck2connectome`:
    * Removed `mean_scalar` metric: this is replaced by being able to import a vector data file (e.g. from `tcksample`). If you have been using this functionality, you should read the new documentation FAQ entry [here](http://mrtrix.readthedocs.io/en/doctest/tutorials/FAQ.html).
    * Changed handling of different mechanisms for scaling the contribution from each streamline. Individual scalings (e.g. inverse streamline length, inverse node volumes, factors from an external data file) are activated independently using separate command-line options (see the command help page for precise details).

  * `tckedit`:
    * Removed track upsampling / downsampling functionality. These were awkward to handle in the code, and the order of their application relative to other operations was ambiguous yet could potentially influence results. This functionality is now instead handled by the `tckresample` command.

* ***Connectome tools***: Major change to how node information is managed. The concept of a '*connectome config file*' has *disappeared*; instead, *everything* is now based on *lookup tables*. The command `labelconfig` has be renamed to `labelconvert` (and its usage has changed; see the [help page](http://mrtrix.readthedocs.io/en/doctest/reference/commands_list.html#maskfilter) and [updated documentation](http://mrtrix.readthedocs.io/en/latest/tutorials/labelconvert.html)), and is best thought of as being responsible for *converting* a parcellation image from one lookup table to another. This means that a parcellation image will only ever be dependent on one text file, simplifying their subsequent use. It is also no longer necessary to specify the *format* of a text lookup table at the command-line: this will be detected automatically.
Note that although the location of the example lookup tables has moved (now located in `src/connectome/tables`), and their contents may have changed, the node indices remain identical to those files provided previously.

* *Registration*: Image registration in *MRtrix3*! Far too much to cover as part of this post; details are provided [here](http://community.mrtrix.org/t/image-registration-and-fixel-based-analysis-now-available-in-mrtrix/207). There's also been various ongoing updates to both the code and the `population_template` script, as we learn and optimise the behaviour of these capabilities.








## Minor updates:

* `5ttgen fsl`: Option to provide a T2-weighted image in addition to the default T1-weighted image. This is used exclusively during the FAST tissue segmentation step. Its effect should however be considered carefully before being used in large studies.

* `5ttgen` *and* `labelsgmfix`: `-sgm_amyg_hipp` option can be used to include the amygdalae and hippocampi in the list of sub-cortical grey matter structures. For `5ttgen`, the sub-cortical grey matter priors will be applied by ACT for streamlines entering these structures. For `labelsgmfix`, the FreeSurfer delineations of these structures will be replaced by those from FSL FIRST.

* **`configure`**: Improve and standardise error messages provided by configure script, so that hopefully users are better guided more towards finding a solution for their installation.

* `connectome2tck`: By default, the command will *not* provide track files for node self-connections. Such data can however be requested using the `-keep_self` option.

* **`dwi2fod` *and* `msdwi2fod`**: The functionality from both of these has now been merged into a single command `dwi2fod`. The [first argument](http://mrtrix.readthedocs.io/en/latest/reference/commands_list.html#dwi2fod) to the command now indicates the FOD estimation algorithm that you wish to use.

* **`dwi2response msmt_5tt`**: The order of the output responses provided has been changed. The order is now: WM, GM, CSF.

* **`dwi2response tournier`**: Dynamic cleanup of temporary files, to reduce incidence of users running out of storage space on temporary file systems.

* `dwi2tensor`:

  * Check the diffusion gradient table, to avoid performing erroneous tensor fitting if the input image does not have adequate b-value contrast to achieve the fit requested (i.e. 2 b-values for basic tensor estimation, 3 b-values for DKI).

  * New option to output predicted DWI volumes.

* `dwiextract`: Enhanced performance, and ability to set strides for the output image. Will now _always_ output a 4D image, even if there's only a single volume at the requested _b_-value.

* `fixelmult` *and* `fixeldivide`: These have been merged into new command `fixelcalc`.

* `fod2fixel`: Increased FOD sampling density to reduce orientation bias in fibre density estimates.

* `mrview`:

  * **Modified interface** for altering colours in the Tractography and Overlay tools. In both of these tools, colours can be either changed using the presented UI controls, or via the context menu by right-clicking on the relevant entry in the file list.

  * **Interface** for handling (track) scalar files is now embedded within the main Tractography tool. Furthermore, thresholding by a (track) scalar file can now be achieved independently of the file / mechanism used to determine the streamline colours.

  * Improved colour mapping for viewing complex images.

  * Various changes and fixes to the handling of dixel-based ODFs (i.e. ODFS where the amplitudes are not provided in the spherical harmonic basis, but based on a set of directions on the hemisphere). Type of ODF information is now selected at image load rather than as part of the user interface, to de-clutter the interface and simplify implementation.

* `sh2power`:

  * Provide the power of the entire SH series as output by default; previous behaviour, where the power of each harmonic degree is provided separately, is instead accessible using the `-spectrum` option.

  * Changed relative scaling of each harmonic degree.

* **`tcksift` / `tcksift2`**: Change default behaviour regarding grey matter contamination of FODs. Previously, these commands had been set up to process single-tissue data, where the overall FOD size in the GM is similar to that of WM. This would result in fixels at the GM-WM interface being under-defined by streamlines, as the FOD size would be comparable to that of deep WM but streamlines were only permitted to occupy a fraction of the voxel volume. To compensate, the fibre density was heuristically scaled according to the relative volumes of different tissues from the 5TT image. In light of more frequent usage of multi-tissue approaches, this heuristic is now *disabled* by default, but can be accessed using the `-fd_scale_gm` option.

* **`transformconvert`**: New command. This will be responsible for *converting* transformation matrices / files between the conventions used by different software packages, whereas `transformcalc` will focus on *calculations* involving affine transformation matrices. Currently it is capable of importing transformations from FSL `flirt` and ITK (e.g. ANTs) and saving in *MRtrix3* convention.

* *Documentation*:

  * **The [document](http://mrtrix.readthedocs.io/en/latest/reference/config_file_options.html)** containing all *MRtrix3* config file options is now once again auto-generated from the code itself.

  * **Minor re-arrangement** of documentation structure. New section 'Reference' now contains the auto-generated documentation for binary commands and scripts.

  * [**New page**](http://mrtrix.readthedocs.io/en/latest/reference/mrtrix2_equivalent_commands.html) providing 'equivalent' commands between MRtrix 0.2 and *MRtrix3* for those users moving from the old software version.

  * Added tutorial on applying warps from other packages.

  * [Instructions](http://mrtrix.readthedocs.io/en/doctest/workflows/multi_tissue_csd.html) for MSMT CSD.

* *Memory allocation*: Detect and report failed memory allocation; applications should give a more meaningful error message if your system does not contain enough RAM to run the command.

* *Memory-mapping*: This is a technique allowing commands to access a file (e.g. an image) on disk as though it were stored on RAM, without requiring that the entire file be explicitly stored on RAM. Previously, we had disabled this functionality for output images, as it would cause commands to stall on clusters when writing to network-based file systems. We are now able to automatically detect whether or not the destination directory for an image is on a network file system, and choose whether or not to use memory-mapping accordingly. This will reduce unnecessary RAM usage for non-networked processing, and may speed up many operations.

* *Scripts*:

  * Most scripts using the *MRtrix3* Python libraries will now accept file paths that contain whitespace.

  * Faster and more secure execution of commands within scripts using `subprocess`.

  * It should now be possible to make use of the *MRtrix3* Python scripting library for developing your own scripts, *without* necessitating placing your script within the *MRtrix3* `scripts/` directory. You need only include the path to the *MRtrix3* `scripts/` directory in your `PYTHONPATH` environment variable.

* *Testing*: The testing framework has been moved from its own repository into the main MRtrix3 repository. This will simplify our own testing, as well as allow external developers to implement tests for their own commands. The data required for testing will not be downloaded as part of a typical MRtrix3 installation; it will only be downloaded if the user explicitly attempts to invoke the tests.










## Bugs squashed:

* `5ttgen fsl`: Fix errors relating to FSL output image types, users providing pre-masked brain images, and requesting that the output image retain the same dimensions as the input image.

* `5ttgen msmt_5tt`: Respect the user-defined brain mask if provided.

* `build`: Correctly identify individual command target on Windows even if the `.exe` extension is not specified.

* `dwi2response manual`: Fix manually setting maximum spherical harmonic degree per shell.

* `dwi2response msmt_5tt`: Fix detection of b-value shells that only contain a single volume.

* **`dwi2response tournier`**: Fix bug that made the script behaviour inconsistent with Donald's original proposal. Only the top 300 voxels were being dilated and used for the next iteration, rather than the top 3,000.

* `dwi2tensor`: Fixed bug in tensor calculation following the `updated_syntax` merge.

* `dwipreproc`:

  * Fix erroneous gradient table output with `-rpe_all` option.

  * Fix header transform comparison when testing for `topup` bug in earlier FSL version.

  * Fix bug when requested to export final gradient table in bvecs / bvals format.

* `fixelcfestats` and `mrclusterstats`: More robust design matrix decomposition.

* `labelsgmfix`: Fix bug preventing over-write of an existing file at completion of the script.

* `mrcalc`: Fix bug where an image used more than once in a single `mrcalc` call could be registered as a complex image, forbidding certain mathematical operations.

* `mrmath product`: More sensible results in the presence of non-finite values.

* `mrview`: 

  * **Fix bug** when displaying an image with non-trivial intensity offset / scaling using a 3D texture (i.e. either off-axis, or in lightbox or volume render modes).

  * Fix bug where screenshot tool would no longer capture images if the user clicked the 'Cancel' button when selecting an output directory.

  * Revert ODF tool tensor glyphs to displaying ADC rather than mean particle displacement.

  * Fix hanging of ROI tool if the viewing plane was heavily off-axis with respect to the ROI, and the user performed a fast swiping draw.

  * Prevent ODF preview window 'lagging behind' the main window whenever a different anatomical plane was selected.

  * Fix incorrect ODF preview window orientation relative to the main window.

  * Resetting the intensity windowing is now based on the displayed slice if locked to axes, or the whole volume if not locked. Also, if the intensity windowing can't be set because the initial displayed slice is empty, it will now automatically reset once you view a non-empty slice.

  * Fix bug in volume render mode when image voxels are anisotropic.

* `sh2response`: Skip voxels for which the provided fibre direction is invalid.

* `tck2connectome`: Fix erroneous warning that no streamlines were found to intersect a particular node.

* **`tckedit`**: Fix handling of streamlines that are cut into multiple sections when using the `-mask` option.

* `tckgen`:

  * Fix application of curvature constraint in the FACT algorithm when angle is set explicitly.

  * Fix interpretation of integer postfixes from the command line (e.g. `tckgen -number 10M`).

* `tckmap` *(and some other commands)*: Fix minor bug in how streamline interpolation was applied at one endpoint of the streamline.

* `tcksift` / `tcksift2`: Fix `-output_debug` option following `updated_syntax` merge.

* *DICOM import*: Fix import for Siemens mosaics for non-square LR phase-encode EPI.

* *FSL compatibility*: Fix bugs relating to data strides, NIfTI conventions and FSL image handling; more information [here](http://community.mrtrix.org/t/bug-in-fsl-bvecs-handling/165/1).

* ***MSMT CSD***: Fix potential bugs due to uninitialized memory. These could affect the application of the non-negativity constraint, and if the requested `-lmax` was greater than that of the response function for the corresponding tissue, but were inconsistent in their appearance.

* *Scripts*: Ensure that the version of *MRtrix3* commands used is the same version as the script library being invoked.

* *Track file output*: Prevent segmentation fault in cases where the target output file path could not be opened.

* *Windows*:

  * **Multi-threading** should now work with any number of threads without lockups on Windows machines.

  * Move the MRtrix configuration file from the Windows user home directory to the MSYS2 user home directory.

  * The shared library file is now stored in the same directory as the command binaries, simplifying installation.

  * The terminal will now use text colouring by default, as is provided on other OS's, since the MSYS2 terminal supports them.
            