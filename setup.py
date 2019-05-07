import os

from setuptools import find_packages, setup


setup(name='django-contact-form',
      version='1.7',
      zip_safe=False, # eggs are the devil.
      description='A generic contact-form application for Django',
      long_description=open(os.path.join(os.path.dirname(__file__),
                                         'README.rst')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='https://github.com/ubernostrum/django-contact-form/',
      include_package_data=True,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Framework :: Django :: 1.11',
                   'Framework :: Django :: 2.0',
                   'Framework :: Django :: 2.1',
                   'Framework :: Django :: 2.2',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Utilities'],
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      install_requires=[
          'Django>=1.11',
      ],
      extras_require={
          'akismet': ['akismet'],
      },
)
