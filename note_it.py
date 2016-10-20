"""
This is a simple Note Taking Interactive command application known as NoteApp.
Usage:
    note_app note_create <note_content>
    note_app note_view <note_id> 
    note_app note_delete <note_id>
    note_app note_list [<limit>]
    note_app note_search <query_string>
    note_app (-i | --interactive)
    note_app (-h | --help)
Options:
    -o, --output  Save to a txt file
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
import os
from docopt import docopt, DocoptExit
from note_it_functions import NoteApplication
from note_it_database import NoteAppdb
#from app.person import person
#from app.rooms import my_room
#from app.database import amity_db
from termcolor import cprint, colored
from pyfiglet import figlet_format


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

class MyInteractive (cmd.Cmd):

    cprint(figlet_format('ezNote', font='univers'), 'green', attrs=['bold'])

    prompt = '(NoteApp) '
    file = None

    @docopt_cmd
    def do_note_create(self, arg):
        """Usage: note_create <note> """ 
        NoteApplication().create_note(arg['<note>'])

    @docopt_cmd
    def do_note_view(self, arg):
        """Usage: note_view <note_id> """
        return NoteApplication().view_note(arg['<note_id>'])   
 
    @docopt_cmd
    def do_delete(self, arg):
        """Usage: delete [note_id] """
        return NoteApplication().delete_note(arg)

    @docopt_cmd
    def do_note_list(self, arg):
        """Usage: note_list [<limit>]"""
        number = arg['<limit>']
        if number is not None:
            return NoteApplication().note_list(number)
        else:
            return NoteApplication().note_list()

    @docopt_cmd
    def do_list_next(self, arg):
        """Usage: list_next <start_point> <step_size>"""
        return NoteApplication().l_next(start_point, step_size)

    @docopt_cmd
    def do_search(self, args):
        """Usage: search <query_string>"""
        return NoteApplication().note_search(args['<query_string>'])

    # @docopt_cmd
    # def do_search_next(self, arg):
    #     """Usage: search_next <query_string> <start> <step> """
    #     return NoteApplication().s_next(query_string, start, step)

    @docopt_cmd
    def do_import(self, arg):
        """Usage: import [filename] """
        NoteApplication().import_note(arg)
        print 'The file contents have been imported into the database.'

    @docopt_cmd
    def do_export(self, arg):
        """Usage: export [filename] """
        NoteApplication().export_note(arg)
        print 'The data has been exported to a JSON file.'

    @docopt_cmd
    def do_sync(self, args):
        """Usage: sync [] """
        NoteApplication().sync_note(args)
        print 'Firebase has been synced with your local database.'

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    os.system('cls')
    print(__doc__)
    MyInteractive().cmdloop()