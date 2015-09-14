#include <Adafruit_NeoPixel.h>

#define PIN 6
// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(30, PIN, NEO_GRB + NEO_KHZ800);

Adafruit_NeoPixel strip_test = Adafruit_NeoPixel(3, 10, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.setBrightness(255); // drop to 80 for debugging
  for (int x=0; x<30; x++) {
    strip.setPixelColor(x, 0, 0,255);
  }
  strip.show(); // Initialize all pixels to 'off'
}

int xffs_in_a_row = 0;
char rgbBuff[44];
char rgbIndex = 0;
char tmp_char;
unsigned long rgbInt; // apparently this is 24 bit lol

/*
Computer sends over data in byte format 10x (B,G,R,0) 
and then 4 bytes straight of (255,255,255,255) which
the arduino use to reset the buffer.
*/
void loop() {
  if (Serial.available() > 0) {
    tmp_char = Serial.read();
    rgbBuff[rgbIndex] = tmp_char;
    rgbIndex++;
    if (tmp_char == '\xff') {
      xffs_in_a_row ++;
      if (xffs_in_a_row >= 4){
        // 10 leds have been signaled, go ahead and light them up
        for (int ledSectionNum = 0; ledSectionNum < 10; ledSectionNum++){
          int ledOffset = ledSectionNum * 3;
          int rgbOffset = ledSectionNum * 4;
          
          memcpy(&rgbInt, rgbBuff+rgbOffset, 4);
          // takes 24 bits as b,g,r
          strip.setPixelColor(ledOffset, rgbInt);
          strip.setPixelColor(ledOffset + 1,rgbInt);
          strip.setPixelColor(ledOffset + 2, rgbInt);
        }
        strip.show();
        rgbIndex = 0;
        xffs_in_a_row = 0;
       }
    } else {
      xffs_in_a_row = 0;
    }
  }
}


