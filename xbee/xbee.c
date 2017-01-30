/********************************************************************************
 Written by: Vinod Desai, NEX Robotics Pvt. Ltd.
 Edited by: Sachitanand Malewar, NEX Robotics Pvt. Ltd.
 AVR Studio Version 4.17, Build 666

 Date: 26th December 2010

 Application example: Robot control over serial port via XBee wireless communication module 
 					  (located on the ATMEGA260 microcontroller adaptor board)

 Concepts covered:  serial communication
 
 Serial Port used: UART0

 There are two components to the motion control:
 1. Direction control using pins PORTA0 to PORTA3
 2. Velocity control by PWM on pins PL3 and PL4 using OC5A and OC5B.

 In this experiment for the simplicity PL3 and PL4 are kept at logic 1.
 
 Pins for PWM are kept at logic 1.
  
 Connection Details:  	
 						
  Motion control:		L-1---->PA0;		L-2---->PA1;
   						R-1---->PA2;		R-2---->PA3;
   						PL3 (OC5A) ----> Logic 1; 	PL4 (OC5B) ----> Logic 1; 


  Serial Communication:	PORTD 2 --> RXD1 UART1 receive for RS232 serial communication
						PORTD 3 --> TXD1 UART1 transmit for RS232 serial communication

						PORTH 0 --> RXD2 UART 2 receive for USB - RS232 communication
						PORTH 1 --> TXD2 UART 2 transmit for USB - RS232 communication

						PORTE 0 --> RXD0 UART0 receive for ZigBee wireless communication
						PORTE 1 --> TXD0 UART0 transmit for ZigBee wireless communication

						PORTJ 0 --> RXD3 UART3 receive available on microcontroller expansion socket
						PORTJ 1 --> TXD3 UART3 transmit available on microcontroller expansion socket

Serial communication baud rate: 9600bps
To control robot use number pad of the keyboard which is located on the right hand side of the keyboard.
Make sure that NUM lock is on.

Commands:
			Keyboard Key   ASCII value	Action
				8				0x38	Forward
				2				0x32	Backward
				4				0x34	Left
				6				0x36	Right
				5				0x35	Stop
				7				0x37	Buzzer on
				9				0x39	Buzzer off

 Note: 
 
 1. Make sure that in the configuration options following settings are 
 	done for proper operation of the code

 	Microcontroller: atmega2560
 	Frequency: 14745600
 	Optimization: -O0 (For more information read section: Selecting proper optimization 
 						options below figure 2.22 in the Software Manual)

 2. Difference between the codes for RS232 serial, USB and wireless communication is only in the serial port number.
 	Rest of the things are the same. 

 3. For USB communication check the Jumper 1 position on the ATMEGA2560 microcontroller adaptor board

 4. Auxiliary power can supply current up to 1 Ampere while Battery can supply current up to 
 	2 Ampere. When both motors of the robot changes direction suddenly without stopping, 
	it produces large current surge. When robot is powered by Auxiliary power which can supply
	only 1 Ampere of current, sudden direction change in both the motors will cause current 
	surge which can reset the microcontroller because of sudden fall in voltage. 
	It is a good practice to stop the motors for at least 0.5seconds before changing 
	the direction. This will also increase the useable time of the fully charged battery.
	the life of the motor.

*********************************************************************************/

/********************************************************************************

   Copyright (c) 2010, NEX Robotics Pvt. Ltd.                       -*- c -*-
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   * Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.

   * Neither the name of the copyright holders nor the names of
     contributors may be used to endorse or promote products derived
     from this software without specific prior written permission.

   * Source code can be used for academic purpose. 
	 For commercial use permission form the author needs to be taken.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE. 

  Software released under Creative Commence cc by-nc-sa licence.
  For legal information refer to: 
  http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

********************************************************************************/


#include<avr/io.h>
#include<avr/interrupt.h>
#include<util/delay.h>

#define vth 150
#define wlth 40

#include "lcd.h"
unsigned char data; //to store received data from UDR1
int flag=1;

