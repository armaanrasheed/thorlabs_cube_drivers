import sys
import time
import unittest

from sipyco.test.generic_rpc import GenericRPCCase

_RESERVED: int = 0x0


class GenericTdcTest:
    def test_pot_parameters(self):
        test_vector = 1, 2, 3, 4, 5, 6, 7, 8
        self.cont.set_pot_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_pot_parameters())

    def test_position_counter(self):
        test_vector = 42
        self.cont.set_position_counter(test_vector)
        self.assertEqual(test_vector, self.cont.get_position_counter())

    def test_encoder_counter(self):
        test_vector = 43
        self.cont.set_encoder_counter(test_vector)
        self.assertEqual(test_vector, self.cont.get_encoder_counter())

    def test_velocity_parameters(self):
        test_vector = 44, 45
        self.cont.set_velocity_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_velocity_parameters())

    def test_jog_parameters(self):
        test_vector = 46, 47, 48, 49, 50
        self.cont.set_jog_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_jog_parameters())

    def test_gen_move_parameters(self):
        test_vector = 51
        self.cont.set_gen_move_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_gen_move_parameters())

    def test_moverelparams(self):
        test_vector = 52
        self.cont.set_move_relative_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_move_relative_parameters())

    def test_move_absolute_parameters(self):
        test_vector = 53
        self.cont.set_move_absolute_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_move_absolute_parameters())

    def test_home_parameters(self):
        test_vector = 54
        self.cont.set_home_parameters(test_vector)
        self.assertEqual(test_vector, self.cont.get_home_parameters())

    def test_limit_switch_parameters(self):
        test_vector = 2, 1, 55, 56, 0x1
        self.cont.set_limit_switch_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_limit_switch_parameters())

    def test_dc_pid_parameters(self):
        test_vector = 57, 58, 59, 60, 0x0F
        self.cont.set_dc_pid_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_dc_pid_parameters())

    def test_av_modes(self):
        for i in range(1):
            for j in range(1):
                for k in range(1):
                    with self.subTest(i=i):
                        with self.subTest(j=j):
                            with self.subTest(k=k):
                                test_vector = i << 2 + j << 1 + k
                                self.cont.set_av_modes(test_vector)
                                self.assertEqual(test_vector, self.cont.get_av_modes())

    def test_button_parameters(self):
        test_vector = 2, 3, 4
        self.cont.set_button_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_button_parameters())

class GenericKdcTest:

    def test_mmi_params(self):
        test_vector = (1, 12000, 5000, 1, 10000, 15000, 75, 20, 5)
        self.cont.set_mmi_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_mmi_parameters())

    def test_trigger_io_config(self):
         test_vector = (0x01, 0x01, 0x0A, 0x01)
         self.cont.set_trigger_io_config(*test_vector)
         self.assertEqual(test_vector, self.cont.get_trigger_io_config())

    def test_position_trigger_parameters(self):
        test_vector = 1,23,4,3,5,12,6,9
        self.cont.set_position_trigger_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_position_trigger_parameters())


class GenericTpzTest:
    def test_position_control_mode(self):
        test_vector = 1
        self.cont.set_position_control_mode(test_vector)
        self.assertEqual(test_vector, self.cont.get_position_control_mode())

    def test_output_volts(self):
        for voltage in 5.0, 10.0, 15.0, round(self.cont.get_tpz_io_settings()[0]):
            with self.subTest(voltage=voltage):
                test_vector = voltage
                self.cont.set_output_volts(test_vector)
                time.sleep(1)  # Wait for the output voltage to converge
                self.assertAlmostEqual(
                    test_vector, self.cont.get_output_volts(), delta=0.03
                )

    def test_output_position(self):
        test_vector = 31000
        self.cont.set_output_position(test_vector)
        self.assertEqual(test_vector, self.cont.get_output_position())

    def test_input_volts_source(self):
        for i in range(3):
            test_vector = i
            self.cont.set_input_volts_source(i)
            with self.subTest(i=i):
                self.assertEqual(test_vector, self.cont.get_input_volts_source())

    def test_pi_constants(self):
        test_vector = 42, 43
        self.cont.set_pi_constants(*test_vector)
        self.assertEqual(test_vector, self.cont.get_pi_constants())

    def test_tpz_display_settings(self):
        for intensity in 0, 10, 30, 50, 100, 150, 254:
            with self.subTest(intensity=intensity):
                test_vector = intensity
                self.cont.set_tpz_display_settings(test_vector)
                self.assertEqual(test_vector, self.cont.get_tpz_display_settings())

    def test_tpz_io_settings(self):
        for v in 75.0, 100.0, 150.0:
            with self.subTest(v=v):
                test_vector = v, 1
                self.cont.set_tpz_io_settings(*test_vector)
                self.assertEqual(test_vector, self.cont.get_tpz_io_settings())

