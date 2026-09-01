# 📊 Ultrasonic A-Scan Analyzer

> An interactive ultrasonic NDT analysis laboratory for visualizing, processing, and interpreting A-scan signals, with a focus on echo detection, time-of-flight, amplitude analysis, and reflector identification.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
[![NumPy](https://img.shields.io/badge/Numerical-NumPy-orange?logo=numpy)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?logo=matplotlib)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img width="966" height="510" alt="image" src="https://github.com/user-attachments/assets/5c671125-0914-4e34-98d2-bf06c4e2e96a" />


---

## 📌 Overview

**Ultrasonic A-Scan Analyzer** is an interactive desktop application for studying and interpreting **A-scan ultrasonic signals** used in Non-Destructive Testing (NDT).

An A-scan displays ultrasonic signal amplitude as a function of time or distance. Peaks within the waveform can represent reflections from material interfaces, back walls, defects, or other acoustic reflectors.

This project provides a virtual analysis environment for exploring:

* A-scan waveform visualization
* Ultrasonic echo detection
* Time-of-flight analysis
* Echo amplitude
* Reflector identification
* Material depth estimation
* Signal attenuation
* Noise
* Signal processing
* NDT inspection concepts

---

# ✨ Key Features

## 📈 A-Scan Visualization

The analyzer displays an ultrasonic waveform in an A-scan-style format.

```text id="a9v3kd"
Amplitude
   │
   │   █
   │   █
   │   █                 █
   │   █                 █
───┼───█─────────────────█──────────► Time
       │                 │
    Initial             Echo
     Pulse
```

The horizontal axis represents time, while the vertical axis represents signal amplitude.

Distinct peaks can indicate ultrasonic reflections within the inspected material.

---

# 🔊 Understanding an A-Scan

An A-scan is one of the fundamental data representations used in ultrasonic testing.

The basic relationship is:

```text id="p7m2cx"
X-Axis → Time / Distance
Y-Axis → Signal Amplitude
```

A typical pulse-echo A-scan may contain:

```text id="k5q8za"
Initial Pulse
      │
      ▼
     █
     █
─────█───────────────────────█────────► Time
                             █
                             █
                         Back-Wall Echo
```

Additional peaks between the initial pulse and back-wall echo may indicate internal reflectors or discontinuities.

---

# 🎯 Echo Detection

Echoes appear as peaks within the received ultrasonic waveform.

Conceptually:

```text id="z8n4rw"
Amplitude
   │
   │     ▲
   │     │
   │     │            ▲
   │     │            │
───┼─────┼────────────┼──────────────► Time
       Echo 1       Echo 2
```

The location and amplitude of each peak can provide information about:

* Reflector position
* Reflector strength
* Material interfaces
* Defect location
* Back-wall position

---

# ⏱️ Time-of-Flight Analysis

The analyzer can be used to study the time taken by an ultrasonic pulse to reach a reflector and return to the transducer.

For pulse-echo inspection:

```text id="f1r8yh"
TOF = 2d / v
```

where:

* `TOF` = round-trip time
* `d` = reflector depth
* `v` = material sound velocity

Therefore:

```text id="s5c7ue"
d = v × TOF / 2
```

This relationship allows the A-scan to be interpreted in terms of reflector depth.

---

# 📐 Depth Estimation

A simplified inspection geometry is:

```text id="q4w6zn"
             Probe
               │
               │
               ▼
        ┌─────────────┐
        │             │
        │   MATERIAL  │
        │             │
        │      ●      │ ← Reflector
        │             │
        │             │
        ├─────────────┤
        │  BACK WALL  │
        └─────────────┘
```

The time position of an echo can be converted into an estimated depth when the ultrasonic velocity is known.

```text id="g2r5mx"
Echo Time
    ↓
Material Velocity
    ↓
Travel Distance
    ↓
Reflector Depth
```

---

# 📊 Echo Amplitude

Echo amplitude represents the relative strength of a reflected ultrasonic signal.

A simplified A-scan might look like:

```text id="n7c3pw"
Amplitude
   │
   │     █
   │     █
   │     █             ███
   │     █             ███
───┼─────█─────────────███──────────► Time
       Initial        Strong
        Pulse         Echo
```

A larger peak generally represents a stronger received reflection.

However, echo amplitude is influenced by many factors, including:

* Reflector orientation
* Reflector size
* Acoustic impedance
* Probe characteristics
* Gain
* Attenuation
* Coupling
* Beam angle
* Material structure

---

# 🔍 Reflector Identification

A-scan analysis can help identify potential reflectors within a material.

Potential reflectors include:

* Cracks
* Voids
* Inclusions
* Delaminations
* Lack of fusion
* Lack of penetration
* Interfaces
* Back walls

A simplified signal interpretation might be:

```text id="c6j9xe"
Initial Pulse       Defect          Back Wall
     │                 │                │
     ▼                 ▼                ▼
     █                 █                █
─────█─────────────────█────────────────█──► Time
```

The position of the defect echo relative to the back-wall echo can provide information about its approximate location.

---

# 📉 Signal Attenuation

Ultrasonic signals lose energy as they propagate through a material.

The received echo amplitude can therefore decrease with increasing propagation distance.

```text id="b4v8qy"
Distance ↑
    ↓
Propagation Loss ↑
    ↓
Echo Amplitude ↓
```

Attenuation can be associated with:

* Absorption
* Scattering
* Material microstructure
* Frequency
* Propagation distance

The simulator provides a simplified environment for studying these effects.

---

# 📡 Gain and Signal Visibility

In practical ultrasonic testing, instrument gain is used to amplify received signals for analysis.

Conceptually:

```text id="m8q1td"
Low Gain

      █
──────█────────────


Higher Gain

      ███
──────███──────────
```

Increasing gain can make weak echoes more visible, but it also increases the visibility of noise and other unwanted signals.

Therefore, gain must be interpreted carefully during inspection.

---

# 🚧 Gate Concept

A measurement gate defines a region of the A-scan where the instrument searches for a signal.

```text id="u6v3pa"
Amplitude
   │
   │                         █
   │                         █
   │        ┌──────────────┐ █
───┼────────│     GATE     │─█──────► Time
   │        └──────────────┘
            ↑              ↑
          Start            End
```

A gate can be used to:

* Search for defects
* Measure echo amplitude
* Determine echo position
* Trigger alarms
* Automate inspection decisions

---

# 📐 Gate-Based Analysis

A simplified inspection workflow is:

```text id="d3k5vz"
A-Scan
  │
  ▼
Define Gate
  │
  ▼
Search Signal
  │
  ▼
Detect Peak
  │
  ├──────────────► Amplitude
  │
  └──────────────► Time-of-Flight
                         │
                         ▼
                    Depth Estimate
```

---

# 🧮 Digital Signal Processing

A-scan data can be analyzed using numerical signal-processing techniques.

A typical workflow is:

```text id="v8f2km"
Raw Signal
    │
    ▼
Preprocessing
    │
    ▼
Noise Reduction
    │
    ▼
Peak Detection
    │
    ▼
Time-of-Flight
    │
    ▼
Depth / Thickness
```

Digital processing can help make ultrasonic signals easier to interpret and quantify.

---

# 🔬 A-Scan Analysis Pipeline

```text id="y5c9fr"
┌───────────────────────────────┐
│       Ultrasonic Signal       │
│                               │
│        A-Scan Data            │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Signal Processing       │
│                               │
│ Filtering / Normalization     │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        Peak Detection         │
│                               │
│ Echo Identification           │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       TOF Measurement         │
│                               │
│ Echo Position                 │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Depth Estimation        │
│                               │
│       d = vt / 2              │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       Inspection Result       │
│                               │
│ Reflector / Defect Analysis   │
└───────────────────────────────┘
```

---

# 🧪 Example Experiments

## Experiment 1 — Identify the Back Wall

Analyze an A-scan containing an initial pulse and a strong back-wall echo.

Identify:

```text
Initial Pulse
Back-Wall Echo
Time-of-Flight
```

---

## Experiment 2 — Detect an Internal Reflector

Introduce an additional echo between the initial pulse and back-wall echo.

```text id="w4j7pk"
Initial Pulse     Defect       Back Wall
     │              │              │
     ▼              ▼              ▼
     █              █              █
─────█──────────────█──────────────█──►
```

Determine the approximate reflector depth from its TOF.

---

## Experiment 3 — Compare Echo Amplitudes

Generate weak and strong reflector responses.

Compare:

```text id="x3n6rz"
Weak Echo
   vs
Strong Echo
```

Observe how reflector strength affects the A-scan.

---

## Experiment 4 — Noise Analysis

Increase the simulated noise level.

Observe how the signal-to-noise ratio affects defect identification.

```text id="f7h2nc"
Low Noise
    ↓
Clear Echo


High Noise
    ↓
Difficult Echo Detection
```

---

## Experiment 5 — Gain Adjustment

Change signal gain and observe how the A-scan changes.

Study the trade-off between:

```text id="q9c4yb"
Signal Visibility
       vs
Noise Visibility
```

---

## Experiment 6 — Velocity Variation

Keep the echo arrival time constant while changing material velocity.

Observe how the calculated reflector depth changes.

This demonstrates the importance of using the correct material velocity during ultrasonic inspection.

---

# 🏭 Industrial Applications

A-scan analysis is relevant to ultrasonic inspection across many industries.

### 🛢️ Oil & Gas

* Pipeline inspection
* Pressure vessel inspection
* Corrosion assessment
* Weld inspection
* Storage tank inspection

### ⚓ Marine

* Ship hull inspection
* Subsea structural inspection
* Offshore structures
* Corrosion monitoring

### ✈️ Aerospace

* Aircraft structures
* Composite inspection
* Bond inspection
* Crack detection

### ⚡ Power Generation

* Boiler components
* Turbine components
* Pressure vessels
* Piping systems

### 🏭 Manufacturing

* Weld inspection
* Forgings
* Castings
* Plates
* Tubes

---

# 🔍 NDT Inspection Concepts

This project provides a foundation for understanding:

```text
A-Scan
  │
  ├── Echo Position
  │       ↓
  │   Depth / Distance
  │
  ├── Echo Amplitude
  │       ↓
  │   Reflector Response
  │
  └── Echo Shape
          ↓
      Signal Interpretation
```

---

# 🎓 Educational Applications

The project can be used to demonstrate:

* Ultrasonic A-Scans
* Pulse-Echo Testing
* Time-of-Flight
* Echo Detection
* Peak Detection
* Reflector Identification
* Defect Detection
* Material Depth Estimation
* Thickness Measurement
* Signal Amplitude
* Gain
* Signal-to-Noise Ratio
* Attenuation
* Gate-Based Inspection
* Ultrasonic Signal Processing
* NDT Fundamentals

---

# 🛠️ Technology Stack

| Technology     | Purpose                                     |
| -------------- | ------------------------------------------- |
| **Python**     | Core application                            |
| **NumPy**      | Numerical computation and signal processing |
| **PyQt5**      | Desktop graphical interface                 |
| **Matplotlib** | A-scan visualization                        |

---

# 🚀 Installation

### 1. Clone the repository

```bash id="k2m7sx"
git clone https://github.com/vishwakiran712/Ultrasonic-A-Scan-Analyzer.git
cd Ultrasonic-A-Scan-Analyzer
```

### 2. Install dependencies

```bash id="c5r8vn"
pip install numpy matplotlib PyQt5
```

### 3. Run the application

```bash id="p6w3ya"
python app.py
```

---

# 📂 Project Structure

```text id="h8q1mz"
Ultrasonic-A-Scan-Analyzer/
│
├── app.py
├── README.md
└── LICENSE
```

---

# 🔭 Possible Future Enhancements

Potential extensions include:

* Real A-scan data import
* CSV waveform import
* Real-time A-scan acquisition
* Automatic peak detection
* Adjustable inspection gates
* Multiple gates
* DAC curve
* Time-Corrected Gain
* Distance-Amplitude Correction
* Back-wall detection
* Automatic thickness measurement
* Defect depth calculation
* Echo amplitude measurement
* Signal-to-noise calculation
* Digital filtering
* Envelope detection
* FFT analysis
* Spectrogram
* B-scan generation
* C-scan generation
* A-scan comparison
* Reference waveform overlay
* Measurement data export
* Inspection report generation
* Real ultrasonic instrument integration

---

# ⚠️ Simulation Notice

This application is intended for **education, experimentation, and ultrasonic/NDT research**.

It is a simplified software analysis environment and should not be used as a substitute for calibrated ultrasonic testing equipment, approved inspection procedures, reference standards, or qualified NDT personnel.

Actual A-scan interpretation depends on probe characteristics, calibration, gain, coupling, material properties, beam geometry, surface condition, frequency, attenuation, and inspection technique.

---

# 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

# 👨‍💻 Author

**Vishwakiran B.V.S.**

Engineering • Sports Technology • Product Research • Marine Robotics • NDT • Acoustics • Signal Processing

GitHub: [@vishwakiran712](https://github.com/vishwakiran712)

---

# ⭐ Project

If you find this project useful for learning, ultrasonic experimentation, NDT research, or signal-processing development, consider giving the repository a ⭐.

**Repository:**
https://github.com/vishwakiran712/Ultrasonic-A-Scan-Analyzer
