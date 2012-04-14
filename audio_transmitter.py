#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Audio Transmitter
# Generated: Thu Apr 12 21:11:33 2012
##################################################

from gnuradio import audio
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import vocoder
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser

class audio_transmitter(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Audio Transmitter")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 125000
		self.audio_rate = audio_rate = 8000

		##################################################
		# Blocks
		##################################################
		self.vocoder_cvsd_encode_fb_0 = vocoder.cvsd_encode_fb(2,0.5)
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		self.uhd_usrp_sink_0.set_center_freq(915e6, 0)
		self.uhd_usrp_sink_0.set_gain(30, 0)
		self.digital_gmsk_mod_0 = digital.gmsk_mod(
			samples_per_symbol=2,
			bt=0.35,
			verbose=False,
			log=False,
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
				samples_per_symbol=2,
				bits_per_symbol=1,
				access_code="",
				pad_for_usrp=True,
			),
			payload_length=0,
		)
		self.audio_source_0 = audio.source(audio_rate, "plughw:0,0", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.vocoder_cvsd_encode_fb_0, 0), (self.blks2_packet_encoder_0, 0))
		self.connect((self.audio_source_0, 0), (self.vocoder_cvsd_encode_fb_0, 0))
		self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_0, 0))
		self.connect((self.digital_gmsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

	def get_audio_rate(self):
		return self.audio_rate

	def set_audio_rate(self, audio_rate):
		self.audio_rate = audio_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = audio_transmitter()
	tb.start()
	raw_input('Press Enter to quit: ')
	tb.stop()

