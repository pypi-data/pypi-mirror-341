"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.util.env import Env
from iprm.util.dir import CurrentSourceDir, SourceDir, RootRelativeSourceDir, CurrentBinaryDir, BinaryDir, \
    RootRelativeBinaryDir
from iprm.project import Project, SubDir
from iprm.cxx import (CppExecutable, CppStaticLibrary, CppSharedLibrary, CppTest, CppPythonModule,
                      CppThirdParty, SourceArchiveBuilder, PrecompiledArchiveBuilder,
                      QtPrecompiledArchiveBuilder, GitBuilder, BoostThirdParty, QtThirdParty,
                      PyBind11ThirdParty, IcuThirdParty, GTestThirdParty)
from iprm.rust import RustExecutable
from iprm.core.typeflags import NONE, PROJECT, SUBDIR, CXX, THIRDPARTY, BOOST, QT, ICU, PYBIND11, GTEST, RUST, PYTHON

GENERAL_CATEGORY = {
    'General': [
        {Project.__name__: PROJECT},
        {SubDir.__name__: SUBDIR},
    ],
}
CPP_CATEGORY = {
    'C++': [
        {CppExecutable.__name__: CXX},
        {CppStaticLibrary.__name__: CXX},
        {CppSharedLibrary.__name__: CXX},
        {CppTest.__name__: CXX},
        {CppPythonModule.__name__: CXX | PYTHON},

        {CppThirdParty.__name__: THIRDPARTY| CXX },
        {BoostThirdParty.__name__: THIRDPARTY| CXX | BOOST},
        {QtThirdParty.__name__: THIRDPARTY| CXX | QT},
        {PyBind11ThirdParty.__name__: THIRDPARTY| CXX | PYBIND11},
        {IcuThirdParty.__name__: THIRDPARTY| CXX | ICU},
        {GTestThirdParty.__name__: THIRDPARTY| CXX | GTEST}
    ],
}
RUST_CATEGORY = {
    'Rust': [
        {RustExecutable.__name__: RUST},
    ],
}

OBJECT_CATEGORIES = {
    **GENERAL_CATEGORY,
    **CPP_CATEGORY,
    **RUST_CATEGORY,
}

UTILITY_CATEGORY = {
    'Utilities': [
        {Env.__name__: NONE},
        {CurrentSourceDir.__name__: NONE},
        {SourceDir.__name__: NONE},
        {RootRelativeSourceDir.__name__: NONE},
        {CurrentBinaryDir.__name__: NONE},
        {BinaryDir.__name__: NONE},
        {RootRelativeBinaryDir.__name__: NONE},
        {SourceArchiveBuilder.__name__: NONE},
        {PrecompiledArchiveBuilder.__name__: NONE},
        {GitBuilder.__name__: NONE},
    ],
}


NAMESPACE = {
    # Utilities
    Env.__name__: Env,
    CurrentSourceDir.__name__: CurrentSourceDir,
    SourceDir.__name__: SourceDir,
    RootRelativeSourceDir.__name__: RootRelativeSourceDir,
    CurrentBinaryDir.__name__: CurrentBinaryDir,
    BinaryDir.__name__: BinaryDir,
    RootRelativeBinaryDir.__name__: RootRelativeBinaryDir,
    SourceArchiveBuilder.__name__: SourceArchiveBuilder,
    PrecompiledArchiveBuilder.__name__: PrecompiledArchiveBuilder,
    QtPrecompiledArchiveBuilder.__name__: QtPrecompiledArchiveBuilder,
    GitBuilder.__name__: GitBuilder,

    # General
    Project.__name__: Project,
    SubDir.__name__: SubDir,

    # C++ Targets
    CppExecutable.__name__: CppExecutable,
    CppStaticLibrary.__name__: CppStaticLibrary,
    CppSharedLibrary.__name__: CppSharedLibrary,
    CppTest.__name__: CppTest,
    CppPythonModule.__name__: CppPythonModule,

    CppThirdParty.__name__: CppThirdParty,
    BoostThirdParty.__name__: BoostThirdParty,
    QtThirdParty.__name__: QtThirdParty,
    PyBind11ThirdParty.__name__: PyBind11ThirdParty,
    IcuThirdParty.__name__: IcuThirdParty,
    GTestThirdParty.__name__: GTestThirdParty,

    # Rust Targets
    RustExecutable.__name__: RustExecutable,
}
