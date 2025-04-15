"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from enum import IntEnum
from typing import Optional
from abc import ABC, abstractmethod
from pathlib import Path

from iprm.target import Target
from iprm.core.typeflags import (CXX, PYTHON, STATIC, SHARED, EXECUTABLE, TEST, HEADER, GUI, THIRDPARTY, IMPORTED,
                                 PKGCONFIG, ARCHIVE, PRECOMPILED, SOURCE, GIT, VCPKG, CONAN, HOMEBREW, SYSTEM, DPKG,
                                 RPM, BOOST, QT, PYBIND11, ICU, GTEST, MSVC, CLANG, GCC, EMSCRIPTEN)
from iprm.util.dir import Dir, BinaryDir, RootRelativeBinaryDir
from iprm.util.env import Env
from iprm.util.platform import windows, macos, linux
from iprm.util.compiler import MSVC_COMPILER_NAME, CLANG_COMPILER_NAME, GCC_COMPILER_NAME, EMSCRIPTEN_COMPILER_NAME, \
    msvc, clang, gcc, emscripten


class MicrosoftCRuntime(IntEnum):
    STATIC = 1
    DYNAMIC = 2


class CppTarget(Target):
    STANDARD = 'standard'
    CONFORMANCE = 'conformance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= CXX
        self.hex_colour = '#3388CC'
        self.properties['headers']: dict[Dir, list[str]] = {}
        self.properties['sources']: dict[Dir, list[str]] = {}
        self.properties['libraries']: list[str] = []
        self.properties['patches']: dict[Dir, list[str]] = {}
        self.properties['defines']: list[str] = []
        self.properties['include_paths']: list[Dir] = []
        self.properties['runtime_files']: dict[Dir, list[str]] = {}
        self.properties['runtime_paths']: list[Dir] = []
        self._compiler_flag = CppTarget.default_compiler_flag()

    @classmethod
    def default_compiler_flag(cls):
        if Env.platform.windows:
            return MSVC
        elif Env.platform.macos:
            return CLANG
        elif Env.platform.linux:
            return GCC
        elif Env.platform.wasm:
            return EMSCRIPTEN
        return None

    @classmethod
    def default_compiler_name(cls):
        if Env.platform.windows:
            return MSVC_COMPILER_NAME
        elif Env.platform.macos:
            return CLANG_COMPILER_NAME
        elif Env.platform.linux:
            return GCC_COMPILER_NAME
        elif Env.platform.wasm:
            return EMSCRIPTEN_COMPILER_NAME
        return None

    @classmethod
    def default_language_properties(cls, **kwargs):
        defaults = {
            cls.STANDARD: '20',
            cls.CONFORMANCE: True,
        }
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return kwargs

    @property
    def compiler_flag(self):
        return self._compiler_flag

    @compiler_flag.setter
    def compiler_flag(self, flag):
        self._compiler_flag = flag

    def headers(self, header_dir: Dir, *headers):
        if header_dir not in self.properties['headers']:
            self.properties['headers'][header_dir] = []
        self.properties['headers'][header_dir].extend(headers)

    def sources(self, src_dir: Dir, *sources):
        if src_dir not in self.properties['sources']:
            self.properties['sources'][src_dir] = []
        self.properties['sources'][src_dir].extend(sources)

    # TODO: Don't assume the lirbaries are on the path or available at the system/compiler level. 
    #  Add a lib_dir parameter to ahndle this
    def libraries(self, *libraries):
        self.properties['libraries'].extend(libraries)

    # TODO: allow to explicitly declare if the defines or include paths are transitive (i.e. targets that
    #  depend on this target will implicitly get these too) or if they are private and only relevant to this target.
    #  Since they can be called multiple times, you can have sets of each property that are transitive, and sets that
    #  aren't

    def defines(self, *defines):
        self.properties['defines'].extend(defines)

    def include_paths(self, *paths: tuple[Dir]):
        self.properties['include_paths'].extend(paths)

    def patches(self, patch_dir: Dir, *patches):
        if patch_dir not in self.properties['patches']:
            self.properties['patches'][patch_dir] = []
        self.properties['patches'][patch_dir].extend(patches)

    def runtime_files(self, files_dir: Dir, *files):
        if files_dir not in self.properties['runtime_files']:
            self.properties['runtime_files'][files_dir] = []
        self.properties['runtime_files'][files_dir].extend(files)

    def runtime_paths(self, *paths: tuple[Dir]):
        self.properties['runtime_paths'].extend(paths)

    def static_crt(self):
        self.microsoft_crt(MicrosoftCRuntime.STATIC)

    def dynamic_crt(self):
        self.microsoft_crt(MicrosoftCRuntime.DYNAMIC)

    @msvc
    def microsoft_crt(self, crt: MicrosoftCRuntime):
        self.properties['microsoft_crt'] = crt

    def imported(self, **kwargs):
        self.properties['imported'] = kwargs

    def output_dir(self, output_dir: Dir):
        self.properties['output_dir'] = output_dir

    def qt(self, qt_lib: str):
        self.properties['qt_library'] = qt_lib
        self.requires(qt_lib, )
        self.type_flags |= QT

    def header(self):
        self.type_flags |= HEADER

    def executable(self):
        self.type_flags |= EXECUTABLE

    def static(self):
        self.type_flags |= STATIC

    def shared(self):
        self.type_flags |= SHARED

    def test(self):
        self.type_flags |= TEST

    def python(self):
        self.type_flags |= PYTHON


