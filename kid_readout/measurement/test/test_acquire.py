import numpy as np

from kid_readout.measurement import acquire
from kid_readout.roach.baseband import RoachBaseband
from kid_readout.roach.heterodyne import RoachHeterodyne
from kid_readout.roach.tests.mock_roach import MockRoach
from kid_readout.roach.tests.mock_valon import MockValon


def test_baseband_sweep():
    num_tones = 16
    num_waveforms = 2**5
    num_tone_samples = 2**10
    length_seconds = 0.1
    ri = RoachBaseband(roach=MockRoach('roach'), initialize=False, adc_valon=MockValon())
    center_frequencies = np.linspace(100, 200, num_tones)
    offsets = np.linspace(-20e-3, 20e-3, num_waveforms)
    tone_banks = [center_frequencies + offset for offset in offsets]
    state = {'something': 'something state'}

    # Load waveforms one at a time.
    sweep = acquire.run_sweep(ri=ri, tone_banks=tone_banks, num_tone_samples=num_tone_samples,
                              length_seconds=length_seconds, state=state, description="description")
    assert len(sweep.stream_arrays) == num_waveforms
    assert all([stream_array.s21_raw.shape[0] == num_tones for stream_array in sweep.stream_arrays])

    # Pre-load all waveforms.
    acquire.load_baseband_sweep_tones(ri, tone_banks, num_tone_samples)
    sweep = acquire.run_loaded_sweep(ri=ri, length_seconds=length_seconds, state=state, description="description")
    assert len(sweep.stream_arrays) == num_waveforms
    assert all([stream_array.s21_raw.shape[0] == num_tones for stream_array in sweep.stream_arrays])


def test_heterodyne_sweep():
    num_tones = 16
    num_waveforms = 2**5
    num_tone_samples = 2**10
    length_seconds = 0.1
    ri = RoachHeterodyne(roach=MockRoach('roach'), initialize=False, adc_valon=MockValon())
    ri.lo_frequency = 1000
    center_frequencies = ri.lo_frequency + np.linspace(-100, 100, num_tones)
    offsets = np.linspace(-20e-3, 20e-3, num_waveforms)
    tone_banks = [center_frequencies + offset for offset in offsets]
    state = {'something': 'something state'}

    # Load waveforms one at a time.
    sweep = acquire.run_sweep(ri=ri, tone_banks=tone_banks, num_tone_samples=num_tone_samples,
                              length_seconds=length_seconds, state=state, description="description")
    assert len(sweep.stream_arrays) == num_waveforms
    assert all([stream_array.s21_raw.shape[0] == num_tones for stream_array in sweep.stream_arrays])

    # Pre-load all waveforms.
    acquire.load_heterodyne_sweep_tones(ri, tone_banks, num_tone_samples)
    sweep = acquire.run_loaded_sweep(ri=ri, length_seconds=length_seconds, state=state, description="description")
    assert len(sweep.stream_arrays) == num_waveforms
    assert all([stream_array.s21_raw.shape[0] == num_tones for stream_array in sweep.stream_arrays])
