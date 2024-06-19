# Code for criminal data
import pandas as pd
import streamlit as st

import web_with_database


def criminal_data(user_id):
    st.header("Criminal Data")
    connection = web_with_database.connect_to_mysql()
    cursor = connection.cursor()
    sql = "SELECT r.criminal_Id, r.criminal_name, r.adress, r.Birth_date, r.Identification_mark, r.country, p.photo FROM criminal_register r Join photos p on r.criminal_id = p.criminal_id WHERE userid = %s"
    cursor.execute(sql, (user_id,))
    data = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    grouped = df.groupby(['criminal_Id', 'criminal_name', 'adress', 'Birth_date', 'Identification_mark', 'country'])
                    
    for (criminal_id, name, address, birth_date, mark, country), group in grouped:
                            left_column, right_column = st.columns([3, 1])  # Ratio of 3:1

                            # Display text data in the left column
                            left_column.write(f"Criminal Id: {criminal_id}")
                            left_column.write(f"Criminal Name: {name}")
                            left_column.write(f"Adress: {address}")
                            left_column.write(f"Birth Date: {birth_date}")
                            left_column.write(f"Identification Mark: {mark}")
                            left_column.write(f"Country: {country}")

                            # Display images in the right column
                            with right_column:
                                web_with_database.display_image(group['photo'].tolist())
                            st.write("-----------------------------------------------------")

