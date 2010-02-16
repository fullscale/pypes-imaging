import logging
import traceback
import StringIO
import Image
from pypes.component import Component

log = logging.getLogger(__name__)

class ImageReader(Component):

    __metatype__ = 'ADAPTER'

    def __init__(self):
        Component.__init__(self)
        log.info('Component Initialized: %s' % self.__class__.__name__)

    def run(self):
        while True:

            # for each document waiting on our input port
            for doc in self.receive_all('in'):
                try:
                    # grab the raw content
                    data = doc.get('data', '')
                    # convert it to an Image object (see PIL API)
                    image = Image.open(StringIO.StringIO(data))
                    # serialize the object 
                    doc.set('image_data', image.tostring())
                    # set some meta-data about the image
                    doc.set_meta('size', image.size, 'image_data')
                    doc.set_meta('mode', image.mode, 'image_data')
                except Exception as e:
                    log.error('Component Failed: %s' % self.__class__.__name__)
                    log.error('Reason: %s' % str(e))                    
                    log.debug(traceback.print_exc())

                # send the document to the next component
                self.send('out', doc)

            # yield the CPU, allowing another component to run
            self.yield_ctrl()

