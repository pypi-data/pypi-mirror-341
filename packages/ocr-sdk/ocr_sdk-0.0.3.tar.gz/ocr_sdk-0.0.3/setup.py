import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocr_sdk",
    version="0.0.3",
    author="tianyishen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "ocr_sdk"},
    packages=setuptools.find_packages(where="ocr_sdk"),
    python_requires=">=3.11",
    install_requires=[
        'pillow==11.1.0',
        'numpy==1.26.4',
        'onnxruntime==1.21.0',
        'rapidocr-onnxruntime==1.3.25',
        'torch==2.6.0',
        'opencv-python==4.11.0.86',
        'opencv-python-headless==4.11.0.86',
    ]
)