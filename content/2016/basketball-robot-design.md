Title: Hardware Design
Slug: basketball-robot-design
Series: Basketball Robot
Project: True
Tags: Robot, Machine-Learning, AAAI
Date: 2016-08-07

Robots are performing complex tasks now which would have been considered not possible a few years back. Robots need a mixture of hardware and software skills that appeal to me as an electronics engineer similar to the embedded systems field. So when the time came for me to decide on a topic for my master's thesis, I was euphoric when me and my advisor [Dr.Heni Ben Amor](http://henibenamor.weebly.com/) decided on building a basketball playing robot.

Single armed robots have seen a lot of research in the past and the present. Dual-armed robots like Baxter are currently used in a lot of research. Our lab already had a Baxter, but the task at hand needed a machine capable of delivering more agility than you can get from a Baxter. Robots are expensive, and I had to choose the components such that any student in the future could also utilize it for his research experiments.

[Dynamixel](http://www.robotis.com/xe/dynamixel_en) servos from [Robotis](http://en.robotis.com/index/) are one of the standard servos used in the research field. [Dynamixel Pro](http://www.robotis.com/xe/DynamixelPro_en) servos provide better precision than their older counterpart. We decided on using the Manipulator-H arms that use Dynamixel Pro servos as their engine. These servos have an accuracy of ~0.0007 degrees and rotate at a speed of 180 degrees/second. The arms are capable of lifting a load of 5 kg.

### Pasta Robot Demo at AAAI-2016
https://youtu.be/17umg0rEZbU

I made use of Bosch Aluminium Profiles to design the stand that could stably support the arms and not tip over during the high speed throwing motion. I also added a big red emergency stop button to keep my professor happy. The rendered images of the model are below.

![Basketball Robot - Front View]({filename}/images/2016/basketball-robot-front.jpg)

![Basketball Robot - Perspective View]({filename}/images/2016/basketball-robot-perspective.jpg)

