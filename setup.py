from setuptools import setup, find_packages

setup(
    name='ThumbMR',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'vcsi',
        'ttkbootstrap',
        'numpy',
        'opencv-python',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'thumbmr=src.main:main',  # Adjust this line according to your main entry point
        ],
    },
)