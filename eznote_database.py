import sqlite3
import json
import collections
from termcolor import colored
from firebase import firebase
firebase = firebase.FirebaseApplication('https://note-95345.firebaseio.com/', None)

class NoteAppdb():
    def __init__(self):  # Initializes the class
        self.conn = sqlite3.connect('NoteApplication.db')
        self.c = self.conn.cursor()

    def create_table(self):
        self.c.execute("CREATE TABLE if not exists note_it_data \
				(id_column INTEGER PRIMARY KEY AUTOINCREMENT, \
				title_column CHAR(20), \
				body_column TEXT)" \
                       )
        self.conn.commit() 

    def save_note(self, title, note_content):
        with self.conn:
            self.c.execute("INSERT INTO note_it_data(title_column, body_column) \
				VALUES ('%s','%s')" % (title, note_content))
            

    def view(self, note_id):
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data WHERE \
				id_column == ('%i')" % (note_id))
            for item in self.c.fetchall():
                return colored('{0} : {1} --> {2}'.format(item[0], item[1], item[2]), green)

    def search(self, query_string):
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data WHERE body_column LIKE \
	            '%{}%'".format(query_string))
            for item in self.c.fetchall():
                print colored('{0} : {1} --> {2}'.format(item[0], item[1], item[2], \
                                                         ensure_ascii=False), 'green')

    def search_next(self, query_string, start, step):
        """"Invokes the next set of data in the running query """
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data WHERE body_column LIKE '%{}%' \
				LIMIT '{}', '{}'".format(query_string, int(start), int(step)))
            for item in self.c.fetchall():
                return item

    def list_(self, limit):
        """Retrieves a list of all the notes taken, where the limit specifies the
			maximum number of notes that can be listed
		"""
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data LIMIT'{}'".format(int(limit)))
            for item in self.c.fetchall():
                print colored('{0} : {1} --> {2}'.format(item[0], item[1], item[2], \
                                                         ensure_ascii=False), 'green')

    def list_next(self, start_point, step_size):
        """Invokes the next set of data in the running query"""
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data LIMIT '{}' \
	 			'{}'".format(start_point, step_size))
            # step_size specifes by how the next item to be shown increases

    def delete(self, note_id):
        """Deletes a note with a particular note_id from database """
        with self.conn:
            self.c.execute("DELETE FROM note_it_data WHERE \
				id_column == '%i'" % (note_id))

    def exp(self, filename):
        rows = None
        with self.conn:
            self.c.execute("SELECT * from note_it_data")
            rows = self.c.fetchall()
            json1 = json.dumps(rows, ensure_ascii=False)
            json_file = str(filename)
            b = open(json_file, 'wb')
            b.write(json1)
            b.close()
            self.c.close()

    def imp(self, filename):
        json_file = str(filename)
        _load = json.load(open(json_file, 'r+'))
        for item in _load:
            with self.conn:
                self.c.execute("INSERT INTO note_it_data (title_column, \
                    body_column) VALUES (?,?)", (item[1], item[2]))

    def sync(self):
        with self.conn:
            self.c.execute("SELECT * FROM note_it_data")
            for items in self.c.fetchall():
                firebase.post('note_it_data', items)
                print colored("sdf", 'red')
