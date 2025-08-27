/*Here, I'm using the the assigning numbers to some variables, so that I won't make mistakes or use wrong pin number later in the code*/
const int forcesensor = 14;   // I've connected force sensor to analog pin A0 (which is pin 14 here)
const int ascendingled = 10;  // I've chosen Green LED for Ascending, it turns on when the device is ascending
const int apogeeled = 11;     // I've chosen Blue LED for Apogee: it turns on when the device is at apogee (peak)
const int descendingled = 12; // I've chosen Red LED for Descending: it turns on when the device is descending
const int piezobuzzer = 9;    // I've put Piezo buzzer at pin 9

// Here, I've defined the variables that'll be used for tracking state of the device 

int lastState = 0; //This variable is defined to tell the previous state of the device
                   // Here,0 = unknown, 1 = ascending, 2 = apogee, 3 = descending
int threshold = 5; // This is what I've chosen as the minimum difference to consider a "real" change
int samples = 10;  // Here, I've chosen the number of readings to take and average for noise filtering

void setup() {
  pinMode(ascendingled, OUTPUT);
  pinMode(apogeeled, OUTPUT);
  pinMode(descendingled, OUTPUT);
  pinMode(piezobuzzer, OUTPUT);
  
  //This function initiates the communication with Arduino so we can see what the code is doing
  Serial.begin(9600);          
}
// Here, I'm going to define a function to get average of multiple sensor readings
// It will help me smooth out noisy sensor values
int getAverageReading() {
  long sum = 0;         // I've used long here in case if the value of sum of the readings is big
  for (int i = 0; i < samples; i++) {
    sum = sum + analogRead(forcesensor);/* analogRead is used to read the value from 
                                           a specified analog input pin, here, it is reading the imput from 
                                           the pin A0, to which, force sensor is connected*/
    delay(5);                  // I've used this function to make tiny delay so sensor has time between the readings
  }
  return sum / samples;        // It returns the average value
}

// This is the loop that runs forever, so that we can get data everytime the loop runs again. 
void loop() {
  // I used this function to take two averages back to back
  int prevAvg = getAverageReading();
  int currAvg = getAverageReading();

  // Here, I am using this to calculate the difference
  int diff = currAvg - prevAvg;

  /* Here, I'm switching off all LEDs at the start of each loop, 
  so that the LED/Buzzer that was switched on before won't remain turned on*/
  digitalWrite(ascendingled, LOW);
  digitalWrite(apogeeled, LOW);
  digitalWrite(descendingled, LOW);

  // Here, I'm using if and else to check the state of the device
  if (diff < -threshold) {
    // If Pressure drops -> Force value going DOWN -> object going UP (ascending)
    digitalWrite(ascendingled, HIGH);
    lastState = 1; //then the laststate will be assigned the value 1
    Serial.println("Ascending");

  } else if (diff > threshold) {
    // If Pressure increases -> Force value going UP -> object going DOWN (descending)
    digitalWrite(descendingled, HIGH);
    lastState = 3; //then the laststate will be assigned the value 3
    Serial.println("Descending");

  } else {
    // If there is Small/no change -> could be apogee or just resting

   /*Initially, the code was giving the signal of apogee even 
   if the device came to rest after descent, so I added another condition here.
   I've explained it below*/
    /* To differentiate the resting situations, i.e., one after ascending(true apogee) 
       and one after descending, I'm using if again to only allow the situations, in which
       the previous state was either ascending or already at apogee.
    */
    if (lastState == 1 || lastState == 2) {
      //If it was ascending or alreasy at apogee
      digitalWrite(apogeeled, HIGH);
      tone(piezobuzzer, 1000, 200);     // Here, the tone function will make the buzzer beep at 1kHz frequency for 200ms
      lastState = 2; //then the laststate will be assigned the value 2
      Serial.println("Apogee");
    } else {
      // If we came from descending or were stable before, then the buzzer should not be beeped.
      Serial.println("Either the device didn't take off or came to stable position after descent)");
    }
  }

  delay(200); /* I'm making a small delay here so that we can avoid rapid
                 switching between states, so we can notice 
                 the states clearly (it gives time to view the 
                 LED lights clearly, n help us avoid rapid buzzing 
                 of piezo buzzer)*/
}
/*So, Here's the code of Task-2, I don't know if it's best one you've seen yet,
 but it is definitely the best one I could come up with, for now:) */