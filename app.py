# not saved
''' code here manages copyright notice '''
# not saved
authors = "David B. Sher"
# not saved
thanks = "John Zelle"
# not saved
year = "2020"
import tkinter as tk
import sys, io, os
import subprocess as subp
import re
from datetime import datetime
from tkinter import filedialog
from os import getcwd,system
from keyword import iskeyword
from math import sqrt


from contextlib import redirect_stdout

# redirect stderr and stdout to strings
GUI_DEBUG=True  # can turn on and off debugging by changing this
def debug_print(to_print,end=''):
  ''' calls a print statement and puts it into the shell window '''
  global shell
  global GUI_DEBUG
  if GUI_DEBUG:
    shell.insert(tk.END,to_print+end,'debug')
    shell.tag_configure('debug',foreground='blue',font=('Consolas', 12, 'italic'))
    shell.mark_set(tk.INSERT, tk.END) # make sure the input cursor is at the end
    shell.cursor = shell.index(tk.INSERT) # save the input position

''' this sets up the window with
  * header (with project file)
  * graphics
  * python shell
  * copyright notice
'''
root = tk.Tk()
root.title('Gui4Sher Window')
root.configure(bg='darkblue')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# position for each frame
row_number = 0


# GUIframe holds clickable stuff
GUIframe = tk.Frame(root)
GUIframe.grid(row=row_number)
row_number+=1  # next row
GUIframe.columnconfigure(0,weight=1)
GUIframe.rowconfigure(0,weight=1)
# top frame will hold graphics window
top = tk.Frame(GUIframe)
top.pack(side=tk.LEFT)
top.columnconfigure(0, weight=1)
top.rowconfigure(0, weight=1)


# bottom frame will hold shell
bottom = tk.Frame(root)
bottom.grid(row=row_number)
row_number+=1  # next row
bottom.columnconfigure(0, weight=1)
bottom.rowconfigure(0, weight=1)

# copy_frame will hold copyright information
copy_frame = tk.Frame(root,height=16)
copy_frame.grid(row=row_number)
row_number+=1  # next row
copy_frame.columnconfigure(0, weight=1)
copy_frame.rowconfigure(0, weight=1)


''' define a canvas that captures mouse events '''
GRAPHICS_WIDTH = 600
GRAPHICS_HEIGHT = 300
class MouseCanvas(tk.Canvas):
  def __init__(self,parent=top,bg='snow',width=GRAPHICS_WIDTH,height=GRAPHICS_HEIGHT):
    tk.Canvas.__init__(self,parent,bg=bg,width=width,height=height)
    self.click_point = tk.StringVar()
    self.click_point.set('Point(0,0)')  # start with 0,0 clicked
    self.bind('<Button-1>', self.mouse_click)
    self.bind('<Motion>', self.mouse_move)
    self.tracking = False # when tracking draws gray horizontal and vertical lines for mouse

  def mouse_click(self,event):
    ''' puts the last clicked mouse position into the variable mouse_click_position '''
    self.click_point.set('Point('+str(event.x)+','+str(event.y)+')')
    self.mouse_point = Point(event.x,event.y)

  def get_mouse_click(self):
    ''' waits for a mouse click and returns the point '''
    debug_print('Waiting for click',end='\n')
    self.wait_variable(self.click_point)
    debug_print('Clicked',end='\n')
    return self.mouse_point

  def toggle_tracking(self):
    if self.tracking:
      # delete tracking lines
      self.delete(self.vertical)
      self.delete(self.horizontal)
      self.tracking = False
    else:
      # put down initial tracking lines and draw them
      self.vertical = self.create_line(0,0,0,GRAPHICS_HEIGHT,fill='lightgray')
      self.horizontal = self.create_line(0,0,GRAPHICS_WIDTH,0,fill='lightgray')
      self.tracking = True
      

  def mouse_move(self,event):
    if self.tracking:
      # delete old tracking lines
      self.delete(self.vertical)
      self.delete(self.horizontal)
      # draw new tracking lines
      self.vertical = self.create_line(event.x,0,event.x,GRAPHICS_HEIGHT,fill='lightgray')
      self.horizontal = self.create_line(0,event.y,GRAPHICS_WIDTH,event.y,fill='lightgray')
      
    
  

''' put graphics canvas in top frame '''
graphics = MouseCanvas()
graphics.pack(fill=tk.BOTH, expand = 1)


copyright_string = tk.StringVar()
copyright_string.set('Copyright {} {} with thanks to {}'.format(authors,year,thanks))
copyright_label = tk.Label(copy_frame,textvariable=copyright_string)
copyright_label.pack()

''' adds an author to the copyright statement '''
def add_author(auth):
  global authors
  authors += ' and ' + auth
  copyright_string.set('Copyright {} {} with thanks to {}'.format(authors,year,thanks))
  save_gui4sher()

''' sets the copyright year to the present year '''
def update_year():
  global year
  year = str(datetime.now().year)
  copyright_string.set('Copyright {} {} with thanks to {}'.format(authors,year,thanks))
  save_gui4sher()

''' adds an author to the copyright statement '''
def add_thanks(thank):
  global thanks
  thanks += ' and ' + thank
  copyright_string.set('Copyright {} {} with thanks to {}'.format(authors,year,thanks))
  save_gui4sher()

''' Copyright David B. Sher 2020 '''

''' code here manages objects in the graphics window '''
objects = [] # no objects initially
##########################################################################
# Module Exceptions

class GraphicsError(Exception):
    """Generic error class for graphics module exceptions."""
    pass

OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"


object_number = 0; # used to number objects

