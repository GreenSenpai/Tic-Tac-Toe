Šis kursinis yra TIC-TAC-TOE žaidimas.

Jis yra paleidžiamas per cmd konsolė, naudojant cd komanda ir parašant aplankalo vardą, kur yra programa.

Tada turi buti instaliuota python compiler ir yra parašoma "pyhon main.py" ir žaidimas pasileidžia konsolėje.

Anlogiškai paleidžiamas ir testų failas naudojant "python -m unittest test_tictactoe.py" komandą.

Kur kas yra naudojama?


Abstraction:

![image](https://github.com/user-attachments/assets/e5624067-efe3-46bc-8858-005f2b11512c)

Sukuriame klasę, ir funkcijas, kurioms nepriskiriam jokiu veiksmų.

Encapsulation and Inheretance and Aggregation:

![image](https://github.com/user-attachments/assets/09acdca9-e162-4095-abcf-e150f706b922)

Naudojame privačias klases, todėl tai yra encapsulation.

Ši klasė paveldi taip pat paveldi abstrakčios klasės Game savybes, todėl tai yra inheritance.

Taip pat ši klasė, naudoją klasę ConsoleSaver, kad išsaugoti žaidimos rezultatus. Console Saver gali egzistuoti be TicTacToe game klasės, todėl tai yra agregacija.

Decorator:

![image](https://github.com/user-attachments/assets/ef0c25d8-3411-4dac-985e-eb47c20cd5c3)

Decorator prideda funkciją į TicTacToeGame jos nekeisdamas, kad kai yra įrašomas X arba O, tą veiksmą išsaugo ir išveda ant ekrano.

Polymorphism ir saugojimas į failą:

![image](https://github.com/user-attachments/assets/9085c960-945c-44f8-8bc0-13be9fd0bac9)

Ši klasė veikia su bet kokiomis Saver pveldenčiomis klasėmis, todėl tai yra Polymorphism.

Kiekvieno žaidimo rezultatai yra išsaugomi į failą ir juos galime pasižiūrėti


Išvados.

Kuriant šį žaidimą buvo sunku panaudoti visus OOP programavimo principus, nes žaidimas nera sudėtingas ir žymiai lengviau kodą parašyti jų nenaudojant.

Rašant šį darbą padėjo dirbtinis intelektas, tik kartais buvo sunku suprasti jo naudojamą sintaksę ir funkcijas.

Buvo parašyti ir preiti visi Unit testai, kurie patikrina ėjimus, išsaugomus rezultatus.



