import numpy as np
from numpy.testing import assert_almost_equal

from ctapipe.image.waveform_cleaning import (NullWaveformCleaner,
                                             CHECMWaveformCleanerAverage,
                                             CHECMWaveformCleanerLocal, BaselineWaveformCleaner)


def test_null_cleaner(example_event):
    telid = 11
    data = example_event.r0.tel[telid].waveform
    nsamples = data.shape[2]
    ped = example_event.mc.tel[telid].pedestal
    data_ped = data - np.atleast_3d(ped / nsamples)
    data_ped = np.array([data_ped[0], data_ped[0]])  # Test LG functionality

    cleaner = NullWaveformCleaner()
    cleaned = cleaner.apply(data_ped)

    assert (np.array_equal(data_ped, cleaned))


def test_checm_cleaner_average(example_event):
    telid = 11
    data = example_event.r0.tel[telid].waveform
    nsamples = data.shape[2]
    ped = example_event.mc.tel[telid].pedestal
    data_ped = data - np.atleast_3d(ped / nsamples)
    data_ped = np.array([data_ped[0], data_ped[0]])  # Test LG functionality

    cleaner = CHECMWaveformCleanerAverage()
    cleaned = cleaner.apply(data_ped)

    assert_almost_equal(data_ped[0, 0, 0], -2.8, 1)
    assert_almost_equal(cleaned[0, 0, 0], -6.4, 1)


def test_checm_cleaner_local(example_event):
    telid = 11
    data = example_event.r0.tel[telid].waveform
    nsamples = data.shape[2]
    ped = example_event.mc.tel[telid].pedestal
    data_ped = data - np.atleast_3d(ped / nsamples)
    data_ped = np.array([data_ped[0], data_ped[0]])  # Test LG functionality

    cleaner = CHECMWaveformCleanerLocal()
    cleaned = cleaner.apply(data_ped)

    assert_almost_equal(data_ped[0, 0, 0], -2.8, 1)
    assert_almost_equal(cleaned[0, 0, 0], -15.9, 1)


def test_baseline_cleaner():

    # waveform : first 20 samples = 0, sencod 20 samples = 10
    waveform = np.full((2, 1855, 40), 10)
    waveform[:, :, 0:20] = 0

    cleaner = BaselineWaveformCleaner()

    cleaner.baseline_width = 20
    cleaner.window_shift = 0
    cleaned = cleaner.apply(waveform)
    assert (cleaned.mean() == 5)

    cleaner.baseline_width = 20
    cleaner.window_shift = 20
    cleaned = cleaner.apply(waveform)
    assert (cleaned.mean() == -5)


