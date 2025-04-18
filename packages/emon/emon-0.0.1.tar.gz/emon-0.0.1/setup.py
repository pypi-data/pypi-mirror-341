from setuptools import setup, find_packages

setup(
    name='emon',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas', 'scikit-learn', 'tensorflow', 'joblib', 'seaborn', 'matplotlib', 'tqdm'
    ],
    author='ABS EMON',
    author_email='iotandrobotics@gmail.com',
    description='Easy AutoML package to clean, train and export models',
    url='https://github.com/ABS-EMON/emon',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
