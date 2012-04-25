import gst
import cv2


class Server:
	def __init__(self, host, pt=96, port=3000):
		self.pipeline = gst.Pipeline( "Server pipeline." )
		self.cam = gst.element_factory_make("videotestsrc") 
		self.coder = gst.element_factory_make("ffenc_h263")
		self.rtp = gst.element_factory_make("rtph263ppay")
		self.rtp.set_property("pt", pt)
		self.emitter = gst.element_factory_make("udpsink")
		self.emitter.set_property("port", port)
		self.emitter.set_property("host", host)

		self.pipline.add(self.cam, self.coder, self.rtp, self.emitter)		
		gst.element_link_many(self.cam, self.coder, self.rtp, self.emitter)
		
		
	def start(self):
		self.pipeline.set_state(gst.STATE_PLAYING)
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)

class Client:
	def __init__(self, movie_window, CAPSparams, port=3000):
		self.movie_window = movie_window
		self.pipeline = gst.Pipeline( "Client pipeline" )
		self.receiver = gst.element_factory_make( "udpsrc" )
		self.receiver.set_property( "port", port )
		self.receiver.set_property( "caps", gst.caps_from_string(CAPSparams) )
#		self.receiver.set_property( "caps", GST_STATIC_CAPS(CAPSparams) )
		self.rtp = gst.element_factory_make( "rtph263pdepay" )
		self.decoder = gst.element_factory_make( "ffdec_h263" )
		self.colorMatch = gst.element_factory_make( "ffmpegcolorspace" )
		self.videoscale = gst.element_factory_make( "videoscale" )
		self.sink = gst.element_factory_make( "autovideosink", "sink" )
		self.pipeline.add( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )
		gst.element_link_many( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )
		#self.pipeline = gst.parse_launch("udpsrc port=3000 ! "+CAPSparams+" ! rtph263pdepay ! ffdec_h263 ! ffmpegcolorspace ! videoscale ! autovideosink ")
		
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()

	def start(self):
		self.bus = self.pipeline.get_bus()
		self.bus.add_signal_watch()
		self.pipeline.set_state(gst.STATE_PLAYING)
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)
	def setMovieWindow(self, movie_window):
		self.movie_window = movie_window


