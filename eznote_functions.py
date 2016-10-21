from eznote_database import NoteAppdb
from termcolor import colored

ndata = NoteAppdb()
#Instantiating ndata as an object of database class NoteAppdb

class NoteApplication(object):
    def __init__(self):
        ndata.create_table()

    def create_note(self, args):
        title = raw_input('Title:')
        note_content = raw_input(':-')
        ndata.save_note(title, note_content)
        print 'Note saved Successfully.'

    def view_one_note(self, note_id):
        note_id = int(raw_input('Enter note ID:'))  # Will display specific note by ID
        print ndata.view(note_id)

    def note_list(self, limit=20):
        # limit = raw_input('Number of Posts to Display?')  # will list a specific number of notes
        return ndata.list_(limit)

    def l_next(self, start_point, step_size):
        """Moves from one set of list results data, to the next """
        return ndata.list_next(start_point, step_size)

    def note_search(self, query_string):
        """Searches and lists notes that containing a particular query_string """
        # query_string = raw_input('Enter a word to search: ')
        # limit = raw_input('Show how many at once?')
        return ndata.search(query_string)

    # def s_next(self, query_string, start, step):
    #     """Moves from one set of search results data, to the next """
    #     return s.search_next(query_string, start, step)

    def delete_note(self, note_id):
        """Deletes note with a particular note_id """
        note_id = int(raw_input('Enter note ID:'))
        s.delete(note_id)
        print 'The note has been Successfully deleted'

    def import_note(self, filename):
        filename = raw_input('File to import from:') # imports json files
        return ndata.imp(filename)

    def export_note(self, filename):
        filename = raw_input('Name of file to be Exported to:')   # exporting note as JSON file
        return ndata.exp(filename)

    def sync_data(self, args):
        if len(args) == 0: # will sync data with firebase
            s.sync()
        else:
            pass







