from setuptools import setup, find_packages

setup(
    name="gst_calculator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "reportlab",
        "pandas",
        "openpyxl",
        # add more libraries if you use others
    ],
    author="Ayush Bisht",
    description="Indian GST Tax Calculator (New Regime)",
    include_package_data=True,
)
