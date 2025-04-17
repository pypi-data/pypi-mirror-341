from setuptools import (
    find_packages,
    setup,
)

extras_require = {
    'linter': [
        'flake8==3.8.3',
    ],
    'dev': [
        'coincurve==13.0.0',
        'python-dotenv==0.13.0',
        'twine==3.1.1',
        'pytest==7.3.1',
        'mock==4.0.2',
    ],
}

extras_require['dev'] = extras_require['linter'] + extras_require['dev']

setup(
    name='sgx.py',
    version='0.10dev0',
    description='SGX',
    url='http://github.com/skalenetwork/sgx.py',
    author='SKALE Labs',
    author_email='support@skalelabs.com',
    install_requires=[
        'web3>=6.20.2,<8.0.0',
        'pyzmq==26.4.0',
        'pem==21.2.0',
        'M2Crypto>=0.40.1,<1.0.0',
        'urllib3==1.26.0',
    ],
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.7,<4',
    extras_require=extras_require,
    package_data={'sgx': ['generate.sh']},
)
