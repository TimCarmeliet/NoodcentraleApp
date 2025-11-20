import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from controllers.NoodcentraleAppController import NoodcentraleAppController
from view.PersonenView import PersonenView
from view.ScenarioView import ScenarioView
from view.CombineerView import CombineerView
from view.StappenView import StappenView

from tkinter import simpledialog

#GUI moet de controller kennen, niet het model
class NoodcentraleApp():

    def __init__(self, naam_app:str, controller:NoodcentraleAppController):
        self.__controller = controller
        self.__root = tk.Tk()
        self.__root.title(str(naam_app))
        self.__root.geometry("800x600")
        self.build_gui()
    
    #CONTROLLER
    def get_controller(self):
        return self.__controller

    #HOOFDVENSTER
    def get_root(self):
        return self.__root

    def open_config_frame(self):
         #Start venster dicht doen
        self.start_frame.pack_forget()
        #Config venster openen
        self.config_frame.pack(side="top", fill="both", expand=True)
    
    def close_config_frame(self):
        #Config venster dicht doen
        self.config_frame.pack_forget()
        #Start venster openen
        self.start_frame.pack(side="top", fill="both", expand=True)     
        self.refresh_start_scenario_buttons() 

    def on_tab_changed(self, event):
        selected_tab = event.widget.tab(event.widget.select(), "text")
  
        if selected_tab == "Personen":
            self.get_controller().activate_controller("personen")
        if selected_tab == "Scenario's":
            self.get_controller().activate_controller("scenario")
        if selected_tab == "Koppel personen aan scenario's":
            self.get_controller().activate_controller("combineer")
        if selected_tab == "Voeg stappen toe aan scenario's":
            self.get_controller().activate_controller("stappen")

    def start_scenario(self, scenario_id):
        self.get_controller().activate_controller("stappen")
        stappen = self.get_controller().get_active_controller().get_stappen_from_scenario(scenario_id)
        print(stappen)

        if len(stappen) == 0:
            messagebox.showerror("Error", f"Geen stappen gevonden voor dit scenario")
        else:
            locatie = "" #voor mogelijks een locatie in op te slaan doorheen de diverse stappen
            locatie_nodig_in_bericht = False
            for stap in stappen:
                if stap[2] == "locatie":
                    locatie = simpledialog.askstring("Locatie", str(stap[4]))
                    locatie_nodig_in_bericht = True
                if stap[2] == "stuur":
                    if locatie_nodig_in_bericht:
                        inhoud_bericht = str(stap[4])
                        inhoud_bericht = inhoud_bericht.replace("XXX.", locatie + ".")
                        locatie_nodig_in_bericht = False
                    else:
                        inhoud_bericht = str(stap[4])
                        
                    messagebox.showinfo("Bericht", str(inhoud_bericht))

            


    def refresh_start_scenario_buttons(self):
        # oude knoppen opruimen
        for oude_scenarios in self.scenario_container.winfo_children():
            oude_scenarios.destroy()
        
        beschikbare_scenarios = self.get_controller().get_scenarios()
        if not beschikbare_scenarios:
            tk.Label(self.scenario_container, text="Geen scenario's gevonden.").grid(row=1, column=1)
 
        else:
            self.scenario_images = []
            
            row_teller = 0
            col_teller = 0
            for scenario in beschikbare_scenarios:                
                
                scenario_id, naam, icoon = scenario

                # Pad naar icoonbestand in dezelfde map als dit bestand
                icoon_pad = os.path.join(os.path.dirname(__file__), icoon)
                
                # Controleer of bestand bestaat
                if os.path.exists(icoon_pad):
                    img = Image.open(icoon_pad).resize((64, 64))
                    img_tk = ImageTk.PhotoImage(img)
                else:
                    img_tk = ImageTk.PhotoImage(Image.new("RGB", (64, 64), color="gray"))

                self.scenario_images.append(img_tk)


                btn = tk.Button(
                self.scenario_container,
                text=naam,
                image=img_tk,
                compound="top", #afbeelding boven tekst
                width=120,
                height=100,
                command=lambda s_id=scenario_id: self.start_scenario(s_id)
                )
                btn.grid(row=row_teller, column=col_teller, padx=10, pady=10)
                if col_teller == 2:
                    col_teller = 0
                    row_teller = row_teller + 1
                else:
                    col_teller= col_teller + 1



    def build_gui(self):

        #************
        #MENU frame
        #************
        self.menu_frame = tk.Frame(self.get_root())
        bestandspad = os.path.join(os.path.dirname(__file__), "instellingen.png")
        self.instellingen_img = ImageTk.PhotoImage(Image.open(bestandspad).resize((20, 20)))
        tk.Button(self.menu_frame, image=self.instellingen_img, command=self.open_config_frame).pack(anchor="ne", padx=10, pady=10)
        #tk.Button(start_frame, image=self.instellingen_img, command=self.open_config_frame).place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

        #Menu_frame toevoegen aan het hoofvenster
        self.menu_frame.pack(side="top", fill="x") #horizontaal vullen, bovenaan

        #************
        #START frame
        #************
        self.start_frame = tk.Frame(self.get_root())
        tk.Label(self.start_frame, text="Overzicht scenario's", font=("Arial", 12)).pack(pady=5)
        
        self.scenario_container = tk.Frame(self.start_frame)
        self.scenario_container.pack(pady=10)    

        self.refresh_start_scenario_buttons()

        self.start_frame.pack(side="top", fill="both", expand=True)


        #************
        #CONFIG frame
        #************
        self.config_frame = tk.Frame(self.get_root())

        #Tabbladen toevoegen voor de diverse config handelingen
        self.notebook = ttk.Notebook(self.config_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #Tabblad om personen te beheren
        self.person_frame = PersonenView(self.notebook, self.get_controller())
        self.notebook.add(self.person_frame, text="Personen")

        #Tabblad om scenario's te beheren
        self.scenario_frame = ScenarioView(self.notebook, self.get_controller())
        self.notebook.add(self.scenario_frame, text="Scenario's")

        #Tabblad om de koppeling te leggen
        self.combineer_frame = CombineerView(self.notebook, self.get_controller())
        self.notebook.add(self.combineer_frame, text="Koppel personen aan scenario's")

        self.stappen_frame = StappenView(self.notebook, self.get_controller())
        self.notebook.add(self.stappen_frame, text="Voeg stappen toe aan scenario's")

        #Tabbladen toevoegen aan het config frame
        self.notebook.pack(fill="both", expand=True)

        #Event binden aan notebook zodat je we de active controller daarmee in lijn kunnen brengen
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
      
        tk.Button(self.config_frame, text="sluit config", command=self.close_config_frame).pack(side="bottom", padx=10, pady=10)
   


