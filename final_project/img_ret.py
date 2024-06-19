import pandas as pd
import web_with_database 

def img_ret(user_id):
    connection = web_with_database.connect_to_mysql()
    cursor = connection.cursor()
    sql = "SELECT photo FROM photos "
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
   # Assuming `p.photo` returns binary data
    df = pd.DataFrame(data, columns=columns)
    
    # If `p.photo` contains multiple photos, ensure they are in a list
    # df['photo'] = df['photo'].apply(lambda x: [x] if not isinstance(x, list) else x)
    
    return df