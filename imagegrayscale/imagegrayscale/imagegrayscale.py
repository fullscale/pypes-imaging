import logging
import traceback
import Image
import ImageOps
from pypes.component import Component

log = logging.getLogger(__name__)

class ImageGrayscale(Component):

    __metatype__ = 'TRANSFORMER'

    def __init__(self):
        Component.__init__(self)
        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

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

                    # perform the gray scaling 
                    gray_image = ImageOps.grayscale(image)

                    # update the meta-data for the image
                    doc.set_meta('size', gray_image.size, 'image_data')
                    doc.set_meta('mode', gray_image.mode, 'image_data')

                    # update the image_data with the new serialized payload
                    doc.set('image_data', gray_image.tostring())

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

                # send the document to the next component
                self.send('out', doc)

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

