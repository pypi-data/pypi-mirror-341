from setuptools import setup, find_packages

setup(
    name='ml_golem',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'file_golem',
        'torch',
        'accelerate',
        'tensorboard'
    ],
    # entry_points={
    #     'console_scripts': [
    #         'ml_lib_main = ml_lib.main:main',
    #     ],
    # },
    author='Your Name',
    author_email='your.email@example.com',
    description='A description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CameronBraunstein/ml_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)