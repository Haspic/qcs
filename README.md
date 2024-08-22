# Quantum Circuit Simulator (qcs)

This program is a (very) basic simulator of quantum circuits.
Drag gates from the widget frame into the circuit frame and see the resulting
states probability distribution of your circuit.

You can right-click 'A' gates in order to edit the position of the target/control gates.

#### Here is an overview of the general structure:

```
<main> ─┬─ dragable widgets (dragable gates)    -   -   -   -   -   -   -   -   -   -   -   .
        │                                                                                   .
        ├─ {widget frame}                                                                   .
        │                                                                                   V
        ├─ secondary buttons (plot, clear, dynamic plot)
        │                                                                     ┌─ dynamic buttons (gate)
        ├─ {circuit frame} ─┬──┬─ {qubit sub-frame 1} ── [dynamic content] ── &
        │                   │  ├─ {qubit sub-frame 2} ── [...]                └─ dynamic canvas (empty space)
        │                   │  ⁞
        │                   │  └─ {qubit sub-frame n} ── [...]
        │                   │
        │                   └──── conversion to simulator                                                     
        │                                   '
        └─ {plot frame} ── plot             '                   
                            Λ               '
                            '               '
                            '               '
                            '               '
<circuit> ───── get probabilities   <   -   '
```


Additional information:
Variable / terms naming within hasn't been the most thorough, namely for:
- qubits / lines
- control / activator
- target / gate
- 'simple' gates (Z, H, I ..)
- 'complex' gates (CZ, CH, and all other control/target gates)

This project has been worked on and tested with python 3.11.

### Package requirements:
- numpy
- matplotlib

In order to run this program simply run the main.py
```
python main.py
```
