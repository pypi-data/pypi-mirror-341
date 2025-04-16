from setuptools import setup, find_packages

setup(
    name='de_sherlock',
    version='0.1.0',
    packages=find_packages(),  # Automatically finds Core, intilizer, etc.
    install_requires=[
        # Add dependencies here, for example:
        'pyyaml',
        'pandas'
    ],
    include_package_data=True,
    description='DE Sherlock - Data Engineering tracking and logging framework',
    author='Your Name',
    author_email='you@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
