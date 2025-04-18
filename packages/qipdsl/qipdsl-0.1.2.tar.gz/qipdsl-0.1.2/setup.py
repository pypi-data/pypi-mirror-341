from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qipdsl',
    version='0.1.2',
    author='QIP-DSL Team',
    author_email='info@qipdsl.org',
    description='Quantum-Inspired Probabilistic Domain-Specific Language (CUDA-only)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qipdsl/qipdsl',
    packages=find_packages(),
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