class GraphicsObject:

    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override _draw and
    #   and _move methods.
    
    def __init__(self, fill='',outline='black',width='1'):
        global object_number
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        self.name = 'object'+str(object_number)
        object_number+=1 # each object starts with a unique name
        self.set_fill(fill)
        self.set_outline(outline)
        self.set_width(width)
        

    def set_name(self, name):
        """Set name of object to name"""
        self.name = name
        if self.id:
            save_gui4sher() # update the save file
            root.update()

    def get_name(self):
      return self.name
        
    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.canvas.itemconfig(self.id,fill=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def get_fill(self):
      return self.fill
        
    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.canvas.itemconfig(self.id,outline=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def get_outline(self):
      return self.outline
        
    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.canvas.itemconfig(self.id,width=self.get_width())
          save_gui4sher() # update the save file
          root.update()

    def get_width(self):
      return self.width

    def draw(self):

        """Draw the object in graphics, which should be a Canvas
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        global objects
        self.canvas = graphics
        self.id = self._draw(graphics)
        # add colors, fonts etc to drawn object
        # if the objects lacks one of these ignore
        try: self.set_fill(self.get_fill())
        except (NameError, AttributeError): None
        try:  self.set_outline(self.get_outline())
        except (NameError, AttributeError): None
        try:  self.set_width(self.get_width())
        except (NameError, AttributeError): None
        try:  self.set_arrow(self.get_arrow())
        except (NameError, AttributeError): None
        try:  self.set_font(self.get_font())
        except (NameError, AttributeError): None
        try:  self.set_justify(self.get_justify())
        except (NameError, AttributeError): None
        objects.append(self)
        save_gui4sher() # update the save file
        root.update()
        return self

            
    def undraw(self):

        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""
        
        global objects
        if self.canvas: # if object has been drawn
          self.canvas.delete(self.id)
          self.canvas = None
          self.id = None
          objects.remove(self)
          save_gui4sher() # update the save file


    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        if self.canvas: # if object has been drawn
            x = dx
            y = dy
            self.canvas.move(self.id, x, y)
            root.update()
            save_gui4sher() # update the save file
           


    def _draw(self, canvas):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass # must override in subclass


    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass # must override in subclass

    def _to_exec(self):
      """ create statements that initialize and object and draw it """
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'({})', # parameters of object will be done with a .format
                     self.name + '.set_name(\'' + self.get_name() + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)
      

         
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self)
        self.set_fill = self.set_outline
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
    def _draw(self, canvas):
        return canvas.create_rectangle(self.x-2,self.y-1,self.x+2,self.y+2,fill=self.get_fill())
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
    def clone(self):
        other = Point(self.x,self.y)
        other.set_name(self.name)
        other.outline = self.outline
        return other
                
    def get_x(self): return self.x
    def get_y(self): return self.y
    def to_exec(): return super()._to_exec.format('' + self.x + ',' + self.y)

class _BBox(GraphicsObject):
    # Internal base class for objects represented by bounding box
    # (opposite corners) Line segment is a degenerate case.
    
    def __init__(self, p1, p2):
        GraphicsObject.__init__(self)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy
                
    def get_p1(self): return self.p1.clone()

    def get_p2(self): return self.p2.clone()
    
    def get_center(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

    
class Rectangle(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Rectangle({}, {})".format(str(self.p1), str(self.p2))
    
    def _draw(self, canvas):
        p1 = self.p1
        p2 = self.p2
        return canvas.create_rectangle(p1.x,p1.y,p2.x,p2.y,outline=self.get_outline(),fill=self.get_fill(),width=self.get_width())
        
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.set_name(self.name)
        other.set_fill(self.fill)
        other.set_outline(self.outline)
        other.set_width(self.width)
        return other
    
    def to_exec(self):
      ''' creates commands to create the rectangle '''
      return super()._to_exec().format('Point('+str(self.p1.x)+','+str(self.p1.y)+'),Point('+str(self.p2.x)+','+str(self.p2.y)+')')


class Oval(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Oval({}, {})".format(str(self.p1), str(self.p2))

        
    def clone(self):
        other = Oval(self.p1, self.p2)
        other.set_name(self.name)
        other.set_fill(self.fill)
        other.set_outline(self.outline)
        other.set_width(self.width)
        return other
   
    def _draw(self, canvas):
        p1 = self.p1
        p2 = self.p2
        return canvas.create_oval(p1.x,p1.y,p2.x,p2.y,outline=self.get_outline(),fill=self.get_fill(),width=self.get_width())

    def to_exec(self):
      ''' creates commands to create the oval '''
      return super()._to_exec().format('Point('+str(self.p1.x)+','+str(self.p1.y)+'),Point('+str(self.p2.x)+','+str(self.p2.y)+')')
    
class Circle(Oval):
    
    def __init__(self, center, radius):
        p1 = Point(center.x-radius, center.y-radius)
        p2 = Point(center.x+radius, center.y+radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    def __repr__(self):
        return "Circle({}, {})".format(str(self.get_center()), str(self.radius))
        
    def clone(self):
        other = Circle(self.get_center(), self.radius)
        other.set_name(self.get_name())
        other.set_fill(self.get_fill())
        other.set_outline(self.get_outline())
        other.set_width(self.get_width())
        return other
        
    def get_radius(self):
        return self.radius

    def to_exec(self):
      ''' creates commands to create the circle '''
      return super()._to_exec().format('Point('+str(self.get_center().x)+','+str(self.get_center().y)+'),'+str(self.radius))

                  
class Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)
        self.set_arrow('none')
   
    def __repr__(self):
        return "Line({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Line(self.p1, self.p2)
        other.set_name(self.get_name())
        other.set_outline(self.get_outline())
        other.set_width(self.get_width())
        other.set_dash(self.get_dash())
        return other

    def set_arrow(self,arrow):
      self.arrow = arrow
      if self.id:
          self.canvas.itemconfig(self.id,arrow=self.get_arrow())
          save_gui4sher() # update the save file
          root.update()

    def get_arrow(self):
      return self.arrow

  
    def _draw(self, canvas):
        p1 = self.p1
        p2 = self.p2
        return canvas.create_line(p1.x,p1.y,p2.x,p2.y,fill=self.get_outline(),width=self.get_width(),arrow=self.get_arrow())

    def set_outline(self, color):
        """Set line color to color"""
        self.outline = color
        if self.id:
          self.canvas.itemconfig(self.id,fill=self.get_outline())
          save_gui4sher() # update the save file
          root.update()
        
   
    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.p1.x)+','+str(self.p1.y)+'),Point('+str(self.p2.x)+','+str(self.p2.y)+'))',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_arrow('"+ self.get_arrow() + "')",
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)
class Dashed_Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)
        self.set_dash((5,5))
        self.set_arrow('none')
   
    def __repr__(self):
        return "Dashed_Line({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Line(self.p1, self.p2)
        other.set_name(self.get_name())
        other.set_outline(self.get_outline())
        other.set_width(self.get_width())
        other.set_dash(self.get_dash())
        return other
  
    def set_arrow(self,arrow):
      self.arrow = arrow
      if self.id:
          self.canvas.itemconfig(self.id,arrow=self.get_arrow())
          save_gui4sher() # update the save file
          root.update()

    def get_arrow(self):
      return self.arrow

    def _draw(self, canvas):
        p1 = self.p1
        p2 = self.p2
        return canvas.create_line(p1.x,p1.y,p2.x,p2.y,fill=self.get_outline(),dash=self.get_dash(),width=self.get_width(),arrow=self.get_arrow())

    def set_dash(self,dash):
      self.dash = dash
      if self.id:
        self.canvas.itemconfig(self.id,dash=self.get_dash())

    def get_dash(self):
      return self.dash

    def set_outline(self, color):
        """Set line color to color"""
        self.outline = color
        if self.id:
          self.canvas.itemconfig(self.id,fill=self.get_outline())
          save_gui4sher() # update the save file
          root.update()
        
   
    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.p1.x)+','+str(self.p1.y)+'),Point('+str(self.p2.x)+','+str(self.p2.y)+'))',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_arrow('"+ self.get_arrow() + "')",
                     self.name + ".set_dash("+ str(self.get_dash()) + ")",
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)


class Polygon(GraphicsObject):
    
    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0]) == type([]):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self)

    def __repr__(self):
        return "Polygon"+str(tuple(p for p in self.points))
        
    def clone(self):
        other = Polygon(*self.points)
        other.set_name(self.name)
        other.set_name(self.name)
        other.set_fill(self.fill)
        other.set_outline(self.outline)
        other.set_width(self.width)
        return other

    def get_points(self):
        return list(map(Point.clone, self.points))

    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx,dy)
   
    def _draw(self, canvas):
        args = []
        for p in self.points:
            args.append(p.x)
            args.append(p.y)
        return graphics.create_polygon(*args,outline=self.get_outline(),fill=self.get_fill(),width=self.get_width()) 

    def to_exec(self):
      ''' creates commands to create the polygon '''
      arguments =""  # make a list of the points
      for point in self.points:
        arguments += 'Point('+str(point.x)+','+str(point.y)+'),'
      return super()._to_exec().format(arguments[:-1])   # :-1 gets rid of last ,

class Label(GraphicsObject):
    
    def __init__(self, p, text):
        GraphicsObject.__init__(self)
        self.set_text(text)
        self.set_justify(tk.CENTER)
        self.set_font(('helvetica',12))
        self.set_width(10000)    # too large width works by default
        self.anchor = p.clone()

    def __repr__(self):
        return "Label({}, '{}')".format(self.anchor, self.getText())
    
    def _draw(self, canvas):
        p = self.anchor
        return canvas.create_text(p.x,p.y,anchor='nw',fill=self.get_outline(),text=self.get_text(),font=self.get_font(), justify=self.get_justify())
        
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def clone(self):
        other = Text(self.anchor, self.text)
        other.set_name(self.get_name())
        other.set_fill(self.get_fill())
        other.set_outline(self.get_outline())
        other.set_width(self.get_width())
        other.set_font(self.get_font())
        return other

    def set_text(self,text):
      self.text = text
      if self.id:
          self.canvas.itemconfig(self.id,text=self.get_text())
          save_gui4sher() # update the save file
          root.update()


    def get_text(self):
      return self.text

    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.canvas.itemconfig(self.id,justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.canvas.itemconfig(self.id,font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

            
    def get_anchor(self):
        return self.anchor.clone()

    def set_outline(self, color):
        """Set text color to color"""
        self.outline = color
        if self.id:
          self.canvas.itemconfig(self.id,fill=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),"'+self.get_text()+'")',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_text('"+ self.get_text()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)


class Entry(GraphicsObject):

    def __init__(self, p, width):
        global clicks_window
        GraphicsObject.__init__(self)
        self.anchor = p.clone()
        #print self.anchor
        self.width = width
        self.text = tk.StringVar()
        self.anchor = p.clone()
        self.set_fill("white")
        self.text.set("")
        self.set_outline("black")
        self.set_font(("courier", 12))
        self.set_justify('left')
        self.frm = tk.Frame(graphics.master)
        self.entry = tk.Entry(self.frm,
                              width=self.width,
                              textvariable=self.text,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font())
        self.entry.bind("<Return>",self.handle_return)

    def __repr__(self):
        return "Entry({}, {})".format(self.anchor, self.width)

    def _draw(self, canvas):
        p = self.anchor
        the_entry = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.entry.pack()
        self.entry.focus_set()
        return the_entry

    def handle_return(self,event):
      ''' if it exists call the return function from the clicks file '''
      # do a return command if the return function exists
      try: exec(self.get_name()+'_return()',globals())
      except (NameError, AttributeError): return None # otherwise no return behavior
      except Error as e: say(e,color='red',font=('Consolas', 12, 'bold')) # output error
      except Exception as exp: say(exp,color='red',font=('Consolas', 12, 'bold')) # output Exception


    def get_text(self):
        return self.text.get()

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.set_name(self.name)
        other.text = tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    def set_text(self, t):
        self.text.set(t)
        save_gui4sher() # update the save file
        root.update()

    def set_name(self, name):
        """Set name of enty to name"""
        old_name = self.name
        self.name = name
        # add a click command if one exists
        try: exec('self.command = '+self.get_name()+'_return')
        except (NameError, AttributeError): self.command = None # otherwise no command
        if self.command != None:
          self.button.config(command=self.command)
        if self.id:
            save_gui4sher() # update the save file
            root.update()
           

            
    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.entry.config(justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.entry.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.entry.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.entry.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.entry.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()

    def get_width(self):
      return self.width


    def to_exec(self):
      debug_print('Creating string to execute for Entry')
      ''' creates commands to create the line '''
      exec_lines = [ self.name + ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),'+str(self.width)+')',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_text('"+ self.text.get()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.set_justify(\''+self.get_justify() + '\')',
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)

class Text(GraphicsObject):

    def __init__(self, p, width, height):
        GraphicsObject.__init__(self)
        self.anchor = p.clone()
        #print self.anchor
        self.width = width
        self.height = height
        self.anchor = p.clone()
        self.set_fill("white")
        self.set_outline("black")
        self.set_font(("courier", 12))
        self.frm = tk.Frame(graphics.master)
        self.scroll = tk.Scrollbar(self.frm)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.box = tk.Text(self.frm,
                              width=self.width,
                              height=self.height,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font(),
                              yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.box.yview)

    def __repr__(self):
        return "Entry({}, {})".format(self.anchor, self.width)

    def _draw(self, canvas):
        p = self.anchor
        the_box = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.box.pack()
        self.box.focus_set()
        return the_box


    def get_text(self):
        return self.box.get("1.0", "end-1c")

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Text(self.anchor, self.width, self.height)
        other.set_name(self.name)
        other.set_text(self.get_text())
        other.fill = self.get_fill()
        other.outline = self.get_outline()
        other.font = self.get_font()
        other.justify = self.get_justify()
        return other

    def set_text(self, t):
        self.box.delete("1.0", "end-1c")
        self.box.insert("1.0",t)
        save_gui4sher() # update the save file
        root.update()

    def get_height(self):
      return self.height

    def set_height(self,height):
      self.height = height
      if self.id:
          self.box.config(height=self.get_height())
          save_gui4sher() # update the save file
          root.update()

            
    def set_font(self,font):
      self.font = font
      if self.id:
          self.box.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.box.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.box.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.box.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()

    def get_width(self):
      return self.width


    def to_exec(self):
      debug_print('Creating string to execute for Text')
      ''' creates commands to create the line '''
      exec_lines = [ self.name + ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),'+str(self.width)+','+str(self.height)+')',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_height('"+ str(self.get_height())+ "')",
                     self.name + ".set_text('"+ self.get_text()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)

class Button(GraphicsObject):

    def __init__(self, p, text):
        debug_print('Initializing button graphics object',end='\n')
        GraphicsObject.__init__(self)
        debug_print('Button Object initialized',end='\n')
        self.anchor = p.clone()
        #print self.anchor
        self.text = text
        self.anchor = p.clone()
        self.set_fill("cyan")
        self.set_outline("black")
        self.set_font(("sanserif", 14,'bold'))
        self.set_justify('center')
        self.frm = tk.Frame(graphics.master)
        self.set_width(len(text))
        debug_print('Button Object name: '+self.get_name(),end='\n')

        self.button = tk.Button(self.frm,
                              width = len(text),
                              text=text,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font(),
                              justify = self.get_justify(),
                              command = self.handle_click)

          

    def __repr__(self):
        return "Button({}, {})".format(self.anchor, self.text)

    def _draw(self, canvas):
        p = self.anchor
        the_button = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.button.pack()
        return the_button

    def handle_click(self):
      ''' if it exists call the return function from the clicks file '''
      # do a return command if the return function exists
      try: exec(self.get_name()+'_click()',globals())
      except (NameError, AttributeError): return None # otherwise no return behavior
      except: say(sys.exc_info(),color='red',font=('Consolas', 12, 'bold')) # output error

    def set_name(self, name):
        """Set name of button to name"""
        old_name = self.name
        self.name = name
        # add a click command if one exists
        try: exec('self.command = '+self.get_name()+'_click')
        except (NameError, AttributeError): self.command = None # otherwise no command
        if self.command != None:
          self.button.config(command=self.command)
        if self.id:
            save_gui4sher() # update the save file
            root.update()


    def set_text(self,text):
      self.text = text
      self.button.config(text=self.get_text())
      self.set_width(len(self.get_text()))
      if self.id:
          save_gui4sher() # update the save file
          root.update()

    def get_text(self):
        return self.text

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Button(self.anchor, self.get_text())
        other.config = self.config.copy()
        other.set_name(self.name)
        other.text = self.text
        return other

    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.button.config(justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.button.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.button.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.button.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.button.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()



    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),"'+str(self.get_text())+'")',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_text('"+ self.get_text()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.set_justify(\''+self.get_justify() + '\')',
                     self.name + '.draw()'
                     ]
      return '''
'''.join(exec_lines)

class Check(GraphicsObject):

    def __init__(self, p, text):
        GraphicsObject.__init__(self)
        self.anchor = p.clone()
        #print self.anchor
        self.text = text
        self.anchor = p.clone()
        self.set_fill('#EEEEEE')
        self.set_outline("black")
        self.set_font(("sanserif", 14,'bold'))
        self.set_justify('center')
        self.frm = tk.Frame(graphics.master)
        self.set_width(len(text))
        self.checked = tk.BooleanVar()
        self.set_checked(False)
        self.button = tk.Checkbutton(self.frm,
                              width = len(text),
                              text=text,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font(),
                              justify = self.get_justify(),
                              variable=self.checked,
                              onvalue=True,offvalue=False,
                              command = self.handle_click)
          

    def __repr__(self):
        return "Button({}, {})".format(self.anchor, self.text)

    def _draw(self, canvas):
        p = self.anchor
        the_button = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.button.pack()
        return the_button

    def handle_click(self):
      ''' if it exists call the return function from the clicks file '''
      # do a return command if the return function exists
      try: exec(self.get_name()+'_click()',globals())
      except (NameError, AttributeError): return None # otherwise no return behavior
      except Error as e: say(e,color='red',font=('Consolas', 12, 'bold')) # output error
      except Exception as exp: say(exp,color='red',font=('Consolas', 12, 'bold')) # output Exception

    def get_checked(self):
      ''' gets whether the button is checked '''
      return self.checked.get()

    def set_checked(self,value):
      ''' sets the check to either true or false '''
      self.checked.set(value)
      if self.id:
        save_gui4sher() # update the save file
        root.update()
      

    def set_name(self, name):
        """Set name of button to name"""
        old_name = self.name
        self.name = name
        # add a click command if one exists
        try: exec('self.command = '+self.get_name()+'_click')
        except (NameError, AttributeError): self.command = None # otherwise no command
        if self.command != None:
          self.button.config(command=self.command)
        if self.id:
            save_gui4sher() # update the save file
            root.update()


    def set_text(self,text):
      self.text = text
      self.button.config(text=self.get_text())
      self.set_width(len(self.get_text()))
      if self.id:
          save_gui4sher() # update the save file
          root.update()

    def get_text(self):
        return self.text

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Button(self.anchor, self.get_text())
        other.config = self.config.copy()
        other.set_name(self.name)
        other.text = self.text
        return other

    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.button.config(justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.button.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.button.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.button.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.button.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()



    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),"'+str(self.get_text())+'")',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_text('"+ self.get_text()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.set_justify(\''+self.get_justify() + '\')',
                     self.name + '.set_checked(\''+str(self.get_checked()) + '\')',
                     self.name + '.draw()'
                     ]
      return '''
'''.join(exec_lines)

group_names = [] # list of RadioGroup names

class RadioGroup():
  ''' Defines a group of radio buttons connected to each other so only 1 can be checked at a time. '''
  def __init__(self,name):
    self.variable = tk.IntVar() # string vars don't work for radio groups
    self.variable.set(0)
    self.new_value = 1;
    self.name = name
    objects.append(self)
    group_names.append(name)

  def get_variable(self):
    return self.variable

  def increment_new_value(self):
    ''' Incrementes the new value variable the next radio button in the group will match this '''
    self.new_value += 1
    return self.new_value - 1   # value to use for new radio button

  def get_value(self):
    return self.variable.get()


  def get_name(self):
    return self.name

  def to_exec(self):
    return self.name+ ' = ' + self.__class__.__name__ +'(\''+self.name+'\')\n' 

class Radio(GraphicsObject):

    def __init__(self, p, text, group, name):
        debug_print('Making radio button: '+name,end='\n')
        self.group = group
        GraphicsObject.__init__(self,fill='#AAFFAA')
        self.anchor = p.clone()
        self.text = text
        self.original_name = name  # needed to reinitialize or copy
        self.set_name(name)
        self.set_font(("sanserif", 14,'bold'))
        self.set_justify('center')
        self.frm = tk.Frame(graphics.master)
        self.set_width(len(text))

        self.button = tk.Radiobutton(self.frm,
                              width = len(text),
                              text=text,
                              indicatoron = 0,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font(),
                              justify = self.get_justify(),
                              variable= self.get_group().get_variable(),
                              value=self.get_group().increment_new_value(),
                              command = self.handle_click)
        self.button.deselect() # button should start out not selected
          

    def __repr__(self):
        return "Button({}, {})".format(self.anchor, self.text)

    def _draw(self, canvas):
        p = self.anchor
        the_button = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.button.pack()
        return the_button

    def handle_click(self):
      ''' If it exists call the return function from the clicks file. '''
      # do a return command if the return function exists
      debug_print('Click caused: '+self.get_group().get_name()+'_click('+self.get_name()+')',end='\n')
      try: exec(self.get_group().get_name()+'_click('+self.get_name()+')',globals())
      except (NameError, AttributeError): return None # otherwise no return behavior
      except Error as e: say(e,color='red',font=('Consolas', 12, 'bold')) # output error
      except Exception as exp: say(exp,color='red',font=('Consolas', 12, 'bold')) # output Exception

    def get_group(self):
      ''' Which RadioGroup does it belong to. '''
      return self.group

    def select(self):
      ''' Clicks the Radio. '''
      self.button.select()
      if self.id:
        save_gui4sher() # update the save file
        root.update()

    def deselect(self):
      ''' Unclicks the Radio. '''
      self.button.deselect()
      if self.id:
        save_gui4sher() # update the save file
        root.update()

    def set_name(self, name):
        """Set name of button to name"""
        old_name = self.name
        self.name = name
        # add a click command if one exists
        try: exec('self.command = '+self.get_name()+'_click')
        except (NameError, AttributeError): self.command = None # otherwise no command
        if self.command != None:
          self.button.config(command=self.command)
        if self.id:
            save_gui4sher() # update the save file
            root.update()


    def set_text(self,text):
      self.text = text
      self.button.config(text=self.get_text())
      self.set_width(len(self.get_text()))
      if self.id:
          save_gui4sher() # update the save file
          root.update()

    def get_text(self):
        return self.text

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Button(self.anchor, self.get_text())
        other.config = self.config.copy()
        other.set_name(self.name)
        other.text = self.text
        return other

    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.button.config(justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.button.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.button.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.button.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.button.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()



    def to_exec(self):
      ''' creates commands to create the line '''
      exec_lines = [ self.name+ ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),"'+str(self.get_text())+'",'+self.get_group().get_name()+',"'+self.original_name+'")',
                     self.name + '.name = \'' + self.name + '\'',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_text('"+ self.get_text()+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.set_justify(\''+self.get_justify() + '\')',
                     self.name + '.draw()'
                     ]
      return '''
'''.join(exec_lines)

class List(GraphicsObject):

    def __init__(self, p, items):
        GraphicsObject.__init__(self)
        self.anchor = p.clone()
        #print self.anchor
        self.anchor = p.clone()
        self.set_fill("yellow")
        self.set_outline("black")
        self.set_font(("arial", 12,'bold'))
        self.set_justify('left')
        self.frm = tk.Frame(graphics.master)
        # height is the number of items but it is at least 1 and <= 5
        self.set_height(len(items))
        if int(self.get_height()) == 0: self.set_height(1)
        elif int(self.get_height()) > 5 : self.set_height(5)
        self.set_width(1)
        self.scroll = tk.Scrollbar(self.frm)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list = tk.Listbox(self.frm,
                              bg = self.get_fill(),
                              fg = self.get_outline(),
                              font = self.get_font(),
                              justify = self.get_justify(),
                              height = self.get_height(),
                              selectmode = tk.SINGLE,   # one one item selected at a time
                              yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.list.yview)
        # add the items to a list
        self.set_items(items)
        self.list.bind("<<ListboxSelect>>",self.handle_select)
    def __repr__(self):
        to_return = "List({}, {})".format(self.anchor, self.width)
        return "List({}, {})".format(self.anchor, self.width)

    def _draw(self, canvas):
        p = self.anchor
        the_listbox = canvas.create_window(p.x,p.y,window=self.frm,anchor='nw')
        self.list.pack()
        return the_listbox

    def handle_select(self,event):
      ''' if it exists call the select function from the clicks file '''
      # do a return command if the return function exists
      try: exec(self.get_name()+'_select()',globals())
      except (NameError, AttributeError): return None # otherwise no return behavior
      except Error as e: say(e,color='red',font=('Consolas', 12, 'bold')) # output error
      except Exception as exp: say(exp,color='red',font=('Consolas', 12, 'bold')) # output Exception


    def get_items(self):
        ''' List of items in List. '''
        to_return = []
        # make a list of items in the list
        for item in self.list.get(0,self.list.size()):
          to_return.append(item)
        return to_return

    def set_items(self,items):
      ''' Change items in List. '''
      for item in items:
        self.add(item)

    def _move(self, dx, dy):
        self.anchor.move(dx,dy)

    def get_anchor(self):
        return self.anchor.clone()

    def clone(self):
        other = List(self.anchor, self.width)
        other.config = self.config.copy()
        other.set_name(self.name)
        other.set_items(self.get_items())
        other.set_outline(self.get_outline())
        other.set_fill(self.get_fill())
        other.set_font(self.get_font())
        other.set_justify(self.get_justify())
        other.set_height(self.get_height())
        return other

    def add(self, item):
      ''' Adds item into list. '''
      self.list.insert(tk.END,item)
      # if item is wider than list make list wider
      if len(item) > int(self.get_width()) : self.set_width(len(item))
      if self.id:
        save_gui4sher() # update the save file
        root.update()

    def delete(self, item):
      ''' Deletes item from list. '''
      try:
        self.list.delete(self.get_items().index(item))
      except ValueError as ve: say(str(ve),color='red',font=('Consolas', 12, 'bold'))
      if self.id:
        save_gui4sher() # update the save file
        root.update()

    def selected(self):
      ''' Returns the selected item or None if none selected. '''
      tup = self.list.curselection()  # a tuple either empty or with selected item
      if len(tup) == 0:
        return None
      else:
        return self.list.get(tup)

    def select(self,item):
      ''' Selects item in list. '''
      self.list.activate(self.data.index(item))
            
    def get_height(self): return self.height

    def set_height(self,height):
      self.height = height
      if self.id:
          self.list.config(height=self.get_height())
          save_gui4sher() # update the save file
          root.update()
            
    def set_justify(self,justify):
      self.justify = justify
      if self.id:
          self.list.config(justify=self.get_justify())
          save_gui4sher() # update the save file
          root.update()

    def get_justify(self):
      return self.justify

    def set_font(self,font):
      self.font = font
      if self.id:
          self.list.config(font=self.get_font())
          save_gui4sher() # update the save file
          root.update()

    def get_font(self):
      return self.font

    def set_fill(self, color):
        """Set interior color to color"""
        self.fill = color
        if self.id:
          self.list.config(bg=self.get_fill())
          save_gui4sher() # update the save file
          root.update()

    def set_outline(self, color):
        """Set outline color to color"""
        self.outline = color
        if self.id:
          self.list.config(fg=self.get_outline())
          save_gui4sher() # update the save file
          root.update()

    def set_width(self, width):
        """Set line weight to width"""
        self.width = width
        if self.id:
          self.list.config(width=self.get_width())
          save_gui4sher() # update the save file
          root.update()

    def get_width(self):
      return self.width

    def set_name(self, name):
        """Set name of select to name"""
        old_name = self.name
        self.name = name
        # add a click command if one exists
        try: exec('self.command = '+self.get_name()+'_select')
        except (NameError, AttributeError): self.command = None # otherwise no command
        if self.command != None:
          self.button.config(command=self.command)
        if self.id:
            save_gui4sher() # update the save file
            root.update()


    def to_exec(self):
      debug_print('Creating string to execute for Entry')
      ''' creates commands to create the line '''
      exec_lines = [ self.name + ' = ' + self.__class__.__name__ +'(Point('+str(self.anchor.x)+','+str(self.anchor.y)+'),'+str(self.get_items())+')',
                     self.name + '.set_name(\'' + self.name + '\')',
                     self.name + '.set_fill(\''+ self.get_fill() + '\')',
                     self.name + ".set_outline('"+ self.get_outline() + "')",
                     self.name + ".set_width('"+ str(self.get_width())+ "')",
                     self.name + ".set_height('"+ str(self.get_height())+ "')",
                     self.name + '.set_font(' + str(self.get_font()) + ')',
                     self.name + '.set_justify(\''+self.get_justify() + '\')',
                     self.name + '.draw()']
      return '''
'''.join(exec_lines)

def names():
  ''' returns a list of object names for all the objects drawn on screen '''
  to_return = []
  for thing in objects:
     to_return.append(thing.get_name())
  return(to_return)
  

''' controls the title '''


def change_title(titler):
  root.title(titler)



''' interactive functions to put down graphics and gui '''
def valid_name(name,thing,prefix=''):
  ''' Interactively dialogs with the user until a valid name is acquired and then returns it. '''
  if name == '':
    name = ask('Name of '+thing)
  while not (prefix+name).isidentifier() or iskeyword(prefix+name) or prefix+name in names():
    if not name.isidentifier():
      name = ask(name+' is not a valid python variable name, Enter a new name')
    elif iskeyword(name):
      name = ask(name+' is a python keyword, Enter a new name')
    elif name in names():
      name = ask('You already used '+name+', Enter a new name')
    else:
      name = ask('Something is wrong with '+name+', Enter a new name')
  return name

def mouse_ask(to_print,color='darkgreen',font=('serif',12),end=': '):
  ''' Prompts the user and returns a point that the user clicked on in the graphics window. '''
  graphics.toggle_tracking()
  say(to_print,color=color,font=font)
  to_return = graphics.get_mouse_click()
  graphics.toggle_tracking()
  return to_return

def place_rectangle(name='',fill='',outline='black',width=1):
  ''' Interactive placement of a rectangle. '''
  global objects
  name = valid_name(name,'Rectangle') # make sure the name of the object is valid
  # get the corners of the rectangle
  corner = mouse_ask('Click on a corner of rectangle "'+name+'"')
  dot = Circle(corner,3) # dot to put on screen
  dot.set_fill('darkgray')
  dot.draw()
  opposite = mouse_ask('Click on the opposite corner of rectangle "'+name+'"')
  dot.undraw() # don't need dot anymore
  # make the rectangle
  rect = Rectangle(corner,opposite)
  rect.set_name(name)
  rect.set_fill(fill)
  rect.set_outline(outline)
  rect.set_width(width)
  rect.draw()
  exec(name+'=objects[-1]',globals())

''' interactive functions to put down graphics and gui '''
def place_oval(name='',fill='',outline='black',width=1):
  ''' Interactive placement of a oval. '''
  name = valid_name(name,'Oval') # make sure the name of the object is valid
  # get the corners of the rectangle enclosing
  corner = mouse_ask('Click on a corner of rectangle that encloses the oval "'+name+'"')
  dot = Circle(corner,3) # dot to put on screen
  dot.set_fill('darkgray')
  dot.draw()
  opposite = mouse_ask('Click on the opposite corner of rectangle that encloses the oval "'+name+'"')
  dot.undraw() # don't need dot anymore
  # make the oval
  oval = Oval(corner,opposite)
  oval.set_name(name)
  oval.set_fill(fill)
  oval.set_outline(outline)
  oval.set_width(width)
  oval.draw()
  exec(name+'=objects[-1]',globals())
  
''' interactive functions to put down graphics and gui '''
def place_line(name='',fill='',outline='black',width=1):
  ''' Interactive placement of a line. '''
  name = valid_name(name,'Line') # make sure the name of the object is valid
  # get the corners of the rectangle enclosing
  corner = mouse_ask('Click on an endpoint of "'+name+'"')
  dot = Circle(corner,3) # dot to put on screen
  dot.set_fill('darkgray')
  dot.draw()
  opposite = mouse_ask('Click on the other endpoint of "'+name+'"')
  dot.undraw() # don't need dot anymore
  # make the Line
  line = Line(corner,opposite)
  line.set_name(name)
  line.set_fill(fill)
  line.set_outline(outline)
  line.set_width(width)
  line.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_dashed_line(name='',fill='',outline='black',width=1,dash=(5,5)):
  ''' Interactive placement of a line. '''
  name = valid_name(name,'Dashed_Line') # make sure the name of the object is valid
  # get the corners of the rectangle enclosing
  corner = mouse_ask('Click on an endpoint of "'+name+'"')
  dot = Circle(corner,3) # dot to put on screen
  dot.set_fill('darkgray')
  dot.draw()
  opposite = mouse_ask('Click on the other endpoint of "'+name+'"')
  dot.undraw() # don't need dot anymore
  # make the Line
  line = Dashed_Line(corner,opposite)
  line.set_name(name)
  line.set_fill(fill)
  line.set_outline(outline)
  line.set_width(width)
  line.set_dash(dash)
  line.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_circle(name='',fill='',outline='black',width=1):
  ''' Interactive placement of a circle. '''
  name = valid_name(name,'Circle') # make sure the name of the object is valid
  # get the center and radius
  center = mouse_ask('Click on the center of the circle "'+name+'"')
  dot = Circle(center,3) # dot to put on screen
  dot.set_fill('darkgray')
  dot.draw()
  circumference = mouse_ask('Click on the circumference of the circle "'+name+'"')
  dot.undraw() # don't need dot anymore
  # find the radius
  x_difference = center.get_x() - circumference.get_x()
  y_difference = center.get_y() - circumference.get_y()
  radius = sqrt(x_difference*x_difference + y_difference*y_difference)
  # make the circle
  circ = Circle(center,radius)
  circ.set_name(name)
  circ.set_fill(fill)
  circ.set_outline(outline)
  circ.set_width(width)
  circ.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_polygon(name='',fill='',outline='black',width=1):
  ''' Interactive placement of a circle. '''
  name = valid_name(name,'Polygon') # make sure the name of the object is valid
  # holds all the corners of the polygon
  corners = []
  circles = []
  while True:
    # get the first corner of the polygon
    first = mouse_ask('Click on the a corner of the polygon "'+name+'"',color='orange')
    first_circle = Circle(first,5)
    first_circle.set_fill('orange')
    first_circle.draw()
    corners.append(first)
    circles.append(first_circle)
    # get more corners of the polygon
    while True:
      another = mouse_ask('Click on another corner of the polygon "'+name+'"',color='#444444')
      # find if the new point is near the first one
      x_difference = first.get_x() - another.get_x()
      y_difference = first.get_y() - another.get_y()
      distance = sqrt(x_difference*x_difference + y_difference*y_difference)
      if distance < 5:
        break
      corners.append(another)
      another_circle = Circle(another,2)
      another_circle.set_fill('#444444')
      another_circle.draw()
      circles.append(another_circle)
    # clear the points
    for circle in circles:
      circle.undraw()
    if len(corners) < 3:
      say('You need at least 3 points for a polygon, try again',color='red')
    else: break # finished the points
  # make the polygon
  poly = Polygon(corners)
  poly.set_name(name)
  poly.set_fill(fill)
  poly.set_outline(outline)
  poly.set_width(width)
  poly.draw()
  exec(name+'=objects[-1]',globals())
    
    
''' interactive functions to put down graphics and gui '''
def place_label(text,name='',fill='',outline='black',font=('times',14)):
  ''' Interactive placement of a label. '''
  name = valid_name(name,'Label') # make sure the name of the object is valid
  # get position of upper left corner of label
  anchor = mouse_ask('Click on the position of the Label "'+name+'"')
  # make the label
  labl = Label(anchor,text)
  labl.set_name(name)
  labl.set_fill(fill)
  labl.set_outline(outline)
  labl.set_font(font)
  labl.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_entry(width,name='',fill='white',outline='black',font=('times',14)):
  ''' Interactive placement of a label. '''
  name = valid_name(name,'Entry') # make sure the name of the object is valid
  # get position of upper left corner of Entry
  anchor = mouse_ask('Click on the position of the Entry "'+name+'"')
  # make the Entry
  entr = Entry(anchor,width)
  entr.set_name(name)
  entr.set_fill(fill)
  entr.set_outline(outline)
  entr.set_font(font)
  entr.draw()
  exec(name+'=objects[-1]',globals())

''' interactive functions to put down graphics and gui '''
def place_text(width,height,name='',fill='white',outline='black',font=('times',10)):
  ''' Interactive placement of a label. '''
  name = valid_name(name,'Text') # make sure the name of the object is valid
  # get position of upper left corner of Entry
  anchor = mouse_ask('Click on the position of the Text "'+name+'"')
  # make the Entry
  box = Text(anchor,width,height)
  box.set_name(name)
  box.set_fill(fill)
  box.set_outline(outline)
  box.set_font(font)
  debug_print('Executing text box insert:\n'+box.to_exec())
  box.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_button(text,name='',fill='cyan',outline='black',font=('times',14)):
  ''' Interactive placement of a Button. '''
  name = valid_name(name,'Button') # make sure the name of the object is valid
  # get position of upper left corner of Button
  anchor = mouse_ask('Click on the position of the Button "'+name+'"')
  # make the button
  debug_print('Creating Buttton',end='\n')
  butn = Button(anchor,text)
  debug_print('Button created',end='\n')
  butn.set_name(name)
  debug_print('Button named',end='\n')
  butn.set_fill(fill)
  butn.set_outline(outline)
  butn.set_font(font)
  # initialize and draw the object with the name specified
  butn.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_check(text,name='',fill='#EEEEEE',outline='black',font=('times',14)):
  ''' Interactive placement of a Check (checkbox). '''
  name = valid_name(name,'Check') # make sure the name of the object is valid
  # get position of upper left corner of Button
  anchor = mouse_ask('Click on the position of the Check "'+name+'"')
  # make the button
  butn = Check(anchor,text)
  butn.set_name(name)
  butn.set_fill(fill)
  butn.set_outline(outline)
  butn.set_font(font)
  butn.draw()
  exec(name+'=objects[-1]',globals())
    
''' interactive functions to put down graphics and gui '''
def place_list(items,name='',fill='yellow',outline='black',font=('times',14)):
  ''' Interactive placement of a Button. '''
  name = valid_name(name,'List') # make sure the name of the object is valid
  # get position of upper left corner of List
  anchor = mouse_ask('Click on the position of the List "'+name+'"')
  # make the List
  lst = List(anchor,items)
  lst.set_name(name)
  lst.set_fill(fill)
  lst.set_outline(outline)
  lst.set_font(font)
  lst.draw()
  exec(name+'=objects[-1]',globals())
    
def place_radio(text,group='',name='',fill='light green',outline='dark blue',font=('Courier',14)):
  global objects
  ''' Interactive placement of a Radio. '''
  if not group in group_names: # if you don't use an existing group
    group = valid_name(group,'RadioGroup') # make sure the name of the RadioGroup is valid
    group_name = group
    the_group = RadioGroup(group) # create the new RadioGroup
    exec(the_group.to_exec(),globals())
  else:
    # find the group specified by the user
    for thing in objects:
      if thing.get_name() == group:
        the_group = thing
  name = valid_name(name,'Radio',prefix=group) # make sure the name of the object is valid
  # get position of upper left corner of Radio
  anchor = mouse_ask('Click on the position of the Radio "'+name+'"')
  # make the List
  rad = Radio(anchor,text,the_group,name)
  rad.set_fill(fill)
  rad.set_outline(outline)
  rad.set_font(font)
  rad.draw()
  exec(name+'=objects[-1]',globals())
      

# end shell not in app

  



def save_gui4sher(): return None

change_title("app")
''' All the objects in the graphics are below '''
ccc = Circle(Point(284.0,123.0),64.03124237432849)
ccc.set_name('ccc')
ccc.set_fill('brown')
ccc.set_outline('black')
ccc.set_width('1')
ccc.draw()
color = Entry(Point(212.0,201.0),18)
color.set_name('color')
color.set_fill('white')
color.set_outline('black')
color.set_width('18')
color.set_text('')
color.set_font(('times', 14))
color.set_justify('left')
color.draw()

def color_return():
	ccc.set_fill(color.get_text())
	color.set_text('')




root.mainloop()