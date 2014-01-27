from distutils.core import setup

setup(
    name='spoke',
    version='0.1',
    author='Ben Holzman',
    author_email='ben.holzman@axial.net',
    scripts=['spokec'],
    data_files=[('/etc/', ['spoke.cfg']),
                ('/etc/spoke/', []),
                ('/var/spoke/', [])],
    url='https://github.com/axialmarket/spoke',
    license='3-BSD',
    description='Spoke -- Reusable Front-End Components',
    long_description=open('./README.rst').read()
)
