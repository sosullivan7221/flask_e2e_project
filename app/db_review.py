import sqlite3
import pandas as pd

# Initialize the database
DATABASE = '/home/sean_osullivan/flask_e2e_project/app/users.db'

# search for user in database
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# get values from users table
df = pd.read_sql_query("SELECT * FROM users", db)
print(df)