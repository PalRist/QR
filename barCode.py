# coding: utf-8
# Barcode scanner demo for Pythonista
# Based on http://www.infragistics.com/community/blogs/torrey-betts/archive/2013/10/10/scanning-barcodes-with-ios-7-objective-c.aspx
 
from objc_util import *
from ctypes import c_void_p
import ui
import sound
import email
import console
import clipboard

s = set()
main_view = None
 
AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureMetadataOutput = ObjCClass('AVCaptureMetadataOutput')
AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
dispatch_get_current_queue = c.dispatch_get_current_queue
dispatch_get_current_queue.restype = c_void_p
 
def captureOutput_didOutputMetadataObjects_fromConnection_(_self, _cmd, _output, _metadata_objects, _conn):
    objects = ObjCInstance(_metadata_objects)
    theCode = ''
    for obj in objects:
        s.add(str(obj.stringValue()))
        # theCode = str(obj.stringValue())
        # if s not in found_code:
        sound.play_effect('digital:PowerUp7')
    # main_view['label'].text = 'Last scan: ' + s
        main_view.close()
 
MetadataDelegate = create_objc_class('MetadataDelegate', methods=[captureOutput_didOutputMetadataObjects_fromConnection_], protocols=['AVCaptureMetadataOutputObjectsDelegate'])
 
@on_main_thread
def CodeScanner():
    global main_view
    delegate = MetadataDelegate.new()
    main_view = ui.View(frame=(0, 0, 400, 400))
    main_view.name = 'Barcode Scanner'
    session = AVCaptureSession.alloc().init()
    device = AVCaptureDevice.defaultDeviceWithMediaType_('vide')
    _input = AVCaptureDeviceInput.deviceInputWithDevice_error_(device, None)
    if _input:
        session.addInput_(_input)
    else:
        print('Failed to create input')
        return
    output = AVCaptureMetadataOutput.alloc().init()
    queue = ObjCInstance(dispatch_get_current_queue())
    output.setMetadataObjectsDelegate_queue_(delegate, queue)
    session.addOutput_(output)
    output.setMetadataObjectTypes_(output.availableMetadataObjectTypes())
    prev_layer = AVCaptureVideoPreviewLayer.layerWithSession_(session)
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
    return s

def newMail(mytext):
    for i in mytext:
        print(i, mytext[i])


def newSMS(mytext):
    for i in mytext:
        print(i, mytext[i])

def ContinueDialog(myResults, lastName):
    variable = console.alert('{} er ført.'.format(lastName), 'Vil du scanne flere?', 'Ja', 'Send resultater', hide_cancel_button=True)
    if variable == 1:
        main()

    elif variable == 2:
        transmit = console.alert('Sende resultater', 'Hvordan vil du sende resultatene?', 'iMessage', 'E-mail', 'Clipboard', hide_cancel_button=True)
        myString = '\n'.join(["{}, {}".format(key, value) for (key, value) in myResults.items()])
        if transmit == 1:
            newSMS(myString)
        elif transmit == 2:
            newMail(myString)
        elif transmit == 3:
            clipboard.set(myString)

def main():
    raw = CodeScanner()
    myScan = list(raw)[-1]
    scan = console.alert('{}'.format(myScan), 'Vil du godkjenne {}'.format(myScan), 'Ja', 'Nei', hide_cancel_button=True)

    if scan == 1:
        myResults[myScan] = 'Godkjent'
    elif scan == 2:
        myResults[myScan] = 'Ikke godkjent'

    ContinueDialog(myResults, myScan)

    return myResults

if __name__ == '__main__':
    myResults = dict()
    myResults = main()
    for i in myResults:
        print(i, myResults[i])
