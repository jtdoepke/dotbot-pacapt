# dotbot-pacapt
A [dotbot](https://github.com/anishathalye/dotbot) plugin to install packages using different package managers via [pacapt](https://github.com/icy/pacapt).

## Installation
```bash
$ git submodule add https://github.com/jtdoepke/dotbot-pacapt
```

Add the plugin dir to your install script.
```
--plugin-dir dotbot-pacapt/
```

## Example
Add a `packages` entry to your dotbot config:

```yaml
- packages:
   # Can just list packages that have a common name across package managers.
   - git
   - wget
   - curl
   - bzip2

   # Or list packages together as a reminder that they are equivalent.
   - ubuntu: build-essential
     fedora:
        - make
        - automake
        - gcc
        - gcc-c++
        - kernel-devel

   - ubuntu:
       - sqlite3
       - libsqlite3-dev
     fedora:
       - sqlite
       - sqlite-devel

   - ubuntu:
       - llvm
       - libncurses5-dev
       - libncursesw5-dev
       - tk-dev

   - ubuntu: libssl-dev
     fedora: openssl-devel

   - ubuntu: zlib1g-dev
     fedora: zlib-devel

   - ubuntu: libbz2-dev
     fedora: bzip2-devel

   - ubuntu: libreadline-dev
     fedora: readline-devel

   - ubuntu: xz-utils
     fedora:
       - xz
       - xz-devel
```