void findactionspace();
void move(int from, int to);
void display_actions(int actionlist[]);



int cur_node,next_node,node1,node2,node3,node4;

int action_counter=0;
int action_space[100]={};
int dispatch_point=10;
int base_station=8;
int store;
int temp_switch=0;
int *actionlist;


void adc_pin_config()
{
	DDRF = 0x00;
	DDRK = 0x00;
}

void adc_init()
{
	ADCSRA = 0x86;
	ADCSRB = 0x00;
	ADMUX = 0x20;
	ACSR = 0x80;
}

void velocity(unsigned char left_vel, unsigned char right_vel)
{
	OCR5AL = left_vel;
	OCR5BL = right_vel;
}

unsigned char adc_convert(unsigned char channel)
{
	if(channel > 7)
	{
		ADCSRB |= 0x08;
	}
	ADMUX |= (channel&7);
	ADCSRA |= 0x40;
	while((ADCSRA & 0x10) == 0);
	unsigned char a = ADCH;
	adc_init();
	return a;
}

void servo1_pin_config (void)
{
 DDRB  = DDRB | 0x20;  
 PORTB = PORTB | 0x20; 
}


void servo2_pin_config (void)
{
 DDRB  = DDRB | 0x40;  
 PORTB = PORTB | 0x40; 
}

void timer1_init(void)
{
	TCCR1B = 0x00; 
	TCNT1H = 0xFC; 
	TCNT1L = 0x01;	
	OCR1AH = 0x03;	
	OCR1AL = 0xFF;	
	OCR1BH = 0x03;	
	OCR1BL = 0xFF;	
	OCR1CH = 0x03;
	OCR1CL = 0xFF;	
	ICR1H  = 0x03;	
	ICR1L  = 0xFF;
	TCCR1A = 0xAB; 
	TCCR1C = 0x00;
	TCCR1B = 0x0C; 
}

void servo_init()
{
	servo1_pin_config();
	servo2_pin_config();
	timer1_init();
}


void servo_1(unsigned char degrees)  
{
	float PositionPanServo = 0;
	PositionPanServo = ((float)degrees / 1.86) + 35.0;
	OCR1AH = 0x00;
	OCR1AL = (unsigned char) PositionPanServo;
}


void servo_2(unsigned char degrees)
{
	float PositionTiltServo = 0;
	PositionTiltServo = ((float)degrees / 1.86) + 35.0;
	OCR1BH = 0x00;
	OCR1BL = (unsigned char) PositionTiltServo;
}

void pick_up_cone()
{
	
	servo_2(220);
	_delay_ms(600);
	
	servo_1(130);
	_delay_ms(600);
	
	servo_2(145);
	_delay_ms(600);
	servo_1(90);
	_delay_ms(300);
}

void drop_cone()
{
	servo_1(115);//droping level
	_delay_ms(500);
	servo_2(220);
	_delay_ms(600);
	servo_1(90);//returning height
	_delay_ms(1000);
	//servo_2(120);
	//_delay_ms(600);
	
	
}

/*void tat()
{
	forward();
	velocity(230,230);
	_delay_ms(250);
	stop();
}*/

unsigned long int ShaftCountLeft = 0;
unsigned long int ShaftCountRight = 0;
unsigned int Degrees;


void encoder_pin_config()
{	
	DDRE &= 0xcf;
	PORTE |= 0x30;
}

void interrupt_init()
{
	cli();
	EIMSK |= 0x30;
	EICRA = 0x00;
	EICRB |= 0x0a;
	sei();
}

ISR(INT4_vect)
{
	ShaftCountLeft++;
}
ISR(INT5_vect)
{
	ShaftCountRight++;
}

void angle_rotate(char dir, unsigned int degrees)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) Degrees/4.090;
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	if(dir == 'r')
	{
		rot_right();
	}
	else if(dir == 'l')
	{
		rot_left();
	}
	buzzer_on(1000);
	while((ShaftCountRight < ReqdShaftCountInt) || (ShaftCountLeft < ReqdShaftCountInt));
