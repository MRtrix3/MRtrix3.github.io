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

---


Instructions
============

- **Install and update MSYS2**

  Download and install the most recent 64-bit 
  [MSYS2 installer](http://msys2.github.io/) (the filename should be of the
  form `msys2-x86_64-*.exe`), and  following the installation instructions from
  the MSYS2 wiki.

- **Start the ‘MinGW-w64 Win64 Shell’** from the start menu

- **Update the system packages**, as per the instructions for the 
  [MSYS2 installer](http://msys2.github.io/):
  ```
  pacman -Syu
  ```
  Close the terminal, start a new ‘MinGW-w64 Win64 Shell’, and repeat as
  necessary until no further packages are updated.

  > **Note:** at time of writing, this MSYS2 system update will give a number of
  > instructions, including: terminating the terminal when the update is
  > completed, and modifying the shortcuts for executing the shell(s). Although
  > these instructions are not as prominent as they could be, it is vital that
  > they are followed correctly!

- **Add the *MRtrix3* repo as a software source.** This is done by adding these
  lines at the end of the `/etc/pacman.conf` file:
  ```
  [mrtrix3]
  SigLevel = Optional TrustAll
  Server = https://www.mrtrix.org/msys2
  ```
  This can be done in one go by copy/pasting this into the MSYS2 command-line:
  ```
  printf "\n[mrtrix3]\nSigLevel = Optional TrustAll\nServer = https://www.mrtrix.org/msys2\n" >> /etc/pacman.conf
  ```

- **Install *MRtrix3* using the MSYS2 package manager.** This is done using the
  `pacman` command:
  ```
  pacman -Syu mingw-w64-x86_64-mrtrix3 
  ```

---

Upgrading *MRtrix3*
===================

If you have already installed *MRtrix3* using the instructions above, your
system is configured to update it when you update the rest of your
installation. This is done using the `pacman` package manager:
```
pacman -Syu
```
This command will bring all your packages up to date, including the *MRtrix3*
ones.

If you need to find out more about how to use the `pacman` utility, there are
plenty of resources available online, e.g. the [Arch Linux
page](https://wiki.archlinux.org/index.php/pacman), or this
[Lifewire tutorial](https://www.lifewire.com/using-the-pacman-package-manager-4018823).

