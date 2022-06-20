+boolean readFromSerial; //Booléen pour autoriser la lecture des données depuis Serial

//Pour la séquence d'inspiration
boolean inspi = 0; //Détermine si le lapin doit inspirer ou pas
double fan_voltage = 0; //Tension à fournir au ventilateur

//Fréquences obtenues par la génération de données
double frequence_cardiaque;
double frequence_respiratoire;

//Traduction des fréquences en périodes utilisables ici
double periodeBattements; // = 150 tic * 4ms par tick / 1000 = 0.6 secondes
double periodeRespi;

int dureeBattement = 10;

//Lecture depuis Serial
boolean choixFrequence;
char ser;
String frequence_cardiaque_lue;
String frequence_respi_lue;

double pourcentage;


//Pour liaison série
const int len = 60;
char my_str[len];
char pos;

int incomingbyte = 0;


//Pour automate arduino
int MS = 8;
int valve = 51;
int coeur = 53;
int buzzer = 49;

void setup() {
  Serial.begin(2000000);
  //Serial.println("Ready");
  pinMode(MS,OUTPUT);
  pinMode(valve,OUTPUT);
  pinMode(coeur,OUTPUT);
  pinMode(buzzer,OUTPUT);
  digitalWrite(valve,HIGH);
  analogWrite(MS,HIGH);
  
//Interruption
  cli(); // Désactive l'interruption globale
  bitClear (TCCR2A, WGM20); // WGM20 = 0
  bitClear (TCCR2A, WGM21); // WGM21 = 0 
  TCCR2B = 0b00000110; // Clock / 256 soit 16 micro-s et WGM22 = 0
  TIMSK2 = 0b00000001; // Interruption locale autorisée par TOIE2
  sei(); // Active l'interruption globale

  readFromSerial = 0; //Ne passe à 1 que lors de l'interruption

}

int varCompteur = 0; // La variable compteur pour l'interruption
int varCompteurEntreBattements = 0; //Interruption pour contrôler le moteur haptique
int varCompteurRespi = 0; //Interruption pour contrôler la respiratio
int varCompteurDiurese = 0;

// Routine d'interruption
ISR(TIMER2_OVF_vect) 
{
  TCNT2 = 256 - 248; // 250 x 16 µS = 4 ms
  
  if (varCompteurEntreBattements++ == int(periodeBattements - dureeBattement) )
  {
    digitalWrite(coeur,HIGH); // Coeur on
  }
  if (varCompteurEntreBattements > periodeBattements )
  {
    varCompteurEntreBattements = 0;
    digitalWrite(coeur,LOW); // Coeur off
  }

    if (int varCompteurDiurese++ == int(periodeDiurese - dureeBattement) )
  {
    digitalWrite(buzzer,HIGH);
  }
  if (varCompteurDiurese > periodeDiurese )
  {
    varCompteurDiurese = 0;
    digitalWrite(buzzer,LOW);
  }

  if (varCompteurRespi++ == int(periodeRespi/2))
  {
    //Serial.println("Expiration");
    digitalWrite(valve,HIGH); //On ouvre l'électrovanne pour laisser échapper l'air
    inspi = 0; //On termine la séquence d'inspiration
    fan_voltage = 0;
    
  }
  if (varCompteurRespi > periodeRespi)
  {
    //Serial.println("Inspiration");
    inspi = 1; //On déclenche la séquence d'inspiration
    digitalWrite(valve,LOW); //On ferme l'électrovanne pour gonfler le poumon
    varCompteurRespi = 0;
  }

  if ((inspi == 1) && (fan_voltage < 255))
  {
    fan_voltage += 255.0/((1.0/3)*periodeRespi); //Calcul de la quantité à incrémenter la tension toutes les 4 ms pour obtenir un gonflement doux
    analogWrite(MS,fan_voltage);
  }
}

void loop() {
  choixFrequence = 0;
  frequence_cardiaque_lue = "";
  frequence_respi_lue = "";
  if (Serial.available() > 0){
    do{
      ser = Serial.read();
      if (ser=='c'){choixFrequence = 1;}
      else if (ser != -1){
        if (choixFrequence == 0){
          frequence_cardiaque_lue += ser;
        }
        else if (choixFrequence == 1){
          frequence_respi_lue += ser;
          }
      }
    }while (ser != 'r');
  }
  if (frequence_cardiaque_lue != ""){
    frequence_cardiaque = frequence_cardiaque_lue.toDouble();
    frequence_respiratoire = frequence_respi_lue.toDouble();
    periodeBattements = (60*1000.0)/(4*frequence_cardiaque);
    periodeRespi = (60*1000.0)/(4*frequence_respiratoire);
  }
}
