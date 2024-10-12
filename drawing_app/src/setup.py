from setuptools import setup, find_packages

setup(
    name='cross_platform_drawing_app',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'PySide6',
        'opencv-python',
        'numpy',
        'PyInstaller',
    ],
    entry_points={
        'console_scripts': [
            'drawing-app=src.main:main',
        ],
    },
)
