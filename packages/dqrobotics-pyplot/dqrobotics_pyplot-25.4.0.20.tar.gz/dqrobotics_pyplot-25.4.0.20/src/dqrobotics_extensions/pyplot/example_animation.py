"""
Copyright (C) 2025 Murilo Marques Marinho (www.murilomarinho.info)

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Auhor: Murilo M. Marinho
"""
import numpy as np

from dqrobotics import *
from dqrobotics.robots import KukaLw4Robot
from dqrobotics.robot_control import DQ_PseudoinverseController, ControlObjective

# Adding the prefix `dqp` to help users differentiate from `plt`
import dqrobotics_extensions.pyplot as dqp

import matplotlib.pyplot as plt
import matplotlib.animation as anm # Matplotlib animation
from functools import partial # Need to call functions correctly for matplotlib animations

# Animation function
def animate_robot(n, robot, stored_q, xd, stored_time):
    """
    Create an animation function compatible with `plt`.
    Adapted from https://marinholab.github.io/OpenExecutableBooksRobotics//lesson-dq8-optimization-based-robot-control.
    :param n:
    :param robot:
    :param stored_q:
    :param xd:
    :param stored_time:
    :return:
    """
    dof = robot.get_dim_configuration_space()

    plt.cla()
    dqp.plot(robot, q=stored_q[n])
    dqp.plot(xd)
    plt.xlabel('x [m]')
    plt.xlim([-2, 2])
    plt.ylabel('y [m]')
    plt.ylim([-2, 2])
    plt.gca().set_zlabel('z [m]')
    plt.gca().set_zlim([0, 2])
    plt.title(f'Translation control time={stored_time[n]:.2f} s out of {stored_time[-1]:.2f} s')

def main():

    # Set up plot
    fig = plt.figure()
    plt.axes(projection='3d')

    # Move the robot and store the data
    # Define the robot
    robot = KukaLw4Robot.kinematics()
    # Define the controller
    translation_controller = DQ_PseudoinverseController(robot)
    translation_controller.set_control_objective(ControlObjective.Translation)
    translation_controller.set_gain(100)
    translation_controller.set_damping(0.1)

    # Desired translation (pure quaternion)
    td = 1 * j_
    # Sampling time [s]
    tau = 0.01
    # Simulation time [s]
    time_final = 1
    # Initial joint values [rad]
    q = np.zeros(7)
    # Store the control signals
    stored_q = []
    stored_time = []

    # Translation controller loop.
    for time in np.arange(0, time_final + tau, tau):
        # Output to console
        print(f"Simulation at time = {time}")

        # Store data for posterior animation
        stored_q.append(q)
        stored_time.append(time)

        # Get the next control signal [rad/s]
        u = translation_controller.compute_setpoint_control_signal(q, vec4(td))

        print(f"u={u} for {td} and fkm={translation(robot.fkm(q))}")

        # Move the robot
        q = q + u * tau

    anim = anm.FuncAnimation(fig,
                      partial(animate_robot,
                              robot=robot,
                              stored_q=stored_q,
                              xd=1 + 0.5 * E_ * td,
                              stored_time=stored_time),
                      frames=len(stored_q))

    plt.show()

if __name__ == "__main__":
    main()