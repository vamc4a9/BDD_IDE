import tkinter as tk
from tkinter import ttk
from configparser import ConfigParser
from PIL import Image, ImageTk

from autocompleter import Autocompleter
from xml import cXml


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)

        self.onFrameConfigure(
            None)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)


class EditScenario():
    def __init__(self, root, filename, text, scenarioName):
        self.textEditor = text
        self.scenarioName = scenarioName
        self.root = root
        self.StepType = {}
        self.StepDetail = {}
        self.StepDelete = {}
        self.StepDTButton = {}
        self.StepMoveButton = {}
        self.StepDTTable = {}
        self.AutoSuggestion = {}

        self.scenarioStep = {}
        self.scenarioStepType = {}
        self.scenarioDTTable = {}

        self.sImages = {}
        self.sExamplesTable = None
        self.AddBtn = None
        self.tags = None
        self.scrollFrame = None
        self.filename = filename
        self.SubmitBtn = None
        self.CancelBtn = None
        self.scenarioname = None
        self.scenarioType = None
        self.AllStatements = []
        oXml = cXml(self.filename)
        sKeys = self.read_config("XML", "keys")
        self.autocompl = Autocompleter()
        df = self.autocompl.import_xml(filename)
        self.new_df = self.autocompl.process_data(df)
        self.model_tf, self.tfidf_matrice = self.autocompl.calc_matrice(self.new_df)

    def read_config(self, sCollection, sKey):
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object[sCollection]
        return userinfo[sKey]

    def getImage(self, sCollection, sKey):
        sImgPath = self.read_config(sCollection, sKey)
        img1 = Image.open(sImgPath)
        self.sImages[sKey] = ImageTk.PhotoImage(img1, master=self.root)

    def find(self, sSearchText):
        if sSearchText:
            idx = '1.0'
            while 1:
                # searches for desried string from index 1
                idx = self.textEditor.search(sSearchText, idx, nocase=1,
                                  stopindex=tk.END)
                if not idx:
                    break
                else:
                    return idx

    def CreateWindow(self):
        frame = tk.Frame(self.root)
        self.getImage("XML", "DeleteIcon")
        self.getImage("XML", "custom_datagrid")
        self.getImage("XML", "move_left")
        self.scrollFrame = ScrollFrame(frame)  # add a new scrollable frame.

        self.insertEmptyRow(self.scrollFrame.viewPort, 1, 1)
        self.insertEmptyRow(self.scrollFrame.viewPort, 2, 1)

        self.scenarioType = ttk.Combobox(self.scrollFrame.viewPort, state='readonly', width=13)
        self.scenarioType['values'] = ('Scenario',
                                  'Scenario Outline',
                                  'Background')
        self.scenarioType.bind("<<ComboboxSelected>>", lambda event, arg=self.scenarioType: self.scenarioTypeSelected(event, arg))
        self.scenarioType.grid(row=3, column=1)
        self.scrollFrame.viewPort.columnconfigure(1, pad=25)

        self.scenarioname = tk.Entry(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10), width=54)
        # self.scenarioname = tk.Entry(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10))
        self.insertEmptyRow(self.scrollFrame.viewPort, 4, 1)
        self.insertEmptyRow(self.scrollFrame.viewPort, 5, 1)

        if self.scenarioName.startswith("Scenario:"):
            self.scenarioType.current(0)
            self.scenarioname.insert('end', self.scenarioName.replace("Scenario:","").strip())
        elif self.scenarioName.startswith("Scenario Outline:"):
            self.scenarioType.current(1)
            self.sExamplesTable = tk.Text(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10), width=54,
                                               height=3)
            self.sExamplesTable.insert('end', "Examples:")
            self.sExamplesTable.grid(row=4, column=2, columnspan=3)
            self.scenarioname.insert('end', self.scenarioName.replace("Scenario Outline:", "").strip())

        self.scenarioname.grid(row=3, column=2, columnspan=3)

        iIndex = self.find(self.scenarioName)
        sNextScenario = self.fn_nextScenario(str(int(iIndex.split(".")[0]) + 1) + ".0")
        endIndex = self.find(sNextScenario)
        print(iIndex)
        print(endIndex)
        sTags =self.fn_GetTags(iIndex)
        self.fn_GetSteps(iIndex, endIndex)
        print(self.scenarioStep)
        print(self.scenarioDTTable)

        intStepIndex = 0
        intRow = 6
        for key in self.scenarioStepType.keys():
            self.StepType[intStepIndex] = self.GetStepType(self.scrollFrame.viewPort,
                                                           self.scenarioStepType[intStepIndex])
            self.StepType[intStepIndex].grid(row=intRow, column=1)
            self.StepDetail[intStepIndex] = tk.Entry(self.scrollFrame.viewPort,
                                                     bg="white", font=('TkDefaultFont', 10), width=54)
            self.StepDetail[intStepIndex].insert('end', self.scenarioStep[intStepIndex])
            self.StepDetail[intStepIndex].grid(row=intRow, column=2, columnspan=3)
            self.StepDetail[intStepIndex].bind('<Down>',lambda event, arg=intStepIndex: self.move(event, arg))
            self.addDeleteBtn(self.scrollFrame.viewPort, intRow, 7)
            self.addDataTableBtn(self.scrollFrame.viewPort, intRow, 8)
            self.addMoveBtn(self.scrollFrame.viewPort, intRow, 9)
            self.insertEmptyRow(self.scrollFrame.viewPort, intRow + 1, 1)
            self.AutoSuggestion[intStepIndex] = tk.Entry(self.scrollFrame.viewPort,
                                                     bg="white", font=('TkDefaultFont', 10), width=54)
            self.AutoSuggestion[intStepIndex].bind('<Down>', lambda event, arg=intStepIndex: self.move2(event, arg))
            AutoSuggestions = self.autocompl.generate_completions(self.scenarioStep[intStepIndex], self.new_df,
                                                                  self.model_tf, self.tfidf_matrice)
            self.AutoSuggestion[intStepIndex].insert('end', AutoSuggestions[0])

            self.AutoSuggestion[intStepIndex].grid(row=intRow, column=10, columnspan=3)

            if key in self.scenarioDTTable.keys():
                self.StepDTTable[int(intStepIndex)] = tk.Text(self.scrollFrame.viewPort, bg="white",
                                                        font=('TkDefaultFont', 10), width=54,
                                                        height=2)
                self.StepDTTable[int(intStepIndex)].insert('end', self.scenarioDTTable[intStepIndex])
                self.StepDTTable[int(intStepIndex)].grid(row=int((intStepIndex * 2 + 6) + 1), column=2, columnspan=6)

            intRow = intRow + 2
            intStepIndex = intStepIndex + 1

        self.AddBtn = tk.Button(self.scrollFrame.viewPort, text="AddStep", bg='Light gray', fg='red',
                                command=lambda: self.addAnewStep(self.scrollFrame.viewPort))

        self.AddBtn.grid(row=intRow, column=4)
        self.insertEmptyRow(self.scrollFrame.viewPort, intRow + 1, 1)

        # self.tags = tk.Text(self.scrollFrame.viewPort, width=54, height=2,relief=tk.RAISED)
        self.tags = tk.Entry(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10), width=54)
        self.tags.insert('end', '@tag1 @tag2')
        self.tags.grid(row=intRow + 2, column=1, columnspan=8)
        self.insertEmptyRow(self.scrollFrame.viewPort, intRow + 3, 1)

        self.SubmitBtn = tk.Button(self.scrollFrame.viewPort, text="Submit", bg='Light gray', fg='red',
                                   command=lambda: self.GetScenarioData())

        self.SubmitBtn.grid(row=intRow + 4, column=3)

        self.CancelBtn = tk.Button(self.scrollFrame.viewPort, text="Cancel", bg='Light gray', fg='red',
                                   command=lambda: self.destryScenarioWin())
        self.CancelBtn.grid(row=intRow + 4, column=9)

        self.scrollFrame.pack(side="top", fill="both", expand=True)
        frame.pack(side="top", fill="both", expand=True)

    def fn_GetTags(self, startIndex):

        if int(startIndex.split(".")[0]) > 1:
            tags = self.textEditor.get(str(int(startIndex.split(".")[0]) - 1) + ".0", startIndex.split(".")[0] + ".0").split("\n")[0]
            if tags.strip().startswith("@"):
                return tags
        else:
            return ""

    def fn_GetSteps(self, startIndex, endIndex):
        arText = self.textEditor.get(str(int(startIndex.split(".")[0])) + ".0",endIndex).split("\n")
        iStepIndex = 0
        for line in arText:
            print(line)
            if line.strip().startswith("Given"):
                print("Given Step here")
                self.scenarioStepType[iStepIndex] = "Given"
                self.scenarioStep[iStepIndex] = line.replace("Given ","").strip()
                iStepIndex = iStepIndex + 1
            elif line.strip().startswith("When"):
                self.scenarioStepType[iStepIndex] = "When"
                self.scenarioStep[iStepIndex] = line.replace("When ","").strip()
                iStepIndex = iStepIndex + 1
            elif line.strip().startswith("And"):
                self.scenarioStepType[iStepIndex] = "And"
                self.scenarioStep[iStepIndex] = line.replace("And ","").strip()
                iStepIndex = iStepIndex + 1
            elif line.strip().startswith("Then"):
                self.scenarioStepType[iStepIndex] = "Then"
                self.scenarioStep[iStepIndex] = line.replace("Then ","").strip()
                iStepIndex = iStepIndex + 1
            elif line.strip().startswith("|"):
                iStepIndex = iStepIndex - 1
                if iStepIndex in self.scenarioDTTable.keys():
                    self.scenarioDTTable[iStepIndex] = self.scenarioDTTable[iStepIndex] + "\n" + line.strip()
                else:
                    self.scenarioDTTable[iStepIndex] = line.strip()
                iStepIndex = iStepIndex + 1
            elif line.strip().startswith("Examples:"):
                break

    def fn_nextScenario(self, startIndex):
        arText = self.textEditor.get(str(int(startIndex.split(".")[0])) + ".0", 'end-1c').split("\n")
        for line in arText:
            if line.strip().lower().startswith("scenario:") or line.strip().lower().startswith("scenario outline:"):
                return line
                break

    def destryScenarioWin(self):
        self.root.destroy()

    def GetScenarioData(self):
        bExamples = False
        sReturn = "    " + self.tags.get() + "\n"
        sReturn = sReturn + "    " + self.scenarioType.get() + ": " + self.scenarioname.get()
        if self.sExamplesTable is not None:
            bExamples = True

        for key in self.StepType.keys():
            if self.StepDetail[key].get() != "":
                sLine = "        " + self.StepType[key].get() + " " + self.StepDetail[key].get()
                sReturn = sReturn + "\n" + sLine
                if key in self.StepDTTable.keys():
                    sDT = self.StepDTTable[key].get("1.0",tk.END).split("\n")
                    for line in sDT:
                        sReturn = sReturn + "\n        " + line

        if bExamples:
            sReturn = sReturn + "\n"
            sDT = self.sExamplesTable.get("1.0",tk.END).split("\n")
            for line in sDT:
                sReturn = sReturn + "\n    " + line
            sReturn = sReturn + "\n\n" + line

        self.textEditor.insert('end', "\n")
        self.textEditor.insert('end', sReturn)
        self.root.destroy()

    def move(self, event, iRowIndex):
        AutoSuggestions = self.autocompl.generate_completions(self.StepDetail[iRowIndex].get(), self.new_df,
                                                              self.model_tf, self.tfidf_matrice)

        popup = tk.Menu(self.scrollFrame.viewPort)

        popup.add_command(label=AutoSuggestions[0], command=lambda: self.AddStepDef(AutoSuggestions[0],
                                                                                     self.StepDetail[iRowIndex]))
        popup.add_command(label=AutoSuggestions[1], command=lambda: self.AddStepDef(AutoSuggestions[1],
                                                                                     self.StepDetail[iRowIndex]))
        popup.add_command(label=AutoSuggestions[2], command=lambda: self.AddStepDef(AutoSuggestions[2],
                                                                                     self.StepDetail[iRowIndex]))
        try:
            popup.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            popup.grab_release()

    def move2(self, event, iRowIndex):
        AutoSuggestions = self.autocompl.generate_completions(self.StepDetail[iRowIndex].get(), self.new_df,
                                                              self.model_tf, self.tfidf_matrice)

        popup = tk.Menu(self.scrollFrame.viewPort)

        popup.add_command(label=AutoSuggestions[0], command=lambda: self.AddStepDef(AutoSuggestions[0],
                                                                                     self.AutoSuggestion[iRowIndex]))
        popup.add_command(label=AutoSuggestions[1], command=lambda: self.AddStepDef(AutoSuggestions[1],
                                                                                     self.AutoSuggestion[iRowIndex]))
        popup.add_command(label=AutoSuggestions[2], command=lambda: self.AddStepDef(AutoSuggestions[2],
                                                                                     self.AutoSuggestion[iRowIndex]))
        try:
            popup.tk_popup(event.x_root, event.y_root+20, 0)
        finally:
            popup.grab_release()

    def AddStepDef(self, statement, EntryElement):
        # print(statement)
        EntryElement.delete(0, 'end')
        EntryElement.insert('end', statement)

    def buttonPushed(self):
        self.scrollFrame.destroy()

    def AddDataTable(self, iIndex, title):
        DT = tk.Tk()
        DT.geometry("850x250")
        DT.title(title)
        DT.resizable(True, True)
        frame = tk.Frame(DT)
        datatableFrame = ScrollFrame(frame)

        rows = []
        for i in range(10):
            cols = []
            for j in range(13):
                e = tk.Entry(datatableFrame.viewPort, relief=tk.RIDGE, width=10)
                e.grid(row=i, column=j)
                cols.append(e)
            rows.append(cols)
            datatableFrame.place(x=20, y=230)

        tk.Button(datatableFrame.viewPort, text="Submit", bg='Light gray', fg='red',
                  command=lambda: self.ReadDataTable(DT, rows, iIndex)).grid(row=14, column=5)
        tk.Button(datatableFrame.viewPort, text="Cancel", bg='Light gray', fg='red',
                  command=lambda: self.destroyDataTable(DT)).grid(row=14, column=8)

        datatableFrame.pack(side="top", fill="both", expand=True)
        frame.pack(side="top", fill="both", expand=True)
        DT.mainloop()

    def destroyDataTable(self, frame):
        frame.destroy()

    def ReadDataTable(self, frame, table, iIndex):
        MaxRows = 0
        MaxCols = 0
        for rows in table:
            for cell in rows:
                if cell.get() != "":
                    MaxRows = MaxRows + 1
                else:
                    break
            break

        for rows in table:
            if rows[0].get() != "":
                MaxCols = MaxCols + 1
            else:
                break

        sReturn = ""
        for iRow in range(MaxRows):
            sColumn = "|"
            if sReturn != "":
                sReturn = sReturn + "\n"

            for iCol in range(MaxCols):
                sColumn = sColumn + table[iRow][iCol].get() + "|"
            sReturn = sReturn + sColumn

        if str(iIndex) == "Examples":
            self.sExamplesTable = tk.Text(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10), width=54,
                                               height=3)
            self.sExamplesTable.insert('end', "Examples:\n" + sReturn)
            self.sExamplesTable.grid(row=4, column=2, columnspan=6)

        else:
            # print("Data table index " + str(iIndex))
            self.StepDTTable[int(iIndex)] = tk.Text(self.scrollFrame.viewPort, bg="white", font=('TkDefaultFont', 10), width=54,
                                               height=2)
            self.StepDTTable[int(iIndex)].insert('end', sReturn)
            self.StepDTTable[int(iIndex)].grid(row=int((iIndex * 2 + 6) + 1), column=2, columnspan=6)
        frame.destroy()

    def insertEmptyRow(self, frame, iRow, iCol):
        label = tk.Label(frame)
        label.grid(column=iCol, row=iRow)

    def addAnewStep(self, frame):
        list = []
        if len(self.StepType) == 0:
            iNewIndex = 0
        else:
            for key in self.StepType.keys():
                list.append(key)
            iNewIndex = list[-1] + 1
        # print("New Step" + str(iNewIndex))
        self.StepType[iNewIndex] = self.GetStepType(frame, 3)
        self.StepType[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=1)
        self.StepDetail[iNewIndex] = tk.Entry(frame, bg="white", font=('TkDefaultFont', 10), width=54)
        self.StepDetail[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=2, columnspan=3)
        # self.StepDetail[iNewIndex].insert('end', iNewIndex)
        self.StepDetail[iNewIndex].bind('<Down>', lambda event, arg=iNewIndex: self.move(event, arg))
        self.addDeleteBtn(frame, int(iNewIndex * 2 + 6), 7)
        self.addDataTableBtn(self.scrollFrame.viewPort, int(iNewIndex * 2 + 6), 8)
        self.addMoveBtn(self.scrollFrame.viewPort, int(iNewIndex * 2 + 6), 9)

        self.AutoSuggestion[iNewIndex] = tk.Entry(self.scrollFrame.viewPort,
                                                     bg="white", font=('TkDefaultFont', 10), width=54)
        self.AutoSuggestion[iNewIndex].bind('<Down>', lambda event, arg=iNewIndex: self.move2(event, arg))
        self.AutoSuggestion[iNewIndex].grid(row=int(iNewIndex * 2 + 6), column=10, columnspan=3)

        self.insertEmptyRow(frame, int((iNewIndex * 2 + 6) + 1), 1)
        self.AddBtn.grid(row=int((iNewIndex * 2 + 6) + 2), column=6)
        self.insertEmptyRow(frame, int((iNewIndex * 2 + 6) + 3), 1)
        self.tags.grid(row=int((iNewIndex * 2 + 6) + 4), column=1, columnspan=4)
        self.insertEmptyRow(frame, int((iNewIndex * 2 + 6) + 5), 1)
        self.SubmitBtn.grid(row=int((iNewIndex * 2 + 6) + 6), column=2)
        self.CancelBtn.grid(row=int((iNewIndex * 2 + 6) + 6), column=4)

    def scenarioTypeSelected(self, event, scenarioType):
        # print(scenarioType.get())
        if scenarioType.get() == "Scenario Outline":
            self.AddDataTable("Examples","Examples table")
        else:
            try:
                self.sExamplesTable.destroy()
            except:
                pass
            # scenarioWindow.geometry("480x300")
            # datatableFrame.destroy()
            # self.datatableFrame = Frame(scenarioWindow, width=54, height=10)
            # SaveBtn.place(x=150, y=250, anchor=NW)
            # CancelBtn.place(x=250, y=250, anchor=NW)

    def deleteStep(self, frame, iRow):
        iRow = int(iRow)
        self.StepType[iRow].destroy()
        self.StepDetail[iRow].destroy()
        self.StepDelete[iRow].destroy()
        self.StepDTButton[iRow].destroy()
        self.StepMoveButton[iRow].destroy()
        self.AutoSuggestion[iRow].destroy()
        list = []
        for key in self.StepType.keys():
            list.append(int(key))

        self.StepType.pop(iRow)
        self.StepDetail.pop(iRow)
        self.StepDelete.pop(iRow)
        self.StepDTButton.pop(iRow)
        self.StepMoveButton.pop(iRow)
        self.AutoSuggestion.pop(iRow)
        if iRow in self.StepDTTable:
            self.StepDTTable[iRow].destroy()
            self.StepDTTable.pop(iRow)
        self.RepositionElements(frame)

    def RepositionElements(self, frame):
        sKeys = self.StepType.keys()

        for iNewIndex in sKeys:
            # print("Repositioning " + str(iNewIndex))
            self.StepType[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=1)
            self.StepDetail[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=2, columnspan=3)
            self.insertEmptyRow(frame, (iNewIndex * 2 + 6) + 1, 1)
            self.AddBtn.grid(row=(iNewIndex * 2 + 6) + 2, column=6)
            self.StepDelete[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=7)
            self.StepDTButton[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=8)
            self.StepMoveButton[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=9)
            self.AutoSuggestion[iNewIndex].grid(row=(iNewIndex * 2 + 6), column=10, columnspan=3)
            self.insertEmptyRow(frame, (iNewIndex * 2 + 6) + 3, 1)
            self.tags.grid(row=(iNewIndex * 2 + 6) + 4, column=1, columnspan=4)
            self.insertEmptyRow(frame, (iNewIndex * 2 + 6) + 5, 1)
            self.SubmitBtn.grid(row=(iNewIndex * 2 + 6) + 6, column=2)
            self.CancelBtn.grid(row=(iNewIndex * 2 + 6) + 6, column=4)

    def addDeleteBtn(self, frame, iRow, iCol):
        list = []
        if len(self.StepType) == 0:
            iNewIndex = 0
        else:
            for key in self.StepType.keys():
                list.append(key)
            iNewIndex = list[-1] + 1

        self.StepDelete[iNewIndex - 1] = tk.Button(self.scrollFrame.viewPort, image=self.sImages['DeleteIcon'] ,
                                                   command=lambda: self.deleteStep(frame, (iRow - 6) / 2))
        self.StepDelete[iNewIndex - 1].grid(row=iRow, column=iCol)

    def addDataTableBtn(self, frame, iRow, iCol):
        list = []
        if len(self.StepType) == 0:
            iNewIndex = 0
        else:
            for key in self.StepType.keys():
                list.append(key)
            iNewIndex = list[-1] + 1

        self.StepDTButton[iNewIndex - 1] = tk.Button(self.scrollFrame.viewPort, image=self.sImages['custom_datagrid'] ,
                                                     command=lambda: self.AddDataTable((iRow - 6) / 2,"DataTable"))
        self.StepDTButton[iNewIndex - 1].grid(row=iRow, column=iCol)

    def addMoveBtn(self, frame, iRow, iCol):
        list = []
        if len(self.StepType) == 0:
            iNewIndex = 0
        else:
            for key in self.StepType.keys():
                list.append(key)
            iNewIndex = list[-1] + 1

        self.StepMoveButton[iNewIndex - 1] = tk.Button(self.scrollFrame.viewPort, image=self.sImages['move_left'])
        self.StepMoveButton[iNewIndex - 1].grid(row=iRow, column=iCol)

    def GetStepType(self, scenarioWindow, sData):
        stepType = ttk.Combobox(scenarioWindow, state='readonly', width=12, height=2)
        stepType['values'] = ('Given',
                              'When',
                              'Then',
                              'And')
        if sData == "Given":
            stepType.current(0)
        elif sData == "When":
            stepType.current(1)
        elif sData == "Then":
            stepType.current(2)
        elif sData == "And":
            stepType.current(3)
        return stepType


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("580x400")
    root.title("NewScenario")
    root.resizable(False, True)
    # Example(root).pack(side="top", fill="both", expand=True)
    myGUI = NewScenario(root, "C:\\Users\\vamsi\\Documents\\MetaData.xml", None)
    myGUI.CreateWindow()
    root.mainloop()
