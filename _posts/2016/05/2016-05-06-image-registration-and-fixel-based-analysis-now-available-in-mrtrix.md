---
layout: post
title: Image registration and fixel-based analysis now available in MRtrix!
author: draffelt
date: 2016-05-06 08:06:41
categories:
discourse_id: 207
---
<h4>We are proud to announce that MRtrix now includes commands for image registration and fixel-based analysis!</h4>

<hr>

<h1>Image registration</h1>

<p>The new <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a> command can be used to perform robust rigid, linear and non-linear registration. In a similar vein to <a href="http://www.ncbi.nlm.nih.gov/pubmed/17659998">Avants et al. (2008)</a> images are symmetrically aligned to a 'midway' space. See <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister --help</code></a> for complete details. </p>

<p>While <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a> can align any two 3D or 4D images, it has been specifically designed for <a href="http://www.ncbi.nlm.nih.gov/pubmed/21316463">registration of Fibre Orientation Distributions (FOD)</a>. If the input images contain a spherical harmonic series, then FOD registration will be automatically performed and include the required <a href="http://www.ncbi.nlm.nih.gov/pubmed/22183751">FOD reorientation</a>.</p>

<p>The current version of <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a> is limited to using a mean squared intensity metric, and therefore it requires input images to be in the same intensity range. However we intend to include a normalised cross-correlation metric for both linear and non-linear registration in the near future. </p>

<h3>mrtransform</h3>

<p>We have also made significant changes to the <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrtransform"><code>mrtransform</code></a> command, so that it can now apply both the forward and reverse linear and non-linear transformations generated from <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a> (including transformation to the midway space). Like <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a>, the <a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrtransform"><code>mrtransform</code></a> command will automatically detect if the input is a spherical harmonic series and perform FOD reorientation. In addition, <a href="http://www.ncbi.nlm.nih.gov/pubmed/22036682">modulation of FODs</a> can be optionally applied to preserve the total fibre density across a fibre bundle's width. </p>

<h3>Population template script</h3>

<p>The recent update also includes a python script called <a href="http://userdocs.mrtrix.org/en/latest/getting_started/scripts_list.html#population-template"><code>population_template</code></a> for building an unbiased study-specific template using an iterative averaging approach. The script can be used on either scalar 3D or FOD images. Using the <code>-rigid</code> option will ensure the initial linear alignment is rigid, which is suited for intra-subject registration of longitudinal data.  While not a requirement, we recommend users use the <code>-mask_dir</code> option to supply brain masks for the input subject images, as this will reduce computation time substantially. </p>

<p><div class="lightbox-wrapper"><a data-download-href="//community.mrtrix.org/uploads/default/1a371b815a4c94571816ffe7f74a98f8aa14ff44" href="//community.mrtrix.org/uploads/default/original/1X/1a371b815a4c94571816ffe7f74a98f8aa14ff44.jpg" class="lightbox" title="registration.jpg"><img src="//community.mrtrix.org/uploads/default/optimized/1X/1a371b815a4c94571816ffe7f74a98f8aa14ff44_1_690x377.jpg" alt="Population template" width="690" height="377"><div class="meta">
<span class="filename">registration.jpg</span><span class="informations">750x410 78.8 KB</span><span class="expand"></span>
</div></a></div></p>

<hr>

<h1>Fixel-based analysis.</h1>

<p>This update also includes a number of commands to perform a fixel-based analysis. What's a fixel? It's just a fancy word for a <em>specific fibre population in a voxel</em> (a.k.a a fibre bundle element) - see <a href="http://userdocs.mrtrix.org/en/latest/concepts/dixels_fixels.html">here for a more detailed description</a>. Group strudies using traditional voxel-based analysis permit white matter changes to be localised to a voxel. However, in a fixel-based analysis individual fixels are compared across individuals, which enables significant differences to be localised to a specific fibre pathway, even in regions containing crossing fibres. </p>

<p>For more information on fixel-based analysis and group statistics on fixel images see our paper on <a href="http://www.ncbi.nlm.nih.gov/pubmed/26004503">connectivity-based fixel enhancement</a> and our upcoming paper on fixel-based morphometry (under review). </p>

<p>Step by step instructions for <a href="http://mrtrix.readthedocs.io/en/latest/workflows/DWI_preprocessing_for_quantitative_analysis.html">DWI preprocessing</a> and <a href="http://mrtrix.readthedocs.io/en/latest/workflows/fixel_based_analysis.html">fixel-based analysis</a> can be found in the MRtrix documentation. </p>

<p><div class="lightbox-wrapper"><a data-download-href="//community.mrtrix.org/uploads/default/d3c453f2c16e4dbc363d1db33c670756df3c9262" href="//community.mrtrix.org/uploads/default/original/1X/d3c453f2c16e4dbc363d1db33c670756df3c9262.jpg" class="lightbox" title="fixel-based-analysis.jpg"><img src="//community.mrtrix.org/uploads/default/optimized/1X/d3c453f2c16e4dbc363d1db33c670756df3c9262_1_690x377.jpg" alt="Population template" width="690" height="377"><div class="meta">
<span class="filename">fixel-based-analysis.jpg</span><span class="informations">750x410 91.5 KB</span><span class="expand"></span>
</div></a></div></p>

<hr>

<h1>List of new commands</h1>

<ul>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrregister"><code>mrregister</code></a>: performs rigid, linear and non-linear registration of images</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#fixelreorient"><code>fixelreorient</code></a>: Reorient fixel directions based on the Jacobian (local affine transform) in a non-linear warp</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#fixelcorrespondence"><code>fixelcorrespondence</code></a>: After spatial normalisation, assign/match fixels from one image (typically a subject) to another image (typically the template). </p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#fixellog"><code>fixellog</code></a>: A simple command to take the natural log of fixel values. Will likely be incorporated into <code>fixelcalc</code> in the future</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mraverageheader"><code>mraverageheader</code></a>: Estimates the orientation of the average image grid. Used to obtain an unbiased image grid for alignment of subjects to a template. </p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrcheckerboardmask"><code>mrcheckerboardmask</code></a>: Used to inspect image alignment after registration.</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#mrmetric"><code>mrmetric</code></a>: Compute the similarity between two images</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#warp2metric"><code>warp2metric</code></a>: Output a map of Jacobian matrices, Jacobian determinats or fibre cross-section for the analysis of white matter morphology. </p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/commands_list.html#warpconvert"><code>warpconvert</code></a>: Convert between different warp formats</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/scripts_list.html#population-template"><code>scripts/population_template</code></a>: Generate an unbiased population template</p></li>
<li><p><a href="http://userdocs.mrtrix.org/en/latest/getting_started/scripts_list.html#dwiintensitynorm"><code>scripts/dwiintensitynorm</code></a>: Perform a global intensity normalisation of multiple DWI images using the median white matter b=0 value.</p></li>
</ul>

<p>Cheers,<br>Dave</p>
            