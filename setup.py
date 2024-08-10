from setuptools import setup, find_packages

setup(
    name='BillboardMaker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            # Define command-line scripts here
            'billboardmaker=main.py',
        ],
    },
    include_package_data=True,
    package_data={
        # Include any package data files here
        '': ['*.json', '*.txt'],
    },
    author='Matyas Martan',
    author_email='maty.martan@gmail.com',
    description='A project for making billboards',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.fel.cvut.cz/martama1/manuboard.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux, Debian, Windows',
    ],
    python_requires='>=3.6',
)