#include <WiFi.h>

// --- VORTEX RESONANCE: WIRELESS LINK ---
const char* ssid = "Achmed";        
const char* password = "azwadavids"; 

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT); // Blue Signal Light

  // COMMAND: Connect
  WiFi.begin(ssid, password);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(2, HIGH); // SOLID BLUE = CONNECTED
    delay(1000);
  } else {
    digitalWrite(2, LOW);  // FLASHING = SEARCHING
    delay(200);
    digitalWrite(2, HIGH);
    delay(200);
  }
}