class GenericKpzTest:
    def test_kcubemmi_params(self):
        test_vector = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.cont.set_kcubemmi_params(*test_vector)
        expected_result = (
            *test_vector,
            _RESERVED,
            _RESERVED,
            _RESERVED,
            _RESERVED,
        )  # Adding reserved bytes for comparison
        self.assertEqual(expected_result, self.cont.get_kcubemmi_params())

    def test_trigio_config(self):
        test_vector = (1, 0, 2, 1)
        self.cont.set_trigio_config(*test_vector)
        expected_result = (
            *test_vector,
            _RESERVED,
            _RESERVED,
            _RESERVED,
            _RESERVED,
            _RESERVED,
            _RESERVED,
        )  # Adding reserved bytes for comparison
        self.assertEqual(expected_result, self.cont.get_trigio_config())


class GenericTpaTest:
    def test_loop_params(self):
        test_vector = 1, 2, 3
        self.cont.set_loop_params(*test_vector)
        self.assertEqual(test_vector, self.cont.get_loop_params())

    def test_oper_mode(self):
        test_vector = 1
        self.cont.set_quad_oper_mode(test_vector)
        self.assertEqual(test_vector, self.cont.get_quad_oper_mode())

    def test_position_demand_params(self):
        test_vector = -32767, 32767, 32767, 32767, 2, 1, 1, 0.3
        self.cont.set_quad_position_demand_params(*test_vector)
        self.assertEqual(test_vector, self.cont.get_quad_position_demand_params())

    def test_display_settings(self):
        test_vector = 150, 2, 30
        self.cont.set_quad_display_settings(*test_vector)
        self.assertEqual(test_vector, self.cont.get_quad_display_settings())

    def test_position_outputs(self):
        test_vector = -15000, 15000
        self.cont.set_quad_position_outputs(*test_vector)
        self.assertEqual(test_vector, self.cont.get_quad_position_outputs())

    def test_loop_params2(self):
        test_vector = 1.5, 2.5, 3.5, 100.0, 200.0, 1.0, 1, 0
        self.cont.set_quad_loop_params2(*test_vector)
        self.assertEqual(test_vector, self.cont.get_quad_loop_params2())

class GenericKpaTest(GenericTpaTest):

    def test_trigger_config(self):
        test_vector = 1, 0, 100, 200, 50, 2, 1, 150, 250, 75
        self.cont.set_trigger_config(*test_vector)
        self.assertEqual(test_vector, self.cont.get_trigger_config())

    def test_digital_outputs(self):
        test_vector = 0xFF
        self.cont.set_digital_outputs(test_vector)
        self.assertEqual(test_vector, self.cont.get_digital_outputs())

class GenericTscTest:
    def test_absolute_position(self):
        test_position = 100000
        self.cont.set_absolute_position(test_position)
        self.assertEqual(test_position, self.cont.absolute_position)

    def test_move_stop(self):
        test_stop_mode = 2
        self.cont.move_stop(test_stop_mode)
        self.assertEqual(test_stop_mode, self.cont.stop_mode)

    def test_av_modes(self):
        for i in range(1):
            for j in range(1):
                for k in range(1):
                    with self.subTest(i=i, j=j, k=k):
                        test_vector = (i << 2) + (j << 1) + k
                        self.cont.set_av_modes(test_vector)
                        self.assertEqual(test_vector, self.cont.get_av_modes())

    def test_button_parameters(self):
        test_vector = (1, 50000, 100000, 500, 1000)
        self.cont.set_button_parameters(*test_vector)
        self.assertEqual(test_vector, self.cont.get_button_parameters())

    def test_eeprom_parameters(self):
        test_msg_id = 42
        self.cont.set_eeprom_parameters(test_msg_id)
        self.assertEqual(test_msg_id, self.cont.msg_id)

    def test_status_update(self):
        self.cont.position = 250000
        self.cont.encoder_count = 1024
        self.cont.status_bits = 0b1010
        self.cont.chan_identity_two = 0x01

        expected_status = (
            self.cont.position,
            self.cont.encoder_count,
            self.cont.status_bits,
            self.cont.chan_identity_two,
        )
        self.assertEqual(expected_status, self.cont.get_status_update())

    def test_sol_operating_mode(self):
        test_operating_mode = 3
        self.cont.set_sol_operating_mode(test_operating_mode)
        self.assertEqual(test_operating_mode, self.cont.get_sol_operating_mode())

    def test_solenoid_cycle_parameters(self):
        test_cycle_params = (100, 200, 50)
        self.cont.set_solenoid_cycle_parameters(*test_cycle_params)
        self.assertEqual(test_cycle_params, self.cont.get_solenoid_cycle_parameters())

    def test_sol_interlock_mode(self):
        test_interlock_mode = 1
        self.cont.set_sol_interlock_mode(test_interlock_mode)
        self.assertEqual(test_interlock_mode, self.cont.get_sol_interlock_mode())

    def test_sol_state(self):
        test_state = 1
        self.cont.set_sol_state(test_state)
        self.assertEqual(test_state, self.cont.get_sol_state())