//	while((ShaftCountRight < 0) || (ShaftCountLeft < 0));

	buzzer_off();
	stop();
}

void distance_mm(char dir, unsigned int distance)
{
	float ReqdShaftCount = 0;
	unsigned long int ReqdShaftCountInt = 0;

	ReqdShaftCount = (float) distance/5.338;
	ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
	ShaftCountRight = 0;
	ShaftCountLeft = 0;

	if(dir == 'f')
	{
		forward();
	}
	else if(dir == 'b')
	{
		backward();
	}
	while((ShaftCountRight < ReqdShaftCountInt) || (ShaftCountLeft < ReqdShaftCountInt));
	stop();
}

void init_devices()
{
	buzzer_pin_config();
	motion_pin_config();
	lcd_port_config();
	lcd_init();
	timer5_init();
	adc_pin_config();
	adc_init();
	servo_init();
	servo_2(220);             //initialisation of servo2
	encoder_pin_config();
	interrupt_init();
	init_xbee();
	//init_uart();
}		

void print_sensor(char row, char coloumn,unsigned char channel)
{
	lcd_print(row, coloumn, adc_convert(channel), 3);
}

unsigned char l = 0; 
unsigned char r = 0;
unsigned char adc_convert(unsigned char);
unsigned char ADC_Value;

void buzzer_pin_config()
{
	DDRC |= 0x08;
	PORTC &= 0xf7;
}

void buzzer_off()
{
	PORTC &= 0xf7;
}

void buzzer_on(int time_in_milli)
{
	PORTC |= 0x08;
	while(time_in_milli--)
		_delay_ms(1);
	buzzer_off();
}
void buzzer_ON()
{
	PORTC |= 0x08;
}

void motion_pin_config()
{
	DDRA |= 0x0f;
	DDRL |= 0x18;
	PORTL |= 0x18;
	PORTA = 0x00;
}

void motion_set(unsigned char dir)
{
	PORTA = (PINA & 0xf0) | dir;
}

void forward()
{
	motion_set(0x06);
}
void stop()
{
	motion_set(0x00);
}
void backward()
{
	motion_set(0x09);
}
void rot_left()
{
	motion_set(0x05);
}
void rot_right()
{
	motion_set(0x0a);
}
void soft_left()
{
	motion_set(0x04);
}
void soft_right()
{
	motion_set(0x02);
}


void timer5_init()
{
	TCCR5A = 0xa9;
	TCCR5B = 0x0b;
	TCNT5H = 0x00;
	TCNT5L = 0x00;
	OCR5AL = 0xff;
	OCR5BL = 0xff;
}


unsigned char left_wl()
{
	return adc_convert(3);
}
unsigned char mid_wl()
{
	return adc_convert(2);
}
unsigned char right_wl()
{
	return adc_convert(3);
}


void rotate_right_901()
{
	rot_right();
	velocity(vth, vth);
	_delay_ms(500);
	if(mid_wl()<wlth)
	{	
		if(right_wl()>wlth)
		{
			while(mid_wl()<wlth);
			while(mid_wl()>wlth);
			while(mid_wl()<wlth);
			//while(left_wl()<wlth);
		}
		else
		{
			while(mid_wl()<wlth);
			//while(left_wl()<wlth);

		}
	}
	else if(mid_wl()>wlth)
	{
		while(mid_wl()>wlth);
		while(mid_wl()<wlth);
		while(left_wl()<wlth);
	}
	//while((mid_wl() < wlth) && (left_wl() < wlth));
	//while(mid_wl()<wlth && left_wl()>wlth);
	stop();
	l = 1;
	r = 0;

}
void rotate_left_901()
{
	
	rot_left();
	velocity(vth, vth);
	_delay_ms(500);
	if(mid_wl()<wlth)
	{	
		if(left_wl()>wlth)
		{
			while(mid_wl()<wlth);
			while(mid_wl()>wlth);
			while(mid_wl()<wlth);
			//while(right_wl()<wlth);
		}
		else
		{
			while(mid_wl()<wlth);
			//while(right_wl()<wlth);
		}	

	}
	else if(mid_wl()>wlth)
	{
		while(mid_wl()>wlth);
		while(mid_wl()<wlth);
		//while(right_wl()<wlth);
	}
	//while((mid_wl() < wlth) && (left_wl() < wlth));
	//while((mid_wl()<wlth) && (left_wl()>wlth);
	stop();
	r = 1;
	l = 0;
	
}

