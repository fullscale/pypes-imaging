"""This component is part of the pypes-imaging project.
It provides a publisher component based on the Python
Imaging Library (PIL).
"""

from setuptools import setup, find_packages

setup(
    name = 'imagepublisher',
    version = '0.1.0',
    description = """A pypes publishing component that uses the
    Python Imaging Library (PIL) to write image files to disk.
    """,
    author = "Eric Gaumer",
    author_email = "eric@diji.us.com",
    url = "http://diji.us.com",
    packages=find_packages(),
    entry_points="""
        [pypesvds.plugins] 
        imagepublisher = imagepublisher.imagepublisher:ImageWriter

        [distutils.setup_keywords]
        paster_plugins = setuptools.dist:assert_string_list
  
        [egg_info.writers]
        paster_plugins.txt = setuptools.command.egg_info:write_arg
    """,
    paster_plugins = ['studio_plugin']
)