class CppExecutable(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diamond()
        self.executable()

    def gui(self):
        self.type_flags |= GUI


class CppStaticLibrary(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ellipse()
        self.static()


class CppSharedLibrary(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ellipse()
        self.shared()


class CppTest(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diamond()
        self.test()


class CppPythonModule(CppTarget):
    def __init__(self, *args, **kwargs):
        py_maj = kwargs.pop('maj')
        py_min = kwargs.pop('min')
        py_mod_lib = kwargs.pop('mod_lib')
        super().__init__(*args, **kwargs)
        self.properties['python_version_major'] = py_maj
        self.properties['python_version_minor'] = py_min
        self.properties['python_module_library'] = py_mod_lib
        self.requires(py_mod_lib, )
        self.suffix(self._get_py_module_suffix())
        self.python()

    @staticmethod
    def _get_py_module_suffix():
        import sysconfig
        ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
        if ext_suffix:
            return ext_suffix
        return None


# TODO: If a backend doesn't have native support for any of these third party library types, then implement it via a
#  custom command

class Builder(ABC):
    def __init__(self, third_party_target):
        self._target: CppThirdParty = third_party_target

    @abstractmethod
    def build(self):
        pass


class ArchiveBuilder(Builder):
    # TODO: provide a way to specify the archive needs to be fetched from a remote location.
    #  To implement this, just allow for this to be initialized with a URL instead of a local directory. The builder
    #  will also expose methods for user specifying authentication as well if required.
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target)
        self._target.properties['archive_dir'] = archive_dir
        self._target.properties['archive_file'] = archive_file
        self._unpack_target_name = f'{self._target.name}_unpack'
        self._unpack_artifacts: list[dict[str, str]] = []

    def build(self):
        self._target.properties['unpack_target_name'] = self._unpack_target_name
        self._target.properties['unpack_artifacts'] = self._unpack_artifacts


class SourceArchiveBuilder(ArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)

    def headers(self, header_dir: Dir, *headers):
        self._target.headers(header_dir, *headers)

    def sources(self, src_dir: Dir, *sources):
        self._target.sources(src_dir, *sources)

    def patches(self, patch_dir: Dir, *patches):
        self._target.patches(patch_dir, *patches)

    def static_crt(self):
        self._target.static_crt()

    def dynamic_crt(self):
        self._target.dynamic_crt()

    def include_paths(self, *paths: tuple[Dir]):
        self._target.include_paths(*paths)

    def header(self):
        self._target.header()

    def executable(self):
        self._target.executable()

    def static(self):
        self._target.static()

    def shared(self):
        self._target.shared()

    def qt(self, qt_lib: str):
        self._target.qt(qt_lib)


class PrecompiledArchiveBuilder(ArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)
        self._include_dir: Optional[Dir] = None
        self._implib_dir: Optional[Dir] = None
        self._lib_dir: Optional[Dir] = None
        self._bin_dir: Optional[Dir] = None
        self._shared_pattern_libraries: list[str] = []
        self._shared_libraries: list[str] = []
        self._static_pattern_libraries: list[str] = []
        self._static_libraries: list[str] = []
        self._include_pattern: Optional[Dir] = None
        self._release_pattern: Optional[str] = None
        self._debug_pattern: Optional[str] = None
        self._shared_lib_targets: list[CppSharedLibrary] = []
        self._static_lib_targets: list[CppStaticLibrary] = []
        self._auxiliary_apps: list[str] = []

    def include_dir(self, include_dir: Dir):
        self._include_dir = include_dir

    def implib_dir(self, implib_dir: Dir):
        self._implib_dir = implib_dir

    def lib_dir(self, lib_dir: Dir):
        self._lib_dir = lib_dir

    def bin_dir(self, bin_dir: Dir):
        self._bin_dir = bin_dir

    def shared_libs(self, *modules):
        self._shared_libraries.extend(modules)

    def shared_lib_pattern(self, **kwargs):
        self._shared_pattern_libraries.extend(kwargs.get('modules'))
        self._lib_pattern(**kwargs)

    # TODO: Support static_lib_pattern
    """
    def static_lib_pattern(self, **kwargs):
        self._static_pattern_libraries.extend(kwargs.get('modules'))
        self._lib_pattern(**kwargs)
    """

    def _lib_pattern(self, **kwargs):
        self._include_pattern = kwargs.get('include', None)
        self._release_pattern = kwargs.get('release')
        self._debug_pattern = kwargs.get('debug')

    # TODO: Add static_lib_explicit

    # TODO: For now these are implicitly relative to the bin dir, but we should allow for specifying apps that are in
    #  sub folders etc and remove this assumption
    def auxiliary_apps(self, *apps):
        self._auxiliary_apps.extend(apps)

    def build(self):
        pattern_lib_names = self._shared_pattern_libraries
        for lib_name in pattern_lib_names:
            lib_target_name = f'{self._target.name}_{lib_name}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | ARCHIVE | PRECOMPILED)
            lib_target.properties['unpack_target_name'] = self._unpack_target_name
            if self._include_pattern:
                dir_type = self._include_pattern.__class__
                lib_include_path = str(self._include_pattern.path)
                lib_include_path = lib_include_path.replace('%module%', lib_name)
                include_dir = dir_type(Path(lib_include_path))
                lib_target.include_paths(include_dir, )

            # TODO: Allow for the bin and implib names to have their own patterns (required for official
            #  precompiled ICU)
            lib_release_name = self._release_pattern.replace('%module%', lib_name)
            lib_debug_name = self._debug_pattern.replace('%module%', lib_name)
            bin_suffix = self._shared_lib_suffix()
            bin_suffix = '' if bin_suffix is None else bin_suffix
            imported_kwargs = {
                'lib_dir': self._lib_dir,
                'release_lib_file': f'{lib_release_name}{bin_suffix}',
                'debug_lib_file': f'{lib_debug_name}{bin_suffix}',
            }
            if self._implib_dir:
                imported_kwargs['implib_dir'] = self._implib_dir
                imported_kwargs['release_implib_file'] = f'{lib_release_name}.lib'
                imported_kwargs['debug_implib_file'] = f'{lib_debug_name}.lib'

            lib_target.type_flags |= IMPORTED
            lib_target.imported(**imported_kwargs)
            self._unpack_artifacts.append(imported_kwargs)
            self._target.requires(lib_target_name, )
            self._shared_lib_targets.append(lib_target)

        lib_names = self._shared_libraries
        for lib_name in lib_names:
            lib_target_name = f'{self._target.name}_{lib_name}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | ARCHIVE | PRECOMPILED)
            lib_target.properties['unpack_target_name'] = self._unpack_target_name

            # TODO: Allow for explicit libraries to distinguish between debug and release
            bin_suffix = self._shared_lib_suffix()
            bin_suffix = '' if bin_suffix is None else bin_suffix
            imported_kwargs = {
                'lib_dir': self._lib_dir,
                'release_lib_file': f'{lib_name}{bin_suffix}',
                'debug_lib_file': f'{lib_name}{bin_suffix}',
            }
            # TODO: Allow for explicit libraries to distinguish between debug and release
            if self._implib_dir:
                imported_kwargs['implib_dir'] = self._implib_dir
                imported_kwargs['release_implib_file'] = f'{lib_name}.lib'
                imported_kwargs['debug_implib_file'] = f'{lib_name}.lib'

            lib_target.type_flags |= IMPORTED
            lib_target.imported(**imported_kwargs)
            self._unpack_artifacts.append(imported_kwargs)
            self._target.requires(lib_target_name, )
            self._shared_lib_targets.append(lib_target)

        # TODO: Handle static libraries

        app_names = self._auxiliary_apps
        for app_name in app_names:
            imported_kwargs = {
                'bin_dir': self._bin_dir,
                'bin_file': f'{app_name}',
            }
            self._unpack_artifacts.append(imported_kwargs)
        super().build()
        if self._include_dir:
            self._target.include_paths(self._include_dir, )
            for target in self._shared_lib_targets:
                target.include_paths(self._include_dir, )

        return self._shared_lib_targets + self._static_lib_targets

    @staticmethod
    def _shared_lib_suffix():
        if Env.platform.windows:
            return '.dll'
        elif Env.platform.macos:
            # TODO: macOS can output a .so too, probably need the compiler context here too to
            #  know for sure what kind it will output (e.g. AppleClang vs GCC)
            return '.dylib'
        elif Env.platform.linux:
            return '.so'
        return None

    @staticmethod
    def _app_suffix():
        if Env.platform.windows:
            return '.exe'
        return ''

    @staticmethod
    def app_suffix():
        bin_suffix = PrecompiledArchiveBuilder._app_suffix()
        return '' if bin_suffix is None else bin_suffix


# TODO: Get rid of Git builder and just make this simple kwargs, only the archive types will have builders given they
#  are a bit more involved, but they could also switch away from that if we wanted
class GitBuilder(Builder):
    def __init__(self, third_party_target):
        super().__init__(third_party_target)
        self._repository: Optional[str] = None
        self._tag: Optional[str] = None

    def repository(self, repository: str):
        self._repository = repository

    def tag(self, tag: str):
        self._tag = tag

    def build(self) -> None:
        self._target.properties['git_clone_dir'] = RootRelativeBinaryDir('_git')
        # TODO: include_paths is not just for the targets transitive includes, it is possible to have include paths
        #  outside of the target. We'll probably be fine here for now given this is for a third party target only,
        #  but this should still get cleaned up/improved
        include_paths = self._target.properties.get('include_paths', [])
        for include_dir in include_paths:
            include_dir.prepend('_git')
        source_files = self._target.properties.get('sources', {})
        for src_dir, src_files in source_files.items():
            src_dir.prepend('_git')

        self._target.properties['git_repository'] = self._repository
        self._target.properties['git_tag'] = self._tag


class CppThirdParty(CppTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= THIRDPARTY

    def source_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | SOURCE)
        return SourceArchiveBuilder(self, archive_dir, archive_file)

    def precompiled_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | PRECOMPILED)
        return PrecompiledArchiveBuilder(self, archive_dir, archive_file)

    def git(self):
        self.type_flags |= GIT
        return GitBuilder(self)

    def vcpkg(self, manifest_dir: Dir):
        # TODO: specify required vcpkg stuff here, ensure to only support the latest/modern way of doing things (I
        #  think that is some manifest stuff?)
        # TODO: For now, actually just make vcpkg (and probably conan too) a project wide thing, where one maps their
        #  names to targets (that will be ContainerTarget's) that first party targets can then depend on
        self.type_flags |= VCPKG
        self.properties['manifest'] = manifest_dir,

    def conan(self):
        # TODO: specify required conan stuff here
        self.type_flags |= CONAN

    @macos
    @linux
    def homebrew(self, **kwargs):
        self.type_flags |= HOMEBREW
        package = kwargs.get('package')
        self.properties['homebrew_package'] = package
        libs = kwargs.get('shared_libs')
        for lib in libs:
            lib_target_name = f'{self.name}_{lib}'
            brew_target_name = f'{self.name}_brew'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | HOMEBREW | IMPORTED)
            lib_target.properties['homebrew_lib'] = lib
            lib_target.properties['homebrew_target'] = brew_target_name
            self.requires(lib_target_name, )
        self.properties['homebrew_libs'] = libs

    # TODO: Technically Windows supports pkg-config, but keep going to keep it to unix only for now
    @macos
    @linux
    def pkgconfig(self, **kwargs):
        # TODO: Some backend (e.g. CMake AND Meson) have native support for this, so this impl will be relatively clean
        # NOTE: Use the freedesktop.svg logo for this int he target properties view
        # NOTE: Windows technically supports this too, when adding tests for it, ensure it is something simple that can
        # be easily done on all platforms, or if not create platform-specific versions of the target that rely on
        # basic/simple packages each platform always has available by default
        self.type_flags |= PKGCONFIG
        prefix = kwargs.get('prefix', None)
        libs = kwargs.get('shared_libs')
        modules = []
        imported_targets = []
        for lib in libs:
            module = lib.removeprefix(prefix) if prefix else lib
            modules.append(module)
            lib_target_name = f'{self.name}_{module}'
            lib_target = CppSharedLibrary(lib_target_name)
            lib_target.type_flags |= (THIRDPARTY | PKGCONFIG | IMPORTED)
            lib_target.properties['pkconfig_module'] = f'{self.name.upper()}_{module.upper()}'
            lib_target.properties['pkconfig_lib'] = lib
            self.requires(lib_target_name, )
            imported_targets.append(lib_target)
        self.properties['pkconfig_modules'] = modules
        return imported_targets

    @linux
    def dpkg(self, **kwargs):
        self.type_flags |= (SYSTEM | DPKG)
        self.properties['dpkg_package'] = kwargs.get('package')

    def rpm(self, **kwargs):
        self.type_flags |= (SYSTEM | RPM)
        self.properties['rpm_package'] = kwargs.get('package')


class BoostThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= BOOST
        self.hex_colour = '#FF9F00'


class QtPrecompiledArchiveBuilder(PrecompiledArchiveBuilder):
    def __init__(self, third_party_target, archive_dir: Dir, archive_file: str):
        super().__init__(third_party_target, archive_dir, archive_file)
        self._modules: list[str] = []
        self._lib_type: str = ''

    def shared_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'shared'

    def static_lib_pattern(self, **kwargs):
        super()._lib_pattern(**kwargs)
        self._lib_type = 'static'

    # TODO: Add ability to customize the actual module name for each Qt core in case of custom Qt build that deviates
    #  from Qts naming conventions here

    def core(self):
        self._module('Core')

    def gui(self):
        self._module('Gui')

    def widgets(self):
        self._module('Widgets')

    def svg(self):
        self._module('Svg')

    def svgwidgets(self):
        self._module('SvgWidgets')

    # TODO: Add remaining modules when needed

    def _module(self, name):
        if self._lib_type == 'shared':
            self._shared_pattern_libraries.append(name)
        elif self._lib_type == 'static':
            self._static_pattern_libraries.append(name)

    def moc(self):
        self._auxiliary_apps.append(f'moc{self.app_suffix()}')

    def rcc(self):
        self._auxiliary_apps.append(f'rcc{self.app_suffix()}')

    def uic(self):
        self._auxiliary_apps.append(f'uic{self.app_suffix()}')

    def build(self):
        targets = super().build()
        for target in targets:
            target.type_flags |= QT
            target.hex_colour = '#41CD52'
            target.rectangle()
        self._target.properties['bin_dir'] = self._bin_dir
        return targets


class QtThirdParty(CppThirdParty):
    MOC = 'moc'
    RCC = 'rcc'
    UIC = 'uic'
    CONF = 'conf'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= QT
        self.hex_colour = '#41CD52'

    @macos
    @linux
    def pkgconfig(self, **kwargs):
        imported_targets = super().pkgconfig(**kwargs)
        for target in imported_targets:
            target.type_flags |= QT
            target.hex_colour = self.hex_colour
        return imported_targets

    def precompiled_archive(self, archive_dir: Dir, archive_file: str):
        self.type_flags |= (ARCHIVE | PRECOMPILED)
        return QtPrecompiledArchiveBuilder(self, archive_dir, archive_file)

    def moc(self):
        self.properties[QtThirdParty.MOC] = True

    def rcc(self):
        self.properties[QtThirdParty.RCC] = True

    def uic(self):
        self.properties[QtThirdParty.UIC] = True

    def conf(self):
        self.properties[QtThirdParty.CONF] = True


# https://github.com/pybind/pybind11
class PyBind11ThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= (PYTHON | PYBIND11)
        self.hex_colour = '#738AFF'
        self.header()
        self.include_paths(
            BinaryDir('include'),
        )


class IcuThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= ICU
        self.hex_colour = '#5555FF'


# TODO: Add OpenSSL, SQLite, and GraphViz as other key/known/registered 3rd party libraries given their popularity

# https://github.com/google/googletest
class GTestThirdParty(CppThirdParty):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_flags |= GTEST
        self.hex_colour = '#4285F4'
        self.static()
        self.include_paths(
            BinaryDir('googletest'),
            BinaryDir('googletest', 'include'),
            BinaryDir('googlemock'),
            BinaryDir('googlemock', 'include'),
        )
        self.sources(
            BinaryDir('googletest', 'src'),
            'gtest-all.cc',
        )
        self.sources(
            BinaryDir('googlemock', 'src'),
            'gmock-all.cc',
        )


# TODO: Add other popular/standard 3rd party C++ test libraries (e.g. Catch2)
