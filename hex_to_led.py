'''This module is for converting hex input from user to RGB values and visualize it in two lesd's.
The latest input is give to LED 1 and state of LED 1 is transfered to LED2.
On power cut or on boot LED 2 restores its previous state''' 

import machine												#import necessary libraries

flag = 0													#flag for tracking user input, initializing it to 0 on each boot
rgbvalue = []												#RGB value array

rpwm = machine.PWM(machine.Pin(5))							#setting ip nessary pins as PWM
gpwm = machine.PWM(machine.Pin(15))
bpwm = machine.PWM(machine.Pin(4))

r2pwm = machine.PWM(machine.Pin(14))
g2pwm = machine.PWM(machine.Pin(12))
b2pwm = machine.PWM(machine.Pin(0))


def led():		
	'''This function turns on led based on user input.
	It takes the input after converting from hex to integer 
	from RGB array'''										
	length = len(rgbvalue)-1								#finding length of RGB array to know the number of inputs

	if length < 5:											#turning on led2 in its previous state
    	r2pwm.duty(rgbvalue[0])
    	g2pwm.duty(rgbvalue[1])
    	b2pwm.duty(rgbvalue[2])

	if length >= 5:											#turning on led1 and led2 based on the inputs
    	rpwm.duty(rgbvalue[-6])
    	gpwm.duty(rgbvalue[-5])
    	bpwm.duty(rgbvalue[-4])

    	r2pwm.duty(rgbvalue[-3])
    	g2pwm.duty(rgbvalue[-2])
    	b2pwm.duty(rgbvalue[-1])


def hex_to_rgb_convert():									#function to conver hex value to integer in initial state
	'''This function converts the hex value of led2
	from its previous state when there is restart of 
	module'''
	with open("data.txt", "r") as file:						#reading previous state of led 2 from file for restoration 
    	filedata = file.readlines()
    	led1 = filedata[-2]

	for i in range(1, 7, 2):								#converting hex value to integer
    	color = int(led1[i:i+2], 16)
    	rgbvalue.append(color)								#appending it to RGB value array

	print("for initial led 2", led1)
	led()													#calling led function to update colors on led


def hex_to_rgb_convert_input():								#function to convert hex to integer in interaction/updation state 
	'''This function converts the hex value of user input 
	and stores in RGB array'''
	if(flag < 2):											#flag to check if this is first user input
    	with open("data.txt", "r") as file:					#reading values from file and converting to integer for led 1 and 2
        	filedata = file.readlines()
        	led1 = filedata[-1]
        	led2 = filedata[-3]								#as this is first input after restoration, no change in led2

    	for i in range(1, 7, 2):
        	color = int(led1[i:i+2], 16)
        	rgbvalue.append(color)

    	print("for led1 after 1st value", led1)
    	led()

    	for i in range(1, 7, 2):
    	    color = int(led2[i:i+2], 16)
    	    rgbvalue.append(color)

    	print("for led2 after 1st value", led2)
    	led()

	else:													#if the present input is not first user input, continuing the flow

    	with open("data.txt", "r") as file:
        	filedata = file.readlines()
        	led1 = filedata[-1]
        	led2 = filedata[-2]								#from second input value of led 1 is passed to led 2 

    	for i in range(1, 7, 2):
        	col = int(led1[i:i+2], 16)
        	rgbvalue.append(col)

    	print("for led1 after 2nd value", led1)
    	led()

    	for i in range(1, 7, 2):
        	col = int(led2[i:i+2], 16)
        	rgbvalue.append(col)

    	print("for led2 after 2nd value", led2)
    	led()


hex_to_rgb_convert()										#calling the hex to integer converter function to restore initial value on boot

while(True):												#prompting for continous user inputs and writing into file

	flag += 1												#updating flag value on user input
	hexvalue = input("Enter hex value")

	with open("data.txt", "a") as file:
	    file.write(hexvalue+"\n")
	hex_to_rgb_convert_input()								
