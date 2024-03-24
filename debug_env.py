import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import sys
import gymnasium
sys.modules["gym"] = gymnasium
import pybullet as p
import matplotlib.pyplot as plt
from stable_baselines3 import SAC
from robotiqGymEnv import robotiqGymEnv
import numpy as np
import csv
from moviepy.editor import ImageSequenceClip

saved_dir = "evaluation"
file_name = "test1"
rend = True

def make_video(images, output_video_file):
        clip = ImageSequenceClip(list(images), fps=30)
        clip.write_videofile(output_video_file, codec="libx264")

def load_model(file_path):
    """
    Load the model from the given file path
    """
    return SAC.load(file_path)

def extract_data(env, model, obs):
    """
    Run the model prediction and extract data into arrays
    """
    position_action_data = []
    angle_action_data = []
    gripper_position_data = []
    gripper_angle_data = []
    gripper_velocity_data = []
    gripper_angular_velocity_data = []
    target_position_data = []
    target_angle_data = []
    target_velocity_data = []
    target_angular_velocity_data = []
    closest_point_data = []
    contact_force_data = []
    rewards_data = []
    done = False

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, rewards, done, info = env.step(action)
        # env.render()

        base_pos, base_orientation = p.getBasePositionAndOrientation(env._robotiq.robotiq_uid)
        target_pos, target_orientation = p.getBasePositionAndOrientation(env.blockUid)

        base_velocity, base_angular_velocity = p.getBaseVelocity(env._robotiq.robotiq_uid)
        target_velocity, target_angular_velocity = p.getBaseVelocity(env.blockUid)

        gripper_angle = p.getEulerFromQuaternion(base_orientation)
        target_angle = p.getEulerFromQuaternion(target_orientation)

        position_action_data.append(action[0:3])
        angle_action_data.append(action[3:6])
        gripper_position_data.append(base_pos)
        gripper_angle_data.append(gripper_angle)
        gripper_velocity_data.append(base_velocity)
        gripper_angular_velocity_data.append(base_angular_velocity)
        target_position_data.append(target_pos)
        target_angle_data.append(target_angle)
        target_velocity_data.append(target_velocity)
        target_angular_velocity_data.append(target_angular_velocity)
        closest_point_data.append(p.getClosestPoints(env._robotiq.robotiq_uid, env.blockUid, 100, -1, -1)[0][8])
        contact_force_data.append(env._contactinfo()[5])
        rewards_data.append(rewards)
    
    if rend:
        make_video(env._cam2_images, f"{saved_dir}/{file_name}.mp4")
    return position_action_data, angle_action_data, gripper_position_data, gripper_angle_data, gripper_velocity_data, gripper_angular_velocity_data, target_position_data, target_angle_data, target_velocity_data, target_angular_velocity_data, closest_point_data, contact_force_data, rewards_data

def plot_data(data, labels):
    """
    Plot the data using matplotlib
    """
    plt.figure()
    for d, label in zip(data, labels):
        plt.plot(d, label=label)
        plt.legend()

def save_to_csv(filename, data_dict):
    """
    Save data to CSV

    :param filename: Name of the file to save to
    :param data_dict: Dictionary containing labels as keys and data as values
    """

    # Get max length of rows for data arrays
    max_length = max(len(v) for v in data_dict.values())

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        headers = list(data_dict.keys())
        csv_writer.writerow(headers)

        # Write rows
        for i in range(max_length):
            row = [data_dict[header][i] if i < len(data_dict[header]) else "" for header in headers]
            csv_writer.writerow(row)

def main():
    """
    Main function to run the program
    """
    model_file = "models/WITH_TACTILE/model.zip"
    model = load_model(model_file)

    with robotiqGymEnv(render= rend, TACTILE=False) as env:
        obs = env.reset()
        position_action_data, angle_action_data, gripper_position_data, gripper_angle_data, gripper_velocity_data, gripper_angular_velocity_data, target_position_data, target_angle_data, target_velocity_data, target_angular_velocity_data, closest_point_data, contact_force_data, rewards_data = extract_data(env, model, obs)


    data_dict = {
        "x action": [data[0] for data in position_action_data],
        "y action": [data[1] for data in position_action_data],
        "z action": [data[2] for data in position_action_data],
        "roll action": [data[0] for data in angle_action_data],
        "pitch action": [data[1] for data in angle_action_data],
        "yaw action": [data[2] for data in angle_action_data],
        "x gripper": [data[0] for data in gripper_position_data],
        "y gripper": [data[1] for data in gripper_position_data],
        "z gripper": [data[2] for data in gripper_position_data],
        "roll gripper": [data[0] for data in gripper_angle_data],
        "pitch gripper": [data[1] for data in gripper_angle_data],
        "yaw gripper": [data[2] for data in gripper_angle_data],
        "x velocity gripper": [data[0] for data in gripper_velocity_data],
        "y velocity gripper": [data[1] for data in gripper_velocity_data],
        "z velocity gripper": [data[2] for data in gripper_velocity_data],
        "x angular velocity gripper": [data[0] for data in gripper_angular_velocity_data],
        "y angular velocity gripper": [data[1] for data in gripper_angular_velocity_data],
        "z angular velocity gripper": [data[2] for data in gripper_angular_velocity_data],
        "x target": [data[0] for data in target_position_data],
        "y target": [data[1] for data in target_position_data],
        "z target": [data[2] for data in target_position_data],
        "roll target": [data[0] for data in target_angle_data],
        "pitch target": [data[1] for data in target_angle_data],
        "yaw target": [data[2] for data in target_angle_data],
        "x velocity target": [data[0] for data in target_velocity_data],
        "y velocity target": [data[1] for data in target_velocity_data],
        "z velocity target": [data[2] for data in target_velocity_data],
        "x angular velocity target": [data[0] for data in target_angular_velocity_data],
        "y angular velocity target": [data[1] for data in target_angular_velocity_data],
        "z angular velocity target": [data[2] for data in target_angular_velocity_data],
        "closest distance": closest_point_data,
        "contact force": contact_force_data,
        "rewards": rewards_data
    }

    save_to_csv(f"{saved_dir}/{file_name}.csv", data_dict)


if __name__ == "__main__":
    main()
