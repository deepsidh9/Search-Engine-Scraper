from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='search_engine_scraper',
      version='0.4',
      description='A module to scrape popular search engines',
      long_description=long_description,
       long_description_content_type='text/markdown',
      url='https://github.com/deepsidh9/Search-Engine-Scraper',
      author='Deep Singh Dhillon',
      author_email='deep.barca@gmail.com',
      license='MIT',
      packages=['search_engine_scraper'],
      install_requires=[
          'requests',
          'lxml'
      ],
      include_package_data=True,
      package_data={'': ['search_engine_scraper/*.txt']},
      zip_safe=False)
