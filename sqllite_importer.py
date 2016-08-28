from collections import Counter
import sqlite3
import re
import requests

conn = sqlite3.connect('../../sql1.sqlite')
cur = conn.cursor()

trunkate_table = cur.execute('''DELETE FROM Counts;''')

req = (requests.get('http://www.pythonlearn.com/code/mbox.txt').content).decode('utf8')

emails = Counter(re.findall(r'From: \S.+@(\S.+)', req))

for email, count in emails.items():
    cur.execute('''INSERT INTO Counts(org, count) VALUES ('{0}', {1})'''
                .format(email, int(count)))
conn.commit()

query = 'SELECT * FROM Counts ORDER BY count DESC LIMIT 10'

# Pretty printed top 10 results
rows = ['{:<20} {}'.format(row[0], row[1]) for row in cur.execute(query)]
print('Counts:\n{}'.format('\n'.join(rows)))
cur.close()
