# Online POS replacement

## Seeding the database
Define environment variables in a `.env` file:
```
ROOT_DIR=*the root directory of the files to be seeded*
PASSWORD=*your password*
```
Then install dependecies and create the database
```
pip install -r requirements.txt
touch database.db
```
And run the seeding (it will take around 30 mins or more)
```
python init.db
```

## Creating the executable for windows
Open the CMD on a windows machine and navigate to the directory. Use `pyinstaller` to create the executable. It might be helpful to create a virtual environment on windows
```
python3 -m venv .venv_win
.venv_win\Scripts\activate
pip install -r requirements
```
```
pyinstaller -F get_data.py --distpath .
```
This will output the executable `get_data.exe`
## Running the executable on windows
Navigate to the folder using CMD run the executable
```
get_data.exe -h
```