import gst

class Server:
	def __init__(self, host, pt=96, port=3000):
		self.pipeline = gst.pipeline( "Server pipeline." )
		self.cam = gst.element_factory_make("v4l2src") 
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
	def __init__(self, CAPSparams, port=3000):
		self.pipeline = gst.pipeline( "Client pipeline" )
		self.receiver = gst.element_factory_make( "udpsrc" )
		self.receiver.set_property( "port", port )
		self.receiver.set_property( "caps", CAPSparams )
		self.rtp = gst.element_factory_make( "rtph263pdepay" )
		self.decoder = gst.element_factory_make( "ffdec_h263" )
		self.colorMatch = gst.element_factory_make( "ffmpegcolorspace" )
		self.videoscale = gst.element_factory_make( "videoscale" )
		self.sink = gst.element_factory_make( "autovideosink" )
		
		self.pipeline.add( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )
		gst.element_link_many( self.receiver, self.rtp, self.decoder, self.colorMatch, self.videoscale, self.sink )

	def start(self):
		self.pipeline.set_state(gst.STATE_PLAYING)
	def stop(self):
		self.pipeline.set_state(gst.STATE_NULL)


