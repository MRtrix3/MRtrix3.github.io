---
layout: post
title: Major update to MRtrix3
author: jdtournier
date: 2016-03-12 12:09:20
categories:
discourse_id: 110
---
<p>We have just pushed a major update for MRtrix3, constituting over a year's work from the developers in preparation for the official software release. Most of these changes will in fact be transparent to users: invoking commands, processing data etc. are more-or-less unaffected by the changes. The only major changes from a user's point of view relate to installation of the software. See <a href="#changes-to-the-installation-process">below for details</a>.</p>

<p>For the sake of clarity, and to encourage people to update and test the newest code prior to the official software release, we are listing here both the <a href="#major-updates">major modifications</a> that have occurred within the code, as well as <a href="#minor-updates">minor updates</a> that have been added within this code branch and are now available to users.</p>

<p>While we firmly believe these updates will prove advantageous for users in the long run, some of these changes will affect the outcome and/or usage of some of the commands. This is the case notably for <code>dwi2response</code>, <code>dwi2tensor</code>, and <code>tckgen</code> (see <a href="#minor-updates">below for details</a>). For users who wish to prevent this upgrade (for example to ensure the same version of the software is<br>used for their study), it may be preferably to checkout the last version of master before this upgrade (see <a href="#preventing-the-upgrade">here for instructions</a>). </p>

<p>If there are any issues encountered with the changes listed below, or indeed any aspect of MRtrix3, please report it. You can either use the <a href="https://github.com/MRtrix3/mrtrix3/issues">GitHub issue tracking page</a> for issues that you are confident are software glitches, or create a new topic in this community forum for more general questions or inquiries.</p>

<hr>

<h1>Changes to the installation process</h1>

<p>There are two major changes related to the installation:</p>

<ul>
<li><p>MRtrix3 now relies on the <a href="http://eigen.tuxfamily.org/">Eigen3</a> library for its linear algebra handling. The <a href="http://www.gnu.org/software/gsl/">GNU Scientific Library</a> is no longer required. </p></li>
<li><p>By default, the executables now reside in the <code>release/bin</code> folder rather than <code>bin/</code>.</p></li>
</ul>

<h3>Instructions for upgrading</h3>

<p>To upgrade cleanly from the current version of MRtrix3, we recommend the following steps:</p>

<ul>
<li><p>Install the <a href="http://eigen.tuxfamily.org/">Eigen3</a> library. This will depend on your distribution. See the <a href="http://mrtrix.readthedocs.org/">updated instructions in the documentation</a> for details.</p></li>
<li><p>Before upgrading, clean out your current installation of any temporary files and executables: </p></li>
</ul>

<p></p><pre><code class="lang-auto">  $ ./build clean</code></pre>

<ul><li>Update the code:</li></ul>

<p></p><pre><code class="lang-auto">  $ git pull</code></pre>

<ul><li>Run the configure script:</li></ul>

<p></p><pre><code class="lang-auto">  $ ./configure</code></pre>

<ul><li>Build the executables:</li></ul>

<p></p><pre><code class="lang-auto">  $ ./build</code></pre>

<ul><li>Update your <code>PATH</code>. This depends on how you set your <code>PATH</code> originally. Assuming you followed our original recommendations, you will most likely have added a line similar to the following to your <code>./~bashrc</code> file:</li></ul>

<p></p><pre><code class="lang-auto">  export PATH=/home/user/mrtrix3/bin:/home/user/mrtrix3/scripts:$PATH</code></pre>

<p>  This line will depend on your exact setup. You will need to modify it to include the <code>release</code> folder between <code>mrtrix3/</code> and <code>bin</code>. Using the example above, this would change to:</p>

<p></p><pre><code class="lang-auto">  export PATH=/home/user/mrtrix3/release/bin:/home/user/mrtrix3/scripts:$PATH</code></pre>

<hr>

<h1>Preventing the upgrade</h1>

<p>Some users may wish to prevent this upgrade to ensure their studies are unaffected by the changes entailed. In this case, it may be better to lock the code to the last version before this upgrade: <code>0.3.13</code>. This can be done with the following instructions:</p>

<p></p><pre><code class="lang-auto">$ git fetch
$ git checkout 0.3.13
$ ./build</code></pre>

