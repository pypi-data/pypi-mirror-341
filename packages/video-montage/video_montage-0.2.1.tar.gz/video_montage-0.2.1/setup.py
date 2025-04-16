from pathlib import Path

from setuptools import find_packages, setup

VERSION = "0.2.1"
DESCRIPTION = "Easily create a video montage (either a sequence or a grid of videos)"
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="video_montage",
    version=VERSION,
    author="Tyler Lum",
    author_email="tylergwlum@gmail.com",
    url="https://github.com/tylerlum/video_montage",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["moviepy<2", "typed-argument-parser", "pillow<10"],
    keywords=["python", "video", "montage", "grid", "sequence"],
    entry_points={
        "console_scripts": [
            "video_grid_montage=video_montage.video_grid_montage:main",
            "video_sequence_montage=video_montage.video_sequence_montage:main",
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
