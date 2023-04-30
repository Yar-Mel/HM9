from setuptools import setup
setup(
    name='command_line_interface',
    version='0.0.1',
    description='command line interface with 4 functions',
    url='https://github.com/Yar-Mel/HM9',
    author='Yaroslav Melnychuk',
    author_email='yarmel.dev@gmail.com',
    packages=['command_line_interface'],
    entry_points={'console_scripts': ['start-cli = command_line_interface.cli:main']}
)