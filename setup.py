from setuptools import setup, find_packages

setup(
    name='android_keystore',
    version='0.1.0',
    url='https://github.com/coint-hub/android-keystore',
    author='Coint',
    author_email='sm.park@coint.co.kr',
    description='android keystore helper',
    packages=['android_keystore'],
    install_requires=["click >= 8.0", "random-password-generator >= 2.1.2"],
    scripts=['bin/android-keystore']
)
