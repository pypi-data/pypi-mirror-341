if __name__ == '__main__':
    from setuptools import setup, find_packages

    setup(
        name='CB11002UNO',
        version='0.1.0',
        packages=find_packages(),
        description='Librería de métodos numéricos para sistemas de ecuaciones lineales y no lineales',
        author='Josep',
        author_email='cb11002@ues.edu.sv',
        url='https://github.com/josepb38/CB11002UNO',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.6',
        install_requires=[
            'numpy',
            'scipy'
        ]
    )
