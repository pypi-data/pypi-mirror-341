from typing import List, Tuple
from loco_mujoco.environments import LocoEnv
from loco_mujoco.core.utils import info_property


class BaseRobotHumanoid(LocoEnv):
    """
    Base Class for the Humanoid robots.

    """

    @info_property
    def sites_for_mimic(self) -> List[str]:
        """
        Returns the default sites that are used for mimic.

        Returns:
            List[str]: List of site names.

        """
        return ["upper_body_mimic", "head_mimic", "pelvis_mimic",
                "left_shoulder_mimic", "left_elbow_mimic", "left_hand_mimic",
                "left_hip_mimic", "left_knee_mimic", "left_foot_mimic",
                "right_shoulder_mimic", "right_elbow_mimic", "right_hand_mimic",
                "right_hip_mimic", "right_knee_mimic", "right_foot_mimic"]

    @info_property
    def root_body_name(self) -> str:
        """
        Returns the name of the root body of the robot in the MuJoCo xml.

        """
        return "pelvis"

    @info_property
    def goal_visualization_arrow_offset(self) -> Tuple[float, float, float]:
        """
        Returns the offset for the goal visualization arrow. This corresponds to the offset from the
        root body of the robot.

        """
        return [0, 0, 0.6]
