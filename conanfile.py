#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
import os


class XercesCConan(ConanFile):
    name = "xerces-c"
    version = "3.2.2"
    description = "Xerces-C++ is a validating XML parser written in a portable subset of C++."

    topics = ("apache", "xml", "xerces")
    url = "https://github.com/midurk/conan-xerces-c"
    homepage = "http://xerces.apache.org/xerces-c/"
    author = "Michal Durkovic <michal.durkovic@innovatrics.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "libcurl/7.61.1@bincrafters/stable",
        "icu/63.1@bincrafters/stable"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "http://tux.rainside.sk/apache/xerces/c/3/sources"
        tools.get("{0}/{1}-{2}.tar.bz2".format(source_url, self.name, self.version), sha256="1f2a4d1dbd0086ce0f52b718ac0fa4af3dc1ce7a7ff73a581a05fbe78a82bce0")
        extracted_dir = self.name + "-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def _build_with_autotools(self):
        build_env = AutoToolsBuildEnvironment(self)
        build_env.fpic = self.options.fPIC
        with tools.environment_append(build_env.vars):
            with tools.chdir(self._source_subfolder):
                configure_args = ['--prefix=%s' % self.package_folder]
                configure_args.append('--enable-shared' if self.options.shared else '--disable-shared')
                configure_args.append('--enable-static' if not self.options.shared else '--disable-static')
                configure_args.append("--with-curl=%s" % self.deps_cpp_info["libcurl"].rootpath)
                configure_args.append("--with-icu=%s" % self.deps_cpp_info["icu"].rootpath)
                build_env.configure(args=configure_args)
                build_env.make(args=["-s", "all"])
                build_env.make(args=["-s", "install"])

    def build(self):
        self._build_with_autotools()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
