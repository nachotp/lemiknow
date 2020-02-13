from setuptools import setup, find_packages
from io import open

setup(
    name='lemiknow',
    version='0.1.0',
    description='Let\'s you know when your function is called, ends or crashes',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nachotp/lemiknow',
    author='Ignacio Tampe',
    author_email='thenachotp@gmail.com',
    license='MIT',
    packages=find_packages(),
        entry_points={
            'console_scripts': [
                'lemiknow = lemiknow.__main__:main'
            ]
    },
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[
        'yagmail>=0.11.214',
        'keyring',
        'keyrings.alt==3.1.1',
        'matrix_client',
        'python-telegram-bot',
        'requests',
        'twilio'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
    ]
)
