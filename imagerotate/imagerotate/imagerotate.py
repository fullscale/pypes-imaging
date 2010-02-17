import logging
import traceback
import Image
from pypes.component import Component

log = logging.getLogger(__name__)

DEFAULT_DEGREE = 0

class ImageRotate(Component):

    __metatype__ = 'TRANSFORMER'

    def __init__(self):
        Component.__init__(self)
        
        # create a runtime parameter to specify a degree of rotation
        self.set_parameter('degree', '0')
        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            degree = self.get_parameter('degree')

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

                    # perform the cropping using our user defined border
                    try:
                        degree = int(degree)
                    except:
                        degree = DEFAULT_DEGREE

                    rotated_image = image.rotate(degree)

                    # update the meta-data for the image
                    doc.set_meta('size', rotated_image.size, 'image_data')
                    doc.set_meta('mode', rotated_image.mode, 'image_data')

                    # update the image_data with the new serialized payload
                    doc.set('image_data', rotated_image.tostring())

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

                # send the document to the next component
                self.send('out', doc)

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

