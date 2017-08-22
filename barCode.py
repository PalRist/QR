# coding: utf-8
# Barcode scanner demo for Pythonista
# Based on http://www.infragistics.com/community/blogs/torrey-betts/archive/2013/10/10/scanning-barcodes-with-ios-7-objective-c.aspx

from objc_util import *
from ctypes import c_void_p
import ui
import sound
import console

found_codes = set()
main_view = None

AVCaptureSession = ObjCClass('AVCaptureSession')
AVCaptureDevice = ObjCClass('AVCaptureDevice')
AVCaptureDeviceInput = ObjCClass('AVCaptureDeviceInput')
AVCaptureMetadataOutput = ObjCClass('AVCaptureMetadataOutput')
AVCaptureVideoPreviewLayer = ObjCClass('AVCaptureVideoPreviewLayer')
dispatch_get_current_queue = c.dispatch_get_current_queue
dispatch_get_current_queue.restype = c_void_p

class PopOverView(ui.View, mode = 1):
	view_main = None
	view_po = None 

	def __init__(self):
		PopOverView.view_main = ui.load_view('pop-over')
		PopOverView.view_main.present('fullscreen')
		if mode == 1:
			PopOverView.view_po.present('Godkjenn 5S?',popover_location=(400,400))
		elif mode == 2:
			PopOverView.view_po.present('Hvordan vil du sende resultatene?',popover_location=(400,400))

		def quit(self, sender, mode):
		    def ask_user(sender, mode):
		    	if mode == 1:
			    	PopOverView.view_po.close()
			    	if sender.name == 'Ja':
			        	PopOverView.view_main.close()
			        	PopOverView(mode = 2)
			    	if sender.name == 'Nei':
			        	PopOverView.view_main.close()
		    	elif mode == 2:
			    	PopOverView.view_po.close()
			    	if sender.name == 'iMessage':
			        	PopOverView.view_main.close()
			        	newSMS()
			    	if sender.name == 'E-Mail':
			        	PopOverView.view_main.close()
			        	newSMS()


		    # PopOverView.view_po = ui.load_view('Nei')
    


# def menu():
# 	global menu_view
# 	menu_view = ui.View()                                      		# [1]
# 	menu_view.name = 'Menu'                                    		# [2]
# 	menu_view.background_color = 'white'                       		# [3]
# 	# QR-knapp
# 	button_QR = ui.Button(title='Scan QR-kode')           		# [4]
# 	button_QR.center = (menu_view.width * 0.5, menu_view.height * 0.25) 	# [5]
# 	button_QR.flex = 'LRTB'                                  	# [6]
# 	button_QR.action = main                               		# [7]
# 	menu_view.add_subview(button_QR)                              	# [8]
# 	# QR-knapp
# 	button_QR = ui.Button(title='Scan QR-kode')           		# [4]
# 	button_QR.center = (menu_view.width * 0.5, menu_view.height * 0.25) 	# [5]
# 	button_QR.flex = 'LRTB'                                  	# [6]
# 	button_QR.action = main                               		# [7]
# 	menu_view.add_subview(button_QR)                              	# [8]
# 	menu_view.present('sheet')                                 		# [9]

def captureOutput_didOutputMetadataObjects_fromConnection_(_self, _cmd, _output, _metadata_objects, _conn, session):
	objects = ObjCInstance(_metadata_objects)
	for obj in objects:
		s = str(obj.stringValue())
		if s not in found_codes:
			found_codes.add(s)
			sound.play_effect('digital:PowerUp7')
		main_view['label'].text = 'Last scan: ' + s
		PopOverView()

def newMail(text):
	console.alert('Ny mail', hide_cancel_button=True)

def newSMS(text):
	console.alert('Ny SMS', hide_cancel_button=True)

# def treatScan(found_codes):
# 	if found_codes:
# 		DoneScanning = console.alert('Vil du vurdere flere?' 'Ja', 'Nei', hide_cancel_button=True)
# 		if DoneScanning == 2:
# 			sendMethod = console.alert('Sende resultater','E-post','iMessage')
# 			mytext = found_codes
# 			if sendMethod == 1:
# 				newMail(mytext)
# 			elif sendMethod == 2:
# 				newSMS(mytext)
# 		elif DoneScanning == 1:
# 			main()
# 		print('All scanned codes:\n' + '\n'.join(found_codes))

# def button_tapped(sender):
#     sender.title = 'Hello'

# def confirmationUI(s):
# 	name = s
# 	view = ui.View()                                      # [1]
# 	view.name = 'Godkjenning'                                  # [2]
# 	view.background_color = 'white'                       # [3]
# 	nameLabel = ui.label(text='Vil du godkjenne {}s 5S?'.format(name))
# 	nameLabel.center = (view.width * 0.5, view.height * 0.1) # [5]
# 	btn_valid = ui.Button(title='5s-vurdering')              # [4]
# 	btn_valid.center = (view.width * 0.25, view.height * 0.5) # [5]
# 	btn_valid.flex = 'LRTB'                                  # [6]
# 	btn_valid.action = button_tapped                         # [7]
# 	view.add_subview(btn_valid)                              # [8]
# 	btn_invalid = ui.Button(title='5s-vurdering')              # [4]
# 	btn_invalid.center = (view.width * 0.75, view.height * 0.5) # [5]
# 	btn_invalid.flex = 'LRTB'                                  # [6]
# 	btn_invalid.action = button_tapped                         # [7]
# 	view.add_subview(btn_invalid)                              # [8]
# 	view.present('sheet')                                 # [9]


MetadataDelegate = create_objc_class('MetadataDelegate', methods=[captureOutput_didOutputMetadataObjects_fromConnection_], protocols=['AVCaptureMetadataOutputObjectsDelegate'])

@on_main_thread
def main():
	global main_view
	delegate = MetadataDelegate.new()
	main_view = ui.View(frame=(0,0,main_view.width, main_view.height))
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

	btn_valid = ui.Button(title='Godkjent')
	btn_valid.center = (view.width * 0.5, view.height * 0.4)
	btn_valid.flex = 'LRTB'                                  # [6]
	btn_valid.action = btn_valid_tapped 
	btn_valid.enabled = False
	main_view.add_subview(btn_valid)

	main_view.add_subview(label)

	session.startRunning()
	main_view.present('sheet')
	main_view.wait_modal()

	session.stopRunning()
	delegate.release()
	session.release()
	output.release()


def btn_valid_tapped(sender):
	print("Godkjent!")

if __name__ == '__main__':
	main()