<hr>

<h1>Major updates</h1>

<ul>
<li><p><em>Image handling code</em>: We have almost completely overhauled the C++ classes responsible for opening, creating and navigating both image header information, and image data contents, both on disk and within RAM. This has greatly reduced the number of different code classes required to perform such operations, and will hopefully ease the learning curve for researchers choosing to make use of the MRtrix3 libraries for their own developmental research. It also makes our own lives easier by reducing unnecessary code duplication.</p></li>
<li><p><em>Mathematics library</em>: We have completely removed the dependence of MRtrix3 on the <a href="http://www.gnu.org/software/gsl/">GNU Scientific Library (GSL)</a>, in favour of the C++ template library <a href="http://eigen.tuxfamily.org/">Eigen</a>. This library provides highly-optimised code for performing linear algebra, and is quite actively developed. In addition to the performance benefits we have observed (a factor of 3 speedup in some instances), it has also made redundant a large fraction of the custom classes and algorithms that were written as part of MRtrix3's own mathematics library component.</p></li>
</ul>

<p>  A side-effect of this change is that MRtrix3 is no longer constrained to use the GNU Public License due to a dependence on GSL. Instead, MRtrix3 is now distributed under the <a href="http://mozilla.org/MPL/2.0/">Mozilla Public License</a>.</p>

<ul>
<li><p><em>Automated testing</em>: We now automatically compile and test various components of MRtrix3 in a fully automated fashion using <a href="https://travis-ci.org/">TravisCI</a>. This means that any proposed changes to the code must be proven to compile and run on a set of testing platforms before the changes can be pushed to users. We also get a little green 'passing' logo on the main GitHub page.</p></li>
<li><p><em>Documentation</em>: This will no longer be managed using the <a href="https://github.com/MRtrix3/mrtrix3/wiki">GitHub wiki</a>; instead, this documentation will be included as part of the downloaded package (compiled into a PDF document), and made available through <a href="http://mrtrix.readthedocs.org/">readthedocs</a>.</p></li>
</ul>

<hr>

<h1>Minor updates</h1>

<p>The merge of the <code>updated_syntax</code> branch pushed a total of 761 code updates to the main code repository branch. Below is a summary of the little updates that have happened along the way, that are tangible for the end user. We will try to group these in a semi-sensible manner...</p>

<h3>Implementation changes</h3>

<ul>
<li>
<p><code>tckgen</code>: A few little tractography tweaks, with respect to Anatomically-Constrained Tractography (ACT):</p>
<ul>
<li><p>Slightly modified how iFOD2 handles the image edges. This should prevent streamlines from being erroneously rejected by ACT as they attempt to leave the inferior edge of the diffusion images due to iFOD2's calibration mechanism.</p></li>
<li><p>Streamlines can now be seeded from <em>within</em> sub-cortical grey matter. The ACT priors are still applied, they are just slightly reformulated to be applicable in this context: each streamline must traverse white matter when tracking from <em>only one</em> direction from the seed point. Hopefully this is useful for e.g. connectivity-based parcellation.</p></li>
<li><p>The back-tracking algorithm has been modified from that presented in the ACT NeuroImage article. There, a simple integer counter was incremented, and the track was truncated according to the value of that counter at each back-tracking event. This meant that if back-tracking was successfully used to traverse one difficult area, but a new difficult area was later encountered, the initial back-tracking step would already be very large. The new algorithm progressively increases the length of back-tracking when attempting to traverse a region, but the counter is <em>reset</em> if the track successfully extends beyond the initial back-tracking event. This should enhance the effectiveness of the approach at improving tracking in difficult areas.</p></li>
</ul>
</li>
<li><p><code>dwi2tensor</code>: Now uses an iteratively-reweighted linear least-squares solver for estimating tensor components.</p></li>
<li><p><code>dwi2response</code>: This command has been <em>deleted</em>, and replaced by a <em>script</em> (see below).</p></li>
<li><p><code>5ttgen</code>: This (effectively unused) command has been deleted; the functionality is instead performed explicitly in the corresponding Python script.</p></li>
</ul>

<h3>Script changes</h3>

