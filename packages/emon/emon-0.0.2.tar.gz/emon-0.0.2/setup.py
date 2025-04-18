from setuptools import setup, find_namespace_packages

setup(
    name='emon',
    version='0.0.2',  # Increment version number
    packages=find_namespace_packages(include=['emon*']),
    include_package_data=True,  # Add this line
    package_data={'': ['*']},  # Add this line
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
