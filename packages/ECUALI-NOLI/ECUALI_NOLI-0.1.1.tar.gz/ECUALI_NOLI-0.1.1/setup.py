from setuptools import setup, find_packages

setup(
    name="ECUALI_NOLI",
    version="0.1.1",  # Incrementa la versión para cada nueva subida
    packages=find_packages(),  # Esto detectará automáticamente tu paquete
    description="Paquete para resolver ecuaciones lineales y no lineales",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Kenner Melgar",
    author_email="NM23016@ues.edu.sv",
    url='https://github.com/Kenner23016/ECUALI_NOLI',
    project_urls={
        'Source Code': 'https://github.com/Kenner23016/ECUALI_NOLI',
        'Bug Tracker': 'https://github.com/Kenner23016/ECUALI_NOLI/issues',
    },
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    python_requires='>=3.7',
    keywords='ecuaciones matemáticas algebra numerico',
)