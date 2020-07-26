# -*- encoding: utf-8 -*-

__version__ = "0.9"

__author__ = "fcFn"

from tkinter.constants import N,E,W,S
from tkinter import messagebox
from tkinter import ttk
import tkinter

class App:
    
    def __init__(self, name):
        
        self.MESSAGES = ['Duplicate item!', 'Enter item name', 'No name provided!']
        self.projectname = ''
        self.containers = []
        self.name = name
        self.createall()
        self.gridall()
        self.model = []
        self.addnewcontainer(name = 'A container')
        self.allselecteditems= []
        self.style = ttk.Style()
        self.style.layout("SelectedItem", [
            ('Checkbutton.padding', {'children':
                [('Checkbutton.focus', {'children': 
                [('Checkbutton.indicator', {'side': 'left', 'sticky': ''}), 
                ('Checkbutton.label', {'sticky': 'nswe'})], 'side': 'left', 'sticky': 'w'})], 'sticky': 'nswe'})])
        self.style.configure("SelectedItem", font = 'helvetica 10 bold', foreground='blue')
        self.root.mainloop()        
        
    def createmainframe(self):   
        self.root = tkinter.Tk()
        self.root.title(self.name)
        self.mainframe = ttk.Frame(self.root)
        self.contframe = ttk.Frame(self.mainframe)
        
    def gridframes(self):
        self.mainframe.grid(row=0, column=0, sticky=(N,E,W,S))
        self.contframe.grid(row=1, column=0, sticky=(N,E,W,S))
    
    def createmenus(self):
        self.topbar = ttk.Frame(self.mainframe)
        self.addcontainer = ttk.Button(self.topbar, text = 'Add new container', underline = 0, command = self.addnewcontainer)
        self.topbar.columnconfigure(0, weight=1)
        self.botbar = ttk.Frame(self.mainframe)
        self.botbar.columnconfigure(0,weight=1)
        self.botbar.columnconfigure(1,weight=1)
        self.botbar.columnconfigure(2,weight=1)
        self.savebutton = ttk.Button(self.botbar, text='Save', command = self.save)
        self.loadbutton = ttk.Button(self.botbar, text='Load', command = self.load)
        self.exportbutton = ttk.Button(self.botbar, text = 'Export', command = self.export)
        self.helpbutton = ttk.Button(self.botbar, text='Help', command = self.showhelp)
        self.bindkeys()
        
    def export(self):
        self.updatemodel()
        exportstring = ''
        for i in self.model:
            exportstring += str(i[0]+1) + '. ' + i[1] + '\n\n'
            if len(i) == 2:
                exportstring += '\tEMPTY\n'
                exportstring += '-' * 40 + '\n'
                continue
            for w in range(2, len(i)):
                exportstring += '\t' + str(i[w][0]+1) + '.' + i[w][1]
                if i[w][2]:
                    exportstring += ' --- CHECK\n' 
                else:
                    exportstring += '\n'
            exportstring += '-' * 40 + '\n'
        self.root.clipboard_clear()
        self.root.clipboard_append(exportstring)
        messagebox.showinfo('Oi!', 'Current list copied to clipboard!') 
            
        
    def bindkeys(self):
        self.root.bind('<Escape>', lambda e: self.quit())
        self.root.bind('<Control-space>', self.addnewcontainer)
        #this was used to bind to russian equiv of Control-A (hotkey was changed to Ctrl-Space
        #which is international
        #self.root.bind('<Control-ocircumflex>', self.addnewcontainer) 
        
    def quit(self):
        sure = messagebox.askyesno('Oi!', 'Are you sure you want to quit?')
        if sure: self.root.destroy()
        return        
        
    def showhelp(self):
        helptext = """
Lugman v0.9

This app manages lists of items.

To add a new container, press the "Add new container" button at the top of the main window. If you only have a default empty container, the newly created container will replace it.

To add a new item to a container, enter the item name into the input box under the container and press the plus button or hit the Enter key.

Click an item to mark it.

The counter beside the name of a container displays the amount of marked items against the total items in the container.

You can also hit Control-Space anywhere to add a new container.

To delete a container or change the container name, right-click the container.

To delete all containers, right-click any container and select "Delete all containers". You will be prompted to save your list beforehand.

To delete an item from a container or edit the item name, right-click the item.

You can move individual items between containers by dragging and dropping.

To move multiple items, use the middle mouse button to mark them and drag and drop them into the desired container (duplicated items will not be moved).

Right-click an item and choose "Drop selection" to drop multiple item selection without moving the items.

Press the "Save" button to save the current list.

Press the "Load" button to select and load a save file.

Press the "Export" button to export the list into the clipboard in human-readable format. Paste it to share it via IM, email, etc.

Press the "Help" button to read this message.
"""
        messagebox.showinfo('Help', helptext)
        
    def gridmenus(self):
        self.topbar.grid(row=0, column=0, padx = 10, sticky=(N))
        self.addcontainer.grid(row=0, column=0, sticky=(N,E,W))
        self.botbar.grid(row=2, column=0, sticky=(N,S,E,W))
        self.savebutton.grid(row=0, column=0, sticky=(S,W))
        self.loadbutton.grid(row=0, column=1, sticky=(S,W))
        self.exportbutton.grid(row=0, column=2, sticky=(S,W))
        self.helpbutton.grid(row=0, column=3, sticky=(S,E))
        
    def createall(self):
        self.createmainframe()
        self.createmenus() 
        
    def gridall(self):
        self.gridframes()
        self.gridmenus()
        
    def addnewcontainer(self, container = None, recreate = False, name = None):
        if not recreate:
            if not name: 
                query = Query('Enter container name', None, self)
                self.root.wait_window(query.question)
                try:
                    result = query.getresult().get()
                except:
                    return
                #check if there is just one empty default container
                if self.containers[0].name == 'A container' and (len(self.containers) == 1 and self.containers[0].isempty()):
                    #if so - replace the default container with newly created one
                    self.containers[0].container.destroy()
                    self.containers.clear()
                    self.containers.append(Container(result, self))
                    self.redraw()
                else:
                    #if not, just create new container besides the last one
                    self.containers.append(Container(result, self))
            if name:
                self.containers.append(Container(name, self))
        if recreate:
            entries = container[2:]
            newcont = Container(container[1], self)
            self.containers.append(newcont)
            #recreate entries
            if entries:
                newcont.additem(True, None, 0, entries)
            else:
                newcont.emptylabel.grid()      
                
        
    def getmainframe(self):
        return self.contframe
    
    def updatemodel(self):
        self.model.clear()
        conts = list(enumerate([i.name for i in self.containers]))
        states = [i.itemdata for i in self.containers]
        for i in enumerate(conts):
            self.model.append(i[1] + tuple(states[i[0]]))
        return self.model
    
    def save(self):
        model = self.updatemodel()
        if not model:
            messagebox.showinfo('Oi!', 'Nothing to save yet! Create some lists!')
            return
        from tkinter import filedialog
        file = filedialog.asksaveasfile(defaultextension = ".txt", filetype=(("Lug JSON files", "*.txt"),("All Files", "*.*")))
        if not file:
            return False
        import json
        json.dump(model, file)
        messagebox.showinfo('Save complete!', 'Successfully saved to {0}'.format(file.name))
        self.projectname = str(file.name).split(sep='/')[-1]
        self.root.title(self.name + '  -  ' + self.projectname)
        file.close()
        return True
        
    def load(self):
        from tkinter import filedialog
        file = filedialog.askopenfile(defaultextension = ".txt", filetype=(("Lug JSON files", "*.txt"),("All Files", "*.*")))
        if not file:
            return
        import json
        self.model = json.load(file)
        for i in self.containers:
                i.container.destroy()
        Container.relcol = 0
        Container.relrow = 0
        self.projectname = str(file.name).split(sep='/')[-1]
        self.root.title(self.name + '  -  ' + self.projectname)
        print(self.projectname)
        self.recreate()
        self.updatemodel()
        file.close()
    
    def recreate(self):
        self.containers.clear()
        for container in self.model:
            self.addnewcontainer(container, True)
    
    def deleteallcontainers(self):
        def deleteall():
            for i in self.containers:
                i.container.destroy()
            self.containers.clear()
            self.addnewcontainer(name = 'A container')
            self.redraw()
        if not (self.containers[0].name == 'A container' and len(self.containers) == 1 and self.containers[0].isempty()):
            maybesave = messagebox.askyesnocancel('Oi!', 'Do you want to save your list before deleting ALL containers?')
            if maybesave:
                if self.save():
                    deleteall()
                else:
                    return
            elif maybesave == False:
                deleteall()
            else:
                return 
            
    def redraw(self):
        Container.relcol = 0
        Container.relrow = 0
        for i in self.contframe.winfo_children():
            i.grid_forget()
        for i in self.contframe.winfo_children():
            i.grid(row = Container.relrow, column = Container.relcol, sticky=(N,S))
            Container.relcol += 1
            if Container.relcol == 4:
                Container.relcol = 0
                Container.relrow += 1

