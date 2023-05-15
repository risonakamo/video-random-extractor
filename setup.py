from setuptools import setup,find_packages

setup(
    name="video_summarise",
    version="2.0.0",
    packages=find_packages(),

    python_requires=">=3.10",
    install_requires=[
        "opencv-python-headless",
        "loguru",
        "rich",
        "devtools",
        "pydantic"
    ]
)