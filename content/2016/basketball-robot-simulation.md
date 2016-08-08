Title: Software and Simulation
Slug: basketball-robot-simulation
Series: Basketball Robot
Project: True
Tags: ROS, Gazebo
Date: 2016-08-08

[Gazebo](http://gazebosim.org/) and [V-REP](http://www.coppeliarobotics.com/) are two of the most prominent simulation tools used by roboticists. I am inclined towards Gazebo. Gazebo is under active development and also has good tutorials and support through its online forum. Also, the integration with [ROS](http://www.ros.org/) is superb, and this makes it easier to integrate your robot into the simulation ecosystem. Gazebo also supports multiple physics engines too.

The software stack for the basketball robot is written using ROS with a mixture of C++ performing the low-level communication with the hardware and Python used to integrate the various components like optimization, plotting, simulation, etc. The communication to the arm is through a USB-to-Serial port.

[ROS-Control](https://github.com/ros-controls/ros_control) is a group of packages that expose a real-time control loop to communicate with the hardware. It also has lots of additional utilities that make it easier to write specific services and actions like joint trajectory control. I have extensively used ROS-Control for interfacing with the arms.

Simulation comes in handy when you are trying to optimize the parameters of the experiment. My experiments usually take ~12 hours to complete, but with it running on Gazebo, it concludes in ~3 hours and most importantly without any supervision. The initial task of getting the arms moving was very easy, but then getting it to pick up the ball was very hard to achieve. If you run the simulation without setting the right parameters for the ball, the moment the arm comes in contact with the ball, the arms start to jitter, and the arms will be unable to grip the ball.

The ball needs to be smooth for it work properly. Gazebo's primary physics engine ODE does provide some support for soft bodies. Other physics engines like Dart and Bullet has much better support for soft objects. ODE has two parameters `soft_cfm` and `soft_erp` that allow controlling the smoothness, but according to my knowledge these two parameters are currently unused and have no effect on the simulation. These two parameters are in turn calculated using `KP` and `KD` which are the spring stiffness and damping coefficients. These two parameters need to be chosen appropriately because if the ball is too smooth, then the contacts will sink through the ball. I was finally able to get the parameters right and run simulations without any trouble as you can see the results below.

https://youtu.be/vbEwS89Vjeo

### Links
1. [ROS Arm Driver](https://github.com/nikhilkalige/robotis_manipulator)
2. [Basketball Robot](https://github.com/nikhilkalige/basketball_robot)


