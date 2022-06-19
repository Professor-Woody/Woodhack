import tkinter as tk
from tkinter import ttk
import json

class App:
    def __init__(self):
        root = tk.Tk()
        root.title('Entity Creator')

        frame = tk.Frame(root)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        label = tk.Label(frame, text="Name")
        label.grid(column=0, row=0)

        self.nameEntry = tk.Entry(frame)        
        self.nameEntry.grid(column=1, row=0)


        label = tk.Label(frame, text="Graphic")
        label.grid(column=0, row=1)

        self.charEntry = tk.Entry(frame)        
        self.charEntry.grid(column=1, row=1)


        label = tk.Label(frame, text="HP")
        label.grid(column=0, row=2)
        
        self.hpEntry = tk.Entry(frame) 
        self.hpEntry.grid(column=1, row=2)       
        

        label = tk.Label(frame, text="Light Radius")
        label.grid(column=0, row=3)
        
        self.lightEntry = tk.Entry(frame) 
        self.lightEntry.grid(column=1, row=3)       
        

        submitButton = ttk.Button(frame, text="Create", command=self.create)
        submitButton.grid(column=1, row=4)
        

        frame2 = tk.Frame(root)
        self.resultTextBox = tk.Text(frame2)
        self.resultTextBox.pack()


        frame.pack(side=tk.LEFT)
        frame2.pack()

        root.mainloop()

    def create(self, evt=None):
        entityName = self.nameEntry.get()
        hp = int(self.hpEntry.get())
        radius = int(self.lightEntry.get())
        char = self.charEntry.get()


        result = {}          
        result["name"] = entityName
        result["components"] = []
        result["components"].append({"type": "Position"})
        result["components"].append({"type": "Collision"})
        result["components"].append({"type": "Stats", "properties": {"hp": hp}})
        result["components"].append({"type": "Initiative"})
        result["components"].append({"type": "Render", "properties": {"entityName": entityName, "char": char}})
        if radius:
            result["components"].append({"type": "Light", "properties": {"radius": radius}})        

        output = json.dumps(result)
        self.resultTextBox.delete(1.0, "end")
        self.resultTextBox.insert(1.0, output)

        

if __name__ == "__main__":
    app = App()

