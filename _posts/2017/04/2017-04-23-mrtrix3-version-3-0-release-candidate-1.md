---
layout: post
title: 'MRtrix3 version 3.0 (release candidate 1)'
author: 'jdtournier'
date: 2017-04-23 22:29:21
categories:
discourse_id: 851
summary: posted by J-Donald Tournier on Apr 23, 2017
---
_MRtrix3_ is finally about to come out of beta status and hit full release!  This is the first release candidate for our forthcoming version 3.0 of _MRtrix3_, the result of many months of work, with many new features and improvements (see below). Hopefully the proper full release will follow shortly after a few weeks of community testing. You are all encouraged to upgrade and try it out - and if you do come across any issues, don't hesitate to let us know, either on the [community forum](http://community.mrtrix.org), or via the [GitHub issue tracker](https://github.com/MRtrix3/mrtrix3/issues): we'll get them fixed straight away.

While the bulk of the functionality will behave as before, there are a number of changes in this version that you will need to know about, in particular:

- [differences in the file layout of the code repository](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/2): this is especially relevant if
  you are upgrading from a previous version - see detailed instructions below to avoid trouble.

- the new [fixel storage format](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/3).

- changes to the [dwipreproc](http://mrtrix.readthedocs.io/en/latest/reference/scripts/dwipreproc.html) and [tckgen](http://mrtrix.readthedocs.io/en/latest/reference/commands/tckgen.html) command-line interface (see the relevant section in [this post](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/5) for the rationale behind the `tckgen` changes). 

- other [new features](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/4): NIfTI-2 support, [JSON](http://www.json.org/) support, system signal handling, and many [other modifications & improvements](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/5). 


## Instructions for upgrading

The arrangement and naming conventions used in the repository structure have been altered, for [reasons described here](http://community.mrtrix.org/t/mrtrix3-version-3-0-release-candidate-1/851/2). This has the potential to introduce problems for users upgrading from previous versions - we therefore _strongly_ recommend users follow the detailed upgrade instructions provided below. 

Now that these instructions assume there was nothing unusual about your previous installation. If you needed to set any environment variables before, you will most likely need to do so again prior to running `./configure`.

1. update the code to the new version: `$ git pull`

2. re-run the configure script: `$ ./configure`

3. build the executables: `$ ./build`

     Note that this step will automatically remove your previous `release` folder if it exists.  This is to avoid conflicts that might arise if the executables from the previous version of _MRtrix3_ remain in place and in your `PATH`. 

4. set your `PATH` to reflect the new location: `./set_path`. 

    Alternatively, you can add the _MRtrix3_ `bin/` to your `PATH` yourself if you prefer. However, we recommend you use the `./set_path` script to handle this step, unless you are comfortable with manipulating the `PATH`, use a different shell, or have other specific requirements.

    Note that if you had previously set your `PATH` manually, we recommend you remove this entry from the relevant shell startup script (most likely `~/.bashrc` or `~/.profile`). 

5. close your terminal, start a fresh one, and verify that the commands used
   are the correct ones, e.g.:
    
        $ mrinfo --version
        == mrinfo 3.0_RC1 ==
        ...
 
    Don't worry if the version is reported as something like `3.0_RC1-3-gc4349e3f`: this simply indicates that you are running a more recent version than `3.0_RC1` (in this example, 3 commits ahead, with latest git commit having SHA1 identifier `c4349e3f`).`
            