void rotate_180()
{
	rot_left();
	velocity(vth, vth);
	_delay_ms(500);
	if(mid_wl()<wlth)
	{	
		while(mid_wl()<wlth);
		while(mid_wl()>wlth);
		
	}
	else if(mid_wl()>wlth)
	{
		while(mid_wl()>wlth);
		while(mid_wl()<wlth);
	}
	stop();
}


void detect_node()
{
	rot_left();
	velocity(vth, vth);
	while(!((left_wl()>wlth) && (mid_wl()>wlth) )|| ((mid_wl()>wlth) && (right_wl()>wlth) ) || ((left_wl()>wlth) && (right_wl()>wlth) ) ||((left_wl()>wlth) && (mid_wl()>wlth) && (right_wl()>wlth)));
	stop();
}
void rotate_right_90()
{  rot_right();
	velocity(240, 240);
	_delay_ms(300);
 while(1)
   {
	
	if(mid_wl() < wlth)
    {
	rot_right();
	velocity(240, 240);
	
	}
	else if((mid_wl() > 20)|(left_wl()>20))
	{
	stop();
	buzzer_on(100);
	break;
	}
	l = 1;
	r = 0;
	}
}

void rotate_left_90()
{	rot_left();
	velocity(240, 240);
	_delay_ms(300); 
	while(1)
	   {
		   
			if(mid_wl()  <wlth)
		    {
				rot_left();
				velocity(240, 240);
			}
		    else if((mid_wl()>wlth))
			{
				stop();
			
				break;
			}
			r = 1;
			l = 0;
		}
}
//Function To Initialize UART0
// desired baud rate:9600
// actual baud rate:9600 (error 0.0%)
// char size: 8 bit
// parity: Disabled
void uart0_init(void)
{
 UCSR0B = 0x00; //disable while setting baud rate
 UCSR0A = 0x00;
 UCSR0C = 0x06;
 UBRR0L = 0x5F; //set baud rate lo
 UBRR0H = 0x00; //set baud rate hi
 UCSR0B = 0x98;
}


void transmitByte(uint8_t data) {
                                     /* Wait for empty transmit buffer */
  loop_until_bit_is_set(UCSR0A, UDRE0);
  UDR0 = data;                                            /* send data */
}



SIGNAL(SIG_USART0_RECV) 		// ISR for receive complete interrupt
{
	data = UDR0; 				//making copy of data from UDR0 in 'data' variable 

	UDR0 = data; 				//echo data back to PC

		if(data == 0x38 && flag==0) //ASCII value of 8
		{
			PORTA=0x06;  //forward
		}

		if(data == 0x32 && flag==0) //ASCII value of 2
		{
			PORTA=0x09; //back
		}

		if(data == 0x34 && flag==0) //ASCII value of 4
		{
			PORTA=0x05;  //left
		}

		if(data == 0x36 && flag==0) //ASCII value of 6
		{
			PORTA=0x0A; //right
		}

		if(data == 0x35 && flag==0) //ASCII value of 5
		{
			PORTA=0x00; //stop
		}

		if(data == 0x37 && flag==0) //ASCII value of 7
		{
			buzzer_on(5000);
		}

		if(data == 0x39 && flag==0) //ASCII value of 9
		{
			buzzer_off();
		}
		if(data == 0x41 && flag==0) //ASCII value of A to hand he control back
		{
			flag=1;
		}
		if(data == 0x44 && flag==0) //ASCII value to to drop the cone, D
		{
			buzzer_ON();
			drop_cone();
			buzzer_off();
		}
		// if(data == 0x4C && flag==0) //ASCII value slow left
		// {
		// 	rot_left();
		// 	velocity(vth,vth);
		// }
		// if(data == 0x52 && flag==0) //ASCII value slow right, R
		// {
		// 	rot_right();
		// 	velocity(vth,vth);
		// }
		if(data == 0x53 && flag==0) //ASCII value slow , S
		{
			velocity(vth,vth);
		}
		if(data == 0x46 && flag==0) //ASCII value F fast
		{
			velocity(200,200);
		}
		if(data == 0x47 && flag==0) //ASCII value superfast
		{
			velocity(255,255);
		}
		if(data == 0x73 && flag==0) //ASCII value superslow, s
		{
			velocity(120,120);
		}
		

}


