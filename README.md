````markdown
# esp32-micropython-dmx512-artnet-rs485
Ansteuerung Lampen via PC_DIMMER → Art-Net → DMX512 Bridge auf Basis eines ESP32 mit MicroPython und MAX485 RS485-Transceiver.

---

## Inhaltsverzeichnis

1. Projektübersicht  
1. Zielsetzung  
1. Systemarchitektur  
1. Hardware-Komponenten  
1. Schaltplan / Verdrahtung  
1. MAX485 – Funktionsweise  
1. DMX512-Protokoll – Frameaufbau und Timings  
1. Art-Net – UDP-DMX über Ethernet  
1. Softwarearchitektur  
1. Installation & Inbetriebnahme  
1. Signal-Analyse – Logikanalysator  
1. Platinenlayout (Platzhalter)  
1. 3D-Gehäuse (Platzhalter)  
1. Quellen  

---

## Projektübersicht

Dieses Projekt implementiert eine performante Art-Net-zu-DMX512-Bridge mit:

- ESP32  
- MicroPython  
- UART @ 250 kBaud, 8N2  
- RS485-Treiber MAX485  
- UDP-ArtNet Empfang auf Port 6454  (PC_DIMMER)

Die Umsetzung ist vollständig echtzeitfähig mit ca. 40 Hz DMX-Frame-Rate.

---

## Zielsetzung

- Empfang von Art-Net DMX-Frames über WLAN  
- Verarbeitung auf einem ESP32  
- Erzeugung normkonformer DMX512-Frames  
- Ausgabe über MAX485 auf RS485-Bus  
- Vollständige Trennung von Break/MAB und Nutzdaten  

---

## Systemarchitektur

```text
ArtNet Client (PC_DIMMER)
        │ UDP 6454 - WLAN
        ▼
        ESP32 ─── UART2 ─── MAX485 ─── DMX512 Bus ─── Fixtures
```

---

## Hardware-Komponenten

| Bauteil                   | Beschreibung              |
| ------------------------- | ------------------------- |
| ESP32 Dev Board           | MicroPython-fähiges Board |
| MAX485 Modul              | TTL ↔ RS485 Wandler       |
| XLR-3 / XLR-5 Buchse      | DMX-Ausgang               |

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
| 3.3 V     | VCC         | VCC     |
| GND       | GND         | GND     |

---

## MAX485 – Funktionsweise

Der MAX485 konvertiert TTL-UART-Signale in differentielle RS485-Pegel und umgekehrt.

* **DI** – Daten vom ESP32
* **RO** – Daten zum ESP32
* **DE / RE** – Treiber- und Empfängersteuerung
* Halbduplex-Betrieb für DMX512

### Quelle

CircuitState – *What is RS-485 & How to use MAX485*

---

## DMX512-Protokoll – Frameaufbau und Timings

### Aufbau

| Abschnitt              | Dauer     |
| ---------------------- | --------- |
| Break                  | ≥ 88 µs   |
| Mark After Break (MAB) | ≥ 8 µs    |
| Startcode              | 1 Byte    |
| Slots 1-512            | 512 Bytes |
| Stopbits               | 2 Bit     |

### Zeitdiagramm

```text
| BREAK | MAB | Startcode | Slot1 | Slot2 | ... | Slot512 |
```

### Parameter

* Baudrate: 250 000
* Format: 8N2
* Framezeit: ca. 30 ms → 40 Hz

---

## Art-Net – UDP-DMX

* Port: 6454
* Opcode: 0x5000 (ArtDMX)
* Universe: 0-15
* Nutzdaten: max. 512 Kanäle

---

## Softwarearchitektur

| Datei     | Funktion                      |
| --------- | ----------------------------- |
| `boot.py` | WLAN-Initialisierung          |
| `main.py` | ArtNet Empfang + DMX-Ausgabe  |
| `wlan.py` | WLAN-Verbindung               |

---

## Installation & Inbetriebnahme

1. MicroPython auf ESP32 flashen
2. WLAN-Zugangsdaten in `wlan.py` anpassen
3. Dateien auf ESP32 kopieren
4. Neustart durchführen
5. Art-Net-Quelle auf Universe 0 konfigurieren

---

## Signal-Analyse – Logikanalysator (Platzhalter)

![](:/dmx_break_analysis.png)
![](:/dmx_uart_decode.png)

Hier werden später:

* Break-Länge
* MAB-Zeit
* UART-Decoding

dokumentiert.

---

## Platinenlayout (Platzhalter)

![](:/pcb_layout.png)

---

## 3D-Gehäuse (Platzhalter)

![](:/3d_case_render.png)

---

## Quellen

* MAX485 RS485 Tutorial – CircuitState

* ESTA DMX512-A Standard

* Art-Net Spezifikation
