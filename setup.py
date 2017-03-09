from setuptools import setup, find_packages

setup(
    name='bencode_py3',
    packages=['bencode_py3'],
    version='1.1329139004',
    description="The BitTorrent bencode module as light-weight, standalone package, ported to Python 3",
    author="Josh Rodd",
    author_email="josh@rodd.us",
    license="BitTorrent Open Source License",
    keywords="bittorrent bencode bdecode python3 bencode_py3",
    url="https://github.com/JoshRodd/bencode_py3",
    download_url='https://github.com/JoshRodd/bencode_py3/archive/1.1329139004.tar.gz',
    test_suite="test.testbencode",
    long_description="""This package simply re-packages the existing bencoding and bdecoding implemention from the 'official' BitTorrent client as a separate, light-weight package for re-using them without having the entire BitTorrent software as a dependency, and then has been ported to Python 3.
""",
    zip_safe=True,
)
