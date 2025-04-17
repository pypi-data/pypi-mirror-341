from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import subprocess

class build_ext_custom(build_ext):
    def run(self):
        # Compile the .so file
        subprocess.check_call(["emcc", "compdismatter/wasm/ising.c", "-s", "SIDE_MODULE=2", "-O3", "-o", "compdismatter/wasm/ising.wasm"])
        
        # Compile the shared object (.so) for native use
        subprocess.check_call(["gcc", "-shared", "-o", "compdismatter/lib/ising.so", "compdismatter/wasm/ising.c"])

        # Proceed with the default build process
        super().run()

setup(
    name="compdismatter",
    version="0.1.0",
    packages=["compdismatter"],
    ext_modules=[Extension("ising", sources=["compdismatter/wasm/ising.c"])],
    cmdclass={"build_ext": build_ext_custom},
    include_package_data=True,
    package_data={
        'compdismatter': [
            'wasm/*.wasm',  # include the wasm file
            'lib/*.so',     # include the .so file
        ],
    },
    install_requires=[
        # Add any dependencies your package might have
    ],
)
