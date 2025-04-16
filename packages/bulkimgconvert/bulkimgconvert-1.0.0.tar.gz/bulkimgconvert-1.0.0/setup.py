from setuptools import setup, find_packages

setup(
    name="bulkimgconvert",  # Name of your package
    version="1.0.0",  # Version number
    description="A CLI tool to bulk convert and resize images",  # Short description of your tool
    long_description=open('README.md', encoding='utf-8').read(),  # Long description from your README file
    long_description_content_type="text/markdown",  # Ensure the description is treated as markdown
    author="Navneet Kaur",  # Your name
    author_email="navi24493@gmail.com",  # Your email address
    packages=find_packages(),  # Automatically finds packages in your project
    install_requires=[  # Dependencies
        "Pillow",  # Library for image processing
        "tqdm",  # Library for progress bars
    ],
    entry_points={  # Define command line tools
        'console_scripts': [
            'bulkimgconvert=bulkimgconvert.main:main',  # Calls the `main` function in `main.py` when `bulkimgconvert` is run in the CLI
        ],
    },
    license="MIT",  # Specify the license type
    classifiers=[  # Classify your package for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    include_package_data=True,  # To include any files defined in MANIFEST.in
    
)