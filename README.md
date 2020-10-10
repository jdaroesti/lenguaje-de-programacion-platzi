# curso-interpretes-platzi

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
