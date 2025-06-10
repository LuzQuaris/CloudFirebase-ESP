#include <WiFi.h>
#include <time.h>
#include <Firebase_ESP_Client.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID "(Wifi SSID kamu)"
#define WIFI_PASSWORD "(Password Wifi Kamu)"
#define API_KEY "(API Key database kamu)"
#define DATABASE_URL "(Database URL kamu)"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
bool signupOK = false;
int counter;
int jam,menit;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  Serial.print("connecting to Wi-Fi");
  while(WiFi.status() != WL_CONNECTED){
    Serial.print("."); delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP : ");
  Serial.println(WiFi.localIP());
  Serial.println();

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  if(Firebase.signUp(&config, &auth, "", "")){
    Serial.println("signUp OK");
    signupOK = true;
  }else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  configTime(7 * 3600, 0, "pool.ntp.org", "time.nist.gov");

  Serial.println("Waiting for time synchronization...");
  struct tm timeinfo;
  while (!getLocalTime(&timeinfo)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nTime synchronized");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 5000) || sendDataPrevMillis == 0){
    sendDataPrevMillis = millis();
    counter++;
    struct tm timeinfo;
    if(getLocalTime(&timeinfo)){
      jam = timeinfo.tm_hour;
      menit = timeinfo.tm_min;
    }
      if(Firebase.RTDB.setInt(&fbdo, "Data/counter", counter)){
        Serial.println(); Serial.print(counter);
        Serial.print("succesfully saved to : " + fbdo.dataPath());
        Serial.println(" (" +fbdo.dataType() + ")");
      }else{
        Serial.println("FAILED: " + fbdo.errorReason());
      }
      if(Firebase.RTDB.setInt(&fbdo, "Waktu/Jam", jam)){
        Serial.println(); Serial.print(jam);
        Serial.print("succesfully saved to : " + fbdo.dataPath());
        Serial.println(" (" +fbdo.dataType() + ")");
      }else{
        Serial.println("FAILED: " + fbdo.errorReason());
      }
      if(Firebase.RTDB.setInt(&fbdo, "Waktu/Menit", menit)){
        Serial.println(); Serial.print(menit);
        Serial.print("succesfully saved to : " + fbdo.dataPath());
        Serial.println(" (" +fbdo.dataType() + ")");
      }else{
        Serial.println("FAILED: " + fbdo.errorReason());
      }
  }
}
