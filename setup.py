try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'pycsgoinfo parses data from demoinfogo and builds a coherent data resource from the resulting data.',
    'author': 'Ville Riikonen',
    'url': 'https://github.com/huqa/pycsgoinfo',
    'download_url': 'https://github.com/huqa/pycsgoinfo',
    'author_email': 'pikkuhukka@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pycsgoinfo'],
    'scripts': [],
    'name': 'pycsgoinfo'
}

setup(**config)
