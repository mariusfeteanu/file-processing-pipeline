from setuptools import setup, find_packages

setup(
    name='file_processing_pipeline',
    version='1.0.0',
    packages=find_packages(),
    test_suite='pytest',
    url='https://github.com/mariusfeteanu/file-processing-pipeline.git',
    author='Marius Feteanu',
    author_email='marius.feteanu@gmail.com',
    description='File Processing Pipeline',
    package_data={'file_processing_pipeline': ['schemas/*']},
    entry_points = {
        'console_scripts': ['file_processing_pipeline=file_processing_pipeline.cli:main'],
    }
)
