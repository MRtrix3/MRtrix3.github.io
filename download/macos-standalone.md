---
layout: "page"
title: macOS pre-compiled stand-alone install
---

The standalone installer will fetch and install the binaries for the latest MRtrix3 release. It includes ``mrview`` and ``shview`` as macos application bundles, enabling tight system integration (e.g. exposing ``mrview`` as a proper macos application, enabling file icons for supported images and double clicking in Finder, ...).

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



