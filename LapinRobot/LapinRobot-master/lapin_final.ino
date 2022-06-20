//librairies à importer
#include <Wire.h>
#include "Adafruit_DRV2605.h"
#include <Servo.h>

//déclaration variables
unsigned long currentMillis;
float value[]= {0,0,0,0};
boolean pret;

//---------- init bouton ------------------------
const int pinBouton=40;    // bouton connecte au pin 10 avec resistance 10kohm
const int ledPinRouge = 30;// led connectee au pin 13 avec resistance 220ohm
const int ledPinVerte = 46;



//---------- init coeur ----------------------
  unsigned long previousMillisCoeur = 0 ;
  const uint8_t effect = 2;
  int lance = 0;
  long ecart_battement = 300; // Equivalent à 200 battements minutes
  long ecart_battement2 = 100;
  int periode_coeur;
  
  Adafruit_DRV2605 drv;
  
//---------- init urine ------------------------
unsigned long previousMillisSon = 0;
const int speakerPin = 50;
const int ton = 311;
const long duree_son = 60;
int sound = 1;
int periode_son = 600;
unsigned long delta_T2;

//---------- init moteur ------------------------
int pos = 0;
unsigned long previousMillisMoteur = 0;
int mot = 1;
float periode_respi = 2000;
float frequence_respi = float(1/periode_respi);
unsigned long delta_T;
int delta_theta = 180;
int pos_demandee = 180;
int pos_init = 0;
int sens = 1;
Servo servo_9;
//----------init detection -----------------------
int substance = 0;
bool detect_adre = false;
int etat =0;
unsigned long previousMillisAdre = 0 ;



// ============================ SETUP ==================================================
void setup() {
  Serial.begin(19200);
  Serial.setTimeout(1);
  
  //------------ setup bouton + led ----------
  pinMode(pinBouton,INPUT_PULLUP);
  pinMode(ledPinRouge, OUTPUT);
  pinMode(ledPinVerte,OUTPUT);

  //------------ setup moteur ----------------
  servo_9.attach(26);
  servo_9.write(pos_init);

}


// ================================= MAIN LOOP ==========================================
void loop() {
  //recuperer nouvelles valeurs freqRespi,freqUree,freqCoeur  
   //controlCoeur();
   
  if(!detect_adre){
    lecture_donnees();
    affecterValeurs();
    allumerLed(etat);
     controleUree();
    controlePoumon();
    if (digitalRead(pinBouton)==0){
      detect_adre = true;
    }
    substance = 0;
}
if(detect_adre ){
    previousMillisAdre = millis();
    substance = 1;
    }
    detect_adre = false;
}
void lecture_donnees(){
  // format des donnees : 1) état ( 0 = repos; 1 = adre; etc) 2) periode uree; 3) periode respi; 4) periode coeur
 while(!pret) {
  if (Serial.available()>0){
  if(Serial.read() ==0) {
    Serial.write(0);
    pret = true;
    Serial.flush();
  }
  else {
    Serial.write(1);
    pret = false;
  }
 }
 }
   for (int i=0; i<4; i++){
    while(Serial.available() <1){
    }
      value[i] = float(Serial.read());
    }
  Serial.write(substance);
    pret = false;
}
void affecterValeurs(){
  etat = value[0];
  periode_son = 100* int(value[1]);
  periode_respi = 10*value[2];
  periode_coeur = value[3];
}

void allumerLed(int etat){
  // led verte : injection possible; led rouge : injection interdite
  if(etat == 0){
    digitalWrite(ledPinRouge, LOW);
    digitalWrite(ledPinVerte,HIGH);
  }
  else {
    digitalWrite(ledPinRouge, HIGH);
    digitalWrite(ledPinVerte,LOW);
  }
}
void controlePoumon(){
  currentMillis = millis();
  delta_T = currentMillis-previousMillisMoteur;
  frequence_respi = float(1/periode_respi);
  if(delta_T > periode_respi){
    changementSens();
  }
  else {
    pos =pos_init + int(180*frequence_respi*delta_T*sens);
    if(pos>180){
      pos = 180;
      changementSens();
    }
    else if (pos<0){
      pos = 0;
      changementSens();
    }
  }
  servo_9.write(pos);
}

void changementSens(){
       sens = - sens;
    pos_init = pos_demandee;
    pos_demandee = abs(180-pos_demandee);
    previousMillisMoteur = millis();
}
void controlCoeur(){
  currentMillis = millis();
  if (lance == 0 && (currentMillis - previousMillisCoeur >= ecart_battement)) {
     //drv.go(); cette commande génère une erreur qu'on a pas eu le temps de debugguer
     lance = 1;
     previousMillisCoeur = millis();
    }
    if (lance == 1 && (currentMillis - previousMillisCoeur >= ecart_battement2)) {
     //drv.go(); idem
     lance = 0;
    }
}

void controleUree(){
  delta_T2 = currentMillis - previousMillisSon;
  if (sound == 1) {
    if (delta_T2 < duree_son) {
      tone(speakerPin, ton);
    }
    else {
      noTone(speakerPin);
      sound = 0;
    }
  } else {
    if (delta_T2 < periode_son) {
      sound = 0;
    } else {
      sound = 1;
      previousMillisSon = millis(); //debut periode son
    }
  }
}