//Function To Initialize all The Devices
void init_xbee()
{
 cli(); //Clears the global interrupts
 //port_init();  //Initializes all the ports
 uart0_init(); //Initailize UART1 for serial communiaction
 sei();   //Enables the global interrupts
}

//Main Function
int main(void)
{
	int i,loop;
	cur_node=base_station;
	actionlist=action_space;	
	
	//printf("bridge_node=");
	//scanf("%d",&dispatch_point);
	init_devices();
	servo_1(90);//returning height
	_delay_ms(1000);//fixing servo1 right
	if(dispatch_point==10)
	{
		loop=2;
		/*printf("node1=");
		scanf("%d",&node1);
		printf("node2=");
		scanf("%d",&node2);*/
	}
	else if(dispatch_point==11)
	{
		loop=4;

		/*printf("node1=");
		scanf("%d",&node1);
		printf("node2=");
		scanf("%d",&node2);
		printf("node3=");
		scanf("%d",&node3);
		printf("node4=");
		scanf("%d",&node4);*/
	}

	if(loop==2)
	{
		store=fetch_storepoint();
		next_node=store;
		findactionspace(cur_node,next_node);
		store=fetch_storepoint();
		next_node=store;
		findactionspace(cur_node,next_node);
	}
	else if(loop==4)
	{
		for(i=0;i<4;i++)
		{
			store=fetch_storepoint();
			next_node=store;
			findactionspace(cur_node,next_node);
		}
	}		
	action_space[action_counter]=7;
	//	flag=0;
	//while(1);
	display_actions(actionlist);
	
}

int fetch_storepoint()
{
	if(temp_switch==0)
	{
		temp_switch=1;		
		return 4;//node1;
	}
	else if(temp_switch==1)
	{
		temp_switch=2;
		return 3;//node2;
	}	
	else if(temp_switch==2)
	{
		temp_switch=3;
		return 6;//node3;
	}
	else if(temp_switch==3)
	{
		temp_switch=4;
		return 1;//node4;
	}
}

