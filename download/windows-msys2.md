---
layout: "page"
title: Windows pre-compiled MSYS2 install
---

---


Important notes - please read first
===================================


- When installing or using *MRtrix3*, **always** use the ‘MinGW-w64 Win64
  shell’; it will **not** work with the ‘MSYS2 shell’ or ‘MinGW-w64 Win32
  shell’.

- Some of the Python scripts provided with MRtrix3 are dependent on external
  software tools (e.g. [FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki) or
  [ANTs](http://stnava.github.io/ANTs/)). If these packages are not available
  on Windows, then the corresponding *MRtrix3* scripts also cannot be run on
  Windows.  A virtual machine may therefore be required in order to use these
  particular scripts; though *MRtrix3* may still be installed natively on
  Windows for other tasks.

- These instructions have changed for version `3.0.1`, and no longer make use
  of a dedicated *MRtrix3* pacman package repository. If you had used our
  previous recommendations and find that `pacman -Syu` warns that the `mrtrix3`
  repo cannot be found, you can fix this by editing the `/etc/pacman.conf` file
  to remove these lines:
  ```
  [mrtrix3]
  SigLevel = Optional TrustAll
  Server = https://www.mrtrix.org/msys2
  ```

---


Install MSYS2
=============

> **Note:** skip this step if [MSYS2](https://www.msys2.org/) is already installed on
> your system. 

At the time of writing, we recommend the use of [MSYS2](https://www.msys2.org/)
to run *MRtrix3* on Microsoft Windows. It provides a complete Unix-like
terminal environment, including the `bash` shell, and allows applications to be
compiled to Windows-native code using the MinGW compiler. This is particularly
important if you plan to use the *MRtrix3* GUI components,
[mrview](https://mrtrix.readthedocs.io/en/latest/reference/commands/mrview.html) 
and
[shview](https://mrtrix.readthedocs.io/en/latest/reference/commands/shview.html),
since these generally won't work otherwise (at least not reliably or with full
performance).

- **Download and install the most recent 64-bit
  [MSYS2 installer](https://www.msys2.org/)** (the filename should be of the
  form `msys2-x86_64-*.exe`), and follow the installation instructions from
  the [MSYS2 wiki](https://www.msys2.org/wiki/MSYS2-installation/).

- **Start the ‘MinGW-w64 Win64 Shell’** from the start menu

- **Update the system packages**, as per the instructions for the
  [MSYS2 installer](https://www.msys2.org/):
  ```
  pacman -Syu
  ```
  Close the terminal, start a new ‘MinGW-w64 Win64 Shell’, and repeat as
  necessary until no further packages are updated.

  > **Note:** at time of writing, this MSYS2 system update may give a number of
  > instructions, including: terminating the terminal when the update is
  > completed, and modifying the shortcuts for executing the shell(s). Although
  > these instructions are not as prominent as they could be, it is vital that
  > they are followed correctly!


Managing MSYS packages with pacman
----------------------------------

Once installed, additional packages can be installed and managed using the
[pacman](https://www.archlinux.org/pacman/pacman.8.html) command that comes
bundled with MSYS2.  If you need to find out more about how to use the `pacman`
utility, there are plenty of resources available online, e.g. the 
[Arch Linux page](https://wiki.archlinux.org/index.php/pacman), or this 
[Lifewire tutorial](https://www.lifewire.com/using-the-pacman-package-manager-4018823).



Install MRtrix3
===============

- **Start the ‘MinGW-w64 Win64 Shell’** from the start menu

- **Download and install the latest MRtrix3 package**.  This can be
  accomplished by copy/pasting the following (rather long) one-line command
  into the terminal (use Shift-Insert to paste into the terminal):
  ```
  tag=$(basename $(curl -Ls -o /dev/null -w %{url_effective} https://github.com/MRtrix3/mrtrix3/releases/latest)) && curl -sL https://github.com/MRtrix3/mrtrix3/releases/download/${tag}/mingw-w64-x86_64-mrtrix3-${tag}-1-x86_64.pkg.tar.xz -O && pacman -U mingw-w64-x86_64-mrtrix3-${tag}-1-x86_64.pkg.tar.xz
  ```

  If necessary, this can also be done by downloading the package directly from 
  the [latest release page](https://github.com/MRtrix3/mrtrix3/releases/latest)
  on the [MRtrix3 GitHub repository](https://github.com/MRtrix3/mrtrix3) (the
  relevant file should be called `mingw-w64-x86_64-mrtrix3-X.Y.Z-1-x86_64.pkg.tar.xz`), and
  installing it using the `pacman -U` command (see links above for instructions
  on how to use `pacman`).

---

Upgrading *MRtrix3*
===================

To update, simply run the install procedure again.

