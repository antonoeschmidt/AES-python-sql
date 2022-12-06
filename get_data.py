from aes import AESCipher
from getpass import getpass
import sqlite3
import argparse

SALT="salt2162"

class Args:
    def __init__(self, args):
        self.cpr: str = args.cpr
        self.dob: str = args.dob
        self.name: str = args.name
        self.show: bool = args.show
        self.output: str = args.output
        self.verbose: int = args.verbose

def get_db_connection():
    db_file = "database.db" # Hardcoded to cope with windows filesystem when running an executable
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    return connection

def get_header():
    connection = get_db_connection()
    header = connection.execute('SELECT Headers FROM headers').fetchone()[0]
    connection.close()
    return header

def citizen_by_cpr(cpr):
    connection = get_db_connection()
    results = connection.execute('SELECT * FROM testResults WHERE CPRnummer = ?',
                                 (cpr,)).fetchall()
    connection.close()
    return {'results': [dict(result) for result in results]}

def citizen_by_cpr_count(cpr):
    connection = get_db_connection()
    count = connection.execute('SELECT COUNT(*) FROM testResults WHERE CPRnummer = ?',
                               (cpr,)).fetchone()[0]
    connection.close()
    return count

def citizen_by_dob(dob, name):
    connection = get_db_connection()
    print("Searching for results...")
    if name:
        distinct_results = connection.execute('SELECT DISTINCT CPRnummer FROM testResults WHERE CPRnummer LIKE ? AND (Fornavn LIKE ? OR Efternavn LIKE ?)',
                                     (f"{dob}%", f"%{name}%", f"%{name}%")).fetchall()
    else:
        distinct_results = connection.execute('SELECT DISTINCT CPRnummer FROM testResults WHERE CPRnummer LIKE ?',
                                 (f"{dob}%",)).fetchall()
    parsed_distinct = [dict(result) for result in distinct_results]
    results = [connection.execute('SELECT CPRnummer, Fornavn, Efternavn FROM testResults WHERE CPRnummer = ?'
                                        , (distinct['CPRnummer'],)).fetchone() for distinct in parsed_distinct]
    connection.close()
    return [dict(res) for res in results]

def program(args: Args):
    if args.show:
        data = citizen_by_cpr(args.cpr)
        header = get_header()
        if (data['results'] == []):
            print("No results found.")
            return
        key = getpass()
        print("Decrypting results...")
        aes_cipher = AESCipher(key, SALT)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(header)
                [f.write(aes_cipher.decrypt(result['Data']).decode('utf-8')) for result in data['results']]
                print(f"Results written to {args.output}")
        else:
            print(header)
            [print(aes_cipher.decrypt(result['Data']).decode('utf-8')) for result in data['results']]

    elif args.cpr:
        print(f"{citizen_by_cpr_count(args.cpr)} test results found.")
    
    elif args.dob:
        res = citizen_by_dob(args.dob, args.name)
        if res == []:
            print("No results found")
            return
        
        print(f"{len(res)} person(s) found")
        print("CPR\t\tName")
        [print(f"{data['CPRnummer']}\t{data['Fornavn']} {data['Efternavn']}") for data in res]
        
    else:
        print("No action specified.")

def main():
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument('-c', '--cpr', action='store',
        help="CPR number to search for")
    argparser.add_argument('-d', '--dob', action='store',
        help="Date of birth to search for")
    argparser.add_argument('-n', '--name', action='store',
        help="Name to search for")
    argparser.add_argument('-s', '--show', action='store_true',
        help='Decrypts and shows the data')
    argparser.add_argument('-o', '--output', action='store',
        help="Output file to write the data to")
    argparser.add_argument('-v', '--verbose', action='count', default=0,
        help='Print detailed progress information.')

    args = argparser.parse_args()
    program(Args(args))

if __name__ == "__main__":
    main()



