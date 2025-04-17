import io
from setuptools import setup
from tilebatch import __version__


def README():
    with io.open('README.md', encoding='utf-8') as f:
        readme_lines = f.readlines()

    return ''.join(readme_lines)
README = README()  # NOQA

setup(
    name='emtilebatch',
    version=f'{__version__}',
    description='Python package of the EM data Tile Batch script',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/mpicbg-scicomp',
    author='HongKee Moon',
    author_email='moon@mpi-cbg.de',
    license='BSD',
    packages=['tilebatch' ],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
