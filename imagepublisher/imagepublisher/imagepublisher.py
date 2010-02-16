import logging
import traceback
import Image
import StringIO
from pypes.component import Component

log = logging.getLogger(__name__)

class ImageWriter(Component):

    __metatype__ = 'PUBLISHER'

    def __init__(self):
        Component.__init__(self)
        
        # remove the defaut outport port since this is a PUBLISHER
        self.remove_output('out')

        # create a runtime parameter for the user to specify an output filename 
        self.set_parameter('filename', 'pypes_converted_image')
        # runtime paraneter allowing user to choose an output format (defaults to JPEG)
        self.set_parameter('format', 'JPEG', ['JPEG', 'PNG', 'GIF', 'BMP', 'TIFF', 'EPS']) 

        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            # grab our runtime parameters
            filename = self.get_parameter('filename')
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

                    # attempt to save the image
                    with open(filename, 'w') as fp:
                        image.save(fp, format)

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

