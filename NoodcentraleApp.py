from view.NoodcentraleAppView import NoodcentraleApp 
from controllers.NoodcentraleAppController import NoodcentraleAppController
from NoodcentraleAppModel import NoodcentraleAppModel

if __name__ == "__main__":
    DB = "noodcentrale.db"

    model = NoodcentraleAppModel(DB)
    nood_controller = NoodcentraleAppController(model)
    nood_app = NoodcentraleApp("Noodcentrale Appl Demo 1", nood_controller)
    nood_app.get_root().mainloop()


