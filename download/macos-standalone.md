---
layout: "page"
title: macOS pre-compiled stand-alone install
---

These instructions are appropriate for macOS users who can't or don't want to
use [anaconda](https://www.anaconda.com/). 


---

Instructions
============

Open a terminal and copy-paste the following command into it:
```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/MRtrix3/macos-installer/master/install)"
```
The `install` script will download the binaries for the latest MRtrix3 release,
unpack them to `/usr/local/mrtrix3`. In addition it will create the appropriate
symbolic links in `/usr/local/bin` and `/Applications`.


---

Uninstalling *MRtrix3*
======================

Open a terminal and copy-paste the following command into it:
```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/MRtrix3/macos-installer/master/uninstall)"
```


Upgrading *MRtrix3*
===================

To update, simply run the install procedure again. The script should detect
previous versions and remove them automatically before proceeding.



