Title: Hardware Design
Slug: bike-pov-hardware-design
Series: Bike POV
Project: True
Tags: PCB, Arm
Date: 2016-08-6

Bike POV is a design to create fancy animation on a bicycle wheel by mounting multiple RGB LED's. Persistence of vision (POV) is a phenomenon by which multiple images which are moving fast combine to form a single image in the human brain. POV's for bicycle wheels are not new, and there are already tried and tested products that you can buy that are pricey. I am an electronics engineer, and I love twiddling with circuits and buying one of the shelves at least in this case would be no fun. I am documenting the development process in this post and a few other posts in the future.

##Drawing Board
I had first thoughts about designing this when I came across a product on the internet, and I was fascinated by it, and I wanted to show off similar disco lights on my bike too as I rode through to college. I initially started with a four arm design that would have a total of 256 LED's, but then I felt that would make it complicated with regards to inter-board connections. As a result, I decided on a two arm board design with 128 LED's, i.e. 64 LED's per arm with 32 on each face of the board.

![Bike POV mounted on a wheel]({filename}/images/2016/bike-pov-render.png)

##PCB Design
[Eagle](https://cadsoft.io/) has been the standard PCB design tool used by hobbyists for a long period, and currently there are is a lot of work going on [KiCAD](http://kicad-pcb.org/), a open source initiative. I have never tried KiCAD, but I have been using Eagle for a long time. During the time I started with this design, I came across [CircuitMaker](http://circuitmaker.com/) from [Altium](http://www.altium.com/) that was still in the early beta stages. I had tried Altium in the past, and the similarities between the two tools convinced me to take it for a spin, and I went ahead and designed the board with CircuitMaker. I would say that I am impressed with the tools that are provided by the software, and I definitely would recommend you to try it as long as you are not paranoid about your data being on the cloud.

##System Design
At the core is a Cortex-M4 microcontroller [STM32F411RET6](http://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32f4-series/stm32f411/stm32f411re.html) from STMicoelectroincs. It runs at 100MHz and has 128 kB of RAM and 512 kB of flash. The deal breaker was that it was the same chip that was used in a Nucleo development board, and this would help me in prototyping my code. The power supply was designed using [TPS62095](http://www.ti.com/product/TPS62095RGTR) from Texas Instruments. It is buck regulator capable of delivering 4A and can operate on 5V input power supply. Since we will be driving LED's and we do not have the necessary io's to directly control, I used [TLC5955](http://www.ti.com/product/TLC5955DCAR) also from Texas Instruments. TLC5955 is 48 channel LED driver with brightness control, and it can control 16 RGB LED's. I used a hall effect sensor to monitor the speed of the wheel. I also had a MPU6050 included so that I could also use the gyroscope to measure the speed. I additionally added a few features like a sd card and few pinouts for supporting a Bluetooth module.

I got the PCB manufactured by Seeedstudio, and you can see the results below.

![Rendered PCB - Top]({filename}/images/2016/bike-pov-top.png)

![Rendered PCB - Bottom]({filename}/images/2016/bike-pov-bottom.png)