class GenericKscTest(GenericTscTest):
    def test_kcubemmi_params(self):
        test_vector = (
            1,
            5000,
            1000,
            0,
            10000,
            20000,
            30000,
            80,
            3000,
            50,
            5,
        )
        self.cont.set_kcubemmi_params(*test_vector)
        self.assertEqual(test_vector, self.cont.get_kcubemmi_params())

    def test_kcubetrigio_config(self):
        test_vector = (1, 0, 2, 1)
        self.cont.set_kcubetrigio_config(*test_vector)
        self.assertEqual(test_vector, self.cont.get_kcubetrigio_config())

    def test_kcubepostrig_params(self):
        test_vector = (
            10000,
            500,
            10,
            15000,
            600,
            15,
            100,
            5,
        )
        self.cont.set_kcubepostrig_params(*test_vector)
        self.assertEqual(test_vector, self.cont.get_kcubepostrig_params())


class TestTdcSim(GenericRPCCase, GenericTdcTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m thorlabs_cube.aqctl_thorlabs_cube "
            + "-p 3255 -P tdc001 --simulation"
        )
        try:
            self.cont = self.start_server("tdc", command, 3255)
        except:
            self.skipTest("Could not start server")

class TestKdcSim(GenericRPCCase, GenericKdcTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (sys.executable.replace("\\", "\\\\")
                            + " -m thorlabs_cube.aqctl_thorlabs_cube "
                            + "-p 3255 -P kdc101 --simulation")
        try:
            self.cont = self.start_server("kdc", command, 3255)
        except:
            self.skipTest("Could not start server")

class TestTpzSim(GenericRPCCase, GenericTpzTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m thorlabs_cube.aqctl_thorlabs_cube "
            + "-p 3255 -P tpz001 --simulation"
        )
        try:
            self.cont = self.start_server("tpz", command, 3255)
        except:
            self.skipTest("Could not start server")

class TestKpzSim(GenericRPCCase, GenericKpzTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m thorlabs_cube.aqctl_thorlabs_cube "
            + "-p 3255 -P kpz101 --simulation"
        )
        try:
            self.cont = self.start_server("kpz", command, 3255)
        except:
            self.skipTest("Could not start server")

class TestTpaSim(GenericRPCCase, GenericTpaTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (sys.executable.replace("\\", "\\\\")
                            + " -m thorlabs_cube.aqctl_thorlabs_cube "
                            + "-p 3255 -P tpa101 --simulation")
        try:
            self.cont = self.start_server("tpa", command, 3255)
        except:
            self.skipTest("Could not start server")

class TestKpaSim(GenericRPCCase, GenericKpaTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m thorlabs_cube.aqctl_thorlabs_cube "
            + "-p 3255 -P kpa101 --simulation"
        )
        try:
            self.cont = self.start_server("kpa", command, 3255)
        except Exception as e:
            self.skipTest(f"Could not start server: {e}")


class TestKpzSim(GenericRPCCase, GenericKpzTest):
    def setUp(self):
        GenericRPCCase.setUp(self)
        command = (
            sys.executable.replace("\\", "\\\\")
            + " -m thorlabs_cube.aqctl_thorlabs_cube "
            + "-p 3255 -P kpz101 --simulation"
        )
        try:
            self.cont = self.start_server("kpz", command, 3255)
        except:
            self.skipTest("Could not start server")
