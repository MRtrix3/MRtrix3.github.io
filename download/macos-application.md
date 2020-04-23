---
layout: "page"
title: macOS pre-compiled application package installer
---

The standalone installer will fetch and install the binaries for the latest MRtrix3 release. It includes ``mrview`` and ``shview`` as macos application bundles, enabling tight system integration (e.g. exposing ``mrview`` as a proper macos application, enabling file icons for supported images and double clicking in Finder, ...).

---

Installing
==========

Open a terminal and copy-paste the following command into it:
```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/MRtrix3/macos-installer/master/install)"
```
The `install` script will download the binaries for the latest MRtrix3 release,
unpack them to `/usr/local/mrtrix3`. In addition it will create the appropriate
symbolic links in `/usr/local/bin` and `/Applications`.

---

Uninstalling
============

Open a terminal and copy-paste the following command into it:
```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/MRtrix3/macos-installer/master/uninstall)"
```

---

Upgrading
=========

To update, simply run the install procedure again:
```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/MRtrix3/macos-installer/master/install)"
```
The script should detect previous versions installed at the same location and remove them automatically before proceeding.
