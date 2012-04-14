#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Audio Receiver
# Generated: Thu Apr 12 20:55:06 2012
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

class audio_receiver(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Audio Receiver")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 125000
		self.audio_rate = audio_rate = 8000

		##################################################
		# Blocks
		##################################################
		self.vocoder_cvsd_decode_bf_0 = vocoder.cvsd_decode_bf(8,0.5)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(915e6, 0)
		self.uhd_usrp_source_0.set_gain(10, 0)
		self.digital_dxpsk_demod_0 = digital.dbpsk_demod(
			samples_per_symbol=2,
			excess_bw=0.35,
			freq_bw=6.28/100.0,
			phase_bw=6.28/100.0,
			timing_bw=6.28/100.0,
			gray_coded=True,
			verbose=False,
			log=False
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)
		self.audio_sink_0 = audio.sink(audio_rate, "plughw:0,0", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.vocoder_cvsd_decode_bf_0, 0), (self.audio_sink_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.vocoder_cvsd_decode_bf_0, 0))
		self.connect((self.digital_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.digital_dxpsk_demod_0, 0))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

	def get_audio_rate(self):
		return self.audio_rate

	def set_audio_rate(self, audio_rate):
		self.audio_rate = audio_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = audio_receiver()
	tb.start()
	raw_input('Press Enter to quit: ')
	tb.stop()