class Container:
    #Container positions (used for redrawing all containers after deleting one)
    relcol = 0
    relrow = 0
    def __init__(self, name, app):
        try:
            app.getmainframe()
        except:
            print("No application found!")
            raise
        self.app = app
        self.items = []
        self.itemdata = []
        self.itemorder = []
        self.itemcount = 0       
        #copy name of the entries labelframe
        self.name = name
        #total items contained in container entries frame and amount of selected items
        self.totalitems = 0 
        self.selecteditems = 0
        #name of the item to add
        self.item = tkinter.StringVar(value = 'Enter item name')
        #initialize widgets
        self.container = ttk.Frame(app.getmainframe())
        self.container.me = self
        self.entries = ttk.Labelframe(self.container, text = name + ' (empty)')
        self.emptylabel = ttk.Label(self.entries, text="Empty container") #default label used to pad entries box
        self.add = ttk.Button(self.container, text='+', command = self.additem)
        self.addentry = ttk.Entry(self.container, textvariable=self.item, width = 30)
        self.options = tkinter.Menu(self.container)
        self.options.add_command(label = 'Sort items by selection', command = self.sortitemsbyselection)
        self.options.add_command(label = 'Change container name', command = self.changecontainername)
        self.options.add_command(label = 'Delete container', command = self.deletecontainer)
        self.options.add_command(label = 'Delete ALL containers', command = self.deleteallcontainers)
        
        self.pack()
    
    def isempty(self):
        if len(self.itemdata) == 0:
            return True
        else:
            return False
        
    def additem(self, recreate = False, name = None, state = 0, *args):
        def dupe():
            nonlocal self
            self.item.set('Duplicate item!')
            self.addentry.focus()
            self.addentry.select_range(0, len(self.item.get()))
        if state:
            state = state
        else:
            state = 0
        if name:
            value = name
        else:
            value = self.item.get()
        if not recreate:
            if value in self.app.MESSAGES:
                self.addentry.focus()
                self.addentry.select_range(0, len(value))
                return
            elif not value:
                self.item.set('No name provided!')
                self.addentry.focus()
                self.addentry.select_range(0, len(value)) 
                return
            self.emptylabel.grid_remove()
            #check if trying to add duplicate item
            itemnames = [w for i in self.items for w in i]
            if value in itemnames:
                self.addentry.focus()
                self.addentry.select_range(0, len(self.item.get()))
                if name and self.app.allselecteditems:
                    self.item.set('Some duplicate items not moved')
                    raise DuplicateItem
                if name:
                    dupe()
                    raise DuplicateItem
                else:
                    dupe()
                    return
            newitem=Item(self, value, state = state)
            self.addentry.focus()
            self.addentry.select_range(0, len(value))
            self.items.append({newitem.name:newitem})
            self.itemorder.append((self.itemcount, newitem))  
            self.itemcount += 1
            self.updatecounters()
            self.addentry.focus()
        else:
            self.emptylabel.grid_remove()
            items = args
            for i in items[0]:
                newitem = Item(self, i[1], state = i[2])
                self.items.append({newitem.name:newitem})
                self.itemorder.append((self.itemcount, newitem)) 
                self.itemcount += 1
                self.updatecounters()
                
    def sortitemsbyselection(self):
        selecteditems = self.selecteditems
        unselecteditems = [w for i in self.items for w in i.values() if w.getstate() == 0]
        [w.item.grid_forget() for i in self.items for w in i.values()]
        [i.item.grid(sticky=(W)) for i in selecteditems]
        self.itemorder.clear()
        for i in enumerate(selecteditems):
            self.itemorder.append((i[0], i[1])) 
        [i.item.grid(sticky=(W)) for i in unselecteditems]
        for i in enumerate(unselecteditems):
            self.itemorder.append((i[0], i[1]))
        self.updatecounters()
        
    def deleteallcontainers(self):
        self.app.deleteallcontainers()
    
    def deletecontainer(self):
        if not self.isempty():
            sure = messagebox.askyesno("Oi!", "Are you sure you want to remove this container and all items there-in?")
            if not sure:
                return
        self.app.containers.remove(self)        
        self.container.destroy()
        if not self.app.containers:
            self.app.addnewcontainer(name = 'A container')
        #If a container was deleted we should redraw everything, so the grid is right
        self.app.redraw()
        
    def changecontainername(self):
        query = Query('Enter new container name', self.name, self.app)
        self.app.root.wait_window(query.question)
        try:
            result = query.getresult().get()
        except:
            return 
        self.name = result
        self.updatecounters()               
        
    def pack(self):
        """Place container and its children in the contframe."""
        self.container.grid(row = Container.relrow, column = Container.relcol, sticky=(N,S)) 
        Container.relcol += 1
        if Container.relcol == 4:
            Container.relrow += 1
            Container.relcol = 0
        self.entries.grid(row=0, column=1, columnspan=2, sticky=(N,S,E,W))
        #Make all container rows resize according to the container with most items
        self.container.rowconfigure(0, weight=1)
        self.add.grid(row=1, column=1)
        self.addentry.grid(row=1, column=2)
        self.addentry.bind('<FocusIn>', lambda e: self.addentry.selection_range(0, len(self.item.get())))
        self.entries.bind('<3>', lambda e: self.options.post(e.x_root, e.y_root))
        self.addentry.bind('<Return>', lambda e: self.additem())
        self.emptylabel.grid(sticky=(N))
        for i in self.container.winfo_children():
            if type(i) != tkinter.Menu:
                i.grid(padx="5", pady="5")
        self.addentry.focus()
        
        
    def updatecounters(self):
        self.totalitems = self.itemcount
        #refresh container model
        self.itemdata = [(i[0], i[1].name, i[1].getstate()) for i in self.itemorder]
        if not self.totalitems:
            self.emptylabel.grid()
            self.entries.config(text = self.name + ' (empty)')    
        else:
            self.selecteditems = [w for i in self.items for w in i.values() if w.getstate() == 1]
            self.entries.configure(text = self.name + ' ({0} of {1})'.format(str(len(self.selecteditems)), str(self.totalitems)))
        
    def deleteitem(self, item):
        self.itemcount -= 1
        for i in self.items:
            if item in i.values():
                try:
                    i.pop(item.name)
                except KeyError:
                    pass
        for i in enumerate(self.itemorder):
            if item in i[1]:
                self.itemorder.pop(i[0])
        if self.itemcount == 0:
            self.emptylabel.grid()
        self.updatecounters()

