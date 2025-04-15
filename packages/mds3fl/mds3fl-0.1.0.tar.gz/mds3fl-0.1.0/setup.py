from setuptools import setup, find_packages

setup(
    name='mds3fl',
    version='0.1.0',
    description='Federated Learning framework with CNN and image input',
    author='QZG',
    author_email='qxg88@case.edu',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.8.0',
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'Pillow'
    ],
    python_requires='>=3.7',
)