import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usbmeter", 
    version="0.0.1",
    author="anfractuosity",
    description="Monitor USB power etc.",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=['pybluez','matplotlib','numpy'],
    package_dir={'usbmeter': 'usbmeter'},
    scripts=['usbmeter/usbmeter']
)
