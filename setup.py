import os

from setuptools import setup


setup(name='django-contact-form',
      version='1.5',
      zip_safe=False, # eggs are the devil.
      description='A generic contact-form application for Django',
      long_description=open(os.path.join(os.path.dirname(__file__),
                                         'README.rst')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='https://github.com/ubernostrum/django-contact-form/',
      packages=['contact_form', 'contact_form.tests'],
      test_suite='contact_form.runtests.run_tests',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Framework :: Django :: 1.11',
                   'Framework :: Django :: 2.0',
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
                   'Topic :: Utilities'],
      install_requires=[
          'Django>=1.11',
      ],
      extras_require={
          'akismet': ['akismet'],
      },
)
