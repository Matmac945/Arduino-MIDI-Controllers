/*
   Copyright (c) 2020 Matías Macías Gómez
   Original by Evan Kale taken from: https://github.com/evankale/ArduinoMidiFader/blob/master/ArduinoMidiFader.ino
   Edited by Matías Macías Gómez github: https://github.com/Matmac945

   You can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
/*
  Compilation note:
  - Requires Ralf Kistner's arcore patch (adds MIDI-USB support)
    into Arduino IDE enviroment to compile.
  - Get it here: https://github.com/rkistner/arcore
*/


#include <pitchToFrequency.h>
#include <pitchToNote.h>
#include <frequencyToNote.h>
#include <MIDIUSB_Defs.h>
#include <MIDIUSB.h>


// Control pins for Mux HEF4067B
#define MUX_ADDRESS_SEL_1 4
#define MUX_ADDRESS_SEL_2 5
#define MUX_ADDRESS_SEL_3 6
#define MUX_ADDRESS_SEL_4 7

// Input analog pin for Mux HEF4067B
#define MUX_IN A0

// Max number of Potentiometers
#define MAX_POTS 16

// Total number of MIDI controls
#define MIDI_CONTROLS 16

// Midi Channel adn CC start
#define MIDI_CHAN 14
#define MIDI_CC_START 14

// Smoothing factor for the signal
#define SMOOTH_FACTOR 10

int readings[MIDI_CONTROLS][SMOOTH_FACTOR] = {0};
byte pos[MIDI_CONTROLS] = {0};
int total[MIDI_CONTROLS] = {0};

// Arrays to store values
int potValue [MAX_POTS] = {1};
int prevPotsValues [MAX_POTS] = {0};

void setup() {
  Serial.begin(9600);

  // Setup I/O for the Arduino
  pinMode(MUX_ADDRESS_SEL_1, OUTPUT);
  pinMode(MUX_ADDRESS_SEL_2, OUTPUT);
  pinMode(MUX_ADDRESS_SEL_3, OUTPUT);
  pinMode(MUX_ADDRESS_SEL_4, OUTPUT);
}

void loop() {
  // Read potentiometers through Mux
  for (int i = 0; i < MAX_POTS; i++) {
    potValue[i] = readAndMap(i); // read the values and store them in the array
  }
  sendMessages();
  //displayData();   //Uncomment this line to print the data in the serial port
  delay(1);
}

// Select Mux input and read it
int readAndMap(byte channel)
{
  digitalWrite(MUX_ADDRESS_SEL_1, bitRead(channel, 0));
  digitalWrite(MUX_ADDRESS_SEL_2, bitRead(channel, 1));
  digitalWrite(MUX_ADDRESS_SEL_3, bitRead(channel, 2));
  digitalWrite(MUX_ADDRESS_SEL_4, bitRead(channel, 3));

  return map(smoothRead(channel), 0, 1023, 0, 127); // map the value from 0 - 1023 to 0 - 127 (MIDI range)
}

// Smooths the signal by taking multiple measures and then averaging them
int smoothRead(byte readIndex) {
  // the running total of the current pot
  total[readIndex] = total[readIndex] - readings[readIndex][pos[readIndex]];
  // read from the sensor and stores
  readings[readIndex][pos[readIndex]] = analogRead(MUX_IN);
  // add the reading to the total
  total[readIndex] += readings[readIndex][pos[readIndex]];
  // Moves one psition in the array
  pos[readIndex]++;
  // resets the position
  if (pos[readIndex] >= SMOOTH_FACTOR) pos[readIndex] = 0;
  // calculates the average:
  int average = (total[readIndex] / SMOOTH_FACTOR);
  return average;
}

// Midi control change  message
void controlChange(byte channel, byte control, byte value) {
  midiEventPacket_t event = {0x0B, 0xB0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}

/*
   Check all of the values, if the value of the selected pot has changed
   sends midi information to the computer, and pu
*/
void sendMessages() {
  for (int i = 0; i < MAX_POTS; i++) {
    if (prevPotsValues[i] != potValue[i]) { // check if the value has changed
      controlChange(MIDI_CHAN, MIDI_CC_START + i, potValue[i]);
      prevPotsValues[i] = potValue[i];
      MidiUSB.flush();
    }
  }
}

/*
    Dumps captured data from the array to the serial monitor
    This is for debugging and cheching if all the pots are working.
*/
void displayData()
{
  Serial.println();
  Serial.println("Values from multiplexer:");
  Serial.println("========================");
  for (int i = 0; i < MAX_POTS; i++)
  {
    Serial.print("input I");
    Serial.print(i);
    Serial.print(" = ");
    Serial.println(potValue[i]);
  }
  Serial.println("========================");
}
