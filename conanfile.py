from conans import ConanFile, AutoToolsBuildEnvironment
from conans import tools
import os


class B2sumConan(ConanFile):
    name = "b2sum_installer"
    version = "20190808"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "https://github.com/google/flatbuffers"
    topics = ("blake2", "blake2 generator", "hashing")
    author = "mjvk <>"
    description = ("b2sum is a program that can generate blake2 hashes")
    license = "MIT"
    settings = "compiler", "arch", "os_build", "arch_build"
    options = {"static_linkage":[True, False]}
    default_options = {"static_linkage":True}   
    
    def source(self):
        git = tools.Git(folder="blake2")
        git.clone("https://github.com/BLAKE2/BLAKE2.git","master")
        git.checkout("997fa5ba1e14b52c554fb03ce39e579e6f27b90c")
    
    def configure(self):
        if self.settings.compiler == "Visual Studio":
            raise Exception("Visual studio is not supported as a compiler as it misses some POSIX features, try mingw on windows!")
    
    def build(self):
        with tools.chdir(os.path.join("blake2","b2sum")):
            autotools = AutoToolsBuildEnvironment(self)
            env_build_vars = autotools.vars
            env_build_vars['CFLAGS'] = "-O3 -march=native "
            if self.options.static_linkage:
                env_build_vars['CFLAGS'] += " -static"
            autotools.make(vars=env_build_vars)


    def package(self):
        self.copy("*b2sum", dst="bin", keep_path=False)
        self.copy("*b2sum.exe", dst="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
        
    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()
    
    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))