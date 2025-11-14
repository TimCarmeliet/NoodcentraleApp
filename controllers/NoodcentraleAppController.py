from NoodcentraleAppModel import NoodcentraleAppModel

#Controller moet het model kennen, niet de view
class NoodcentraleAppController():
    def __init__(self, model: NoodcentraleAppModel):
        self.__model = model

        #subcontrollers => personen, scenario, combineer
        self.__subcontrollers = {
            "personen" : PersonenController(model),
            "scenario" : ScenarioController(model),
            "combineer": CombineerController(model)
        }

        self.__active_controller = None
        self.activate_controller("personen")

    #MODEL
    def get_noodcentraleAppModel(self):
        return self.__model
    
    #CONTROLLERS
    def get_active_controller(self):
        return self.__active_controller

    def activate_controller(self, naam):
        if naam in self.__subcontrollers:
            self.__active_controller = self.__subcontrollers[naam]
        else:
            raise ValueError(f"Controller {naam} bestaat niet.")
    
    #DATA inladen/ophalen
    def get_data(self):
        return self.get_active_controller().data_inladen()
    
    def get_scenarios(self):
        return self.__subcontrollers["scenario"].data_inladen()
    

#PERSONEN CONTROLLER
class PersonenController():
    def __init__(self, model: NoodcentraleAppModel):
        self.__model = model
    
    #MODEL
    def get_noodcentraleAppModel(self):
        return self.__model

    #Personen
    def data_inladen(self):
        return self.get_noodcentraleAppModel().get_personen()
    
    def voeg_persoon_toe(self, naam, telefoonnummer):
        self.get_noodcentraleAppModel().add_persoon(naam, telefoonnummer)

#SCENARIO CONTROLLER
class ScenarioController():
    def __init__(self, model: NoodcentraleAppModel):
        self.__model = model
    
    #MODEL
    def get_noodcentraleAppModel(self):
        return self.__model

    #Scenarios
    def data_inladen(self):
        return self.get_noodcentraleAppModel().get_scenarios()
    
    def voeg_scenario_toe(self, naam, icoon):
        self.get_noodcentraleAppModel().add_scenario(naam, icoon)

#COMBINEER CONTROLLER
class CombineerController():
    def __init__(self, model: NoodcentraleAppModel):
        self.__model = model

    #MODEL
    def get_noodcentraleAppModel(self):
        return self.__model

    #Combinatie
    def data_inladen(self):
        return self.get_noodcentraleAppModel().get_scenario_users()
    
    def get_personen(self):
        return self.get_noodcentraleAppModel().get_personen()
    
    def get_scenarios(self):
        return self.get_noodcentraleAppModel().get_scenarios()
    
    def voeg_koppeling_toe(self, scenario_id, user_id):
        self.get_noodcentraleAppModel().add_scenario_users(scenario_id, user_id)