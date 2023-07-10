#include <avr/io.h>
#include <stdio.h>
#include <avr/interrupt.h>
#define F_CPU 1000000

unsigned int result_low = 0, result_high = 0, result = 0;
volatile unsigned long temp = 0, temp_avg = 0, Vread = 0, Vinp[4] = {0};
volatile unsigned long min_temp = 9999, max_temp = 0; //global variables to store min and max temp
unsigned char cycles = 0;
volatile char command = 'n'; //global variable to store command from pc
volatile unsigned char seven_seg[] = {0x01, 0x4F, 0x12, 0x06, 0x4C, 0x24, 0x20, 0x0F, 0x00, 0x0C};
	
void send_temp(unsigned long t)
{
    char buffer[10];
    sprintf(buffer, "%lu\r\n", t); //convert temp to string with newline
    for(int i = 0; buffer[i] != '\0'; i++) //loop until end of string
    {
        while(!(UCSRA & (1 << UDRE))); //wait until UDR is empty
        UDR = buffer[i]; //send one byte
    }
}

int main(void)
{
	//For 7SEG displays
	DDRB = 0xFF;
	DDRA = 0xFE;
	
	//initializing UART
	UBRRL=0xC ; // set Baud Rate to 4800
	UCSRB |= (1<<RXEN) | (1<<RXCIE) | (1 << TXEN); //enable receiver and receiver interrupt
	UCSRC |= (1<<URSEL)|(1<<UCSZ0)|(1<<UCSZ1) ; // set data size (8 bits)

	//Configuring ADC
	
	//2.56V reference, right adjust, and ADC0 as input
	ADMUX = 0b11000000;
	
	//8 prescalar, no interrupt, no auto trigger
	ADCSRA = 0b10000011;
	
	TCNT1 = 0; // Initializing timer 1
	OCR1A = 15625;
	
	TCCR1A = 0x00; // WGM13:WGM10 = 0100 for CTC mode
	TCCR1B = 0x0B; //CS12 : CS10 = 011 for clk/64 prescalar
	
	sei(); // enable global interrupt
	TIMSK = 0x10 ; // enable compare match of timer 1

	
	while (1)
	{
		ADCSRA |= (1 << ADSC); //start conversion
		
			while (ADCSRA & (1 << ADSC)); //polling
			
			//reading digital output
			result_low = ADCL;
			
			//we only want value from last two bits of ADCH (they are 8th and 9th bits)
			result_high = ADCH & 0b00000011;
			
			//complete digital value
			result = result_low + (256 * result_high);
			
			Vread = ((unsigned long) result * 2560ul) / 1023ul;
			
			if (cycles < 4)
			{
				Vinp[cycles] = Vread;
				
				temp = Vread;
				
				cycles++;
			}
			
			if (cycles >= 4)
			{
				for(int j = 0; j < 3; j++)
				{
					Vinp[j] = Vinp[j + 1];
				}
				
				Vinp[3] = Vread;
				
				temp_avg = (Vinp[3] + Vinp[2] + Vinp[1] + Vinp[0]) / 4;
				
				//Linear regression equation, to calibrate the reading
				temp = (1.0712 * temp_avg) - 0.5320;
			}
			
			if(temp < min_temp) //update min temp
			{
				min_temp = temp;
			}
			
			if(temp > max_temp) //update max temp
			{
				max_temp = temp;
			}
	}
	
	return 0;
}

ISR(USART_RXC_vect)
{
	command = UDR; //read data from UDR
}

ISR (TIMER1_COMPA_vect)
{
	if(command == 'n') //nominal value
	{
		PORTB = seven_seg[(temp / 100) % 10];
		PORTA = (seven_seg[(temp / 10) % 10]) << 1;
	}
	
	else if(command == 'm') //minimum value
	{
		PORTB = seven_seg[(min_temp / 100) % 10];
		PORTA = (seven_seg[(min_temp / 10) % 10]) << 1;
		
	}
	
	else if(command == 'M') //maximum value
	{
		PORTB = seven_seg[(max_temp / 100) % 10];
		PORTA = (seven_seg[(max_temp / 10) % 10]) << 1;
	}
	
	 send_temp(temp / 10);
}
