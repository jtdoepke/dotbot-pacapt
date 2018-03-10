import os
import platform
import subprocess

import dotbot


class Pacapt(dotbot.Plugin):
    """Install packages via pacapt."""
    _directive = 'pacapt'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        success = True
        system_name = get_system_short_name()
        packages_to_install = []
        for item in data:
            if isinstance(item, str):
                packages_to_install.append(item)
            elif isinstance(item, dict):
                if system_name in item:
                    item_packages = item[system_name]
                    if isinstance(item_packages, str):
                        item_packages = [item_packages]
                    packages_to_install += item_packages
            else:
                raise TypeError('Package does not understand {0!r}'.format(item))
        packages_to_install = list(sorted(set(packages_to_install)))

        executable = os.environ.get('SHELL')
        cmd = ' '.join(['sudo', _pacapt_path(), '-Sy'])
        self._log.lowinfo('Updating package cache(s) [%s]' % cmd)
        ret = subprocess.call(
            cmd,
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            cwd=self._context.base_directory(),
            executable=executable,
        )
        if ret != 0:
            success = False
            self._log.warning('Command [%s] failed' % cmd)
        cmd = ' '.join(['sudo', _pacapt_path(), '-S'] + packages_to_install)
        self._log.lowinfo('Installing %s [%s]' % (', '.join(packages_to_install), cmd))
        ret = subprocess.call(
            cmd,
            shell=True,
            stdin=None,
            stdout=None,
            stderr=None,
            cwd=self._context.base_directory(),
            executable=executable,
        )
        if ret != 0:
            success = False
            self._log.warning('Command [%s] failed' % cmd)
        if success:
            self._log.info('Packages were installed')
        else:
            self._log.error('Some commands were not successfully executed')
        return success


def _pacapt_path():
    here_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(here_dir, 'pacapt', 'pacapt')
    if not os.path.exists(path):
        raise Exception('%s not found. Submodule init?' % path)
    return path


def _maybe_read(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        return ''


DISTROS = {
    'Arch Linux': 'arch',
    'Ubuntu': 'ubuntu',
    'Debian': 'debian',
    'CentOS': 'centos',
    'Red Hat': 'redhat',
    'Alpine Linux': 'alpine',
    'Fedora': 'fedora',
}


def get_system_short_name():
    mac_ver = platform.mac_ver()[0]
    if mac_ver:
        return 'mac'

    distro = platform.linux_distribution()[0]
    if distro in DISTROS:
        return DISTROS[distro]

    issue = _maybe_read('/etc/issue').lower()
    release = _maybe_read('/etc/os-release').lower()

    for short_name, long_name in DISTROS:
        long_name = long_name.lower()
        if long_name in issue or long_name in release:
            return short_name
