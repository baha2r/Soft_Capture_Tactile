The primary objective of this study is to demonstrate the significance of utilizing tactile sensors during the soft-capture phase of grasping. To highlight this, we compare two identical agents that differ in only one aspect to observe how this singular difference influences the training outcomes. One agent is equipped with tactile sensors, thereby incorporating the normal contact force applied to the robotic gripper within its state information, whereas the other agent lacks this feature. 
# Training Schematic 
<img width="1063" alt="Screenshot 2024-03-31 at 1 10 19 AM" src="https://github.com/baha2r/Soft_Capture_Tactile/assets/75396051/33082b74-9442-48d7-866a-71c87cf75a13">

# Results 
<img width="1270" alt="Screenshot 2024-03-31 at 1 12 19 AM" src="https://github.com/baha2r/Soft_Capture_Tactile/assets/75396051/86a73c96-97e0-4bf5-9698-1faea24d3896">

# Reward and SuccessRate Comparison
![image](https://github.com/baha2r/Soft_Capture_Tactile/assets/75396051/516051b1-5d17-4f47-8db7-5915435ff51f)

# TACTILE Sensor Feedback Random Episode
[WITH_TACTILE](evaluation/WITH_TACTILE)
Here is sample episode:
[Sample Episode With Tactile](evaluation/WITH_TACTILE/test1.mp4)

# NO TACTILE Sensor Feedback Random Episode
[WITHOUT_TACTILE](evaluation/WITHOUT_TACTILE)
Here is sample episode:
[Sample Episode With no Tactile](evaluation/WITHOUT_TACTILE/test3.mp4)

# Observation Space
The state representation for each agent combines several parameters: the pose and velocity of the gripper, the pose and velocity of the target, their respective differences, and the minimum distance in each direction between them, all defined within the inertial frame. Consequently, this results in a 39-dimensional state space for the agent without access to contact force data. In contrast, the other agent's state space is 40-dimensional, including an additional dimension for the cumulative normal contact force exerted on the gripper.
The observation space for the robotic arm environment is represented by the configuration, Box(-inf, inf, (40,), float32) or Box(-inf, inf, (40,), float32). This space consists of a set of variables, each describing a distinct attribute related to the position, movement, and velocity of both the robotic gripper and its target. These variables embody an extensive range of information about the environment, capturing the dynamism and intricacies involved in the manipulative tasks of the robotic arm. 

The table provided below offers a comprehensive overview of each variable within the observation space. It outlines not only the variable itself, but also the corresponding limits and the unit of measurement used. This range from negative infinity to positive infinity underscores the continuous nature of these variables, further emphasizing the complexity of the tasks and movements this robotic arm is designed to perform.
[Observation Space](evaluation/State_Space.md)

# Action Space
The action space is defined within a Box(-1.0, 1.0, (6,), float32), which encapsulates the absolute position and orientation of the 3f RobotiQ gripper when functioning as an end-effector. Control actions are enforced by modulating the physical motion of the gripper's base across six degrees of freedom (6dof). This comprises three translational (linear) and three rotational (angular) movements that are executed by the robotic manipulator through inverse kinematics. For compatibility purposes, control action inputs are scaled to a range between -1 and 1. The elements of the action array are as follows:

[Action Space](evaluation/Action_Space.md)
# Rewards
In this work, we introduce a novel reward function that integrates both dense and sparse rewards, aiming to address the challenge of precisely approaching to grasp a moving, floating object. The agent employs the dense reward component to ascertain the appropriate approach towards the target, while simultaneously maintaining its position and orientation. Subsequently, the sparse reward aspect of the reward function provides guidance to maintain an optimal posture, preserve a safe distance between the gripper and the target, and ultimately prevent contact with the target.

# Episode End
The episode will be truncated when the duration reaches a total of max_episode_steps which by default is set to 500 timesteps. The episode is never terminated since the task is continuing with an infinite horizon.



