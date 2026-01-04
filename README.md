# esp32-micropython-dmx512-artnet-rs485

Ansteuerung von DMX-Lampen via **PC_DIMMER → Art-Net → DMX512 Bridge** auf Basis eines ESP32 mit MicroPython und MAX485 RS485-Transceiver.

---

## Inhaltsverzeichnis

1. Projektübersicht  
1. Zielsetzung  
1. Systemarchitektur  
1. Hardware-Komponenten  
1. Schaltplan / Verdrahtung  
1. MAX485 – Funktionsweise  
1. DMX512-Protokoll – Frameaufbau und Timings  
1. Art-Net – UDP-DMX  
1. Softwarearchitektur  
1. Installation & Inbetriebnahme  
1. Signal-Analyse – Logikanalysator  
1. Platinenlayout  
1. 3D-Gehäuse  
1. Quellen  

---

## Projektübersicht

Dieses Projekt implementiert eine performante **Art-Net-zu-DMX512-Bridge** mit folgenden Eigenschaften:

- ESP32 mit MicroPython  
- UART @ **250 kBaud, 8N2**  
- RS485-Treiber **MAX485**  
- UDP-Art-Net Empfang auf Port **6454** (z. B. PC_DIMMER)  
- DMX-Frame-Rate ca. **40 Hz**

---

## Zielsetzung

- Empfang von Art-Net-Frames über WLAN  
- Verarbeitung der DMX-Daten auf dem ESP32  
- Erzeugung normkonformer DMX512-Frames  
- Ausgabe über MAX485 auf den RS485-Bus  
- Saubere Trennung von **Break / MAB** und Nutzdaten

---

## Systemarchitektur

```text
PC_DIMMER / Lichtsoftware
        │ UDP 6454 – WLAN
        ▼
        ESP32 ─── UART2 ─── MAX485 ─── DMX512 Bus ─── Fixtures
````

---

## Hardware-Komponenten

| Bauteil              | Beschreibung              |
| -------------------- | ------------------------- |
| ESP32 Dev Board      | MicroPython-fähiges Board |
| MAX485 Modul         | TTL ↔ RS485 Wandler       |
| XLR-3 / XLR-5 Buchse | DMX-Ausgang               |

### Komponentenbilder

![](:/max485_front.png)
![](:/esp32_board.png)

---

## Schaltplan / Verdrahtung

| ESP32 Pin | Funktion    | MAX485  |
| --------- | ----------- | ------- |
| GPIO17    | UART2 TX    | DI      |
| GPIO16    | UART2 RX    | RO      |
| GPIO4     | BREAK / MAB | DE & RE |
| 3.3 V     | Versorgung  | VCC     |
| GND       | Masse       | GND     |

---

## MAX485 – Funktionsweise

Der MAX485 wandelt die TTL-UART-Signale des ESP32 in differentielle RS485-Pegel und ermöglicht damit eine störsichere DMX-Übertragung über längere Distanzen.

* **DI** – Daten vom ESP32
* **RO** – Daten zum ESP32
* **DE / RE** – Sende- und Empfangsfreigabe
* Halbduplex-Betrieb für DMX512

### Quelle

CircuitState – *What is RS-485 & How to use MAX485 with Arduino for reliable long-distance serial communication*
[https://www.circuitstate.com/tutorials/what-is-rs-485-how-to-use-max485-with-arduino-for-reliable-long-distance-serial-communication/](https://www.circuitstate.com/tutorials/what-is-rs-485-how-to-use-max485-with-arduino-for-reliable-long-distance-serial-communication/)

---

## DMX512-Protokoll – Frameaufbau und Timings

### Aufbau

| Abschnitt              | Dauer    |
| ---------------------- | -------- |
| Break                  | ≥ 88 µs  |
| Mark After Break (MAB) | ≥ 8 µs   |
| Startcode              | 1 Byte   |
| Slots 1–512            | 512 Byte |
| Stopbits               | 2 Bit    |

### Zeitdiagramm

```text
| BREAK | MAB | Startcode | Slot1 | Slot2 | ... | Slot512 |
```

### Parameter

* Baudrate: **250 000 Baud**
* Format: **8N2**
* Framezeit: ca. **30 ms** → ca. **40 Hz**

---

## Art-Net – UDP-DMX

* Port: **6454**
* Opcode: **0x5000 (ArtDMX)**
* Universe: **0–15**
* Nutzdaten: **max. 512 Kanäle**

---

## Softwarearchitektur

| Datei     | Funktion                      |
| --------- | ----------------------------- |
| `boot.py` | WLAN-Initialisierung          |
| `main.py` | Art-Net Empfang + DMX-Ausgabe |
| `wlan.py` | WLAN-Verbindung               |

---

## Installation & Inbetriebnahme

1. MicroPython auf den ESP32 flashen
2. WLAN-Zugangsdaten in `wlan.py` eintragen
3. Dateien auf den ESP32 kopieren
4. Neustart durchführen
5. Art-Net-Quelle auf **Universe 0** konfigurieren

---

## Signal-Analyse – Logikanalysator

![](:/dmx_break_analysis.png)
![](:/dmx_uart_decode.png)

Hier werden später folgende Messungen dokumentiert:

* Break-Länge
* MAB-Zeit
* UART-Decoding der Slots

---

## Platinenlayout

![](:/pcb_layout.png)

---

## 3D-Gehäuse

![](:/3d_case_render.png)

---

## Quellen

* CircuitState – MAX485 RS485 Tutorial
* ESTA DMX512-A Standard
* Art-Net Spezifikation
