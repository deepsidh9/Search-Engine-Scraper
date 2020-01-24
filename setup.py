from setuptools import setup

setup(name='search_engine_scraper',
      version='0.1',
      description='A module to scrape popular search engines',
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
