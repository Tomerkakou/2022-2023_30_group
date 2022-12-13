import mysql.connector

mydb = mysql.connector.connect(
  host="rendit-db.crfj8gkk0yln.eu-central-1.rds.amazonaws.com",
  user="tomer",
  password="t38tTNsQg2PBltlg"
)

print(mydb)