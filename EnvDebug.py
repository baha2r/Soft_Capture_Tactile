import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import sys
import gymnasium
sys.modules["gym"] = gymnasium
import numpy as np
import matplotlib.pyplot as plt
import pybullet as p
from robotiqGymEnv import robotiqGymEnv



def main():

  env = robotiqGymEnv(render=False)

  dones = False
  obs = env.reset()
 
  while not dones:
    action = [1 , 0 , 0 , 0 , 0 , 0 ]
    # else:
    #   action = [0 , 0 , 0 , 0 , 0 , 0 ]
    # action = env.action_space.sample()
    # action = [0 , 0 , 0 , 0 , 0 , 0]
    obs, rewards, dones, info = env.step(action)
    # targetspeed = p.getBaseVelocity(env.blockUid)
    # print(p.getAABB(env.blockUid))
    # print((p.getBasePositionAndOrientation(env._robotiq.robotiqUid)[1]))
    # print(p.getBasePositionAndOrientation(env.blockUid)[0])
    # print(p.getBaseVelocity(env.blockUid)[0])
    print(p.getBaseVelocity(env._robotiq.robotiq_uid)[0])
    # print(targetspeed)
    # print(len(env._robotiq.linkpos))
    # print(env._contactinfo()[4])
    # env.render()


if __name__ == "__main__":
  main()