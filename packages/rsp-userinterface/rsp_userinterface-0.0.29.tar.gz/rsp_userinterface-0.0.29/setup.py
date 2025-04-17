from setuptools import setup, find_packages

VERSION = '0.0.29' 
DESCRIPTION = 'An OpenCv-based frontend library'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="rsp-userinterface", 
        version=VERSION,
        author="Robert Schulz",
        author_email="schulzr256@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        package_dir={"rsp": "rsp"},
        license="MIT",
        packages=find_packages(),
        # needs to be installed along with your package. Eg: 'caer'
        url = "https://github.com/SchulzR97/rsp-userinterface",
        install_requires=[
            'rsp-common>=0.0.25',
            'numpy',
            'opencv-python'
        ], # add any additional packages that 
        keywords=['python', 'OpenCV', 'UI', 'UserInterface', 'Frontend'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",     
        ]
)