from distutils.core import setup
import os


setup(name='django-contact-form',
      version='1.0',
      description='Generic contact-form application for Django',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
      author='James Bennett',
      author_email='james@b-list.org',
      url='https://bitbucket.org/ubernostrum/django-contact-form/',
      packages=['contact_form', 'contact_form.tests'],
      download_url='http://bitbucket.org/ubernostrum/django-contact-form/downloads/django-contact-form-1.0.tar.gz', 
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Utilities'],
      )
