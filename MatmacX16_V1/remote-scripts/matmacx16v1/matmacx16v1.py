from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent # Class encompassing several channel strips to form a mixer
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement

class matmacx16v1(ControlSurface):

	def __init__(self, c_instance):
		super(matmacx16v1, self).__init__(c_instance)
		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode
			# mixer
			global mixer
			num_tracks = 128
			num_returns = 24
			self.mixer = MixerComponent(num_tracks, num_returns)
			global active_mode
			active_mode = "_mode1"
			self._set_active_mode()
			self.show_message("Powered by mtmc")

	def _mode1(self):
		self.show_message("_mode1 is active")
		# mixer
		global mixer
		# volumes
		self.mixer.channel_strip(7).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 25, _map_modes.absolute))
		self.mixer.channel_strip(6).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 24, _map_modes.absolute))
		self.mixer.channel_strip(5).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 23, _map_modes.absolute))
		self.mixer.channel_strip(4).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 22, _map_modes.absolute))
		self.mixer.channel_strip(3).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 17, _map_modes.absolute))
		self.mixer.channel_strip(2).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 16, _map_modes.absolute))
		self.mixer.channel_strip(1).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 15, _map_modes.absolute))
		self.mixer.channel_strip(0).set_volume_control(EncoderElement(MIDI_CC_TYPE, 14, 14, _map_modes.absolute))
		# pan
		self.mixer.channel_strip(7).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 29, _map_modes.absolute))
		self.mixer.channel_strip(6).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 28, _map_modes.absolute))
		self.mixer.channel_strip(5).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 27, _map_modes.absolute))
		self.mixer.channel_strip(4).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 26, _map_modes.absolute))
		self.mixer.channel_strip(3).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 21, _map_modes.absolute))
		self.mixer.channel_strip(2).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 20, _map_modes.absolute))
		self.mixer.channel_strip(1).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 19, _map_modes.absolute))
		self.mixer.channel_strip(0).set_pan_control(EncoderElement(MIDI_CC_TYPE, 14, 18, _map_modes.absolute))

	def _remove_mode1(self):
		# mixer
		global mixer
		# volumes
		self.mixer.channel_strip(7).set_volume_control(None)
		self.mixer.channel_strip(6).set_volume_control(None)
		self.mixer.channel_strip(5).set_volume_control(None)
		self.mixer.channel_strip(4).set_volume_control(None)
		self.mixer.channel_strip(3).set_volume_control(None)
		self.mixer.channel_strip(2).set_volume_control(None)
		self.mixer.channel_strip(1).set_volume_control(None)
		self.mixer.channel_strip(0).set_volume_control(None)
		# pan 
		self.mixer.channel_strip(7).set_pan_control(None)
		self.mixer.channel_strip(6).set_pan_control(None)
		self.mixer.channel_strip(5).set_pan_control(None)
		self.mixer.channel_strip(4).set_pan_control(None)
		self.mixer.channel_strip(3).set_pan_control(None)
		self.mixer.channel_strip(2).set_pan_control(None)
		self.mixer.channel_strip(1).set_pan_control(None)
		self.mixer.channel_strip(0).set_pan_control(None)

	def _on_selected_track_changed(self):
		ControlSurface._on_selected_track_changed(self)
		self._display_reset_delay = 0
		value = "selected track changed"
		if (hasattr(self, '_set_track_select_led')):
			self._set_track_select_led()
		if (hasattr(self, '_reload_active_devices')):
			self._reload_active_devices(value)
		if (hasattr(self, 'update_all_ab_select_LEDs')):
			self.update_all_ab_select_LEDs(1)

	def _is_prev_device_on_or_off(self):
		self._device = self.song().view.selected_track.view.selected_device
		self._device_position = self.selected_device_idx()
		if (self._device is None) or (self._device_position == 0):
			on_off = "off"
		else:
			on_off = "on"
		return on_off

	def _is_nxt_device_on_or_off(self):
		self._selected_device = self.selected_device_idx() + 1  # add one as this starts from zero
		if (self._device is None) or (self._selected_device == len(self.song().view.selected_track.devices)):
			on_off = "off"
		else:
			on_off = "on"
		return on_off

	def _set_active_mode(self):
		global active_mode
		# activate mode
		if active_mode == "_mode1":
			self._mode1()
		if hasattr(self, '_set_track_select_led'):
			self._set_track_select_led()
		if hasattr(self, '_turn_on_device_select_leds'):
			self._turn_off_device_select_leds()
			self._turn_on_device_select_leds()
		if hasattr(self, '_all_prev_device_leds'):
			self._all_prev_device_leds()
		if hasattr(self, '_all_nxt_device_leds'):
			self._all_nxt_device_leds()
		if hasattr(self, 'update_all_ab_select_LEDs'):
			self.update_all_ab_select_LEDs(1)

	def _remove_active_mode(self):
		global active_mode
		# remove activate mode
		if active_mode == "_mode1":
			self._remove_mode1()

	def _activate_mode1(self,value):
		global active_mode
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "off"
			self._remove_active_mode()
			active_mode = "_mode1"
			self._set_active_mode()

	def _activate_shift_mode1(self,value):
		global active_mode
		global previous_shift_mode1
		global shift_previous_is_active
		if value > 0:
			shift_previous_is_active = "on"
			previous_shift_mode1 = active_mode
			self._remove_active_mode()
			active_mode = "_mode1"
			self._set_active_mode()
		elif shift_previous_is_active == "on":
			try:
				previous_shift_mode1
			except NameError:
				self.log_message("previous shift mode not defined yet")
			else:
				self._remove_active_mode()
				active_mode = previous_shift_mode1
				self._set_active_mode()

	def selected_device_idx(self):
		self._device = self.song().view.selected_track.view.selected_device
		return self.tuple_index(self.song().view.selected_track.devices, self._device)

	def selected_track_idx(self):
		self._track = self.song().view.selected_track
		self._track_num = self.tuple_index(self.song().tracks, self._track)
		self._track_num = self._track_num + 1
		return self._track_num

	def tuple_index(self, tuple, obj):
		for i in xrange(0, len(tuple)):
			if (tuple[i] == obj):
				return i
		return(False)

	def disconnect(self):
		super(matmacx16v1, self).disconnect()