void display_actions(int actionlist[])
{
	int i;
	//printf("move fwd\n");
	lcd_wr_command(0x01);
	lcd_string("move fwd");
	follow_path();
	
	for(i=0; actionlist[i+1] !=7 ;i++)
	{
		//printf("actionlist_value=%d\n",actionlist[i]);
		if(actionlist[i+1]==5)
		{
			//printf("stopped\n");
			stop();
			
			//printf("***PICK NUMBER **\n");
			lcd_wr_command(0x01);
			lcd_string("picking number");
			//detect node
			//detect_node();

			//adjustment for arm and picking up of the number
			//distance_mm('b',0);
			pick_up_cone();
			//distance_mm('f',80);
			actionlist[i+1]=actionlist[i];
		}
		else if(actionlist[i+1]==6)//for handling control back to bot
		{
			//printf("stopped\n");
			stop();

			//printf("***HANDLING CONTROL TO PC **\n");
			lcd_wr_command(0x01);
			lcd_string("handling control to pc");
			transmitByte('I');
			flag=0;
			buzzer_ON();
			while(flag==0);
			//drop_cone();
			buzzer_off();
			actionlist[i+1]=actionlist[i];
		}
		else
		{
			if(abs(actionlist[i]-actionlist[i+1]) ==0)
			{
			
				//printf("no change in direction\n");
				lcd_wr_command(0x01);
				lcd_string("no change in direction");
				_delay_ms(1000);
			
	
				//printf("move fwd\n");
				lcd_wr_command(0x01);
				lcd_string("move fwd");
				follow_path();
			

			}

			else if (abs(actionlist[i]-actionlist[i+1]) ==1)
			{
			
				if(actionlist[i]<actionlist[i+1])
				{
					//printf("moving left 90deg\n");
					lcd_wr_command(0x01);
					lcd_string("rotate left");
					rotate_left_901();
				
				
					//printf("move fwd\n");
					lcd_wr_command(0x01);
					lcd_string("move fwd");
					follow_path();
				
				}
				else
				{
				
					//printf("moving right 90 deg\n");
					lcd_wr_command(0x01);
					lcd_string("rotate right");
					rotate_right_901();
				
				
				
					//printf("move fwd\n");
					lcd_wr_command(0x01);
					lcd_string("move fwd");
					follow_path();
				
				}

			}
			else if (abs(actionlist[i]-actionlist[i+1]) ==2)
			{
			
				//printf("moving left 90deg twice\n");
				lcd_wr_command(0x01);
				lcd_string("rotate left");
				// rotate_left_901();
				// lcd_wr_command(0x01);
				// lcd_string("rotate left");
				// rotate_left_901();
				rotate_180();
			
			
			
				//printf("move fwd\n");
				lcd_wr_command(0x01);
				lcd_string("move fwd");
				follow_path();
			

			}
			else if (abs(actionlist[i]-actionlist[i+1]) ==3)
			{
				if(actionlist[i]>actionlist[i+1])
				{
				
					//printf("moving left 90deg\n");
					lcd_wr_command(0x01);
					lcd_string("rotate left");
					rotate_left_901();
				
				
					//printf("move fwd\n");
					lcd_wr_command(0x01);
					lcd_string("move fwd");
					follow_path();
				
				}
				else
				{
				
					//printf("moving right 90 deg\n");
					lcd_wr_command(0x01);
					lcd_string("rotate right");
					rotate_right_901();
				
				
				
					//printf("move fwd\n");
					lcd_wr_command(0x01);
					lcd_string("move fwd");
					follow_path();
				
				}
			}
		}
		
	}

}

void findactionspace()
{
	move(cur_node,next_node);
	
	cur_node=base_station;
	next_node=dispatch_point;
	move(cur_node,next_node);
		
	cur_node=dispatch_point;
	next_node=base_station;
	move(cur_node,next_node);
	
	cur_node=base_station;
	next_node=store;		
	
}

