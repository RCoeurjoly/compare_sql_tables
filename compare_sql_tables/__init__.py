import os
import sys
import subprocess
import csv
import mysql.connector
import click
import uuid
import pdb


def get_csv_from_query(host, port, user, password, database, table):
    cnx = mysql.connector.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
    cursor = cnx.cursor()
    query = "Select * from " + table + ";"
    cursor.execute(query)
    field_names = [i[0] for i in cursor.description ]
    rows = cursor.fetchall()
    my_file_name = '/tmp/' + str(uuid.uuid4()) + '.csv'
    fp = open(my_file_name, 'w')
    myFile = csv.writer(fp)
    myFile.writerow(field_names)
    myFile.writerows(rows)
    fp.close()
    cursor.close()
    cnx.close()
    return my_file_name

@click.command()
@click.option("--host", default="db", required=True, help="Database 1 IP.")
@click.option("--port", default=3306, required=True, help="Database 1 port.")
@click.option("--user", required=True, help="Database 1 user.")
@click.option("--password", required=True, help="Database 1 password.")
@click.option("--database", required=True, help="Database 1 name.")
@click.option("--table", required=True, help="Table to be compared.")
@click.option("--host2", default=None, help="Database 2 IP.")
@click.option("--port2", default=None, help="Database 2 port.")
@click.option("--user2", default=None, help="Database 2 user.")
@click.option("--password2", default=None, help="Database 2 password.")
@click.option("--database2", required=True, default=None, help="Database 2 name.")
@click.option("--ignore_column", multiple=True, default=[], help="Column to ignore. Can be specified multiple times")
def main(host,  port,  user,  password,  database,
         host2, port2, user2, password2, database2,
         table,
         ignore_column):
    if host2 is None:
        host2 = host
    if port2 is None:
        port2 = port
    if user2 is None:
        user2 = user
    if password2 is None:
        password2 = password
    if database2 is None:
        database2 = database
    # We improve the name of the variable
    ignore_columns = ignore_column
    csv1 = get_csv_from_query(host, port, user, password, database, table)
    csv2 = get_csv_from_query(host2, port2, user2, password2, database2, table)

    rc = subprocess.call(['graphtage -k '
                            + csv1 + ' '
                            + csv2], shell=True)
    #breakpoint()
    os.remove(csv1)
    os.remove(csv2)
    return rc


if __name__ == '__main__':
    main(standalone_mode=False)
