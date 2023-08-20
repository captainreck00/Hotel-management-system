import sqlite3




def verify(email,password):
    conn=sqlite3.connect("my_database.db")
    cursor=conn.cursor()
    query = "SELECT * FROM users WHERE email=? AND password=?"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result==None:
        return False
    else:
        return True
   
     

            
        