class Item:
    def __init__(self, container, name, state = 0):
        self.parent = container
        self.name = name
        self.item = None
        self.menu = 0
        self.state = state
        self.createitem()
        self.createmenu()
        self.griditem()        
        
    def createitem(self):
        self.item = ttk.Checkbutton(self.parent.entries, text = self.name, command = self.updatecounters)
        self.item.state = tkinter.IntVar(value = self.state)
        self.item.configure(variable = self.item.state)
        self.item.me = self
        
    def createmenu(self):
        #and bind keys
        self.menu = tkinter.Menu(self.item)
        self.menu.add_command(label = 'Edit item', command = self.edititem)
        self.menu.add_command(label = 'Delete item', command = self.deleteitem)
        self.menu.add_command(label = 'Drop selection', command = self.dropselection)
        #bind menu to right-click
        self.item.bind('<3>', lambda e: self.menu.post(e.x_root, e.y_root))
        self.item.bind('<2>', self.selected)
        self.item.bind('<1>', self.grab)
        self.item.bind('<ButtonRelease-1>', self.release)
        
    def edititem(self):
        query = Query('Enter new item name', self.name, self.parent.app)
        self.parent.app.root.wait_window(query.question)
        try:
            result = query.getresult().get()
        except:
            return
        self.name = result
        self.item.configure(text = self.name)
        self.parent.updatecounters()
        
    
    def dropselection(self):
        for i in self.parent.app.allselecteditems:
            i[0].item.configure(style = "TCheckbutton")
        self.parent.app.allselecteditems.clear()
    
    def selected(self, e):
        if self.item['style'] == "SelectedItem":
            self.item.configure(style="TCheckbutton")
            return
        self.item.configure(style="SelectedItem")
        self.parent.app.allselecteditems = [(w[1], w[1].getstate()) for i in self.parent.app.containers for w in i.itemorder if w[1].item['style'] == "SelectedItem"]
        
    def grab(self, event):
            def moving(event):
                nonlocal self
                self.parent.app.root.configure(cursor = "based_arrow_down")
            self.item.bind('<Motion>', moving)
        
        
    def release(self, event):
    
        self.item.unbind('<Motion>')
        self.parent.app.root.configure(cursor = "arrow")
        target = self.item.winfo_containing(event.x_root, event.y_root)
        #released into something outside a container?
        if len(str(target).split(".")) < 3:
            return
        #released into itself?
        try:
            if str(target).split(".")[3] in str(self.item).split(".")[3]:
                return
        except IndexError:
            return
        #released into another container?
        if str(target).split(".")[3] != str(self.item).split(".")[3]:
            if self.parent.app.allselecteditems:
                for i in self.parent.app.allselecteditems:
                    try:
                        self.item.nametowidget('.'.join(str(target).split(".")[:4])).me.additem(name = i[0].name, state = i[1])
                        i[0].item.configure(style='TCheckbutton')
                        i[0].deleteitem()
                    except DuplicateItem:
                        i[0].item.configure(style='TCheckbutton')
                        continue
                self.parent.app.allselecteditems.clear()
                return    
            #copy entry into container
            try:
                self.item.nametowidget('.'.join(str(target).split(".")[:4])).me.additem(name = self.name, state = self.getstate())
            except DuplicateItem:
                return
            #remove self from previous container
            self.deleteitem()
            return
        
        
    def deleteitem(self):
        self.item.destroy()
        self.updatecounters()
        self.parent.deleteitem(self)
        
    def griditem(self):
        self.item.grid(sticky=(W))
        
    def updatecounters(self):
        self.parent.updatecounters()
        
    def getstate(self):
        return self.item.state.get()
        
