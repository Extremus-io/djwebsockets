from distutils.core import setup

setup(
    name='djwebsockets',
    version='0.7',
    packages=['djwebsockets'],
    url='https://github.com/extremus-io/djwebsockets',
    requires=['websockets', 'asyncio'],
    license='BCD',
    author='kittu',
    author_email='kittuov@gmail.com',
    description='A django wrapper for websockets. for more info visit my GitHub page',
    long_description='''
The app is almost production ready. It lacks good documentation. But you can get started with tutorial at
http://github.com/extremus-io/djwebsockets
    ''',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3'
    ]
)
