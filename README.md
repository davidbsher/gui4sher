# gui4sher
This is the repository for the education software that is gui4sher.
Gui4sher is a python app creation environment written in python.
To start a gui4sher project just download gui4sher.py and execute it with python
It will ask for a project name initially. 
Make sure you suggest a project name that works as a python variable.
Any time you add or change a graphics or gui object on the graphics screen gui4sher automatically saves the changes.
If you want to continue working on your project after you closed it just execute the project-name.py file and it will take up where you left off.

All app editing actions are doe by writing lines of code to execute in the python shell window.

You can manipulate the copyright notice at the bottom of the screen with:
- add_author(author) - adds a new author to the copyright notice
- update_year() - changes the copyright notice to the current year
- add_thanks(thankee) - allows you to thank a person who wasn't actually an author but did help with the code

You can manipulate the title on the top of the screen with the change_title function

You can interactively add graphics to the app with these functions:

- place_rectangle()
- place_oval()
- place_circle()
- place_line()
- place_dashed_line()
- place polygon()

All of the parameters of the graphics place functions are optional.
The options are:
- name (name of the graphics object, if none supplied will be acquired interactively)
- width (width of outline, default 1)
- fill (color of interior, default '' (no color))
- outline (color of outline, default 'black')
The position of the shape is interactively acquired by the app designer clicking on the graphics window.

You can interactively add GUI components to the app with these functions:

- place_label(text)
- place_button(text)
- place_entry(length) - (for text entry)
- place_list(list)

Each of the GUI place function has one required parameter.
The options are:
- name (name of the graphics object, if none supplied will be acquired interactively)
- fill (background color, default '' (no color))
- outline (color of text, default 'black')
- font (a tuple like ('arial', 14) or ('wingdings',30,'bold'))
- justify ('left', 'center' or 'right')
The position of the GUI widget is interactively acquired by the app designer clicking on the graphics window.

Each place method creates an object with the name supplied.  For example place_button('Click Me',name='clicker') creates a Button named clicker.

Every graphics and gui object has a move method that moves it on the graphics screen, set and get methods for each of the options.
Lines also of have set and get methods for arrow ('first', 'last' and 'both')

When a GUI widget (except Label) is added, gui4sher automatically creates a file called name_clicks.py where name is the name of the project.
After creating a GUI widget you can write in the shell: edit_clicks()
edit_clicks() will close the gui4sher window and call idle to edit name_clicks.py
You can add actions for the GUI widgets.
If a Button has a name the_button, when you click on it the Button will execute the function: the_button_click
If a Entry has a name the_entry, when you hit return the Entry will execute the function: the_entry_return
If a List has a name the_list, when you select an item in the List it will execute the function: the_list_select

edit_clicks() gives the app designer an opportunity to write these functions and give the widgets real power.
running the clicks file from idle will start back up the gui4sher environment with the graphics window and shell and all the graphics and GUI objects.
You can test the code with by selecting list items, clicking on buttons or writing on entries and hitting enter.  

Once you get an app the way you want it you can call the function: make_app()
make_app() will get a file name and generate a python file with that name that does the app.  
This app file will be stand alone and only requires a fairly vanilla version of python to run (it must have tkinter).

Your widgets can communicate with the shell with two functions:
- say(text)       - writes text to the shell
- ask(question)   - asks a question on the shell and returns the user's answer 
Both of these functions accept these options:
- color - color of the letters
- font - font of the letters
- end  - appended to the end of the text or question
You can call them from the shell to see what the defaults are.
Calling either of these from a widget will prevent an app file created by make_app from working but they are good for debugging.
If you want to use make_app() have your widgets change the text of Labels and Entries rather than communicate with the shell.

Improvements expected (no schedule supplied):
- More widgets
  + Check
  + Text
  + Radios
- Better documentation including videos
- Versions that work on:
  + Chromebook
  + Android
  + ipad
- Webpage Version that works on most browsers



