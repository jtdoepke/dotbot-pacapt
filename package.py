import platform
import sys

import dotbot


if sys.version_info >= (3, 3):
    from shutil import which as find_executable
else:
    from distutils.spawn import find_executable


class PackageInstaller(dotbot.Plugin):
    """Dotbot plugin to install packages via different package managers."""
    _directive = 'packages'

    def can_handle(self, action):
        return action == self._directive

    def handle(self, action, data):
        pass

    def detect_pacakage_manager(self):
        # Inspired by how https://github.com/icy/pacapt
        # detects the package manager.
        uname = platform.uname()

        if uname.system == 'SunOS':
            return SunTools

        issue = _maybe_read('/etc/issue').lower()
        release = _maybe_read('/etc/os-release').lower()

        for package_manager in PACKAGE_MANAGERS:
            system = package_manager.system_name.lower()
            if package_manager.get_executable() and (system in issue or system in release):
                return package_manager


def _maybe_read(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except IOError:
        return ''


class PackageManager(object):
    command_name = None
    system_name = None

    def __init__(self):
        if None in (self.command_name, self.system_name):
            raise ValueError('subclass must set command_name and system_name')

    def get_executable(self):
        return find_executable(self.command_name)

    def update_packages(self):
        raise NotImplementedError

    def install_packages(self, packages, noconfirm=True):
        raise NotImplementedError


class SunTools(PackageManager):
    command_name = 'sun_tools'
    system_name = 'SunOS'


class ArchLinux(PackageManager):
    command_name = 'pacman'
    system_name = 'Arch Linux'


class Debian(PackageManager):
    command_name = 'dpkg'
    system_name = 'Debian GNU/Linux'


class Ubuntu(PackageManager):
    command_name = 'dpkg'
    system_name = 'Ubuntu'


class ExherboLinux(PackageManager):
    command_name = 'cave'
    system_name = 'Exherbo Linux'


class CentOS(PackageManager):
    command_name = 'yum'
    system_name = 'CentOS'


class RedHat(PackageManager):
    command_name = 'yum'
    system_name = 'Red Hat'


class SUSE(PackageManager):
    command_name = 'zypper'
    system_name = 'SUSE'


class OpenBSD(PackageManager):
    command_name = 'pkg_tools'
    system_name = 'OpenBSD'


class Bitrig(PackageManager):
    command_name = 'pkg_tools'
    system_name = 'Bitrig'


class AlpineLinux(PackageManager):
    command_name = 'apk'
    system_name = 'Alpine Linux'



PACKAGE_MANAGERS = list(PackageManager.__subclasses__())
