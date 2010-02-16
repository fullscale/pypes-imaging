"""This component is part of the pypes-imaging project.
It provides an adapter component based on the Python
Imaging Library (PIL).
"""

from setuptools import setup, find_packages

setup(
    name = 'imageadapter',
    version = '0.1.0',
    description = """A pypes adapter component that takes
    incoming image files and converts them to a format that 
    can be passed to other pypes imaging components using 
    the Python Imaging Library (PIL).
    """,
    author = "Eric Gaumer",
    author_email = "eric@diji.us.com",
    url = "http://diji.us.com",
    packages=find_packages(),
    entry_points="""
        [pypesvds.plugins] 
        imageadapter = imageadapter.imageadapter:ImageReader

        [distutils.setup_keywords]
        paster_plugins = setuptools.dist:assert_string_list
  
        [egg_info.writers]
        paster_plugins.txt = setuptools.command.egg_info:write_arg
    """,
    paster_plugins = ['studio_plugin']
)

