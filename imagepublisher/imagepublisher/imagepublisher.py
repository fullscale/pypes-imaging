import logging
import traceback
import Image
import StringIO
import os.path
from pypes.component import Component

log = logging.getLogger(__name__)

class ImageWriter(Component):

    __metatype__ = 'PUBLISHER'

    def __init__(self):
        Component.__init__(self)
        
        # remove the defaut outport port since this is a PUBLISHER
        self.remove_output('out')

        # create a runtime parameter for the user to specify an output filename 
        self.set_parameter('output directory', '')
        # runtime paraneter allowing user to choose an output format (defaults to JPEG)
        self.set_parameter('format', 'JPEG', ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'EPS']) 

        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            # grab our runtime parameters
            out_dir = self.get_parameter('output directory')
            format = self.get_parameter('format')

            # for each document waiting on our input port
            for doc in self.receive_all('in'):
                try:
                    # grab the serialized image
                    raw_image = doc.get('image_data')

                    # grab the meta-data we need
                    size = doc.get_meta('size', 'image_data')
                    mode = doc.get_meta('mode', 'image_data')

                    # deserialize the image content
                    image = Image.fromstring(mode, size, raw_image)
               
                    # use the original file name of the image. if we can't 
                    # determine the original filename then just make one up 
                    fname = doc.get_meta('url', default='tmp_image.')
                        
                    # strip the extension and add the new one since we
                    # may have changed the format.
                    fname = '.'.join(fname.split('.')[:-1]) + '.' + format.lower()

                    file_path = os.path.join(out_dir, fname)

                    # attempt to save the image
                    with open(file_path, 'w') as fp:
                        image.save(fp, format)

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

