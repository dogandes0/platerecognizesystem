const int ledPin = 7;  

void setup() {
  pinMode(ledPin, OUTPUT);  
  Serial.begin(9600);  
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  
    command.trim();  
    
    if (command == "1") {
      digitalWrite(ledPin, HIGH);  
    }
    else if(command == "0"){
      digitalWrite(ledPin, LOW);
    }
  }
}