<p>The provided Python scripts have all been renamed, and undergone significant implementation changes. Apart from making the naming convention more consistent with the binary commands, hopefully it will also enable expansion of their capabilities, rather than having many scripts with subtle differences.</p>

<ul>
<li><p><code>dwi2response</code> is no longer a binary command, but a <em>script</em>. Furthermore, it provides access to a number of different algorithms for estimating the response function from image data, and parameters for each. The discussion on <a href="http://mrtrix.readthedocs.org/en/updated_syntax/concepts/response_function_estimation.html">response function estimation</a> has been updated accordingly.</p></li>
<li><p><code>act_anat_prepare_fsl</code> and <code>act_anat_prepare_freesurfer</code> have been combined into a single script, <code>5ttgen</code>.</p></li>
<li><p><code>revpe_distcorr</code> and <code>revpe_dwicombine</code> have been combined into a single script, <code>dwipreproc</code>. The command-line options for this script are used to indicate what type of reversed phase-encoding data are to be provided; it also works in the absence of any reversed phase-encode data. In addition, the script will now make use of the rotated diffusion gradient vectors provided by <code>eddy</code> in the latest version of FSL.</p></li>
<li><p><code>fs_parc_replace_sgm_first</code> has been renamed to <code>labelsgmfix</code>.</p></li>
<li><p>Script <code>dwibiascorrect</code> can use either FSL's FAST, or the N4 algorithm provided with ANTS to estimate the inhomogeneity field.</p></li>
</ul>

<h3>New commands</h3>

<ul>
<li><p><code>msdwi2fod</code>: Performs Multi-Shell Multi-Tissue (MSMT) CSD. The necessary response function files will most typically be generated using the new <code>dwi2response</code> script with the <code>msmt_5tt</code> algorithm; alternative approaches are still in development.</p></li>
<li><p><code>tckconvert</code>: Commands <code>tckimport</code> and <code>tck2vtk</code> have been removed, and replaced with this more general command, which can perform conversion of track data both to and from a number of file formats, as well as apply transformations between spatial conventions.</p></li>
<li><p><code>dwinormalise</code>: This is used for performing inter-subject DWI intensity normalisation.</p></li>
<li><p><code>fod2dec</code>: For generating Directionally-Encoded Colour images based on FOD data rather than the tensor model. Includes options for panchromatic sharpening, and luminance/perception correction.</p></li>
<li><p><code>tckglobal</code>: For performing global tractography (see <a href="http://www.sciencedirect.com/science/article/pii/S1053811915007168">this paper for details</a>).</p></li>
</ul>

<h3>New features</h3>

<ul>
<li><p><code>tckgen</code>: Null distribution tracking algorithms for both 1st- and 2nd-order tractography algorithms (the latter provides the null case of the default iFOD2 algorithm).</p></li>
<li><p><code>dwi2tensor</code>: Now capable of estimating diffusion kurtosis tensor (DKI) components.</p></li>
<li><p>Bash completion. After compilation, execute the file <code>scripts/mrtrix_bash_completion</code> as part of your Bash profile startup. Then, hitting the TAB key while writing out an MRtrix command will auto-complete options; and, when searching for an input file, prompt only those files within the directory that are relevant (e.g. image files only when the command expects an input image).</p></li>
<li><p>Additional tensor metrics available in the <code>tensor2metric</code> command.</p></li>
<li><p>Job counter during the <code>build</code> script, to give an indication of likely duration of compilation.</p></li>
<li><p>The ODF tool in <code>mrview</code> is now capable of displaying, in addition to spherical harmonic data:</p></li>
<li><p>Amplitudes as defined based on a set of directions on the hemisphere. Note that this includes single- and multi-shell diffusion data, allowing direct visualisation of the diffusion signal on the half-sphere (rather than mapping to spherical harmonics, which may obscure features or artefacts).</p></li>
<li><p>Diffusion Tensor glyphs (visualized as mean particle displacement).</p></li>
<li><p>Integer postfixes at the command-line. Tired of running <code>tckgen -number 10000000</code>, and questioning whether you've accidentally got an extra zero in there? Just use <code>tckgen -number 10M</code> instead.</p></li>
</ul>

<p>As always, please report any issues you encounter with this.<br>Cheers!</p>

<p>Donald.</p>
            