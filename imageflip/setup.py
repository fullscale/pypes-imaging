"""This component is part of the pypes-imaging project.
It provides a transfomer component that allows images to
be flipped. It is based on the Python Imaging Library (PIL).
"""

from setuptools import setup, find_packages

setup(
    name = 'imageflip',
    version = '0.1.0',
    description = """A pypes tramsformer component that provides
    image flipping capabilities using PIL.
    """,
    author = "Eric Gaumer",
    author_email = "eric@diji.us.com",
    url = "http://diji.us.com",
    packages=find_packages(),
    entry_points="""
        [pypesvds.plugins] 
        imageflip = imageflip.imageflip:ImageFlip

        [distutils.setup_keywords]
        paster_plugins = setuptools.dist:assert_string_list
  
        [egg_info.writers]
        paster_plugins.txt = setuptools.command.egg_info:write_arg
    """,
    paster_plugins = ['studio_plugin']
)

