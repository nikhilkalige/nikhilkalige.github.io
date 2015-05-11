Title: UEFI with BeagleBoard on Ubuntu using Qemu
Category: UEFI
Tags: UEFI, Beagleboard, FreeRTOS, Qemu
Slug: uefi-with-beagleboard-using-qemu
Summary: Develop an UEFI osloader that is capable of loading a FreeRTOS application on Beagleboard using Qemu


[Unified Extensible Firmware Interface(UEFI)](http://www.uefi.org/ "UEFI") is the new standard that is being developed in order to replace BIOS. UEFI was first developed by Intel and was later joined by other organizations.  All the open source components of Intel's implementation of UEFI is currently hosted at [tianocore](http://www.tianocore.org/ "Tianocore") website. [EDK II](http://www.tianocore.org/edk2/ "EDK2")  is a modern, feature-rich, cross-platform firmware development environment for the UEFI and PI specifications.

In this article, we will be going over how to setup edk2 for beagleboard on Ubuntu 14.04. I will be using qemu in order to simulate beagleboard. Finally we will develop an osloader that can load a [FreeRTOS](www.freertos.org "FreeRTOS") application.

###  Creating SdCard Image
In order to boot beagleboard, we need the sdcard image with u-boot in it. We will be using **linaro image creator** to create the image file. Linaro group maintains a ppa from which we can install these tools.
```shell-session
user@bash:$ sudo add-apt-repository ppa:linaro-maintainers/tools
user@bash:$ sudo apt-get update
user@bash:$ sudo apt-get install linaro-image-tools
```

We also need a few additional files to create the image.
```shell-session
user@bash:$ wget http://releases.linaro.org/platform/linaro-m/hwpacks/final/hwpack_linaro-omap3_20101109-1_armel_supported.tar.gz
user@bash:$ wget http://releases.linaro.org/platform/linaro-m/headless/release-candidate/linaro-m-headless-tar-20101101-0.tar.gz
```
Now we can create the sdcard image file with the following commands
```shell-session
user@bash:$ sudo linaro-media-create --image_file beagle_sd.img --dev beagle --binary linaro-m-headless-tar-20101101-0.tar.gz --hwpack hwpack_linaro-omap3_20101109-1_armel_supported.tar.gz
```
This will create a `beagle_sd.img` image file in your current directory.

### Mounting SdCard Image
I spent some time trying to figure out how to mount the sdcard to access the files. I have listed the commands used to mount the sdcard.
```shell-session
user@bash:$ fdisk -l beagle_sd.img
        Device Boot      Start         End      Blocks   Id  System
beagle_sd.img1   *          63      106494       53216    c  W95 FAT32 (LBA)
beagle_sd.img2          106496     6291455     3092480   83  Linux
user@bash:$ mkdir /tmp/beagle
user@bash:$ sudo mount -o loop,offset=$[63*512] beagle_sd.img /tmp/beagle
```

You will notice that the value I used in `$[63*512]` is the same value I get from `fdisk` command under `Start`. So you should replace 63 by the value you get.

The mounted sd card has the following files
```shell-session
boot.ini  boot.scr  boot.txt  MLO  u-boot.bin  uImage  uInitrd
```

### Install Qemu
Installing Qemu in Ubuntu is very easy as it exists in the system repository. But the main qemu branch does not support beagleboard. Linaro has forked qemu and they have added support for beagle board in their release. I was unable to find a ppa for that release. We need to install it from the [source](git://git.linaro.org/qemu/qemu-linaro.git "linaro qemu"), but if you install the latest release which is currently at `0677e6e`, you will be able to boot the system but you will be unable to browse the contents of the sdcard which is essential if you need to run an UEFI application.

I found that a older version of the code works and you can download the zip file from [here](https://launchpad.net/~linaro-maintainers/+archive/ubuntu/tools/+files/qemu-linaro_1.5.0-2013.06+git74+20130802+ef1b0ae.orig.tar.bz2 "linaro-qemu zip"). Extract the file and then use the below commands to install qemu. If you directly use the below commands, the build will fail with an error related to `fdt32_t`. So you have to patch `include/libfdt_env.h` file by adding the below lines after line 22.
``` C
#ifdef __CHECKER__
    #define __force __attribute__((force))
    #define __bitwise __attribute__((bitwise))
#else
    #define __force
    #define __bitwise
#endif

typedef uint16_t __bitwise fdt16_t;
typedef uint32_t __bitwise fdt32_t;
typedef uint64_t __bitwise fdt64_t;
```

``` shell-session
user@bash:$ sudo apt-get build-dep qemu
user@bash:$ ./configure --target-list=arm-softmmu --prefix=$HOME/qemu
user@bash:$ make 
user@bash:$ make install
```
The above commands will install qemu into `qemu` folder in your home directory. Now add the directory to you path by editing your `.bashrc` file.
``` shell-session
PATH=$PATH:~/qemu/bin
```
Now `qemu-system-arm` command should be available at prompt.
``` shell-session
user@bash:$ qemu-system-arm --version
QEMU emulator version 1.5.0 (qemu-linaro from git), Copyright (c) 2003-2008 Fabrice Bellard
```

### Testing Qemu
At this point, we can test whether qemu is working with the sd card image we generated. When you run the below command you should get the u-boot prompt.
``` shell-session 
user@bash:$ qemu-system-arm -M beagle -sd beagle_sd.img -serial stdio -clock unix
Texas Instruments X-Loader 1.4.4ss (Sep 30 2010 - 14:44:32)
Beagle Rev C4
Reading boot sector
Loading u-boot.bin from mmc
```

### Building UEFI
In order to build UEFI, we need the Arm toolchain. Follow the simple instructions below and you should be able to generate the  file without any trouble.
``` shell-session
user@bash:$ sudo apt-get install gcc-arm-linux-gnueabi
user@bash:$ gcc-arm-linux-gnueabi --version
arm-linux-gnueabi-gcc (Ubuntu/Linaro 4.7.3-12ubuntu1) 4.7.3
user@bash:$ git clone https://github.com/tianocore/edk2.git
user@bash:$ cd edk2
user@bash:$ source edksetup.sh
user@bash:$ cd BeagleBoardPkg
user@bash:$ ./build.sh
user@bash:$ ls ../Build/BeagleBoard/DEBUG_ARMLINUXGCC/FV/
```
 
Now you should be able to see `BEAGLEBOARD_EFI.FD` which is the file we will be using to boot UEFI. 

Mount the sdcard using the commands that were given in the beginning. Now we need to replace the `u-boot.bin` file with the `BEAGLEBOARD_EFI.fd` file in the sdcard. Lets now start UEFI on the beagle board.

```shell-session
user@bash:$ qemu-system-arm -M beagle -sd beagle_sd.img -serial stdio -clock unix 
```
This will start the qemu and after that it prints some gibberish and then you should get the boot selection option of UEFI.
```
The default boot selection will start in   5 seconds
[1] Linux from SD
......
[2] Shell
[3] Boot Manager
Start: 
```
If you get some lines  saying `SD: CMD12 in a wrong state` just ignore them. We need to enter the shell, so enter `2` to select the shell. This will output the Mapping table and the important thing to note here is that you should have a `FS0:` entry. If you did not get that then you are doing something wrong. 

I had some problem with the number of lines that the shell could print, so you can use `mode 100 31` to fix this. You can use  `cls`  to clear the screen. 

### Building FreeRTOS and OSLoader
FreeRTOS is a simple real time operating system suited for small and medium sized micro-controllers. I was not the one who ported FreeRTOS on to beagleboard, here I will be only going over the changes I had to make in order for it work with UEFI. 

UEFI defines a simple set of instructions to build a osloader. 

- Load the application in to the memory.
- Call `GetMemoryMap()` to get the memory map and the key
- Call `ExitBootServices()` to stop the boot time services provided by UEFI.
- Now transfer control to the application

So it is as simple as that.

We need to install [CodeSourcery toolchain](http://www.mentor.com/embedded-software/sourcery-tools/sourcery-codebench/editions/lite-edition/ "Mentor Graphics Codebench") to be able to compile the FreeRTOS code. I downloaded the lite version and installed it and added it to my path. If you did this right at the end you should be able to run the below command.
``` shell-session
user@bash:$ arm-none-eabi-gcc --version
arm-none-eabi-gcc (Sourcery CodeBench 2014.11-36) 4.9.1
Copyright (C) 2014 Free Software Foundation, Inc.
```

I have put up the source code for this project on [github](https://github.com/NikhilKalige/uefi_freertos_beagleboard "UEFI Beagleboard"). I also have added the instructions needed to compile the FreeRTOS and UEFI application in the readme. 

### Loading Application in to memory
Compiling FreeRTOS will generate an `elf` file and we need to load this file in to the memory. Elf file has a very simple file format and `readelf` is command that is very handy. Elf has a main header that holds the gist of the overall file and it also holds the pointers to other sections. Elf has different kinds of sections but we are interested only in the program section. The osloader just loops over all the program headers and loads the content starting at the virtual address. The virtual address value can obtained from `p_vaddr` variable in the elf header. The header also has one more important parameter and that is the entry point (`e_entry`). This points to the location from which the code should start executing. 

UEFI has two kinds of services boot time and run time services. The OS cannot use the boot time services but it can make use of the run time services that are provided. So we need to provide a pointer to the structure.
``` C
/** Function pointer to FreeRTOS main  */
typedef VOID (*freertos_elf)(EFI_RUNTIME_SERVICES* runtime);

/** Inside main */
/** declare function ptr */
freertos_elf start_elf;
.... 
/** Jump to the entry point */
start_elf = (freertos_elf)EntryPoint;
start_elf(gRT);
```
The above code should be self explanatory. The 1st lines defines a function pointer to the main with a pointer to the UEFI runtime services as a parameter.  The start address of the FreeRTOS application is held by the `Entrypoint` variable. Finally you just call the function and this should start the FreeRTOS app.

### FreeRTOS Modifications
I had to make a few modifications to the FreeRTOS application for it to work. 

You need to include `UEFI.h` and modify the main function declaration so that it can accept the UEFI runtime services pointer. 
``` C
#include <Uefi.h>
EFI_RUNTIME_SERVICES  *uefi_services;
int main(void *pointer) {
    uefi_services = (EFI_RUNTIME_SERVICES*)pointer;
```

ARM has two modes of operation **ARM** and **Thumb** mode. When you jump from UEFI it seems to be in thumb mode whereas our application was compiled in arm mode. So we basically check and  then make a switch to arm mode if needed. The pointer value also needs to stored as we will be using the registers for other operations.
``` Assembly
/** Application code starts here */
start:
_start:r 
_mainCRTStartup:
    .thumb
thumb_entry_point:
    blx arm_entry_point
    .arm
arm_entry_point:
    /* store runtime pointer in r10 */
    mov r10, r0 
    ....
    /* Load the pointer back to r0 */
    mov r0, r10
    mov r1, #0          /* no argv either */
    bl  main
```
The exception vector table that is responsible for handling interrupts in ARM can be moved around. UEFI uses a different location and in order for our interrupts to work we need to relocate the vector table address.
```
ldr   r0, =0x40014000
mcr   p15, 0, r0, c12, c0, 0
mrc   p15, 0, r1, c12, c0, 0
```

### Debugging UEFI
We will be using `arm-none-eabi-gdb` to debug UEFI code on qemu. Gdb needs UEFI core application symbols and also you need add those of the application you developed. When you start qemu you will get a log at the beginning that looks like this.
```
add-symbol-file path-to-edk2/Build/BeagleBoard/DEBUG_ARMLINUXGCC/ARM/Omap35xxPkg/MmcHostDxe/MmcHostDxe/DEBUG/MMC.dll 0x87AD0240 
```
You should see a number of lines that show the path and address for different `dll` files. You can either copy all those lines to a file and run the below command to load it or else you can just copy and paste it at the gdb prompt.
```
(gdb) source filename
```
Finally you need to add the symbol for your UEFI  and freertos application. You can load the freertos symbols using
```
(gdb) add-symbol-file path-to-file/rtosdemo.elf 0x80300000
```
Copy  `rtosdemo.elf` and  `osloader.efi` file to the sdcard and then start qemu but now add `-s` to enable debugging using gdb. Connect gdb to qemu with the below command
```
(gdb) target remote :1234
```
You should get the UEFI shell prompt as was shown above. Now we just need to run the osloader.
```
Shell> fs0:
FS0:\> osloader.efi
add-symbol-file path-to-file/osloader.dll 0x86E04240
```
Copy the above line and paste it in to gdb and you should be able set the breakpoints and step in and out of the code.

### Conclusion
I wrote this long post hoping that it will help anybody the trouble I went though to get to this point. When I started, I had problems getting qemu to work, after that point I did not have any idea about how to get gdb to debug my code. Finally I had problems with ARM FreeRTOS application, mainly with regards to the thumb mode and the vector table address. 

Please send me a mail if you need any additional info or if you find any mistakes.

### References and Links
1. [Tianocore](https://github.com/tianocore/edk2 "Tianocore")
2. [Building Linaro Qemu](http://wiki.minix3.org/doku.php?id=developersguide:minixonlinaroqemuarm "Build Linaro")
3. [Tianocore Beagleboard](http://tianocore.sourceforge.net/wiki/BeagleBoardPkg "beagleboard tianocore")
4. [UEFI Bootloader](https://github.com/fgken/uefi-bootloader "UEFI Bootloader")
5. [Source Code](https://github.com/NikhilKalige/uefi_freertos_beagleboard "UEFI freertos beagleboard")






