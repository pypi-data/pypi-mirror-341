from setuptools import setup, find_packages
#with open('./requirements.txt') as f:
#    requirements = f.read().splitlines()

classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CaliforniaVirtualCampusAPI',
  version='0.0.2',
  description='A simple API for the California Virtual Campus platform.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='https://github.com/rob-m1/california-virtual-campus-api',  
  author='Robert Meli',
  author_email='robertmeli1@outlook.com',
  classifiers=classifiers,
  keywords=['california virtual campus','web scraping', 'beautifulsoup', 'api', 'education', 'course scraping', 'student resources', 'college resources'], 
  package_dir={'': 'src'},
  packages=find_packages(where='src'),
  install_requires=[
    "Requests",
    "beautifulsoup4",
    "selenium",
    "setuptools",
    "textdistance"
], 
  project_urls={
        'Issue Tracker': 'https://github.com/rob-m1/california-virtual-campus-api/issues',
    }
)