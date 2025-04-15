from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="num2words-BD-INR",
    version="0.1.0",
    author="Rifat Anwar",
    author_email="rifatanwarrobin@gmail.com",
    description="Convert numerical amounts to words with support for Indian and Bangladeshi currency formats/numberinc system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RifatAnwarRobin/num2words-BD-INR",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "num2words",
    ],
    keywords="INR, BD, num2words_bd_inr, amounttowords, num2words, amount, currency, words, conversion, indian, bangladeshi, taka, rupee, format, lakh, koti, crore, hazar, thousand",
)