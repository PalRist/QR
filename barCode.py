# coding: utf-8
# Barcode scanner demo for Pythonista
# Based on http://www.infragistics.com/community/blogs/torrey-betts/archive/2013/10/10/scanning-barcodes-with-ios-7-objective-c.aspx

from objc_util import *
from ctypes import c_void_p
import ui
import sound

class QRscanner(self):
    self.found_codes = set()   
    self.main_view = None
    self.AVCaptureSession = ObjCClass('AVCaptureSession')
    self.AVCaptureDevice = ObjCClass('AVCaptureDevice')
    self.AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
    self.AVCaptureMetadataOutput = ObjCClass('AVCaptureMetadataOutput')
    self.AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
    self.dispatch_get_current_queue = c.dispatch_get_current_queue
    self.dispatch_get_current_queue.restype = c_void_p


    def captureOutput_didOutputMetadataObjects_fromConnection_(_self, _cmd, _output, _metadata_objects, _conn):
        objects = ObjCInstance(_metadata_objects)
        for obj in objects:
            s = str(obj.stringValue())
            if s not in self.found_codes:
                self.found_codes.add(s)
                sound.play_effect('digital:PowerUp7')
            self.main_view['label'].text = 'Last scan: ' + s

    self.MetadataDelegate = create_objc_class('MetadataDelegate', methods=[captureOutput_didOutputMetadataObjects_fromConnection_], protocols=['AVCaptureMetadataOutputObjectsDelegate'])

    @on_main_thread
    def main(self):
        global main_view
        delegate = self.MetadataDelegate.new()
        self.main_view = ui.View(frame=(0, 0, 400, 400))
        self.main_view.name = 'Barcode Scanner'
        session = self.AVCaptureSession.alloc().init()
        device = self.AVCaptureDevice.defaultDeviceWithMediaType_('vide')
        _input = self.AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
        if _input:
            session.addInput_(_input)
        else:
            print('Failed to create input')
            return
        output = self.AVCaptureMetadataOutput.alloc().init()
        queue = ObjCInstance(self.dispatch_get_current_queue())
        output.setMetadataObjectsDelegate_queue_(delegate, queue)
        session.addOutput_(output)
        output.setMetadataObjectTypes_(output.availableMetadataObjectTypes())
        prev_layer = self.AVCaptureVideoPreviewLayer.layerWithSession_(session)
        prev_layer.frame = ObjCInstance(main_view).bounds()
        prev_layer.setVideoGravity_('AVLayerVideoGravityResizeAspectFill')
        ObjCInstance(main_view).layer().addSublayer_(prev_layer)
        label = ui.Label(frame=(0, 0, 400, 30), flex='W', name='label')
        label.background_color = (0, 0, 0, 0.5)
        label.text_color = 'white'
        label.text = 'Nothing scanned yet'
        label.alignment = ui.ALIGN_CENTER
        main_view.add_subview(label)
        session.startRunning()
        main_view.present('sheet')
        main_view.wait_modal()
        session.stopRunning()
        delegate.release()
        session.release()
        output.release()
        if found_codes:
            print('All scanned codes:\n' + '\n'.join(found_codes))

if __name__ == '__main__':
    QRscanner.main()