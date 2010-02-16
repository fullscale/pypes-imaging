import logging
import traceback
import Image
import ImageOps
from pypes.component import Component

log = logging.getLogger(__name__)

DEFAULT_RESOLUTION = (128, 128)

class ImageThumbnail(Component):

    __metatype__ = 'TRANSFORMER'

    def __init__(self):
        Component.__init__(self)
        
        self.set_parameter('size', '(128, 128)')
        self.set_parameter('filter', 'ANTIALIAS', ['ANTIALIAS', 'NEAREST', 'BILINEAR', 'BICUBIC'])

        self.filter_dict = {
            'ANTIALIAS': Image.ANTIALIAS,
            'NEAREST': Image.NEAREST,
            'BILINEAR': Image.BILINEAR,
            'BICUBIC': Image.BICUBIC
        }

        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            resolution = self.get_parameter('size')
            filter_type = self.get_parameter('filter')
            try:
                filter = self.filter_dict[filter_type]
            except:
                filter = Image.ANTIALIAS

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
                        resolution = eval(size)
                    except:
                        resolution = DEFAULT_RESOLUTION

                    # assume resolution is a 2 item tuple
                    # if it isn't, we'll land in the excpetion block below
                    image.thumbnail(resolution, filter)

                    # update the meta-data for the image
                    doc.set_meta('size', image.size, 'image_data')
                    doc.set_meta('mode', image.mode, 'image_data')

                    # update the image_data with the new serialized payload
                    doc.set('image_data', image.tostring())

                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

                # send the document to the next component
                self.send('out', doc)

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

