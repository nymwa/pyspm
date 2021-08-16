import setuptools

setuptools.setup(
        name = 'pyspm',
        version = '0.1.0',
        packages = setuptools.find_packages(),
        install_requires=[
                'tqdm',
                'sentencepiece',
                'pyyaml',
            ],
        entry_points = {
            'console_scripts':[
                'pyspm-train = pyspm.train:main',
                'pyspm-encode = pyspm.encode:main',
                'pyspm-decode = pyspm.decode:main',
                ]},)