void move(int from, int to)
{
	if(from==base_station )
	{
		if(to==store)
		{
			if(store==4)
			{
				action_space[action_counter++]=4;
				action_space[action_counter++]=3;

				action_space[action_counter++]=5;

				action_space[action_counter++]=1;
				action_space[action_counter++]=2;
			
			}
			else if(store==6)
			{
				action_space[action_counter++]=4;
				action_space[action_counter++]=1;

				action_space[action_counter++]=5;

				action_space[action_counter++]=3;
				action_space[action_counter++]=2;

			}
			else if(store==1)
			{
				action_space[action_counter++]=4;
				action_space[action_counter++]=4;
				action_space[action_counter++]=3;

				action_space[action_counter++]=5;

				action_space[action_counter++]=1;
				action_space[action_counter++]=2;
				action_space[action_counter++]=2;

			}
			else if(store==3)
			{
				action_space[action_counter++]=4;
				action_space[action_counter++]=4;
				action_space[action_counter++]=1;

				action_space[action_counter++]=5;

				action_space[action_counter++]=3;
				action_space[action_counter++]=2;
				action_space[action_counter++]=2;

			}
			
		}

		else if(to==dispatch_point)
		{
			if(dispatch_point==10)
			{
				action_space[action_counter++]=3;
				action_space[action_counter++]=2;

				action_space[action_counter++]=6;
			}
			if(dispatch_point==11)
			{
				action_space[action_counter++]=1;
				action_space[action_counter++]=2;

				action_space[action_counter++]=6;				
			}
		}
	}
	if(from==dispatch_point)
	{
		if(dispatch_point==10)
		{
			action_space[action_counter++]=4;
			action_space[action_counter++]=1;
		}
		
		else if(dispatch_point==11)
		{
			action_space[action_counter++]=4;
			action_space[action_counter++]=3;
		}

	}

}
void follow_path()
{
	unsigned char Left_white_line,Center_white_line,Right_white_line;
	unsigned char th=wlth;
	forward();
	while(1)
	{
		Left_white_line = adc_convert(3);	//Getting data of Left WL Sensor
		Center_white_line = adc_convert(2);	//Getting data of Center WL Sensor
		Right_white_line = adc_convert(1);	//Getting data of Right WL Sensor

		//flag=0;

		//print_sensor(2,1,3);	//Prints value of White Line Sensor1
		//print_sensor(2,5,2);	//Prints Value of White Line Sensor2
		//print_sensor(2,9,1);	//Prints Value of White Line Sensor3
		
		

		if(Left_white_line<th && Center_white_line<th && Right_white_line<th)  //www
		{
			//backward();
			forward();
			velocity(vth,vth);//forward
			//forward();
		}

		if(Left_white_line<th && Center_white_line<th && Right_white_line>th)  //wwb -- left
		{
			//velocity(180,220);//left turn
			stop();
			rot_right();
			velocity(vth,vth);
			
		}

		if(Left_white_line<th && Center_white_line>th && Right_white_line<th)  //wbw -- valid
		{
			forward();
			velocity(vth,vth);//forward
			

		}

		if(Left_white_line<th && Center_white_line>th && Right_white_line>th)  //wbb -- more left
		{
		//	velocity(175,220);
			//forward();
			//velocity(120,0);
			stop();
			rot_right();
			velocity(vth,vth);
		}

		if(Left_white_line>th && Center_white_line<th && Right_white_line<th)  //bww -- right
		{
		//	velocity(120,80);
			stop();
			rot_left();
			velocity(vth,vth);
		}


		/*if(Left_white_line>40 && Center_white_line<40 && Right_white_line>40)	 //bwb -- straight
		{
		//	velocity(220,220);
			forward();
		}*/

		if(Left_white_line>th && Center_white_line>th && Right_white_line<th)  //bbw -- more right
		{
			//forward();
			//velocity(0,120);
			//rot_right();
			stop();
			rot_left();
			velocity(vth,vth-30);
			
		}

		if((Left_white_line>th && Center_white_line>th && Right_white_line>th) )//|| (Left_white_line>(th+40) && Center_white_line>(th+40) && Right_white_line<th) || (Left_white_line<th && Center_white_line>(th+40) && Right_white_line>(th+40)))  //bbb
		{							//bbb or highBhighBwhite or whitehighBhighB
			stop();
			//_delay_ms(1000);
			//velocity(200,200);
			//while(Left_white_line>40 && Center_white_line>40 && Right_white_line>40);
			buzzer_on(500);
			distance_mm('f',40);
			//velocity(0,0);
			stop();
			break;
		}


	/*	
		if(Center_white_line<40)
		{
			flag=1;
			forward();
			velocity(200,200);
		}

		if((Left_white_line>40) && (flag==0))
		{
			flag=1;
			forward();
			velocity(220,180);
		}

		if((Right_white_line>40) && (flag==0))
		{
			flag=1;
			forward();
			velocity(180,220);
		}

		if(Center_white_line>40 && Left_white_line>40 && Right_white_line>40)
		{
			stop();
			velocity(0,0);
		} */
	}
}
