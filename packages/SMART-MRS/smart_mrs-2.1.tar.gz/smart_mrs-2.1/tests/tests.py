# Testing of SMART_MRS Toolbox (many tests rely on correct functionality of to_fids and to_specs)
# For testing in terminal: python -m unittest -v tests.tests.TestToolbox.test_function

import unittest
import numpy as np
from src.SMART_MRS import IO, support, artifacts, applied


class TestToolbox(unittest.TestCase):

    def setUp(self):
        # create fids, specs, time and ppm
        dir = 'C:/Users/Hanna B/Desktop/MRS_Artifact_Toolbox_Package/Example Synthetic Data/'
        self.ON_fids = np.load(f'{dir}fids_on.npy')
        self.OFF_fids = np.load(f'{dir}fids_off.npy')
        self.specs = np.load(f'{dir}specs.npy')     # need to add

        # NIFTI data
        self.fidsNIFTI, self.timeNIFTI, self.ppmNIFTI = IO.get_nifti_mrs_data(dir_nifti=dir+"jdifference_nifti_SMART_MRS_EX.nii.gz", cf=3)

        # MAT data
        struct_name_ON = "finalSpecON"
        struct_name_OFF = "finalSpecOFF"
        fids_onMAT, timeMAT, ppmMAT = IO.get_FIDA_mat_data(dir_mat=dir+"GABAPlusOn_4096_3Sets.mat", struct_name=struct_name_ON)
        fids_offMAT, self.timeMAT, self.ppmMAT = IO.get_FIDA_mat_data(dir_mat=dir+"GABAPlusOff_4096_3Sets.mat", struct_name=struct_name_OFF)
        self.fidsMAT = support.interleave(fids_on=fids_onMAT, fids_off=fids_offMAT)

        # NPY data
        self.fidsNPY = np.load(f'{dir}fids.npy')
        self.timeNPY = np.load(f'{dir}time.npy')
        self.ppmNPY = np.load(f'{dir}ppm.npy')

    # testing support functions
    def test_to_fids(self):
        '''
        confirm to_fids() is the same as specs and can be applied along multiple dimensions
        '''
        # spectral points along axis 1
        fids_a1 = support.to_fids(self.specs, axis=1)

        # spectral points along axis 0
        swap_specs = self.specs.T
        fids_a0 = support.to_fids(swap_specs, axis=0).T

        # compare to specs
        np.testing.assert_allclose(fids_a1, self.fidsNPY, rtol=1e-08, err_msg='FIDs along axis 1 are incorrect.')
        np.testing.assert_allclose(fids_a0, self.fidsNPY, rtol=1e-08, err_msg='FIDs along axis 0 are incorrect.')


    def test_to_specs(self):
        '''
        confirm to_specs() is the same as FIDs and can be applied along multiple dimensions
        '''
        # spectral points along axis 1
        specs_a1 = support.to_specs(self.fidsNPY, axis=1)

        # spectral points along axis 0
        swap_fids = self.fidsNPY.T
        specs_a0 = support.to_specs(swap_fids, axis=0).T

        # compare to specs
        np.testing.assert_allclose(specs_a1, self.specs, rtol=1e-08, err_msg='Specs along axis 1 are incorrect.')
        np.testing.assert_allclose(specs_a0, self.specs, rtol=1e-08, err_msg='Specs along axis 0 are incorrect.')


    def test_interleave(self):
        '''
        confirm interleave() produces an ON, OFF, ON, OFF sequence
        '''
        # interleaved fids
        inter_fids = support.interleave(fids_on=self.ON_fids, fids_off=self.OFF_fids)

        # compare to specs
        np.testing.assert_array_equal(inter_fids[4, :], self.ON_fids[2, :], err_msg='Interleaved ON fids are incorrect.')
        np.testing.assert_array_equal(inter_fids[7, :], self.OFF_fids[3, :], err_msg='Interleaved OFF fids are incorrect.')
    

    def test_undo_interleave(self):
        '''
        confirm undo_interleave() properly extracts ON and OFF
        '''
        # undo interleaving of fids
        fids_on, fids_off = support.undo_interleave(fids=self.fidsNPY)

        # compare to specs
        np.testing.assert_array_equal(fids_on, self.ON_fids, err_msg='ON fids extracted from interleaved fids are incorrect.')
        np.testing.assert_array_equal(fids_off, self.OFF_fids, err_msg='OFF fids extracted from interleaved fids are incorrect.')


    def test_scale(self):
        '''
        confirm scale() normalizes to +1 (for mag, about equal for real)
        '''
        # scale specs/fids
        scaled_fids = support.scale(fids=self.fidsNPY)
        scaled_specs = support.to_specs(scaled_fids[0], axis=1)

        # compare to specs
        self.assertTrue((np.max(scaled_specs) <= 1.1), 'Specs upper bound properly scaled.')
        self.assertTrue((np.min(scaled_specs) >= -1.1), 'Specs lower bound properly scaled.')


    def test_undo_scale(self):
        '''
        confirm undo_scale() returns scale back to original scale
        '''
        # scale specs/fids
        scaled_fids, scaled_fact = support.scale(fids=self.fidsNPY)
        OG_fids = support.undo_scale(fids=scaled_fids, scale_fact=scaled_fact)
        OG_specs = support.to_specs(OG_fids, axis=1)

        # compare to specs
        np.testing.assert_allclose(OG_specs, self.specs, rtol=1e-08, err_msg='Specs did not return to original scale.')
    

    # testing artifact functions (general)
    def test_artifact_location(self, fids, artif_name, single_fids, single_locs, true_s_loc, multi_fids, multi_locs, true_m_locs, datatype):
        '''
        confirm add_ARTIFACT_NAME() can be applied to a specific transient(s) (2x tests)
        '''

        # single Locations test
        unch_fids_s = np.delete(single_fids, obj=single_locs, axis=0)
        np.testing.assert_array_equal(single_locs, true_s_loc, err_msg=f'{artif_name} for {datatype} data is at incorrect location selected during single location testing.')
        np.testing.assert_allclose(unch_fids_s, np.delete(fids, obj=single_locs, axis=0), rtol=1e-08, err_msg=f'{artif_name} added at incorrect location(s) during single location testing.')
        np.testing.assert_raises(AssertionError, np.testing.assert_array_equal, single_locs, fids[single_locs, :], err_msg=f'{artif_name} not added at specified location during single location testing.')

        # multi Locations test
        unch_fids_m = np.delete(multi_fids, obj=multi_locs, axis=0)
        np.testing.assert_array_equal(multi_locs, true_m_locs, err_msg=f'{artif_name} for {datatype} data is at incorrect locations selected during multi location testing.')
        np.testing.assert_allclose(unch_fids_m, np.delete(fids, obj=multi_locs, axis=0), rtol=1e-08, err_msg=f'{artif_name} added at incorrect location(s) during multi location testing.')
        np.testing.assert_raises(AssertionError, np.testing.assert_array_equal, multi_locs, fids[multi_locs, :], err_msg=f'{artif_name} not added at specified location(s) during multi location testing.')


    def test_artifact_number(self, num_artifs, artif_name, artif_loc_lt, artif_loc_gt, datatype):
        '''
        confirm add_ARTIFACT_NAME() is overridden by number of artifacts (2x test)
        '''

        # locations Override (< less than) test
        self.assertTrue(len(artif_loc_lt)==num_artifs, f'{artif_name} for {datatype} is at locations were not overridden by number of artifacts during less than locations override testing.')

        # locations Override (> greater than) test
        self.assertTrue(len(artif_loc_gt) == num_artifs, f'{artif_name} for {datatype} is at locations were not overridden by number of artifacts during greater than locations override testing.')


        # testing artifact functions (specific)
    def test_spur_echo_artifact(self):
        '''
        confirm add_spur_echo_artifact() is functioning as intended
        '''

        ## Test NPY DATA
        print(f'\n Running tests on add_spur_echo_artifact() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_spur_echo_artifact(fids=self.fidsNPY, time=self.timeNPY, gs_locs=true_sing_loc, nmb_sps=1)
        artif_fids_m, artif_loc_m = artifacts.add_spur_echo_artifact(fids=self.fidsNPY, time=self.timeNPY, gs_locs=true_multi_locs, nmb_sps=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Spur Echo', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_spur_echo_artifact(fids=self.fidsNPY, time=self.timeNPY, gs_locs=[9], nmb_sps=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_spur_echo_artifact(fids=self.fidsNPY, time=self.timeNPY, gs_locs=[4, 5, 9], nmb_sps=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Spur Echo', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test MAT DATA
        print(f'\n Running tests on add_spur_echo_artifact() for MAT data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_spur_echo_artifact(fids=self.fidsMAT, time=self.timeMAT, gs_locs=true_sing_loc, nmb_sps=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_spur_echo_artifact(fids=self.fidsMAT, time=self.timeMAT, gs_locs=true_multi_locs, nmb_sps=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Spur Echo', single_fids=artif_fids_sM, single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM, multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        artif_fids_ltM, artif_loc_ltM = artifacts.add_spur_echo_artifact(fids=self.fidsMAT, time=self.timeMAT, gs_locs=[9], nmb_sps=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_spur_echo_artifact(fids=self.fidsMAT, time=self.timeMAT, gs_locs=[4, 5, 9], nmb_sps=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Spur Echo', artif_loc_lt=artif_loc_ltM, artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test NIFTI DATA
        print(f'\n Running tests on add_spur_echo_artifact() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_spur_echo_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, gs_locs=true_sing_loc, nmb_sps=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_spur_echo_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, gs_locs=true_multi_locs, nmb_sps=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Spur Echo', single_fids=artif_fids_sN, single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN, multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_spur_echo_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, gs_locs=[9], nmb_sps=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_spur_echo_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, gs_locs=[4, 5, 9], nmb_sps=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Spur Echo', artif_loc_lt=artif_loc_ltN, artif_loc_gt=artif_loc_gtN, datatype="NIFTI")

    def test_eddy_current_artifact(self):
        '''
        confirm add_eddy_current_artifact() is functioning as intended
        '''

        ## Test NPY DATA
        print(f'\n Running tests on add_eddy_current_artifact() for NPY data...')

        # test artifact location
        true_sing_loc = [3]
        true_multi_locs = [1, 6, 7]
        artif_fids_s, artif_loc_s = artifacts.add_eddy_current_artifact(fids=self.fidsNPY, time=self.timeNPY, ec_locs=true_sing_loc, nmb_ecs=1)
        artif_fids_m, artif_loc_m = artifacts.add_eddy_current_artifact(fids=self.fidsNPY, time=self.timeNPY, ec_locs=true_multi_locs, nmb_ecs=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Eddy Current', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_eddy_current_artifact(fids=self.fidsNPY, time=self.timeNPY, ec_locs=[3], nmb_ecs=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_eddy_current_artifact(fids=self.fidsNPY, time=self.timeNPY, ec_locs=[4, 6, 8], nmb_ecs=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Eddy Current', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test MAT DATA
        print(f'\n Running tests on add_eddy_current_artifact() for MAT data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_eddy_current_artifact(fids=self.fidsMAT, time=self.timeMAT, ec_locs=true_sing_loc, nmb_ecs=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_eddy_current_artifact(fids=self.fidsMAT, time=self.timeMAT, ec_locs=true_multi_locs, nmb_ecs=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Eddy Current', single_fids=artif_fids_sM, single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM, multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        artif_fids_ltM, artif_loc_ltM = artifacts.add_eddy_current_artifact(fids=self.fidsMAT, time=self.timeMAT, ec_locs=[3], nmb_ecs=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_eddy_current_artifact(fids=self.fidsMAT, time=self.timeMAT, ec_locs=[4, 6, 8], nmb_ecs=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Eddy Current', artif_loc_lt=artif_loc_ltM, artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test NIFTI DATA
        print(f'\n Running tests on add_eddy_current_artifact() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_eddy_current_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, ec_locs=true_sing_loc, nmb_ecs=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_eddy_current_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, ec_locs=true_multi_locs, nmb_ecs=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Eddy Current', single_fids=artif_fids_sN, single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN, multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_eddy_current_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, ec_locs=[3], nmb_ecs=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_eddy_current_artifact(fids=self.fidsNIFTI, time=self.timeNIFTI, ec_locs=[4, 6, 8], nmb_ecs=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Eddy Current', artif_loc_lt=artif_loc_ltN, artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


    def test_linebroad_artifact(self):
        '''
        confirm add_linebroad() is functioning as intended
        '''

        ## Test for NPY data
        print(f'\n Running tests on add_linebroad() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_linebroad(fids=self.fidsNPY, time=self.timeNPY, mot_locs=true_sing_loc, nmb_motion=1)
        artif_fids_m, artif_loc_m = artifacts.add_linebroad(fids=self.fidsNPY, time=self.timeNPY, mot_locs=true_multi_locs, nmb_motion=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Line Broadening', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_linebroad(fids=self.fidsNPY, time=self.timeNPY, mot_locs=[9], nmb_motion=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_linebroad(fids=self.fidsNPY, time=self.timeNPY, mot_locs=[4, 5, 9], nmb_motion=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Line Broadening', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test for MAT data
        print(f'\n Running tests on add_linebroad() for MAT data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_sM, artif_loc_sM = artifacts.add_linebroad(fids=self.fidsMAT, time=self.timeMAT, mot_locs=true_sing_loc,
                                                            nmb_motion=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_linebroad(fids=self.fidsMAT, time=self.timeMAT, mot_locs=true_multi_locs,
                                                            nmb_motion=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Line Broadening', single_fids=artif_fids_sM,
                                    single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        num_artifs = 2
        artif_fids_ltM, artif_loc_ltM = artifacts.add_linebroad(fids=self.fidsMAT, time=self.timeMAT, mot_locs=[9],
                                                              nmb_motion=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_linebroad(fids=self.fidsMAT, time=self.timeMAT, mot_locs=[4, 5, 9],
                                                              nmb_motion=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Line Broadening', artif_loc_lt=artif_loc_ltM,
                                  artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test for NIFTI data
        print(f'\n Running tests on add_linebroad() for NIFTI data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_sN, artif_loc_sN = artifacts.add_linebroad(fids=self.fidsNIFTI, time=self.timeNIFTI, mot_locs=true_sing_loc,
                                                            nmb_motion=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_linebroad(fids=self.fidsNIFTI, time=self.timeNIFTI, mot_locs=true_multi_locs,
                                                            nmb_motion=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Line Broadening', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        num_artifs = 2
        artif_fids_ltN, artif_loc_ltN = artifacts.add_linebroad(fids=self.fidsNIFTI, time=self.timeNIFTI, mot_locs=[9],
                                                              nmb_motion=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_linebroad(fids=self.fidsNIFTI, time=self.timeNIFTI, mot_locs=[4, 5, 9],
                                                              nmb_motion=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Line Broadening', artif_loc_lt=artif_loc_ltN,
                                  artif_loc_gt=artif_loc_gtN, datatype="NIFTI")

    def test_nuisance_peak_artifact(self):
        '''
        confirm add_nuisance_peak() is functioning as intended
        '''

        test_peak = {
            "peak_type": None,
            "amp": None,
            "width": None,
            "res_freq": None,
            "edited": None}

        ## Test NPY data
        print(f'\n Running tests on add_nuisance_peak() for NPY data...')

        # test artifact location
        true_sing_loc = [3]
        true_multi_locs = [1, 6, 7]
        artif_fids_s, artif_loc_s = artifacts.add_nuisance_peak(fids=self.fidsNPY, time=self.timeNPY, peak_profile=test_peak, np_locs=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_nuisance_peak(fids=self.fidsNPY, time=self.timeNPY, peak_profile=test_peak, np_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Nuisance Peak', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_nuisance_peak(fids=self.fidsNPY, time=self.timeNPY, peak_profile=test_peak, np_locs=[9], num_trans=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_nuisance_peak(fids=self.fidsNPY, time=self.timeNPY, peak_profile=test_peak, np_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Nuisance Peak', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test MAT data
        print(f'\n Running tests on add_nuisance_peak() for MAT data...')

        # test artifact location
        true_sing_loc = [3]
        true_multi_locs = [1, 6, 7]
        artif_fids_sM, artif_loc_sM = artifacts.add_nuisance_peak(fids=self.fidsMAT, time=self.timeMAT, peak_profile=test_peak,
                                                                np_locs=true_sing_loc, num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_nuisance_peak(fids=self.fidsMAT, time=self.timeMAT, peak_profile=test_peak,
                                                                np_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Nuisance Peak', single_fids=artif_fids_sM,
                                    single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        num_artifs = 2
        artif_fids_ltM, artif_loc_ltM = artifacts.add_nuisance_peak(fids=self.fidsMAT, time=self.timeMAT,
                                                                  peak_profile=test_peak, np_locs=[9],
                                                                  num_trans=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_nuisance_peak(fids=self.fidsMAT, time=self.timeMAT,
                                                                  peak_profile=test_peak, np_locs=[4, 5, 9],
                                                                  num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Nuisance Peak', artif_loc_lt=artif_loc_ltM,
                                  artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test NIFTI data
        print(f'\n Running tests on add_nuisance_peak() for NIFTI data...')

        # test artifact location
        true_sing_loc = [3]
        true_multi_locs = [1, 6, 7]
        artif_fids_sN, artif_loc_sN= artifacts.add_nuisance_peak(fids=self.fidsNIFTI, time=self.timeNIFTI, peak_profile=test_peak,
                                                                np_locs=true_sing_loc, num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_nuisance_peak(fids=self.fidsNIFTI, time=self.timeNIFTI, peak_profile=test_peak,
                                                                np_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Nuisance Peak', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        num_artifs = 2
        artif_fids_ltN, artif_loc_ltN = artifacts.add_nuisance_peak(fids=self.fidsNIFTI, time=self.timeNIFTI,
                                                                  peak_profile=test_peak, np_locs=[9],
                                                                  num_trans=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_nuisance_peak(fids=self.fidsNIFTI, time=self.timeV,
                                                                  peak_profile=test_peak, np_locs=[4, 5, 9],
                                                                  num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Nuisance Peak', artif_loc_lt=artif_loc_ltN,
                                  artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


    def test_baseline_artifact(self):
        '''
        confirm add_baseline() is functioning as intended
        '''

        test_baseline = {  # profile for baseline
            "base_type": None,
            "num_bases": None,
            "amp_bases": None,
            "comp_bases": None,
            "base_var": None,
            "slope_bases": None,
            "spline_fitted": None}

        ## Test NPY data
        print(f'\n Running tests on add_baseline() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_baseline(fids=self.fidsNPY, ppm=self.ppmNPY, base_profile=test_baseline, nbase_locs=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_baseline(fids=self.fidsNPY, ppm=self.ppmNPY, base_profile=test_baseline, nbase_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids= self.fidsNPY, artif_name='Line Broadening', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_baseline(fids=self.fidsNPY, ppm=self.ppmNPY, base_profile=test_baseline, nbase_locs=[9], num_trans=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_baseline(fids=self.fidsNPY, ppm=self.ppmNPY, base_profile=test_baseline, nbase_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Baseline', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test MAT data
        print(f'\n Running tests on add_baseline() for MAT data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_baseline(fids=self.fidsMAT, ppm=self.ppmMAT, base_profile=test_baseline,
                                                           nbase_locs=true_sing_loc, num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_baseline(fids=self.fidsMAT, ppm=self.ppmMAT, base_profile=test_baseline,
                                                           nbase_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Line Broadening', single_fids=artif_fids_sM,
                                    single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        artif_fids_ltM, artif_loc_ltM = artifacts.add_baseline(fids=self.fidsMAT, ppm=self.ppmMAT, base_profile=test_baseline,
                                                             nbase_locs=[9], num_trans=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_baseline(fids=self.fidsMAT, ppm=self.ppmMAT, base_profile=test_baseline,
                                                             nbase_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Baseline', artif_loc_lt=artif_loc_ltM,
                                  artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test NIFTI data
        print(f'\n Running tests on add_baseline() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_baseline(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, base_profile=test_baseline,
                                                           nbase_locs=true_sing_loc, num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_baseline(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, base_profile=test_baseline,
                                                           nbase_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Line Broadening', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_baseline(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, base_profile=test_baseline,
                                                             nbase_locs=[9], num_trans=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_baseline(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, base_profile=test_baseline,
                                                             nbase_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Baseline', artif_loc_lt=artif_loc_ltN,
                                  artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


    def test_freq_drift_artifact(self):
        '''
        confirm add_freq_drift_linear() is functioning as intended
        '''

        ## Test for NPY data
        print(f'\n Running tests on add_freq_drift_linear() for NPY data...')

        # test artifact location
        true_sing_loc = 3
        true_multi_locs = [3, 4, 5]
        artif_fids_s, artif_loc_s = artifacts.add_freq_drift_linear(fids=self.fidsNPY, time=self.timeNPY, start_trans=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_freq_drift_linear(fids=self.fidsNPY, time=self.timeNPY, start_trans=true_sing_loc, num_trans=3)
        artif_loc_m = range(artif_loc_m[0], artif_loc_m[0]+artif_loc_m[1])
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Linear Frequency Drift', single_fids=artif_fids_s, single_locs=artif_loc_s[0], true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        ## Test for MAT data
        print(f'\n Running tests on add_freq_drift_linear() for MAT data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_freq_drift_linear(fids=self.fidsMAT, time=self.timeMAT,
                                                                    start_trans=true_sing_loc, num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_freq_drift_linear(fids=self.fidsMAT, time=self.timeMAT,
                                                                    start_trans=true_sing_loc, num_trans=3)
        artif_loc_mM = range(artif_loc_mM[0], artif_loc_mM[0] + artif_loc_mM[1])
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Linear Frequency Drift', single_fids=artif_fids_s,
                                    single_locs=artif_loc_sM[0], true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        ## Test for NIFTI data
        print(f'\n Running tests on add_freq_drift_linear() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_freq_drift_linear(fids=self.fidsNIFTI, time=self.timeNIFTI,
                                                                    start_trans=true_sing_loc, num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_freq_drift_linear(fids=self.fidsNIFTI, time=self.timeNIFTI,
                                                                    start_trans=true_sing_loc, num_trans=3)
        artif_loc_mN = range(artif_loc_mN[0], artif_loc_mN[0] + artif_loc_mN[1])
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Linear Frequency Drift', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN[0], true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")


    def test_frequency_shift_artifact(self):
        '''
        confirm add_freq_shift_random() is functioning as intended
        '''

        ## Test for NPY data
        print(f'\n Running tests on add_freq_shift_random() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_freq_shift(fids=self.fidsNPY, time=self.timeNPY, shift_locs=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_freq_shift(fids=self.fidsNPY, time=self.timeNPY, shift_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Random Frequency Shift', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_freq_shift(fids=self.fidsNPY, time=self.timeNPY, shift_locs=[9], num_trans=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_freq_shift(fids=self.fidsNPY, time=self.timeNPY, shift_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Random Frequency Shift', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test for MAT data
        print(f'\n Running tests on add_freq_shift_random() for MAT data data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_freq_shift(fids=self.fidsMAT, time=self.timeMAT, shift_locs=true_sing_loc,
                                                             num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_freq_shift(fids=self.fidsMAT, time=self.timeMAT, shift_locs=true_multi_locs,
                                                             num_trans=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Random Frequency Shift', single_fids=artif_fids_sM,
                                    single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        artif_fids_ltM, artif_loc_ltM = artifacts.add_freq_shift(fids=self.fidsMAT, time=self.timeMAT, shift_locs=[9],
                                                               num_trans=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_freq_shift(fids=self.fidsMAT, time=self.timeMAT, shift_locs=[4, 5, 9],
                                                               num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Random Frequency Shift', artif_loc_lt=artif_loc_ltM,
                                  artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test for NIFTI data
        print(f'\n Running tests on add_freq_shift_random() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_freq_shift(fids=self.fidsNIFTI, time=self.timeNIFTI, shift_locs=true_sing_loc,
                                                             num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_freq_shift(fids=self.fidsNIFTI, time=self.timeNIFTI, shift_locs=true_multi_locs,
                                                             num_trans=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Random Frequency Shift', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_freq_shift(fids=self.fidsNIFTI, time=self.timeNIFTI, shift_locs=[9],
                                                               num_trans=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_freq_shift(fids=self.fidsNIFTI, time=self.timeNIFTI, shift_locs=[4, 5, 9],
                                                               num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Random Frequency Shift', artif_loc_lt=artif_loc_ltN,
                                  artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


    def test_zero_phase_shift_artifact(self):
        '''
        confirm add_zero_order_phase_shift() is functioning as intended
        '''

        ## Test for NPY data
        print(f'\n Running tests on add_zero_order_phase_shift() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_zero_order_phase_shift(fids=self.fidsNPY, shift_locs=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_zero_order_phase_shift(fids=self.fidsNPY, shift_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Zero Order Phase Shift', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_zero_order_phase_shift(fids=self.fidsNPY, shift_locs=[9], num_trans=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_zero_order_phase_shift(fids=self.fidsNPY, shift_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")

        ## Test for MAT data
        print(f'\n Running tests on add_zero_order_phase_shift() for MAT data...')

        # test artifact location
        artif_fids_sM, artif_loc_sM = artifacts.add_zero_order_phase_shift(fids=self.fidsMAT, shift_locs=true_sing_loc,
                                                                         num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_zero_order_phase_shift(fids=self.fidsMAT, shift_locs=true_multi_locs,
                                                                         num_trans=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Zero Order Phase Shift', single_fids=artif_fids_sM,
                                    single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM,
                                    multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        artif_fids_ltM, artif_loc_ltM = artifacts.add_zero_order_phase_shift(fids=self.fidsMAT, shift_locs=[9],
                                                                           num_trans=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_zero_order_phase_shift(fids=self.fidsMAT, shift_locs=[4, 5, 9],
                                                                           num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_ltM,
                                  artif_loc_gt=artif_loc_gtM, datatype="MAT")

        ## Test for NIFTI data
        print(f'\n Running tests on add_zero_order_phase_shift() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_zero_order_phase_shift(fids=self.fidsNIFTI, shift_locs=true_sing_loc,
                                                                         num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_zero_order_phase_shift(fids=self.fidsNIFTI, shift_locs=true_multi_locs,
                                                                         num_trans=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Zero Order Phase Shift', single_fids=artif_fids_sN,
                                    single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN,
                                    multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_zero_order_phase_shift(fids=self.fidsNIFTI, shift_locs=[9],
                                                                           num_trans=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_zero_order_phase_shift(fids=self.fidsNIFTI, shift_locs=[4, 5, 9],
                                                                           num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_ltN,
                                  artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


    def test_first_phase_shift_artifact(self):
        '''
        confirm add_first_order_phase_shift() is functioning as intended
        '''

        ## Test for NPY data
        print(f'\n Running tests on add_first_order_phase_shift() for NPY data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_s, artif_loc_s = artifacts.add_first_order_phase_shift(fids=self.fidsNPY, ppm=self.ppmNPY, shift_locs=true_sing_loc, num_trans=1)
        artif_fids_m, artif_loc_m = artifacts.add_first_order_phase_shift(fids=self.fidsNPY, ppm=self.ppmNPY, shift_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNPY, artif_name='Zero Order Phase Shift', single_fids=artif_fids_s, single_locs=artif_loc_s, true_s_loc=true_sing_loc, multi_fids=artif_fids_m, multi_locs=artif_loc_m, true_m_locs=true_multi_locs, datatype="NPY")

        # test number of artifacts
        num_artifs = 2
        artif_fids_lt, artif_loc_lt = artifacts.add_first_order_phase_shift(fids=self.fidsNPY, ppm=self.ppmNPY, shift_locs=[9], num_trans=num_artifs)
        artif_fids_gt, artif_loc_gt = artifacts.add_first_order_phase_shift(fids=self.fidsNPY, ppm=self.ppmNPY, shift_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_lt, artif_loc_gt=artif_loc_gt, datatype="NPY")


        ## Test for MAT data
        print(f'\n Running tests on add_first_order_phase_shift() for MAT data...')

        # test artifact location
        true_sing_loc = [9]
        true_multi_locs = [2, 5, 8]
        artif_fids_sM, artif_loc_sM = artifacts.add_first_order_phase_shift(fids=self.fidsMAT, ppm=self.ppmMAT, shift_locs=true_sing_loc, num_trans=1)
        artif_fids_mM, artif_loc_mM = artifacts.add_first_order_phase_shift(fids=self.fidsMAT, ppm=self.ppmMAT, shift_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsMAT, artif_name='Zero Order Phase Shift', single_fids=artif_fids_sM, single_locs=artif_loc_sM, true_s_loc=true_sing_loc, multi_fids=artif_fids_mM, multi_locs=artif_loc_mM, true_m_locs=true_multi_locs, datatype="MAT")

        # test number of artifacts
        num_artifs = 2
        artif_fids_ltM, artif_loc_ltM = artifacts.add_first_order_phase_shift(fids=self.fidsMAT, ppm=self.ppmMAT, shift_locs=[9], num_trans=num_artifs)
        artif_fids_gtM, artif_loc_gtM = artifacts.add_first_order_phase_shift(fids=self.fidsMAT, ppm=self.ppmMAT, shift_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_ltM, artif_loc_gt=artif_loc_gtM, datatype="MAT")


        ## Test for NIFTI data
        print(f'\n Running tests on add_first_order_phase_shift() for NIFTI data...')

        # test artifact location
        artif_fids_sN, artif_loc_sN = artifacts.add_first_order_phase_shift(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, shift_locs=true_sing_loc, num_trans=1)
        artif_fids_mN, artif_loc_mN = artifacts.add_first_order_phase_shift(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, shift_locs=true_multi_locs, num_trans=3)
        self.test_artifact_location(fids=self.fidsNIFTI, artif_name='Zero Order Phase Shift', single_fids=artif_fids_sN, single_locs=artif_loc_sN, true_s_loc=true_sing_loc, multi_fids=artif_fids_mN, multi_locs=artif_loc_mN, true_m_locs=true_multi_locs, datatype="NIFTI")

        # test number of artifacts
        artif_fids_ltN, artif_loc_ltN = artifacts.add_first_order_phase_shift(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, shift_locs=[9], num_trans=num_artifs)
        artif_fids_gtN, artif_loc_gtN = artifacts.add_first_order_phase_shift(fids=self.fidsNIFTI, ppm=self.ppmNIFTI, shift_locs=[4, 5, 9], num_trans=num_artifs)
        self.test_artifact_number(num_artifs=num_artifs, artif_name='Zero Order Phase Shift', artif_loc_lt=artif_loc_ltN, artif_loc_gt=artif_loc_gtN, datatype="NIFTI")


if __name__ == 'main':
    unittest.main()
