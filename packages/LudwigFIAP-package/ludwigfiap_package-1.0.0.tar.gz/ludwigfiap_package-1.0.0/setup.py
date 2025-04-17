from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='LudwigFIAP-package',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib LudwigFIAP',
    author='Leandro Ludwig',
    author_email='leandro.ludwig@live.com',
    url='https://github.com/LeLudwig18/LudwigFIAP',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
