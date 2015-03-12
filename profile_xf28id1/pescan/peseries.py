#!/usr/bin/env python

# TODO: some error checking to make sure detector is connected
# and property initialized

class PESeries(object):
    """Execute a series of PE scans with optional background scans.

    """

    WAIT_TIME = 0.01

    def __init__(self, detector, shutter):
        self.detector = detector
        self.detector.tiff1.auto_increment.put(1)
        self.detector.image_mode.put(self.detector.ImageMode.MULTIPLE)
        self.shutter = shutter
        return


    @property
    def exposuretime(self):
        return self.detector.acquire_time.get()


    @exposuretime.setter
    def exposuretime(self, value):
        self.detector.acquire_time.put(value)
        return


    @property
    def filepath(self):
        return self.detector.tiff1.file_path.get()


    # TODO: check that path is valid
    @filepath.setter
    def filepath(self, path):
        self.detector.tiff1.file_path.put(path)
        return


    @property
    def filecounter(self):
        return self.detector.tiff1.file_number.get()


    @filecounter.setter
    def filecounter(self, value):
        self.detector.tiff1.file_number.put(value)
        return


    def reset_filecounter(self):
        self.filecounter = 0
        return


    def single(self, filename, exposuretime, repeats):
        import time
        self.exposuretime = exposuretime
        darkfile = ''.join([filename, '_dark'])
        for r in range(repeats):
            # take dark current
            self.shutter.closeShutter()
            if not self.shutter.shutterStatus:
                time.sleep(1.0)
                self.detector.tiff1.file_name.put(darkfile)
                self.detector.acquire.put(1)
                while (self.detector.detector_state.value == 1 \
                        and self.detector.acquire.value == 1):
                    time.sleep(self.WAIT_TIME)
            self.shutter.openShutter()
            if self.shutter.shutterStatus:
                time.sleep(1.0)
                self.detector.tiff1.file_name.put(filename)
                self.detector.acquire.put(1)
                while (self.detector.detector_state.value == 1 \
                        and self.detector.acquire.value == 1):
                    time.sleep(self.WAIT_TIME)
        return
