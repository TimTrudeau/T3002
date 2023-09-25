from setuptools import find_packages, setup
setup(
    name='T3002',
    version="0.0",
    description="Interpreter for the NPD cycle tester robot",
    author="Tim Trudeau",
    author_email="tim.trudeau@assaabloy.com",
    platforms=["Raspberry Pi running Buster", 'Windows'],
    install_requires=['pyserial', 'pytest', 'gpiozero',  dearpygui],
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={'console_scripts': ['t3002=T3002_fixture:main']}
)
