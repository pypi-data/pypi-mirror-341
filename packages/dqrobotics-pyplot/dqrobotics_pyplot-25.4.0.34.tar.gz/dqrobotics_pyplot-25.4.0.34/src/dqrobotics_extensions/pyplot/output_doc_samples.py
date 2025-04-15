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
from dqrobotics import *
from dqrobotics.robots import KukaLw4Robot
from dqrobotics.utils.DQ_Math import deg2rad

# Adding the prefix `dqp` to help users differentiate from `plt`
import dqrobotics_extensions.pyplot as dqp

from matplotlib import pyplot as plt

from math import sin, cos, pi

def main():

    output_poses()
    output_lines()
    output_planes()

def _set_plot_labels():
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.gca().set_zlabel('z [m]')


def _set_plot_limits():
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.gca().set_zlim([-0.5, 0.5])

def output_poses():

    # x1
    t1 = 0
    r1 = 1
    x1 = r1 + 0.5 * E_ * t1 * r1

    # x2
    t2 = 0.1 * j_
    r2 = cos(pi / 4) + i_ * sin(pi / 4)
    x2 = r2 + 0.5 * E_ * t2 * r2

    # x3
    t3 = - 0.1 * k_ + 0.2 * i_
    r3 = cos(pi / 32) + k_ * sin(pi / 32)
    x3 = r3 + 0.5 * E_ * t3 * r3

    # x4
    x4 = x1 * x2 * x3

    # Plot using subplot
    fig = plt.figure(figsize=(12, 10))

    pose_list = [x1, x2, x3, x4]

    for i in range(0, len(pose_list)):
        x = pose_list[i]

        ax = plt.subplot(2, 2, i+1, projection='3d')
        dqp.plot(x)
        ax.title.set_text(rf'$\boldsymbol{{x}}_{i}$')
        _set_plot_labels()
        _set_plot_limits()

    fig.tight_layout()
    plt.savefig("output_poses.png")

def output_lines():
    """
    Underline unfortunately does not work well on mathtex and playing with latex distributions for this purpose is a bit
    much right now.
    Hopefully this gets added https://github.com/matplotlib/matplotlib/issues/14235
    so that titles can get the underline.
    """

    # l1
    l1 = i_
    m1 = cross(-0.1 * j_, l1)
    l1_dq = l1 + E_ * m1

    # l2
    l2 = j_
    m2 = cross(0.3 * k_, l2)
    l2_dq = l2 + E_ * m2

    # l3
    l3 = k_
    m3 = cross(0.2 * i_, l3)
    l3_dq = l3 + E_ * m3

    # l4
    l4 = j_
    m4 = 0
    l4_dq = l4 + E_ * m4

    # Plot using subplot
    fig = plt.figure(figsize=(12, 10))

    line_list = [l1_dq, l2_dq, l3_dq, l4_dq]
    color_list = ['r-', 'k-', 'g-', 'c-.']

    for i in range(0, len(line_list)):
        l_dq = line_list[i]
        color = color_list[i]

        ax = plt.subplot(2, 2, i+1, projection='3d')
        dqp.plot(l_dq, line=True, scale=0.5, color=color)
        ax.title.set_text(rf'$\boldsymbol{{l}}_{i}$')
        _set_plot_labels()
        _set_plot_limits()

    fig.tight_layout()
    plt.savefig("output_lines.png")

def output_planes():
    """
    Same underline issue as mentioned in `output_lines`.
    """

    # l1
    n1_pi = i_
    d1_pi = 0.1
    pi1_dq = n1_pi + E_ * d1_pi

    # l2
    n2_pi = j_
    d2_pi = -0.1
    pi2_dq = n2_pi + E_ * d2_pi

    # l3
    n3_pi = k_
    d3_pi = 0.2
    pi3_dq = n3_pi + E_ * d3_pi

    # l4
    n4_pi = normalize(i_ + j_ + k_)
    d4_pi = 0
    pi4_dq = n4_pi + E_ * d4_pi

    # Plot using subplot
    fig = plt.figure(figsize=(12, 10))

    plane_list = [pi1_dq, pi2_dq, pi3_dq, pi4_dq]
    color_list = ['r', 'k', 'g', 'c']

    for i in range(0, len(plane_list)):
        pi_dq = plane_list[i]
        color = color_list[i]

        ax = plt.subplot(2, 2, i+1, projection='3d')
        dqp.plot(pi_dq, plane=True, scale=0.5, color=color)
        ax.title.set_text(rf'$\boldsymbol{{\pi}}_{i}$')
        _set_plot_labels()
        _set_plot_limits()

    fig.tight_layout()
    plt.show()
    plt.savefig("output_planes.png")

if __name__ == "__main__":
    main()