class Query:
    
    def __init__(self, text, name, app):
        self.name = name
        self.text = text
        self.parent = app
        self.input = None
        self.children = None
        self.createdialog()
        self.griddialog()
        
    def createdialog(self):
        self.input = tkinter.StringVar(value = self.name)
        self.question = tkinter.Toplevel(self.parent.root)
        questionframe = ttk.Frame(self.question)
        questionlab = ttk.Label(questionframe, text = self.text)
        questionentry = ttk.Entry(questionframe, textvariable = self.input)
        questionframe.grid()
        questionlab.grid(row = 0, column = 0, columnspan=2, padx = 20, pady = 10)
        questionentry.grid(row=1, column = 0, padx=20, columnspan=2, pady=10, sticky=(N,S))
        questionentry.select_range(0, len(self.input.get()))
        ok = ttk.Button(questionframe, text = 'OK', 
                        command = self.post)
        cancel = ttk.Button(questionframe, text = 'Cancel', command = self.question.destroy)       
        ok.grid(row=2, column=0, padx=20, pady=10, sticky=(N,S))
        cancel.grid(row=2, column = 1, padx=20, pady=10, sticky=(N,S))
        questionentry.bind('<Return>', lambda e: self.post())
        self.question.bind('<Escape>', lambda e: self.question.destroy())
        self.children = [self.question, questionframe, questionlab, cancel, ok, questionentry]
        
    def griddialog(self):
        for i in self.children:
            i.grid()
        self.children[-1].focus()
            
    def post(self):
        if not self.input.get():
            self.children[-1].focus()
            return
        self.result = self.input
        self.question.destroy()
    
    def getresult(self):
        return self.result

class DuplicateItem(Exception):
    pass

if __name__ == "__main__":
    App('Lugman v. 0.9')
