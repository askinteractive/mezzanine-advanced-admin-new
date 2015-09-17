from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    authors=["Aymeric Bois","Xavier Amiot"],
    author_emails=["abois@askin.fr","xamiot@askin.fr"],
    name='mezzanine-advanced-admin',
    version='0.0.1',
    description='A Bootstrap theme for Django Mezzanine Admin with advanced features',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/abois/mezzanine-advanced-admin',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'setuptools',
        'Mezzanine>=4.0.1'
    ],
    test_suite='mezzanine_advanced_admin.runtests.runtests',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
