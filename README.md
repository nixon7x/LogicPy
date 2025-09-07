# LogicPy
A Python-based interactive logic gate simulator with drag-and-drop components, wiring, saving, loading, and real-time circuit evaluation.

## Features

- Drag-and-drop placement of logic gates and components  
- Interactive wiring system with bend points  
- Switches to toggle signals ON/OFF  
- LEDs to display outputs in real-time  
- Save and load circuits (JSON format)  
- Real-time evaluation of logic gates  
- Delete components and wires easily
**Note:** Your circuit will be saved and loaded using the file named `circuit.json`.
**Warning:** Be careful! Saving will overwrite the existing `circuit.json` file!
### Supported Components

- **Logic Gates:** AND, OR, NOT, NAND, NOR, XOR, XNOR  
- **Input Components:** Switch  
- **Output Components:** LED  
- **Wires:** Connect components with flexible wiring and bend points

## Installation

1. Make sure Python 3.8+ is installed  
2. Install pygame and numpy:  
   ```bash
   pip install pygame, numpy
   ```  
3. Clone this repository:  
   ```bash
   git clone <(https://github.com/EgeOnderX/LogicPy)>
   ```  
4. Run the simulator:  
   ```bash
   python main.py
   ```

## Usage

- Click on a component from the sidebar to select it  
- Click on the canvas to place the selected component  
- Drag components to reposition them  
- Click on slots to start and end wiring  
- Right-click on wires or components to delete them  
- Press `S` to save the current circuit  
- Press `L` to load the last saved circuit

## Screenshots

<img width="998" height="627" alt="image" src="https://github.com/user-attachments/assets/e4670bcd-4654-4e59-85b5-e4c1b3bd4706" />


## License

MIT License

Copyright (c) 2025 Ege Önder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
