from cube import Cube
from mindstorms import MSHub, Motor
from mindstorms.control import wait_for_seconds, wait_until
from mindstorms.operator import equal_to


class Cubot:
    TURN_RATIO = 3  #  24 / 8

    def __init__(self):
        self.hub = MSHub()
        self.color_arm = Motor("D")
        self.grabbing_arm = Motor("E")
        self.turning_base = Motor("F")
        self.color_arm_home_pos = self.color_arm.get_position()
        self.grabbing_arm_home_pos = self.grabbing_arm.get_position()
        self.turning_base_home_pos = self.turning_base.get_position()
        self.last_rotation_direction = None

        for motor in [self.color_arm, self.grabbing_arm, self.turning_base]:
            motor.set_stop_action("brake")
            motor.set_stall_detection(True)

        self.cube = Cube()

    def reset_color_arm(self):
        self.color_arm.start_at_power(-30)
        wait_for_seconds(0.5)
        wait_until(self.color_arm.get_speed, equal_to, 0)
        self.color_arm.stop()
        self.color_arm_home_pos = self.color_arm.get_position()

    def reset_grabbing_arm(self):
        self.grabbing_arm.start_at_power(40)
        wait_for_seconds(1)
        wait_until(self.grabbing_arm.get_speed, equal_to, 0)
        self.grabbing_arm.stop()
        self.grabbing_arm_home_pos = self.grabbing_arm.get_position()

    def reset_turning_base(self):
        self.turning_base_home_pos = self.turning_base.get_position()

    def reset_all(self):
        self.reset_color_arm()
        self.reset_grabbing_arm()
        self.reset_turning_base()
        self.hub.light_matrix.show_image("SQUARE")
        wait_for_seconds(0.5)

    def _move_grabbing_arm_to_pos(self, pos, speed=70):
        target_position = self.grabbing_arm_home_pos + pos
        if target_position < 0:
            target_position += 360
        self.grabbing_arm.run_to_position(target_position, speed=speed)

    def grab(self):
        self.grabbing_arm.set_stop_action("hold")
        self._move_grabbing_arm_to_pos(-75)

    def tilt(self):
        self.grab()
        self._move_grabbing_arm_to_pos(-155)
        wait_for_seconds(0.05)
        self._move_grabbing_arm_to_pos(-55, 100)
        self._move_grabbing_arm_to_pos(-75)
        wait_for_seconds(0.05)
        self.cube.apply("F")

    def rest(self):
        self._move_grabbing_arm_to_pos(0, 40)
        self.grabbing_arm.set_stop_action("brake")

    @staticmethod
    def _check_direction(direction):
        assert direction in ["clockwise", "counterclockwise"]

    def rotate_cube(self, direction):
        Cubot._check_direction(direction)
        self.rest()
        self.turning_base.set_stop_action("hold")
        distance_in_degrees = Cubot.TURN_RATIO * 90
        if direction == "clockwise":
            distance_in_degrees = -distance_in_degrees
        self.turning_base.run_for_degrees(distance_in_degrees, 80)
        self.last_rotation_direction = direction
        if direction == "clockwise":
            self.cube.apply("U")
        else:
            self.cube.apply("U'")

    def turn_bottom_face(self, direction):
        Cubot._check_direction(direction)
        self.grab()
        self.turning_base.set_stop_action("hold")
        distance_in_degrees = Cubot.TURN_RATIO * 90
        extra_distance = Cubot.TURN_RATIO * 19
        if self.last_rotation_direction and self.last_rotation_direction != direction:
            extra_distance += Cubot.TURN_RATIO * 3
        if direction == "counterclockwise":
            distance_in_degrees = -distance_in_degrees
            extra_distance = -extra_distance
        self.turning_base.run_for_degrees(distance_in_degrees + extra_distance, 80)
        self.turning_base.run_for_degrees(-extra_distance, 80)
        self.last_rotation_direction = direction
        if direction == "clockwise":
            self.cube.apply("D")
        else:
            self.cube.apply("D'")


c = Cubot()
c.reset_all()
c.grab()
wait_for_seconds(0.2)
c.rest()
wait_for_seconds(0.2)
c.tilt()
wait_for_seconds(0.2)
c.rotate_cube("clockwise")
wait_for_seconds(0.2)
c.tilt()
wait_for_seconds(0.2)
c.rotate_cube("counterclockwise")
wait_for_seconds(0.2)
c.turn_bottom_face("clockwise")
wait_for_seconds(0.2)
c.rotate_cube("clockwise")
wait_for_seconds(0.2)
c.tilt()
wait_for_seconds(0.2)
c.turn_bottom_face("counterclockwise")
wait_for_seconds(0.2)
c.rest()
