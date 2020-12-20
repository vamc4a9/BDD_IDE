import tkinter as tk
from configparser import ConfigParser
from tkinter import *
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
from tkinter import messagebox

from autocompleter import Autocompleter
from xml import cXml

class AddStepDefinition:
    def __init__(self, root, filename, sOldXPath):
        self.sOldXPath = sOldXPath
        self.filename = filename
        self.root = root
        self.myFont1 = font.Font(family='TkDefaultFont', size=14, weight='bold')
        self.myFont2 = font.Font(family='TkDefaultFont', size=10, weight='bold')
        self.myFont3 = font.Font(family='TkDefaultFont', size=10)
        self.myFont4 = font.Font(family='TkDefaultFont', size=13)
        self.entry = None
        self.R1 = None
        self.R2 = None
        self.extdata = None
        self.Outputtext = None
        self.OptionList = None
        self.parametertext = None
        self.instructionstext = None
        self.ConfirmationMessage = None
        self.SubmitBtn = None
        self.DeleteBtn = None
        self.StepDefVar = StringVar()
        self.StepDefVar.set("Welcome To Add Step Definition Window")
        self.info = tk.PhotoImage(file='./icons/info_icon.png', master=self.root)
        self.infobutton = self.info.subsample(4, 4)

    def CreateUI(self):

        # define font
        canvas = tk.Canvas(self.root, height=568, width=898)
        canvas.pack()

        # background_image = tk.PhotoImage(file='BG.PNG')
        # background_label = tk.Label(root, image=background_image)
        # background_label.place(x=0, y=0)

        frame = tk.Frame(self.root, bd=2, bg='#d9ecd0')
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # statusbar = Label(frame, textvariable=self.StepDefVar, bd=1, relief=SUNKEN, anchor=W)
        # statusbar.pack(side=BOTTOM, fill=X)

        # width=22, height=22
        Button(frame, image=self.infobutton, command=lambda: self.statement_info_function()).place(
            relx=0.53, rely=0.2, relwidth=0.025, relheight=0.04)

        # width=22, height=22
        Button(frame, image=self.infobutton, command=self.datatable_info_function).place(
            relx=0.41, rely=0.3, relwidth=0.025, relheight=0.04)

        # width=22, height=22
        Button(frame, image=self.infobutton, command=self.parameters_info_function).place(
            relx=0.53, rely=0.5, relwidth=0.025, relheight=0.04)

        # width=22, height=22
        Button(frame, image=self.infobutton, command=self.instructions_info_function).place(
            relx=0.53, rely=0.65, relwidth=0.025, relheight=0.04)

        if self.sOldXPath == '':
            label = tk.Label(frame, text="Add Step Definition", bg='#d9ecd0')
            label.place(relx=0.4, rely=0.08, relwidth=0.23, relheight=0.05)
            label['font'] = self.myFont1
        else:
            label = tk.Label(frame, text="Edit/Delete Step Definition", bg='#d9ecd0')
            label.place(relx=0.4, rely=0.08, relwidth=0.30, relheight=0.05)
            label['font'] = self.myFont1

        label = tk.Label(frame, text="Statement", bg="#d9ecd0", anchor=W)
        label.place(relx=0.11, rely=0.2, relwidth=0.13, relheight=0.045)
        label['font'] = self.myFont2

        self.entry = tk.Entry(frame, bg="white", font=('TkDefaultFont', 10))
        self.entry.place(relx=0.22, rely=0.2, relwidth=0.3, relheight=0.045)

        label = tk.Label(frame, text="Data Table?", bg='#d9ecd0', anchor=W)
        label.place(relx=0.11, rely=0.3, relwidth=0.13, relheight=0.045)
        label['font'] = self.myFont2

        self.extdata = StringVar()
        self.extdata.set("Yes")
        self.R1 = Radiobutton(frame, text="Yes", variable=self.extdata, value='Yes', bg='#d9ecd0',
                         font=('TkDefaultFont', 10))
        self.R1.place(relx=0.22, rely=0.3, relwidth=0.1, relheight=0.045)

        self.R2 = Radiobutton(frame, text="No", variable=self.extdata, value='No', bg='#d9ecd0',
                         font=('TkDefaultFont', 10))
        self.R2.place(relx=0.3, rely=0.3, relwidth=0.1, relheight=0.045)

        label = tk.Label(frame, text="Category", bg='#d9ecd0', anchor=W)
        label.place(relx=0.11, rely=0.4, relwidth=0.13, relheight=0.045)
        label['font'] = self.myFont2

        sKeys = self.read_config("XML", "keys")
        self.OptionList = ttk.Combobox(frame, state='readonly')
        self.OptionList['values'] = sKeys.split(",")
        self.OptionList.current(0)

        self.OptionList.place(relx=0.22, rely=0.4, relwidth=0.3, relheight=0.045)

        label = tk.Label(frame, text="Parameters", bg='#d9ecd0', anchor=W)
        label.place(relx=0.11, rely=0.5, relwidth=0.13, relheight=0.045)
        label['font'] = self.myFont2

        self.parametertext = ScrolledText(frame, font=('TkDefaultFont', 10))
        self.parametertext.place(relx=0.22, rely=0.5, relwidth=0.3, relheight=0.1)

        label = tk.Label(frame, text="Instructions", bg='#d9ecd0', anchor=W)
        label.place(relx=0.11, rely=0.65, relwidth=0.13, relheight=0.045)
        label['font'] = self.myFont2

        self.instructionstext = ScrolledText(frame, font=('TkDefaultFont', 10))
        self.instructionstext.place(relx=0.22, rely=0.65, relwidth=0.3, relheight=0.2)

        self.Outputtext = ScrolledText(frame)
        self.Outputtext.place(relx=0.58, rely=0.2, relwidth=0.3, relheight=0.65)

        if self.sOldXPath == '':
            self.SubmitBtn = tk.Button(frame, text="Submit", bg='Light gray', fg='red',
                               command=lambda: self.addDatatoXML())
            self.SubmitBtn.place(relx=0.34, rely=0.89, relwidth=0.13, relheight=0.045)
            self.SubmitBtn['font'] = self.myFont3
        else:
            self.DeleteBtn = tk.Button(frame, text="Update", bg='Light gray', fg='red',
                               command=lambda: self.UpdateXML())
            self.DeleteBtn.place(relx=0.34, rely=0.89, relwidth=0.13, relheight=0.045)
            self.DeleteBtn['font'] = self.myFont3

        if self.sOldXPath == '':
            button = tk.Button(frame, text="Reset", bg='Light gray', fg='red', command=lambda: self.reset())
            button.place(relx=0.51, rely=0.89, relwidth=0.13, relheight=0.045)
            button['font'] = self.myFont3
        else:
            button = tk.Button(frame, text="Delete", bg='Light gray', fg='red', command=lambda: self.delete())
            button.place(relx=0.51, rely=0.89, relwidth=0.13, relheight=0.045)
            button['font'] = self.myFont3

        self.ConfirmationMessage = tk.Label(frame, text="", bg='#d9ecd0', anchor=W)
        self.ConfirmationMessage.place(relx=0.30, rely=0.95, relwidth=0.40, relheight=0.05)
        self.ConfirmationMessage['font'] = self.myFont1

    def read_config(self, sCollection, sKey):
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object[sCollection]
        return userinfo[sKey]

    def delete(self):
        xml = cXml(self.filename)
        xml.RemoveNode(self.sOldXPath)
        self.reset()
        messagebox.showwarning('Message', 'step definition is deleted successfully', parent=self.root)
        self.root.destroy()
        # self.ConfirmationMessage.config(text="step definition is deleted successfully")

    def UpdateXML(self):
        xml = cXml(self.filename)
        xml.RemoveNode(self.sOldXPath)
        self.Outputtext.delete("1.0", END)
        if self.AddToXML():
            messagebox.showwarning('Message', 'Step definition is updated successfully', parent=self.root)
            self.sOldXPath = "//StepDefinition[@Statement='"+self.entry.get().strip()+"']"

    def AddToXML(self):
        xml = cXml(self.filename)
        sData = xml.ReadNode("//StepDefinition[@Statement='"+self.entry.get().strip()+"']")
        if len(sData) > 0:
            messagebox.showwarning('Warning Message', 'There is an existing step definition with same statement'
                                   , parent=self.root)
            return False
        else:
            xml.insertNode("//" + self.OptionList.get(), self.entry.get().strip(),
                           self.parametertext.get("1.0", tk.END).strip(),
                           self.GetRadiobutton(), self.instructionstext.get("1.0", tk.END).strip())

            self.Outputtext.insert('end', self.GetOutput())
            return True

    def reset(self):
        self.entry.delete(0, END)
        self.parametertext.delete("1.0", END)
        self.instructionstext.delete("1.0", END)
        self.extdata.set("Yes")
        self.OptionList.current(0)
        self.Outputtext.delete("1.0", END)
        self.ConfirmationMessage.config(text="")
        if self.sOldXPath == '':
            self.SubmitBtn["state"] = "normal"
        else:
            self.DeleteBtn["state"] = "normal"

    def GetRadiobutton(self):
        if self.extdata.get() == 'No':
            return "No"
        else:
            return "Yes"

    def GetOutput(self):
        return "Statement: " + self.entry.get().strip()\
               + "\n\nCategory: " + self.OptionList.get() \
               + "\n\nExternalData: " + self.GetRadiobutton() \
               + "\n\nParameters: " + self.parametertext.get("1.0", tk.END).strip() \
               + "\n\nInstructions: " + self.instructionstext.get("1.0", tk.END).strip()

    def addDatatoXML(self):
        if self.entry.get() == '':
            messagebox.showwarning('Warning Message', 'Statement should not be empty', parent=self.root)
        elif self.checkParameters():
            self.autocompl = Autocompleter()
            df = self.autocompl.import_xml(self.filename)
            self.new_df = self.autocompl.process_data(df)
            self.model_tf, self.tfidf_matrice = self.autocompl.calc_matrice(self.new_df)
            AutoSuggestions = self.autocompl.generate_completions(self.entry.get().strip(), self.new_df,
                                                                  self.model_tf, self.tfidf_matrice)

            sMessage = "Please check if one of the below can perform your operation\n"
            for suggestion in AutoSuggestions:
                sMessage = sMessage + "\n" + suggestion

            sMessage = sMessage + "\n\nIf you click on Yes, new step definition will not get added"
            answer = messagebox.askyesno('Auto Suggestions Based on Existing Step Definitions', sMessage,
                                         parent=self.root)
            # print(answer)
            if not answer:
                if self.AddToXML():
                    messagebox.showwarning('Warning Message', 'Step definition is added successfully', parent=self.root)
                    self.SubmitBtn["state"] = "disabled"
        else:
            messagebox.showwarning('Warning Message', "Parameters are not in expected format."
                                                      "\nBelow is the expected format:\n"
                                                      "PartOfTheStatement==ShortDescription"
                                                      "\n\nIf multiple parameters are to be added, then each of "
                                                      "them should be in new line", parent=self.root)

    def checkParameters(self):
        if self.parametertext.get("1.0", tk.END).strip() != '':
            print(self.parametertext.get("1.0", tk.END))
            sText = self.parametertext.get("1.0", tk.END).strip()
            sStatement = self.entry.get()
            arText = sText.split("\n")
            for parameter in arText:
                if "==" in parameter:
                    arParameters = parameter.split("==")
                    if len(arParameters) == 2:
                        if arParameters[1] != '':
                            if arParameters[0] not in sStatement:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            return True
        else:
            return True

    def statement_info_function(self):
        messagebox.showinfo("Message",
                            "This is the Step defintion Name. Using BDD IDE, User can import this step definition "
                            "while creating the test scenario.", parent=self.root)

    def datatable_info_function(self):
        messagebox.showinfo("Message",
                            "This indicates to user if there is any table content to be passed below the "
                            "step definition \nFor Eg: 'Verify the below controls' statement might need below "
                            "table to be passed along with the statement: "
                            "\n|ControlName1|Displayed|"
                            "\n|ControlName2|NotDisplayed|", parent=self.root)

    def datatable_info_function(self):
        messagebox.showinfo("Message",
                            "This indicates to user if there is any table content to be passed below the step "
                            "definition. \nFor Eg: 'Verify the below controls' statement might need below table"
                            " to be passed along with the statement: "
                            "\n|ControlName1|Displayed|"
                            "\n|ControlName2|NotDisplayed|", parent=self.root)

    def parameters_info_function(self):
        messagebox.showinfo("Message",
                            "If the user parameterize the statement, when it is being added to the feature file, there "
                            "will be an additional pop up window dislayed to enter the parameter values"
                            "\nFor eg: if the Statement is 'Enter TestData in ObjectName control' "
                            "User can just add TestData and ObjectName as parameters. "
                            "Below is the format to be followed: "
                            "\n\nTestData==Enter the value to be updated in the object "
                            "\nObjectName==Enter the object name "
                            "\n\nUser needs to update both parameter name and some information regarding the parameter."
                            " It is not limited to add only 2 parameters, user can parameterize based on requirement"
                            , parent=self.root)

    def instructions_info_function(self):
        messagebox.showinfo("Message",
                            "The Information provided in 'Instructions' can help user understand the functionality "
                            "behind the statement", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = AddStepDefinition(root, "C:\\Users\\vamsi\\Documents\\MetaData.xml", '')
    app.CreateUI()
    root.mainloop()
