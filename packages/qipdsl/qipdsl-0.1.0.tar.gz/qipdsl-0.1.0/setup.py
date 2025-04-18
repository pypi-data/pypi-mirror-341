import os
import sys
import subprocess
import platform
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

# Force CUDA-only mode
os.environ['QIPDSL_USE_CUDA'] = '1'
os.environ['QIPDSL_DISABLE_CPU'] = '1'

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the extension")

        # Check CUDA
        try:
            subprocess.check_call(['nvcc', '--version'])
        except (OSError, subprocess.SubprocessError):
            raise RuntimeError("CUDA is required for this CUDA-only package")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}',
            '-DBUILD_PYTHON_BINDINGS=ON',
            '-DBUILD_BENCHMARKS=OFF',
            '-DBUILD_EXAMPLES=OFF',
            '-DQIPDSL_USE_CUDA=ON',
            '-DQIPDSL_DISABLE_CPU=ON',
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]
        cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']
        
        if platform.system() == "Windows":
            build_args += ['--', '/m']
        else:
            build_args += ['--', '-j', str(os.cpu_count() or 2)]

        os.makedirs(self.build_temp, exist_ok=True)
        
        try:
            subprocess.check_call(
                ['cmake', ext.sourcedir] + cmake_args, 
                cwd=self.build_temp
            )
            subprocess.check_call(
                ['cmake', '--build', '.'] + build_args, 
                cwd=self.build_temp
            )
        except subprocess.CalledProcessError as e:
            print(f"CMake build failed with error: {e}")
            if os.path.exists(os.path.join(self.build_temp, 'CMakeFiles', 'CMakeError.log')):
                with open(os.path.join(self.build_temp, 'CMakeFiles', 'CMakeError.log'), 'r') as f:
                    print("CMake Error Log:")
                    print(f.read())
            raise

with open("README.CUDA-ONLY.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qipdsl',
    version='0.1.0',
    author='QIP-DSL Team',
    author_email='info@qipdsl.org',
    description='Quantum-Inspired Probabilistic Domain-Specific Language (CUDA-only)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qipdsl/qipdsl',
    packages=find_packages(),
    ext_modules=[CMakeExtension('qipdsl')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.0',
        'matplotlib>=3.3.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
    ],
    keywords='quantum, matrix, optimization, probabilistic, dsl, cuda, gpu',
)
