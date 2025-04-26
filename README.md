# CSV Visualizer
Приложение для визуализации CSV данных на Python с PyQt5

## Установка
1. Клонировать репозиторий:
```bash
git clone https://github.com/Kuzmina-Karina/kursovaya.git
```


2. установить зависимости
```bash
pip install -r requirements.txt
```


3. Скомпилировать C++ модуль (опционально):
```bash
cd cpp
g++ -shared -fPIC -o libfast_search.dylib fast_search.cpp
cp libfast_search.dylib ../
```


4. Запустить приложение:
```bash
python main.py
```
или
```bash
python3 main.py
```