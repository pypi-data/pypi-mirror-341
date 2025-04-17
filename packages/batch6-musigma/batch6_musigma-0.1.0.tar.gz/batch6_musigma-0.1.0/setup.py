from setuptools import setup, find_packages

setup(
    name='batch6-musigma',  # How the package will be listed on PyPI
    version='0.1.0',
    author='Bhargavesh Dakka',  # Replace with your name
    author_email='bhargaveshdakka@gmail.com',  # Replace with your email
    description='A Python package for Batch 6 Mu Sigma, potentially including Grok API chat functionality.',
    packages=find_packages(),
    license_files = "LICENSE",
    install_requires=[
        'groq>=0.4.0', # Use the official Groq SDK
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        # 'License :: OSI Approved :: MIT License', # Temporarily removed for testing
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    
)
