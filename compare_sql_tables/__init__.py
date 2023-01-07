import os
import sys
import subprocess
import csv
import mysql.connector


def main():
    cnx = mysql.connector.connect(user='root',
                                  password='redhatbolsa',
                                  host='10.0.9.242',
                                  port=50603,
                                  database='testrd_omscommon')
    cursor = cnx.cursor()
    query = "Select * from oms_firm_defaults;"
    cursor.execute(query)
    field_names = [i[0] for i in cursor.description ]
    print(field_names)
    rows = cursor.fetchall()
    fp = open('file.csv', 'w')
    myFile = csv.writer(fp)
    myFile.writerow(field_names)
    myFile.writerows(rows)
    fp.close()

if __name__ == '__main__':
    main()
