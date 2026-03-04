# Brain-Controlled Robot — EEG + SVM + Arduino

A real-time Brain-Computer Interface (BCI) system that classifies EEG 
brainwave signals into directional commands (Forward / Backward / Left / Right)
using a Support Vector Machine, then transmits those commands over serial
communication to an Arduino-controlled differential drive robot.

---

## Project Structure

Brain-Controlled-Robot/
├── ml/
│   ├── BCW.py                  # Main ML pipeline
│   ├── serial_communication.py # CSV-based SVM training loop
│   └── model_and_features.pkl  # Pre-trained SVM model
├── arduino/
│   └── motor_control.ino       # Arduino dual-mode motor control
├── data/
│   └── Dataset.csv             # EEG band power feature dataset
└── README.md

---

## How It Works

1. **EEG Signal Acquisition**
   EEG headset records brainwave activity and extracts frequency band 
   power features: Delta, Theta, Alpha1, Alpha2, Beta1, Beta2, 
   Gamma1, Gamma2, and Total Power.

2. **ML Classification (Python)**
   - Features are log-transformed and standardized.
   - A Support Vector Machine (SVM) classifies each sample into one 
     of 4 movement commands: Forward, Backward, Left, Right.
   - A confidence threshold + majority-vote smoothing window filters 
     out uncertain predictions, defaulting to STOP for safety.

3. **Serial Communication**
   The predicted command character (F / B / L / R) is sent over 
   serial port to the Arduino.

4. **Motor Control (Arduino)**
   The Arduino operates in two modes:
   - **Manual Mode** (button released): joystick potentiometers and 
     push buttons control the motors directly.
   - **BCI Mode** (button held): serial commands from the Python 
     classifier drive the motors.

---

## Getting Started

### Python Setup
```bash
pip install numpy pandas scikit-learn joblib pyserial
```

**Train and evaluate the model:**
```bash
cd ml
python BCW.py
```

**Run serial communication classifier:**
```bash
python serial_communication.py
```
> Update the `directory` path inside the script to point to your Dataset folder.

---

### Arduino Setup
1. Open `arduino/motor_control.ino` in the Arduino IDE.
2. Connect your L298N motor driver to the pins defined:
   - Motor A: IN1 (pin 5), IN2 (pin 6)
   - Motor B: IN3 (pin 9), IN4 (pin 10)
   - Mode button: pin 12
   - Joystick X-axis: A0, Y-axis: A1
   - Speed pots: A2, A3
3. Upload to your Arduino board.
4. Set Serial Monitor baud rate to **9600**.

---

## Hardware Requirements

| Component | Purpose |
|-----------|---------|
| EEG Headset | Brainwave signal acquisition |
| Arduino Uno/Mega | Motor control & serial interface |
| L298N Motor Driver | Drive DC motors |
| DC Motors (x2) | Differential drive movement |
| Joystick + Buttons | Manual override control |
| Potentiometers (x2) | Speed control |

---

## ML Model Details

| Model | Accuracy | Notes |
|-------|----------|-------|
| Linear SVM | ~baseline | Fast, balanced class weights |
| RBF SVM (tuned) | best | GridSearchCV over C and gamma |

**Classes:**
| Label | Command |
|-------|---------|
| 0 | Forward |
| 1 | Backward |
| 2 | Left |
| 3 | Right |

**Safety Layer:**
- Predictions below `0.65` confidence → output `STOP`
- Majority vote over last `N=5` samples for command smoothing

---

## Dependencies

- Python 3.8+
- `numpy`, `pandas`, `scikit-learn`, `joblib`, `pyserial`
- Arduino IDE 1.8+

---

## Dataset

`Dataset.csv` contains EEG frequency band power features labeled with 
movement classes. Columns include:
`Delta, Theta, Alpha1, Alpha2, Beta1, Beta2, Gamma1, Gamma2, totPwr, class`
```
