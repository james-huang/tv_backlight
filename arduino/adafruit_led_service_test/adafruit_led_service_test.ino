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
  strip.setBrightness(100);
  for (int x=0; x<30; x++) {
    strip.setPixelColor(x, 0, 0,255);
  }
  strip_test.begin();
  strip_test.setBrightness(100);
  strip_test.setPixelColor(0, 255,0,0);
  strip_test.setPixelColor(1, 255,0,0);
  strip_test.setPixelColor(2, 255,0,0);
  strip_test.show();
  strip.show(); // Initialize all pixels to 'off'
}

char rgbBuff[60];
char rgbIndex = 0;
char tmpHexString[7];

void loop() {
  if (Serial.available() > 0) {
    char tmp_char = Serial.read();
    if (tmp_char == '\n') {
//      Serial.println(rgbBuff);
      // new line is a buffer clear. send buffer data to leds
      for (int ledSectionNum = 0; ledSectionNum < 10; ledSectionNum++){
        int hexOffset = ledSectionNum*6;
        tmpHexString[0] = rgbBuff[hexOffset];
        tmpHexString[1] = rgbBuff[hexOffset + 1];
        tmpHexString[2] = rgbBuff[hexOffset + 2];
        tmpHexString[3] = rgbBuff[hexOffset + 3];
        tmpHexString[4] = rgbBuff[hexOffset + 4];
        tmpHexString[5] = rgbBuff[hexOffset + 5];
        tmpHexString[6] = '\0';

        long rgb_number = (long) strtol(tmpHexString, NULL, 16);
        int r = rgb_number >> 16;
        int g = rgb_number >> 8 & 0xFF;
        int b = rgb_number & 0xFF;
//        Serial.print(tmpHexString);
//        Serial.print('/');
//        Serial.print(rgb_number);
//        Serial.print(' ');
//        Serial.print(r);
//        Serial.print(g);
//        Serial.println(b);
        int ledOffset = ledSectionNum * 3;
        strip.setPixelColor(ledOffset, r, g, b);
        strip.setPixelColor(ledOffset + 1, r, g, b);
        strip.setPixelColor(ledOffset + 2, r, g, b);
      }
      strip.show();
    } else {
      rgbBuff[rgbIndex] = tmp_char;
      rgbIndex++;
      if (rgbIndex >= 60){
        rgbIndex = 0 ;
      }
    }
  }
  //  if (Serial.available() > 0) {
  //    rgbBuff[rgbIndex] = Serial.read();
  //    rgbIndex++;
  //    if (rgbIndex >= 3){
  //      rgbIndex = 0 ;
  //      strip.setPixelColor(ledIndex, rgbBuff[0], rgbBuff[1], rgbBuff[2]);
  //      Serial.println(rgbBuff);
  //      ledIndex++;
  //      if (ledIndex >= 30){
  //        ledIndex = 0;
  //        strip.show();
  //      }
  //    }
  //  }
}

