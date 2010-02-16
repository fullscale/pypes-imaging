import logging
import traceback
import Image
import ImageOps
from pypes.component import Component

log = logging.getLogger(__name__)

DEFAULT_BORDER = 0

class ImageCrop(Component):

    __metatype__ = 'TRANSFORMER'

    def __init__(self):
        Component.__init__(self)

        # Create a runtime parameter allowing a border to be specified 
        self.set_parameter('border', '0')
        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            # get out user defined border
            border = self.get_parameter('border')

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
                        border = int(border)
                    except:
                        border = DEFAULT_BORDER
                    cropped_image = ImageOps.crop(image, border)

                    # update the meta-data for the image
                    doc.set_meta('size', cropped_image.size, 'image_data')
                    doc.set_meta('mode', cropped_image.mode, 'image_data')

                    # update the image_data with the new serialized payload
                    doc.set('image_data', cropped_image.tostring())

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

                # send the document to the next component
                self.send('out', doc)

            # yield the CPU
            self.yield_ctrl()

