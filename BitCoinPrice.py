from urllib.request import Request, urlopen

from sqlalchemy import create_engine
import json

id = 1

class BitcoinAverage():
    global id

    def __init__(self, average, date):
        global id
        self.id = id
        self.average = average
        self.date = date
        id += 1

    def addToDB(self, bitcoinAverage):
        conn.execute("INSERT INTO bitcoinAvg (average, time) VALUES (" + str(bitcoinAverage.average) + ", '" + str(
            bitcoinAverage.date) + "')")
        pass


def data_parse(data):
    data = data[2:-1]
    a = data.split("\\n")
    data_input = ""
    for i in range(len(a)):
        data_input += a[i].strip()
    db_input = json.loads(data_input)
    for i in range(0, len(db_input)):
        c = BitcoinAverage(db_input[i]["average"],db_input[i]["time"])
        c.addToDB(c)


def main():
    request = Request('https://apiv2.bitcoinaverage.com/indices/global/history/BTCUSD?period=daily&format=json')
    response = urlopen(request)
    data = response.read()
    data_parse(str(data))
    print("--------Bitcoin Prices are stored in database")

def init():
    print("--------Start bitcoinaverage API")
    global eng
    global conn
    eng = create_engine("sqlite:///mydb.db")
    conn = eng.connect()
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bitcoinAvg'")
    results = str(result.first())
    if 'bitcoinAvg' not in results:
        conn.execute("CREATE TABLE bitcoinAvg (id INTEGER PRIMARY KEY AUTOINCREMENT, average REAL, time TEXT)")
    else :
       conn.execute("DROP TABLE bitcoinAvg")
       conn.execute("CREATE TABLE bitcoinAvg (id INTEGER PRIMARY KEY AUTOINCREMENT, average REAL, time TEXT)")
    main()