from setuptools import setup, find_packages

setup(
    name='BA-NSGA',  # Package name
    version='0.0.2.2',
    description='A high-dimensional evolutionary structure explorer library',
    long_description=open('README.md', encoding='utf-8').read(),  # Ensure proper encoding for the README
    long_description_content_type='text/markdown',
    author='Juan Manuel Lombardi',
    author_email='lombardi@fhi-berlin.mpg.de',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license='MIT',
    install_requires=[
        'numpy>=1.20',          # Provides array manipulation and linear algebra
        'matplotlib>=3.4',       # For colormap and plotting functionalities
        'ase>=3.22.1',          # Atomic Simulation Environment for molecular dynamics and optimization
        'scipy>=1.5',           # For statistics, distances, and additional scientific computing
        'scikit-learn>=0.24',    # Provides PCA, regression, and other machine learning tools (este es el paquete "sklearn")
        'sage_lib>=0.1.5.33',
        'spglib'                # Library for crystal symmetry analysis
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'bansga = bansga.main:main',  # Command-line entry point; verify the module path is correct
        ],
    },
    keywords='evolutionary optimization high-dimensional structure explorer genetic algorithm',
    classifiers=[
        'Development Status :: 3 - Alpha',  # Update as your project matures
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
