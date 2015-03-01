#include <Adafruit_NeoPixel.h>

#define PIN 6

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(15, PIN, NEO_GRB + NEO_KHZ800);
    
void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.setBrightness(50);
  for (int x=0; x<15; x++) {
    strip.setPixelColor(x, 255, 0, 0);
  }
  strip.show(); // Initialize all pixels to 'off'
}

char rgbBuff[3]; 
char rgbIndex = 0;
char ledIndex = 0;
void loop() {
  if (Serial.available() > 0) {
    rgbBuff[rgbIndex] = Serial.read();
    rgbIndex++;
    if (rgbIndex >= 3){
      rgbIndex = 0 ;
      strip.setPixelColor(ledIndex, rgbBuff[0], rgbBuff[1], rgbBuff[2]);
      ledIndex++;
      if (ledIndex >= 15){
        ledIndex = 0;
        strip.show();
      }
    }
  }
}
