# Lenguaje de programación Platzi

Source code for the Interpreters course at Platzi.

# Install dependencies

1. Create a virtual environment:
```bash
python3.8 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies
```bash
pip3 install -r requirements.txt
```

# Run type checker and test suite

To run the type checker and and the test suite run the following command from
the root directory.

```bash
mypy . && nosetests
```

# Run the interpreter
```bash
python3.8 main.py
```

# A sneak peak of the language
```
Bienvenido al Lenguaje de Programación Platzi.
Escribe un oración para comenzar.
>> variable a = 5;
>> variable b = 10;
>> a + b;
15
>> variable mayor_de_edad = procedimiento(edad) { 
        si(edad > 18) { 
            regresa verdadero;
        si_no {
            regresa falso;
        }
    };
>> mayor_de_edad(20);
verdadero
>> mayor_de_edad(15);
falso
>> variable sumador = procedimiento(x) {
       regresa procedimiento(y) {
           regresa x + y;
       };
   };
>> variable suma_dos = sumador(2);
>> suma_dos(5);
7
>> variable suma_cinco = sumador(5);
>> suma_cinco(20);
25
>> mayor_de_edad(suma_cinco(20));
verdadero
```
