from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sgx-storage-client',
    version='0.0.5',
    author='Maksim',
    author_email='mpe@exan.tech',
    include_package_data=True,
    description='sgx storage client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests==2.32.3',
        'cryptography==44.0.2',
        'pycryptodome==3.22.0',
    ],
    python_requires='>=3.8',
    license='EULA',
    zip_safe=False,
    keywords='sgx security enclave dcap attestation',
    packages=find_packages(exclude=['docs', 'tests']),
)
