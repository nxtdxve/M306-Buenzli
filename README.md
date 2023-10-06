# M306-Buenzli
For the Modul 306 in BZZ. It allows Energieagentur Bünzli to efficiently manage the data from the electricity meters of the swiss power grid by visualising the data. The software is capable to read sdat- and ESL-Files and display the data in a graph. The software is also capable to export the data in a CSV-File and a JSON-File and can load the Data with http POST on a server. The software is written in Python and uses tkinter for the GUI.

## Table of Contents

- [M306-Buenzli](#m306-buenzli)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Usage](#usage)
  - [How to use](#how-to-use)
  - [Technologies Used](#technologies-used)
  - [License](#license)

## Features
- Read sdat-Files
- Read ESL-Files
- Display the data in a graph
- Export the data in a CSV-File
- Export the data in a JSON-File
- Load the data with http POST on a server

## Usage
- Load the sdat- and ESL-Files in the software
- Software read the data and allows the selection of consumption data or meter reading data
- Software displays the data in a graph
- Software allows the export of the data in a CSV-File
- Software allows the export of the data in a JSON-File
- Software allows the load of the data with http POST on a server

## How to use
 ```bash
   git clone git@github.com:nxtdxve/M306-Buenzli.git
```
 Open the project in a virtual environment. Put the sdat- and ESL-Files in the data directory if this is the first time you're using the software. If you changed the language you'll have to restart the software.

## Technologies Used
- Python
- GUI: Dear PyGui
- Graph: Dear PyGui

## License
This project is licensed under the MIT License.
