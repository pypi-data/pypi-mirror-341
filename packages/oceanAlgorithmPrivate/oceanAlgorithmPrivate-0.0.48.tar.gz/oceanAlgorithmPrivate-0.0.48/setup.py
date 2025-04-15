from setuptools import setup, find_packages

setup(
    name='oceanAlgorithmPrivate',
    version='0.0.48',
    description='PYPI ocean Algorithm private file written by Terry',
    author='taeung28',
    author_email='taeung28@gmail.com',
    url='https://www.linkedin.com/in/tae-ung-hwang-790014221/',
    install_requires=['boto3==1.36.00'
                    ,'botocore==1.36.00'
                    ,'contourpy==1.1.1'
                    ,'cycler==0.12.1'
                    ,'fonttools==4.53.0'
                    ,'importlib-resources==6.4.0'
                    ,'jmespath==1.0.1'
                    ,'joblib==1.4.2'
                    ,'kiwisolver==1.4.5'
                    ,'matplotlib==3.7.5'
                    ,'numpy==1.24.4'
                    ,'packaging==24.1'
                    ,'pandas==2.0.3'
                    ,'patsy==0.5.6'
                    ,'pillow==10.3.0'
                    ,'pyparsing==3.1.2'
                    ,'python-dateutil==2.9.0.post0'
                    ,'pytz==2024.1'
                    ,'s3transfer==0.11.0'
                    ,'scikit-learn==1.3.2'
                    ,'six==1.16.0'
                    ,'statsmodels==0.14.1'
                    ,'threadpoolctl==3.5.0'
                    ,'tzdata==2024.1'
                    ,'urllib3==1.26.20'
                    ,'zipp==3.19.2'
                    ,'logtos3==0.0.19'],
    packages=find_packages(exclude=[]),
    keywords=['terry', 'oceanAi', 'algorithm', 'private', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)