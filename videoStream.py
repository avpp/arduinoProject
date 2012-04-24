import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class Server:
	def __init__(self, host, pt=96, port=3000):
		self.pipeline = gst.Pipeline( "Server_pipeline." )
		self.cam = gst.element_factory_make("v4l2src") 
		self.coder = gst.element_factory_make("ffenc_h263")
		self.rtp = gst.element_factory_make("rtph263ppay")
		self.rtp.set_property("pt", pt)
		self.emitter = gst.element_factory_make("udpsink")
		self.emitter.set_property("port", port)
		self.emitter.set_property("host", host)

		self.pipeline.add(self.cam, self.coder, self.rtp, self.emitter)		
		gst.element_link_many(self.cam, self.coder, self.rtp, self.emitter)
		
		
	def start(self):
		self.pipeline.set_state(gst.STATE_PLAYING)
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)

class Client:
	def createWindow(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Webcam-Viewer")
		self.window.set_default_size(500, 400)
		self.window.connect("destroy", gtk.main_quit, "WM destroy")
		self.vbox = gtk.VBox()
		self.window.add(self.vbox)
		self.movie_window = gtk.DrawingArea()
		self.vbox.add(self.movie_window)
		self.hbox = gtk.HBox()
		self.vbox.pack_start(self.hbox, False)
		self.hbox.set_border_width(10)
		self.hbox.pack_start(gtk.Label())
		self.window.show_all()

	def __init__(self, CAPSparams='application/x-rtp,media=(string)video, clock-rate=(int)90000,encoding-name=(string)H263-1998, payload=(int)96,ssrc=(uint)2983818323, clock-base=(uint)2169357240,seqnum-base=(uint)49320', port=3000):
		self.pipeline = gst.Pipeline( "Client_pipeline" )
		self.receiver = gst.element_factory_make( "udpsrc" )
		self.receiver.set_property( "port", port )
		self.receiver.set_property( "caps", gst.caps_from_string(CAPSparams) )
		self.rtp = gst.element_factory_make( "rtph263pdepay" )
		self.decoder = gst.element_factory_make( "ffdec_h263" )
		self.colorMatch = gst.element_factory_make( "ffmpegcolorspace" )
		self.videoscale = gst.element_factory_make( "videoscale" )
		self.sink = gst.element_factory_make( "autovideosink" )
		
		self.pipeline.add( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )
		gst.element_link_many( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )

		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()


	def start(self):
		self.createWindow()
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()
		self.pipeline.set_state(gst.STATE_PLAYING)

	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)


