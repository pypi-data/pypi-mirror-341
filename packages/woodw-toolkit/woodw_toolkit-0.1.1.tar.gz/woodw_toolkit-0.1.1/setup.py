from setuptools import setup, find_packages

setup(
    name='woodw-toolkit',
    version='0.1.1',
    description="It is a toolkit that includes various common operations and will continue to be improved in the future.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='jinghewang',
    author_email='jinghewang@163.com',
    license='MIT License',
    url='https://gitee.com/jinghewang/python-woodw-toolkit.git',
    packages=find_packages(),
    excluded_packages=['tests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[''],
    entry_points={
        'console_scripts': [''],
    },

)
