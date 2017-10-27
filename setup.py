import setuptools

setuptools.setup(
        install_requires=['pyyaml'],
        author = 'Caleb Boylan',
        name = 'libdolphin',
        description = 'Python library for interacting with Dolphin-emu and Super Smash Bros. Melee',
        author_email = 'calebboylan@gmail.com',
        url = 'https://github.com/squidboylan/libdolphin',
        version = '0.0.1',
        classifiers = [
            'License :: OSI Approved :: MIT',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
        ],
        packages=setuptools.find_packages(),
        entry_points = {
            'console_scripts': ['apt_package_mirror=apt_package_mirror.__main__:main'],
        }
)
