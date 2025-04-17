from setuptools import setup, find_packages

setup(
    name='SetAPI',  # Package name
    version='0.1',  # Initial version
    packages=find_packages(),
    description="A simple web framework in Python",  # Short description
    long_description="A simple web framework to help you set up your APIs.",
    long_description_content_type='text/markdown',
    author='Kayra Aça',  # Your name here
    author_email='kayraaca@gmail.com',  # Your email here
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)
