"""
Lab5 SQLite  Dan Smestad ITEC 2905-80 Software Dev. Capstone Clara James
A menu - you need to add the database and fill in the functions. 
"""

import sqlite3


db = 'chainsaw_juggling_records_db.sqlite'


def main():
    menu_text = """  
  
    Chainsaw Juggling Record Holders as of July 2018
    ************************************************
    1. Display all records
    2. Add new record
    3. Edit existing record
    4. Delete record 
    5. Search by Name
    6. Quit
    """
    create_table()  #calling to create a new table.
    insert_record_holders_data()  # intial data incerted. 

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            add_new_record()
        elif choice == '3':
            edit_existing_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            search_records_by_name()    
        elif choice == '6':
            drop_table_on_quit()  
            # Table is droped fot this program and new data and table created at start. 
            break
        else:
            print('Not a valid selection, please try again')
            #simple value check that seletion is a int and is valid selection

def create_table():
    with sqlite3.connect(db) as conn:  #creating the table for jugglers records.
        conn.execute('CREATE TABLE IF NOT EXISTS jugglers (name text, country text, catch_count int)')  
    #conn.commit  #need to have:IF NOT EXISTS for tables and DB's.
    conn.close()   

def drop_table_on_quit():
    with sqlite3.connect(db) as conn:  #deleting the table for jugglers records.
        conn.execute('DROP TABLE jugglers')  
    #conn.commit  #need to have:IF NOT EXISTS for tables and DB's.
    conn.close()   

def insert_record_holders_data():
    with sqlite3.connect(db) as conn:
    #keeping this for testing creating re-reun option(6) on quit deletes table.
        conn.execute('INSERT INTO jugglers VALUES ("Janne Mustonen", "Finland", "98")' )
        conn.execute('INSERT INTO jugglers VALUES ("Ian Stewart", "Canada", 94)')
        conn.execute('INSERT INTO jugglers VALUES ("Aaron Greg", "Canada", "88")' )
        conn.execute('INSERT INTO jugglers VALUES ("Chad Taylor", "USA", 78)')
            
    conn.close()  

         
def display_all_records():
    conn = sqlite3.connect(db)  # connects datbase link
    results = conn.execute('SELECT * FROM jugglers')  #calls for all records from db for table jugglers 
    print('All jugglers records: ')
    for row in results:
        print(row)
    conn.close()


def search_records_by_name():
    search_name = input('enter new jugglers name: ')
    search_cases = search_name.lower() 
    conn = sqlite3.connect(db)
    results = conn.execute('SELECT * FROM jugglers WHERE name like ?', (search_cases, ))
    first_row = results.fetchone()
    if first_row:
        print('\nYour jugglers record is:', first_row )
    else:
        print('\nnot found in database')     
    conn.close()


def add_new_record():
    new_name = input('enter new jugglers name: ')
    new_country = input('enter Country name: ')
    new_catch_count = int(input('enter number of catches: '))
    # no format strings {new_id} use paramerized value queries, sql statement.
    with sqlite3.connect(db) as conn:
        conn.execute('INSERT INTO jugglers VALUES (?, ?, ?)', (new_name, new_country, new_catch_count) )
    conn.close()

# edits an existing record. Message passed if user wants to edit record that does not exist?'
def edit_existing_record():
    #conn = sqlite3.connect(db)
    edit_name = input('enter jugglers name to edit: ')
    edit_catch_count = int(input('enter new number of catches: '))
    with sqlite3.connect(db) as conn:
        try:                  
            conn.execute('UPDATE jugglers SET name = ? WHERE catch_count = ?', (edit_name, edit_catch_count,))
        except:
            print('record does not exist')      
    conn.close()


#'todo delete existing record. What if user wants to delete record that does not exist?'
def delete_record():
    delete_name = input('enter jugglers name to delete: ')
    delete_cases = delete_name.lower()     
    with sqlite3.connect(db) as conn:
        try:                 
            for row in conn.execute('SELECT * FROM jugglers WHERE lower(name) like ?', (delete_cases, )):
                conn.execute('DELETE FROM jugglers WHERE name = ? ', (row[0],  ))
                print('Your juggler:', delete_cases, 'was deleted, please use menu to verify.')           
        except:                   
               print('not found in database')     
        #conn.execute('DELETE FROM jugglers WHERE name = ?', (delete_cases,  ))
        #currently only exact match deletes record, update with any case entery sqlite does care case.   
    conn.close()

def message(msg):
    """ Prints a message for the user
    :param msg: the message to print"""
    print(msg)

class RecordError(Exception):
    pass

   
if __name__ == '__main__':
    main()