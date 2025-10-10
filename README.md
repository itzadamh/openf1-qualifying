# openf1-qualifying

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/itzadamh/openf1-qualifying?color=blue&logo=opensourceinitiative)](https://github.com/itzadamh/openf1-qualifying/blob/main/LICENSE)

A small project I’m working on using the [OpenF1 API](https://openf1.org/).  
Originally based on the **Singapore 2025 qualifying results**, it now supports **user input** for any Grand Prix.  
Enter the country and year of the race you want to view, and the program will display the qualifying results.

## 🏎️ Project Goal
To explore working with public APIs and display real Formula 1 qualifying data in a simple, readable format.  
This project also serves as a learning exercise for Python, API requests, and working with JSON data.

## ⚙️ Requirements
- **Python 3.x (3.7 or newer recommended)**
- **requests** module

Install dependencies with:

```
pip install requests
```

## 🚀 Usage
Run the program in your terminal:

```
python openf1_qualifying.py
```

Then follow the prompts to enter the race country and year:

```
Please enter the country of the race (e.g. Singapore):
Canada
Please enter the year of the race:
2024
```

## 🧾 Example Output
```
Please enter the country of the race (e.g. Singapore):
Azerbaijan
Please enter the year of the race:
2025

(for this example, this is just pole position - the program shows the whole grid)

Driver: Max VERSTAPPEN | 1
Team: Red Bull Racing
Position: 1
Fastest Lap: 01:41.117
...
```

## 🧩 Planned / Potential Features
- [x] Formatting changes — lap times formatted to `mm:ss.ss`
- [x] User input (e.g. `"Silverstone"`, `"2024"`)
- [ ] Gap timing statistics between drivers
- [ ] Command-line arguments (e.g. `python openf1_qualifying.py monaco 2024`)
- [ ] Option to export results to a text or CSV file

## 🤝 Contributing
Contributions, suggestions, or improvements are welcome!  
If you’d like to help, feel free to:
- Open an **issue** to report a bug or suggest a feature.
- Submit a **pull request** with improvements.

## 📜 License
This project is open-source under the [MIT License](LICENSE).

## 🔗 Resources
- [OpenF1 API Documentation](https://openf1.org/)
- [Python Requests Library](https://requests.readthedocs.io/en/latest/)
