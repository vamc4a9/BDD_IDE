import os

from EditScenario import EditScenario
from NewScenario import NewScenario
from StepDefinition import AddStepDefinition
from xml import cXml
import tkinter as tk
from hashlib import md5
from itertools import islice
from tkinter import *
from tkinter import ttk, filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from configparser import ConfigParser
import re


class Document:
    def __init__(self, Frame, TextWidget):
        self.textbox = TextWidget
        self.status = md5(self.textbox.get(1.0, 'end').encode('utf-8'))


class MyGUI(tk.Frame):
    def __init__(self, master):

        self.root = master
        # self.img = None
        self.scenarioWindow = None
        self.statusvar = StringVar()
        self.statusvar.set("Welcome To BDD Editor")
        self.tabIndex = 0
        self.sTabsList = {}
        self.sOriginalText = {}
        self.selectedPath = {}
        self.sOpenedTabs = []
        self.tabs = {}
        self.sXMLImages = {}
        self.datatableFrame = None
        self.dataTableRows = []

        self.OpenBtn = None
        self.SaveBtn = None
        self.SaveAllBtn = None
        self.RefreshBtn = None

        self.StepOpenBtn = None
        self.View_Edit_Btn = None
        self.FindBtn = None
        self.StepDefRefreshBtn = None

        self.filename = ""
        self.EditorTabs = None

        iDelete_icon = './icons/custom_delete.png'
        iDelete_icon_pic1 = Image.open(iDelete_icon)  # Open the image like this first
        self.iDelete_icon_pic2 = ImageTk.PhotoImage(iDelete_icon_pic1)

        iDataTable = './icons/custom_datagrid.png'
        iDataTable1 = Image.open(iDataTable)  # Open the image like this first
        self.iDataTable2 = ImageTk.PhotoImage(iDataTable1)

        iOpen_folder = './icons/open_folder.png'
        open_folder_pic1 = Image.open(iOpen_folder)  # Open the image like this first
        self.open_folder_pic2 = ImageTk.PhotoImage(open_folder_pic1)

        iFolder = './icons/folder_icon.png'
        folder_pic1 = Image.open(iFolder)  # Open the image like this first
        self.folder_pic2 = ImageTk.PhotoImage(folder_pic1)

        iSourceCode = './icons/source_code.png'
        iSourceCode1 = Image.open(iSourceCode)  # Open the image like this first
        self.iSourceCode2 = ImageTk.PhotoImage(iSourceCode1)

        iCancel = './icons/cancel_icon.png'
        cancel_pic1 = Image.open(iCancel)  # Open the image like this first
        self.cancel_pic2 = ImageTk.PhotoImage(cancel_pic1)

        iSaveTab = './icons/save_tab.png'
        savetab_pic1 = Image.open(iSaveTab)  # Open the image like this first
        self.savetab_pic2 = ImageTk.PhotoImage(savetab_pic1)

        iFindIcon = './icons/find_icon.png'
        find_pic1 = Image.open(iFindIcon)  # Open the image like this first
        self.find_pic2 = ImageTk.PhotoImage(find_pic1)

        iStepDefIcon = './icons/step_def_icon.png'
        step_pic1 = Image.open(iStepDefIcon)  # Open the image like this first
        self.step_pic2 = ImageTk.PhotoImage(step_pic1)

        iUndoIcon = './icons/undo_icon.png'
        undo_pic1 = Image.open(iUndoIcon)  # Open the image like this first
        self.undo_pic2 = ImageTk.PhotoImage(undo_pic1)

        iredoIcon = './icons/redo_icon.png'
        redo_pic1 = Image.open(iredoIcon)  # Open the image like this first
        self.redo_pic2 = ImageTk.PhotoImage(redo_pic1)

        iScenario = './icons/scenario_icon.png'
        scenario_pic1 = Image.open(iScenario)  # Open the image like this first
        self.scenario_pic2 = ImageTk.PhotoImage(scenario_pic1)

        ixmltab = './icons/xml_for_tab.png'
        ixmltab_pic1 = Image.open(ixmltab)  # Open the image like this first
        self.xmltab_pic2 = ImageTk.PhotoImage(ixmltab_pic1)

        iFeature = './icons/feature_icon.png'
        feature_pic1 = Image.open(iFeature)  # Open the image like this first
        self.feature_pic2 = ImageTk.PhotoImage(feature_pic1)

        iXml = './icons/xml_icon.png'
        xml_pic1 = Image.open(iXml)  # Open the image like this first
        self.xml_pic2 = ImageTk.PhotoImage(xml_pic1)

        iCucumber = './icons/cucumber_icon.png'
        cucumber_pic1 = Image.open(iCucumber)  # Open the image like this first
        self.cucumber_pic2 = ImageTk.PhotoImage(cucumber_pic1)

        iJava = './icons/java_icon.png'
        java_pic1 = Image.open(iJava)  # Open the image like this first
        self.java_pic2 = ImageTk.PhotoImage(java_pic1)

        iFile = './icons/file_icon.png'
        file_pic1 = Image.open(iFile)  # Open the image like this first
        self.file_pic2 = ImageTk.PhotoImage(file_pic1)

        self.master = master
        self.ProjectExplorerTree = None
        self.StepDefExplorerTree = None

    def CreateGUI(self):

        # master = Tk()
        master = self.master
        self.addMenu(self.master)
        master.title("BDD Editor")
        master.geometry("600x500")
        master.resizable(True, True)
        master.minsize(600, 500)
        photo = PhotoImage(file="./icons/tool_icon.png")
        master.iconphoto(False, photo)

        MainWindow = PanedWindow(master, orient=HORIZONTAL, bg='#ccccb3', borderwidth=3)
        MainWindow.pack(fill=BOTH, expand=1)

        ExplorerPane = PanedWindow(MainWindow, orient=VERTICAL, width=325, borderwidth=3, bg='#ccccb3')
        ExplorerPane.pack(fill=BOTH, expand=1)

        ProjectExplorer = PanedWindow(ExplorerPane, orient=VERTICAL, height=400)
        ProjectExplorer.pack(fill=BOTH, expand=1)

        ProjectExplorerControls = Frame(ProjectExplorer)
        self.OpenBtn = Button(ProjectExplorerControls, text="Open", width=10, fg="red", command=self.browse_project)
        self.OpenBtn.pack(side=LEFT)
        self.SaveBtn = Button(ProjectExplorerControls, text="Save", fg="red", width=10, command=self.save_current_tab)
        self.SaveBtn.pack(side=LEFT)
        self.SaveBtn["state"] = "disabled"
        self.SaveAllBtn = Button(ProjectExplorerControls, text="SaveAll", fg="red", width=10,
                                 command=self.save_all_tabs)
        self.SaveAllBtn.pack(side=LEFT)
        self.SaveAllBtn["state"] = "disabled"
        self.RefreshBtn = Button(ProjectExplorerControls, text="Refresh", fg="red", width=10)
        self.RefreshBtn.pack(side=LEFT)
        self.RefreshBtn["state"] = "disabled"
        ProjectExplorer.add(ProjectExplorerControls)

        # ProjectExplorerFrame = tk.Frame(master,
        #                          background="#ffffff")
        self.ProjectExplorerTree = ttk.Treeview(master, show="tree")
        self.set_scrollbar(self.ProjectExplorerTree, ProjectExplorer)
        self.ProjectExplorerTree.bind("<Double-1>", self.OnProjectDoubleClick)
        self.ProjectExplorerTree.bind("<Button-3>", self.do_popup)

        ProjectExplorer.add(self.ProjectExplorerTree)

        # ProjectExplorer.add(ProjectExplorerFrame)

        StepDefExplorer = PanedWindow(ExplorerPane, orient=VERTICAL)
        StepDefExplorer.pack(fill=BOTH, expand=1)

        StepDefExplorerControls = Frame(StepDefExplorer)
        self.StepDefExplorerTree = ttk.Treeview(master, show="tree")
        # self.StepDefExplorerTree = self.set_scrollbar(master, StepDefExplorer)
        self.set_scrollbar(self.StepDefExplorerTree, StepDefExplorer)
        self.StepDefExplorerTree.bind("<Double-1>", self.onStepDefDoubleClick)
        self.StepDefExplorerTree.bind("<Button-1>", self.RenameViewBtn)

        self.StepOpenBtn = Button(StepDefExplorerControls, text="Load", width=10, fg="red", command=self.stepdefload)
        self.StepOpenBtn.pack(side=LEFT)
        self.FindBtn = Button(StepDefExplorerControls, text="Find", fg="red", width=10)
        self.FindBtn.pack(side=LEFT)
        self.FindBtn["state"] = "disabled"
        self.View_Edit_Btn = Button(StepDefExplorerControls, text="Add", fg="red", width=10,
                                    command=self.AddStepDefinition)
        self.View_Edit_Btn.pack(side=LEFT)
        self.View_Edit_Btn["state"] = "disabled"
        self.StepDefRefreshBtn = Button(StepDefExplorerControls, text="Refresh", fg="red", width=10,
                                        command=self.RefreshXML)
        self.StepDefRefreshBtn.pack(side=LEFT)
        self.StepDefRefreshBtn["state"] = "disabled"
        StepDefExplorer.add(StepDefExplorerControls)

        StepDefExplorer.add(StepDefExplorerControls)
        StepDefExplorer.add(self.StepDefExplorerTree)

        EditorPane = PanedWindow(MainWindow)

        EditorTabs = ttk.Notebook(master)
        EditorTabs.pack(expand=1, fill="both")
        self.EditorTabs = EditorTabs
        self.EditorTabs.bind('<Button-3>', self.tab_on_right_click)

        EditorPane.add(EditorTabs)
        EditorPane.pack(fill=BOTH, expand=1)

        #####################################################################
        #####################################################################
        #####################################################################

        ExplorerPane.add(ProjectExplorer)
        ExplorerPane.add(StepDefExplorer)
        MainWindow.add(ExplorerPane)
        MainWindow.add(EditorPane)
        statusbar = Label(self.master, textvariable=self.statusvar, bd=1, relief=SUNKEN, anchor=W)
        statusbar.pack(side=BOTTOM, fill=X)

    def tab_on_right_click(self, event):
        clicked_tab = self.EditorTabs.tk.call(self.EditorTabs._w, "identify", "tab", event.x, event.y)
        self.EditorTabs.select(clicked_tab)
        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label="Save (CTRL+S)", image=self.savetab_pic2, compound=tk.LEFT,
                               command=lambda: self.save_current_tab())
        self.popup.add_command(label="Close", image=self.cancel_pic2, compound=tk.LEFT,
                               command=lambda: self.closeTab(clicked_tab))
        self.popup.add_command(label="Search (CTRL+F)", image=self.find_pic2, compound=tk.LEFT,
                               command=lambda: self.searchText())
        self.popup.add_command(label="Undo (CTRL+Z)", image=self.undo_pic2, compound=tk.LEFT,
                               command=lambda: self.undo())
        self.popup.add_command(label="Redo (CTRL+Y)", image=self.redo_pic2, compound=tk.LEFT,
                               command=lambda: self.redo())
        self.popup.add_command(label="New Scenario (CTRL+N)", image=self.savetab_pic2, compound=tk.LEFT,
                               command=lambda: self.newScenario())
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def read_config(self, sCollection, sKey):
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object[sCollection]
        return userinfo[sKey]

    def closeTab(self, clicked_tab):
        bFlag = False
        curr_tab = self.get_tab()
        nb = self.EditorTabs
        tabName = nb.tab(nb.select(), "text")
        sRevisedText = self.tabs[curr_tab].textbox.get(1.0, 'end')
        bQuestion = False
        if tabName.startswith("* "):
            answer = messagebox.askokcancel("This tab has unsaved changes", "Do you want to close without saving?")
            if answer:
                bQuestion = True
        else:
            bQuestion = True

        if bQuestion:
            iTotalKeys = len(self.sTabsList)
            currentIID = self.sTabsList[clicked_tab]
            self.sOpenedTabs.remove(tabName.replace("* ", ""))
            del self.tabs[next(islice(self.tabs, clicked_tab, None))]
            for key in range(iTotalKeys):
                if key == clicked_tab:
                    self.sTabsList.pop(key)
                    self.sOriginalText.pop(key)
                    bFlag = True
                elif bFlag:
                    self.sTabsList[key - 1] = self.sTabsList[key]
                    self.sOriginalText[key - 1] = self.sOriginalText[key]

            x = self.ProjectExplorerTree.get_children(currentIID)
            for item in x:
                self.ProjectExplorerTree.delete(item)

            self.tabIndex -= 1
            self.EditorTabs.forget(clicked_tab)

    def set_scrollbar(self, treeview, splitter):
        treeview.propagate(True)
        treeview.pack(side="left", fill='y')
        fr_y = tk.Frame(treeview)
        fr_y.pack(side='right', fill='y')
        tk.Label(fr_y, borderwidth=1, relief='raised', font="Arial 8").pack(side='bottom', fill='x')
        sb_y = tk.Scrollbar(fr_y, orient="vertical", command=treeview.yview)
        sb_y.pack(expand='yes', fill='y')
        fr_x = tk.Frame(treeview)
        fr_x.pack(side='bottom', fill='x')
        sb_x = tk.Scrollbar(fr_x, orient="horizontal", command=treeview.xview)
        sb_x.pack(expand='yes', fill='x')
        treeview.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

    def onStepDefDoubleClick(self, event):
        iid = self.StepDefExplorerTree.identify("item", event.x, event.y)

        if iid.lower().startswith("//"):
            if len(self.sOpenedTabs) > 0:
                self.StepDefUpdateWindow(self.StepDefExplorerTree.item(iid)["text"])

    def RenameViewBtn(self, event):
        iid = self.StepDefExplorerTree.identify("item", event.x, event.y)

        if iid.lower().startswith("//"):
            self.View_Edit_Btn.configure(text="View/Edit")
        else:
            self.View_Edit_Btn.configure(text="Add")

    def OnProjectDoubleClick(self, event):
        iid = self.ProjectExplorerTree.identify("item", event.x, event.y)
        if iid.lower().endswith(".feature") or iid.lower().endswith(".java") or iid.lower().endswith(".xml"):
            children = self.ProjectExplorerTree.get_children(iid)
            if self.ProjectExplorerTree.item(iid)["text"] in self.sOpenedTabs:
                self.statusvar.set(self.ProjectExplorerTree.item(iid)["text"] + " is already opened")
                self.EditorTabs.select(self.sOpenedTabs.index(self.ProjectExplorerTree.item(iid)["text"]))
            else:
                sOriginalText = self.expandForScenarios(iid)
                currentTab = ttk.Frame(self.EditorTabs)
                self.tabs[currentTab] = Document(currentTab, self.create_text_widget(currentTab))
                iLine = 1
                for line in sOriginalText:
                    self.tabs[currentTab].textbox.insert('end', line)
                    self.defineFeatureFileTags(iLine, line, self.tabs[currentTab].textbox)
                    iLine = iLine + 1

                # self.tabs[currentTab].textbox.insert('end', sOriginalText)
                if iid.lower().endswith(".feature"):
                    self.EditorTabs.add(currentTab, text=self.ProjectExplorerTree.item(iid)["text"],
                                        image=self.cucumber_pic2, compound=tk.LEFT)
                elif iid.lower().endswith(".java"):
                    self.EditorTabs.add(currentTab, text=self.ProjectExplorerTree.item(iid)["text"],
                                        image=self.iSourceCode2, compound=tk.LEFT)
                elif iid.lower().endswith(".xml"):
                    self.EditorTabs.add(currentTab, text=self.ProjectExplorerTree.item(iid)["text"],
                                        image=self.xmltab_pic2, compound=tk.LEFT)
                self.EditorTabs.select(currentTab)
                self.sOriginalText[self.tabIndex] = "".join(sOriginalText)
                self.sTabsList[self.tabIndex] = iid
                self.sOpenedTabs.append(self.ProjectExplorerTree.item(iid)["text"])
                self.tabIndex += 1
                self.statusvar.set("Opened " + self.ProjectExplorerTree.item(iid)["text"] + " file")
            self.SaveBtn["state"] = "normal"
            self.SaveAllBtn["state"] = "normal"
        elif self.ProjectExplorerTree.item(iid)["text"].lower().startswith("feature:") or \
                self.ProjectExplorerTree.item(iid)["text"].lower().startswith("scenario:") or \
                self.ProjectExplorerTree.item(iid)["text"].lower().startswith("scenario outline:"):
            self.find(self.ProjectExplorerTree.item(iid)["text"])

    def create_text_widget(self, frame):
        # Horizontal Scroll Bar
        xscrollbar = tk.Scrollbar(frame, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        # Vertical Scroll Bar
        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        textbox = tk.Text(frame, relief='sunken', borderwidth=0, wrap='none')
        textbox.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)

        # Keyboard / Click Bindings
        textbox.bind('<Control-f>', self.searchText)
        textbox.bind('<Control-s>', self.save_current_tab)
        textbox.bind('<Control-z>', self.undo)
        textbox.bind('<Control-y>', self.redo)
        textbox.bind('<Control-n>', self.newScenario)
        textbox.bind("<Button-1>", self.cleartags)
        textbox.bind("<Key>", self.UpdateFeatureFile)
        # textbox.bind("<Return>", self.UpdateFeatureFile)

        # Pack the textbox
        textbox.pack(fill='both', expand=True)

        # Configure Scrollbars
        xscrollbar.config(command=textbox.xview)
        yscrollbar.config(command=textbox.yview)

        return textbox

    def create_tree_widget(self, frame):
        # Horizontal Scroll Bar
        xscrollbar = tk.Scrollbar(frame, orient='horizontal')
        xscrollbar.pack(side='bottom', fill='x')

        # Vertical Scroll Bar
        yscrollbar = tk.Scrollbar(frame)
        yscrollbar.pack(side='right', fill='y')

        # Create Text Editor Box
        tree = ttk.Treeview(frame, show="tree")
        # textbox = tk.Text(frame, relief='sunken', borderwidth=0, wrap='none')
        tree.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, undo=True, autoseparators=True)

        # Pack the textbox
        tree.pack(fill='both', expand=True)

        # Configure Scrollbars
        xscrollbar.config(command=frame.xview)
        yscrollbar.config(command=frame.yview)

        return frame

    def cleartags(self, *args):
        curr_tab = self.get_tab()
        text = self.tabs[curr_tab].textbox
        text.tag_remove('found', '1.0', END)

    def FormatFeature(self, *args):
        curr_tab = self.get_tab()
        sCursorPos = self.tabs[curr_tab].textbox.index(tk.INSERT)
        sChars = self.tabs[curr_tab].textbox.get(sCursorPos.split(".")[0] + ".0",
                                                 float(self.tabs[curr_tab].textbox.index(tk.INSERT)) + 0.1)
        if sChars.strip().startswith("Scenario:") or sChars.strip().startswith("Scenario Outline:"):
            print(sCursorPos)
            text = self.tabs[curr_tab].textbox
            text.insert(str(int(sCursorPos.split(".")[0]) + 1) + ".0", '    ')
            print(self.tabs[curr_tab].textbox.index(tk.INSERT))

            tabWidth = 1
            # previous = text.get("insert -%d chars" % tabWidth, "insert")
            # if previous == " " * tabWidth:
            # text.delete("insert-%d chars" % tabWidth, "insert")
            # text.delete(last_insert[0], last_insert[1])
            # text.insert(tk.INSERT, "\n")
            # text.insert('end', "    ")
            # text.insert()

    def UpdateFeatureFile(self, *args):
        curr_tab = self.get_tab()
        nb = self.EditorTabs
        tabName = nb.tab(nb.select(), "text")
        sCursorPos = self.tabs[curr_tab].textbox.index(tk.INSERT)
        sChars = self.tabs[curr_tab].textbox.get(sCursorPos.split(".")[0] + ".0",
                                                 float(self.tabs[curr_tab].textbox.index(tk.INSERT)) + 0.1)
        text = self.tabs[curr_tab].textbox
        self.defineFeatureFileTags(sCursorPos.split(".")[0], sChars, text)
        sRevisedText = self.tabs[curr_tab].textbox.get(1.0, 'end')
        if sRevisedText != self.sOriginalText[nb.index(nb.select())]:
            if not tabName.startswith("* "):
                nb.tab("current", text="* " + tabName)

    def defineFeatureFileTags(self, lineNumber, sChars, text, *args):

        sCursorPos = str(lineNumber) + "." + str(len(sChars))
        line = sChars.strip()

        # if line == "":
        #     iCharsToAdd = ""
        #     if int(sCursorPos.split(".")[0]) > 1:
        #         iPreviousLine = int(sCursorPos.split(".")[0]) - 1
        #         sPreviousLine = text.get(str(int(sCursorPos.split(".")[0]) - 1) + ".0",
        #                                                         str(iPreviousLine) + ".30")
        #         if sPreviousLine.strip() != "":
        #             sPreviousLine = text.get(str(int(sCursorPos.split(".")[0]) - 2) + ".0",
        #                                                             str(iPreviousLine) + ".30")
        #         sStrippedLine = sPreviousLine.lstrip()
        #         print(sPreviousLine)
        #         iCharsToAdd = sPreviousLine.replace(sStrippedLine, "")
        #
        #     text.insert(tk.INSERT, iCharsToAdd)

        if line.startswith("Given"):
            idx = re.search("Given", sChars)
            startIndex = str(sChars.index("Given"))
            endIndex = str(sChars.index("Given") + 5)
            text.tag_add('given', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "."
                         + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('given', foreground='purple')
        elif line.startswith("When"):
            idx = re.search("When", sChars)
            startIndex = str(sChars.index("When"))
            endIndex = str(sChars.index("When") + 4)
            text.tag_add('when', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "." + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('when', foreground='purple')
        elif line.startswith("Then"):
            idx = re.search("Then", sChars)
            startIndex = str(sChars.index("Then"))
            endIndex = str(sChars.index("Then") + 4)
            text.tag_add('then', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "." + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('then', foreground='purple')
        elif line.startswith("And"):
            idx = re.search("And", sChars)
            startIndex = str(sChars.index("And"))
            endIndex = str(sChars.index("And") + 3)
            text.tag_add('and', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "." + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('and', foreground='purple')
        elif line.startswith("Feature:"):
            idx = re.search("Feature:", sChars)
            startIndex = str(sChars.index("Feature:"))
            endIndex = str(sChars.index("Feature:") + 8)
            text.tag_add('feature', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "."
                         + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('feature', foreground='blue')
        elif line.startswith("Scenario:"):
            idx = re.search("Scenario:", sChars)
            startIndex = str(sChars.index("Scenario:"))
            endIndex = str(sChars.index("Scenario:") + 9)
            text.tag_add('Scenario', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "."
                         + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('Scenario', foreground='green')
        elif line.startswith("Scenario Outline:"):
            idx = re.search("Scenario Outline:", sChars)
            startIndex = str(sChars.index("Scenario Outline:"))
            endIndex = str(sChars.index("Scenario Outline:") + 17)
            text.tag_add('Scenario', sCursorPos.split(".")[0] + "." + startIndex, sCursorPos.split(".")[0] + "."
                         + endIndex)
            text.see(sCursorPos.split(".")[0] + "." + endIndex)
            text.tag_config('Scenario', foreground='green')

        if len(line.split('"')) > 1:
            arSplit = line.split('"')
            for x in range(len(arSplit) - 2):
                if x % 2 == 0:
                    idx = re.search('"' + arSplit[x + 1] + '"', sChars)
                    startIndex = str(sChars.index('"' + arSplit[x + 1] + '"'))
                    endIndex = str(sChars.index('"' + arSplit[x + 1] + '"') + len('"' + arSplit[x + 1] + '"'))
                    text.tag_add('doublequotes', sCursorPos.split(".")[0] + "." + startIndex,
                                 sCursorPos.split(".")[0] + "." + endIndex)
                    text.see(sCursorPos.split(".")[0] + "." + endIndex)
                    text.tag_config('doublequotes', foreground='blue')

    def do_popup(self, event):
        item = self.ProjectExplorerTree.identify_row(event.y)
        self.ProjectExplorerTree.focus(item)
        self.ProjectExplorerTree.selection_set(item)
        self.popup = Menu(root, tearoff=0)
        isdir = os.path.isdir(item)
        isFile = os.path.isfile(item)
        if item is not "":
            if isdir:
                self.popup.add_command(label="New File", command=lambda: self.CreateNewFile(item))
                self.popup.add_separator()
                self.popup.add_command(label="Delete", command=lambda: self.deleteFile(item))
                # self.popup.add_command(label="Search Scenarios", command=lambda: self.closeWindow())
            elif isFile:
                self.popup.add_command(label="Rename", command=lambda: self.renameFile(item))
                self.popup.add_command(label="Delete", command=lambda: self.deleteFile(item))

            if self.ProjectExplorerTree.item(item)["text"] in self.sOpenedTabs:
                self.popup.add_separator()
                self.popup.add_command(label="New Scenario", command=lambda: self.newScenario())
                self.EditorTabs.select(self.sOpenedTabs.index(self.ProjectExplorerTree.item(item)["text"]))

            if item.endswith("ScenarioXYZ"):
                self.popup.add_command(label="Edit Scenario",
                                       command=lambda: self.editScenario(self.ProjectExplorerTree.item(item)["text"]))
        try:
            self.popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup.grab_release()

    def closeWindow(self):
        root.destroy()
        sys.exit()

    def editScenario(self, scenarioName):
        if self.filename == "":
            messagebox.showinfo("Information", "Please load the xml before creating the new scenario")
        else:
            curr_tab = self.get_tab()
            text = self.tabs[curr_tab].textbox
            root = tk.Tk()
            root.geometry("800x400")
            root.title("EditScenario")
            root.resizable(True, True)
            myGUI = EditScenario(root, self.filename, text, scenarioName)
            myGUI.CreateWindow()
            root.mainloop()

    def newScenario(self, *args):
        if self.filename == "":
            messagebox.showinfo("Information", "Please load the xml before creating the new scenario")
        else:
            curr_tab = self.get_tab()
            text = self.tabs[curr_tab].textbox
            root = tk.Tk()
            root.geometry("580x400")
            root.title("NewScenario")
            root.resizable(False, True)
            myGUI = NewScenario(root, self.filename, text)
            myGUI.CreateWindow()
            root.mainloop()

    def StepDefUpdateWindow(self, statement):
        stepDefRoot = tk.Tk()
        # stepDefRoot.geometry("400x200")
        stepDefRoot.resizable(False, False)
        frame = tk.Frame(stepDefRoot, bd=2, bg='#d9ecd0')  # , bg='#d9ecd0')
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        oXml = cXml(self.filename)

        var = tk.StringVar(frame, 0)
        R1 = Radiobutton(frame, text="Given", variable=var, value='Given', bg='#d9ecd0', font=('TkDefaultFont', 10))
        R1.select()
        R1.place(x=50, y=30, width=70)
        R2 = Radiobutton(frame, text="When", variable=var, value='When', bg='#d9ecd0', font=('TkDefaultFont', 10))
        R2.place(x=125, y=30, width=70)
        R3 = Radiobutton(frame, text="And", variable=var, value='And', bg='#d9ecd0', font=('TkDefaultFont', 10))
        R3.place(x=200, y=30, width=70)
        R4 = Radiobutton(frame, text="Then", variable=var, value='Then', bg='#d9ecd0', font=('TkDefaultFont', 10))
        R4.place(x=275, y=30, width=70)

        # var.get() will let us know what is selected
        entry = tk.Entry(frame, bg="white", font=('TkDefaultFont', 10))
        entry.place(x=50, y=70, width=290)
        entry.insert(END, statement)

        Parameters = oXml.ReadNode("//StepDefinition[@Statement='" + statement + "']/@Parameters")
        mParamDict = {}
        iInitY = 120;
        if len(Parameters) > 0:
            if Parameters[0].strip() != "":
                arParameters = Parameters[0].split("\n")
                for parameter in arParameters:
                    arIndParams = parameter.split("==");
                    label = tk.Label(frame, text=arIndParams[0], bg='#d9ecd0', anchor=W)
                    label.place(x=50, y=iInitY)
                    entry2 = tk.Entry(frame, bg="white", font=('TkDefaultFont', 10))
                    entry2.place(x=190, y=iInitY)
                    iInitY = iInitY + 40
                    mParamDict[arIndParams[0]] = entry2

        button = tk.Button(frame, text="Submit", bg='Light gray', fg='red',
                           command=lambda: self.AddStatement(var.get() + " " + statement, mParamDict, stepDefRoot))
        button.place(x=150, y=iInitY)

        stepDefRoot.geometry("400x" + str(iInitY + 70))

        stepDefRoot.mainloop()

    def AddStatement(self, statement, ParameterDict, stepDefRoot):
        for parameter in ParameterDict.keys():
            statement = statement.replace(parameter, ParameterDict.get(parameter).get())
        curr_tab = self.get_tab()
        nb = self.EditorTabs
        sCursorPos = self.tabs[curr_tab].textbox.index(tk.INSERT)
        iCharsToAdd = ""
        if int(sCursorPos.split(".")[0]) > 1:
            iPreviousLine = int(sCursorPos.split(".")[0]) - 1
            sPreviousLine = self.tabs[curr_tab].textbox.get(str(int(sCursorPos.split(".")[0]) - 1) + ".0",
                                                            str(iPreviousLine) + ".30")
            if sPreviousLine.strip() != "":
                sPreviousLine = self.tabs[curr_tab].textbox.get(str(int(sCursorPos.split(".")[0]) - 2) + ".0",
                                                                str(iPreviousLine) + ".30")

            sStrippedLine = sPreviousLine.lstrip()
            iCharsToAdd = sPreviousLine.replace(sStrippedLine, "")

        text = self.tabs[curr_tab].textbox
        sNewLine = iCharsToAdd + statement
        text.insert(tk.INSERT, sNewLine)
        sChars = self.tabs[curr_tab].textbox.get(sCursorPos.split(".")[0] + ".0",
                                                 float(self.tabs[curr_tab].textbox.index(tk.INSERT)) + 0.1)
        self.defineFeatureFileTags(sCursorPos.split(".")[0], sNewLine, text)
        text.insert(tk.INSERT, '\n')
        stepDefRoot.destroy()

    def cancelScenario(self, scenarioWindow):
        scenarioWindow.destroy()

    def scenarioTypeSelected(self, scenarioType, scenarioWindow, datatableFrame, SaveBtn, CancelBtn):
        if scenarioType.get() == "Scenario Outline":
            self.dataTableRows.clear()
            for i in range(5):
                cols = []
                for j in range(11):
                    e = Entry(datatableFrame, relief=RIDGE, width=6)
                    e.grid(row=i, column=j, sticky=NSEW)
                    cols.append(e)
                self.dataTableRows.append(cols)
                datatableFrame.place(x=20, y=230, anchor=NW)
                scenarioWindow.geometry("480x400")
                SaveBtn.place(x=150, y=350, anchor=NW)
                CancelBtn.place(x=250, y=350, anchor=NW)
        else:
            scenarioWindow.geometry("480x300")
            datatableFrame.destroy()
            self.datatableFrame = Frame(scenarioWindow, width=54, height=10)
            SaveBtn.place(x=150, y=250, anchor=NW)
            CancelBtn.place(x=250, y=250, anchor=NW)

    def addScenario(self):
        for rows in self.dataTableRows:
            for col in rows:
                print(col.get())
            print('')

    def addStep(self):
        for rows in self.dataTableRows:
            for col in rows:
                print(col.get())
            print('')

    def autoscroll(self, sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            # print("deactivate")
            sbar.activate()
            # sbar.grid_remove()
        else:
            # print("deactivate")
            sbar.deactivate()
            # sbar.grid()
        sbar.set(first, last)

    def create_file_list(self, treeview, ParentIID, folder_location):
        dirlist = [x for x in os.listdir(folder_location) if os.path.isdir(os.path.join(folder_location, x))]
        filelist = [x for x in os.listdir(folder_location) if not os.path.isdir(os.path.join(folder_location, x))]
        for i, item in enumerate(dirlist + filelist):
            abspath = os.path.join(folder_location, item)
            isdir = os.path.isdir(abspath)
            self.InsertNode(treeview, ParentIID, abspath, item)
            if isdir:
                self.create_file_list(self.ProjectExplorerTree, abspath, abspath)

    def InsertNode(self, treeview, ParentIID, currentIID, item):
        isdir = os.path.isdir(currentIID)
        if isdir:
            treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.folder_pic2)
        else:
            if currentIID.lower().endswith(".xml"):
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.xml_pic2)
            elif currentIID.lower().endswith(".java"):
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.java_pic2)
            elif currentIID.lower().endswith(".feature"):
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.cucumber_pic2)
            elif item.lower().startswith("feature:"):
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.feature_pic2, open=True)
            elif item.lower().startswith("scenario:") or item.lower().startswith("scenario outline:"):
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.scenario_pic2)
            else:
                treeview.insert(ParentIID, 'end', iid=currentIID, text=item, image=self.file_pic2)

    def CreateNewFile(self, item):
        USER_INP = simpledialog.askstring(title="New File",
                                          prompt="Enter the new file name along with extension?")

        if USER_INP != "":
            if os.path.isfile(item + "/" + USER_INP):
                messagebox.showinfo("New File", "File Already exist with the same name")
            else:
                f = open(item + "/" + USER_INP, "w+")
                f.close()
                self.InsertNode(self.ProjectExplorerTree, item, item + "/" + USER_INP, USER_INP)

    def expandForScenarios(self, item):
        file = open(item, "r")
        Lines = file.readlines()
        newParentIID = ""
        for line in Lines:
            if line.strip().lower().startswith("feature:"):
                self.InsertNode(self.ProjectExplorerTree, item, item + "/" + line.strip(), line.strip())
                self.ProjectExplorerTree.item(item, open=True)
                newParentIID = item + "/" + line.strip()
                break
        file.close()
        self.ReadScenarios(item, newParentIID)
        return Lines

    def ReadScenarios(self, sFile, item):
        file = open(sFile, "r")
        Lines = file.readlines()
        for line in Lines:
            if line.strip().lower().startswith("scenario:") or line.strip().lower().startswith("scenario outline:"):
                self.InsertNode(self.ProjectExplorerTree, item, item + "/" + line.strip() + "ScenarioXYZ", line.strip())
        file.close()

    def deleteFile(self, item):
        answer = messagebox.askokcancel("Question", "Do you want to delete this file?")
        if answer:
            if os.path.exists(item):
                try:
                    os.remove(item)
                    self.ProjectExplorerTree.delete(item)
                except:
                    messagebox.showinfo("Information", "Unable to delete the file")

    def renameFile(self, item):

        if self.ProjectExplorerTree.item(item)["text"] in self.sOpenedTabs:
            messagebox.showinfo("Information", "We cannot rename a file which is already opened")
            self.statusvar.set("We cannot rename a file which is already opened")
            self.EditorTabs.select(self.sOpenedTabs.index(self.ProjectExplorerTree.item(item)["text"]))
        else:
            USER_INP = simpledialog.askstring(title="Rename File",
                                              prompt="Enter the new file name along with extension?")
            parent_iid = self.ProjectExplorerTree.parent(item)

            if USER_INP != "":
                if os.path.isfile(parent_iid + "/" + USER_INP):
                    messagebox.showinfo("Rename File", "File Already exist with the same name")
                else:
                    try:
                        os.rename(item, parent_iid + "/" + USER_INP)
                        self.ProjectExplorerTree.delete(item)
                        self.InsertNode(self.ProjectExplorerTree, parent_iid, parent_iid + "/" + USER_INP, USER_INP)
                    except:
                        messagebox.showinfo("Information", "Unable to rename the file")

    def CreateNewFolder(self, item):
        USER_INP = simpledialog.askstring(title="New Folder",
                                          prompt="Enter the new folder name?")
        print(USER_INP)

    def addMenu(self, master):
        menu = Menu(master)
        master.config(menu=menu)

        # File menu.
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu, underline=0)

        file_menu.add_command(label="New", compound='left', accelerator='Ctrl+N',
                              underline=0)
        file_menu.add_command(label="Open", compound='left', accelerator='Ctrl+O',
                              underline=0, command=lambda: self.browse_project())
        file_menu.add_separator()
        file_menu.add_command(label="Save", compound='left', accelerator='Ctrl+S',
                              underline=0)
        file_menu.add_command(label="Close", accelerator='Alt+F4', underline=0)

        # Edit Menu.
        edit_menu = Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu, underline=0)

        edit_menu.add_command(label="Undo", compound='left', accelerator='Ctrl+Z',
                              underline=0, command=self.undo)
        edit_menu.add_command(label="Redo", compound='left', accelerator='Ctrl+Y',
                              underline=0, command=self.redo)
        edit_menu.add_separator()

    def browse_project(self):
        if len(self.sTabsList) == 0:
            folder_location = filedialog.askdirectory(title="Select a directory")
            tree = self.ProjectExplorerTree
            if folder_location != "":
                tree.delete(*tree.get_children())
                tree.insert('', '0', folder_location, text=folder_location, image=self.folder_pic2, open=True)
                self.create_file_list(tree, folder_location, folder_location)
                self.statusvar.set(folder_location + " is loaded")
            # self.SaveBtn["state"] = "normal"
            # self.SaveAllBtn["state"] = "normal"
            self.RefreshBtn["state"] = "normal"
            return folder_location
        else:
            messagebox.showinfo("Information", "Please close all the tabs before opening a new project")

    def get_tab(self):
        return self.EditorTabs._nametowidget(self.EditorTabs.select())

    def searchText(self, *args):
        USER_INP = simpledialog.askstring(title="Find",
                                          prompt="Enter the string that needs to be found")
        self.find(USER_INP)

    def find(self, sSearchText):

        # remove tag 'found' from index 1 to END
        curr_tab = self.get_tab()
        text = self.tabs[curr_tab].textbox
        text.tag_remove('found', '1.0', END)

        # returns to widget currently in focus
        iTotalFound = 0
        if sSearchText:
            idx = '1.0'
            while 1:
                # searches for desried string from index 1
                idx = text.search(sSearchText, idx, nocase=1,
                                  stopindex=END)
                if not idx:
                    break
                else:
                    iTotalFound += 1

                # last index sum of current index and
                # length of text
                lastidx = '%s+%dc' % (idx, len(sSearchText))

                # overwrite 'Found' at idx
                text.tag_add('found', idx, lastidx)
                idx = lastidx
                text.see(idx)
                # mark located string as red

            text.tag_config('found', foreground='red', background='yellow')
        self.statusvar.set(str(iTotalFound) + " matches found for " + sSearchText)

    def save_all_tabs(self):
        intIndex = 0
        for i in self.EditorTabs.tabs():
            nb = self.EditorTabs
            curr_tab = nb._nametowidget(i)
            tabName = nb.tab(curr_tab, "text")
            print(tabName)
            sRevisedText = self.tabs[curr_tab].textbox.get(1.0, 'end')
            with open(self.sTabsList[intIndex], 'w') as f:
                f.write(sRevisedText)
            nb.tab(curr_tab, text=tabName.replace("* ", ""))
            self.sOriginalText[intIndex] = sRevisedText
            intIndex += 1
        self.statusvar.set("All the opened tabs are saved!")

    def save_current_tab(self, *args):
        curr_tab = self.get_tab()
        nb = self.EditorTabs
        tabName = nb.tab(nb.select(), "text")
        sRevisedText = self.tabs[curr_tab].textbox.get(1.0, 'end')
        with open(self.sTabsList[nb.index(nb.select())], 'w') as f:
            f.write(sRevisedText)

        self.sOriginalText[nb.index(nb.select())] = sRevisedText
        nb.tab("current", text=tabName.replace("* ", ""))
        self.statusvar.set(self.sTabsList[nb.index(nb.select())] + " is saved")

    def undo(self, *args):
        self.tabs[self.get_tab()].textbox.edit_undo()

    def redo(self, *args):
        self.tabs[self.get_tab()].textbox.edit_redo()

    def AddStepDefinition(self):
        if self.View_Edit_Btn.cget('text') == 'Add':
            root = tk.Tk()
            app = AddStepDefinition(root, self.filename, '')
            app.CreateUI()
            root.mainloop()
        else:
            root = tk.Tk()
            curItem = self.StepDefExplorerTree.focus()
            oXml = cXml(self.filename)
            statement = self.StepDefExplorerTree.item(curItem)["text"]
            parameters = oXml.ReadNode("//StepDefinition[@Statement='" + statement + "']/@Parameters")
            instructions = oXml.ReadNode("//StepDefinition[@Statement='" + statement + "']/@Instructions")
            xtrnlData = oXml.ReadNode("//StepDefinition[@Statement='" + statement + "']/@ExternalData")
            parent_iid = self.StepDefExplorerTree.parent(curItem)
            app = AddStepDefinition(root, self.filename, "//StepDefinition[@Statement='" + statement + "']")
            app.CreateUI()
            app.entry.insert(0, statement)
            app.instructionstext.insert('end', "".join(instructions))
            app.parametertext.insert('end', "".join(parameters))
            if "".join(xtrnlData) == 'Yes':
                app.R1.select()
            else:
                app.R2.select()
            sKeys = self.read_config("XML", "keys")
            arKeys = sKeys.split(",")
            app.OptionList.current(arKeys.index(self.StepDefExplorerTree.item(parent_iid)['text']))
            sOutput = "Statement: " + statement \
                      + "\n\nCategory: " + self.StepDefExplorerTree.item(parent_iid)['text'] \
                      + "\n\nExternalData: " + "".join(xtrnlData) \
                      + "\n\nParameters: " + "".join(parameters) \
                      + "\n\nInstructions: " + "".join(instructions)
            app.Outputtext.insert('end', sOutput)
            root.mainloop()

    def stepdefload(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   filetypes=(("XML File", "*.xml"), ("All Files", "*.*")),
                                                   title="Choose a file."
                                                   )

        tree = self.StepDefExplorerTree
        if self.filename != "":
            oXml = cXml(self.filename)
            tree.delete(*tree.get_children())
            tree.insert('', '0', self.filename, text=self.filename, image=self.folder_pic2, open=True)
            sKeys = self.read_config("XML", "keys")
            arKeys = sKeys.split(",")
            for key in arKeys:
                self.getImage("XML", key)
                tree.insert(self.filename, 'end', iid=key, text=key, image=self.sXMLImages[key])
                sValues = oXml.ReadNode("//" + key + "/StepDefinition/@Statement")
                for value in sValues:
                    tree.insert(key, 'end', iid="//" + key + "/StepDefinition[@Statement='" + value + "']", text=value,
                                image=self.step_pic2)
            self.FindBtn["state"] = "normal"
            self.View_Edit_Btn["state"] = "normal"
            self.StepDefRefreshBtn["state"] = "normal"

    def RefreshXML(self):
        tree = self.StepDefExplorerTree
        if self.filename != "":
            oXml = cXml(self.filename)
            tree.delete(*tree.get_children())
            tree.insert('', '0', self.filename, text=self.filename, image=self.folder_pic2, open=True)
            sKeys = self.read_config("XML", "keys")
            arKeys = sKeys.split(",")
            for key in arKeys:
                self.getImage("XML", key)
                tree.insert(self.filename, 'end', iid=key, text=key, image=self.sXMLImages[key])
                sValues = oXml.ReadNode("//" + key + "/StepDefinition/@Statement")
                for value in sValues:
                    tree.insert(key, 'end', iid="//" + key + "/StepDefinition[@Statement='" + value + "']", text=value,
                                image=self.step_pic2)
            self.FindBtn["state"] = "normal"
            self.View_Edit_Btn["state"] = "normal"
            self.StepDefRefreshBtn["state"] = "normal"

    def getImage(self, sCollection, sKey):
        sImgPath = self.read_config(sCollection, sKey)
        img1 = Image.open(sImgPath)
        self.sXMLImages[sKey] = ImageTk.PhotoImage(img1)


root = tk.Tk()
myWin = MyGUI(root)
myWin.CreateGUI()
root.mainloop()
