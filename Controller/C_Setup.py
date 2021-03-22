from pubsub import pub

from View import V_Setup
from data_manager import Data_manager
from Model.pressure_image import Pressure_img
from Controller import C_Metadata, C_ImagePreSegmentation, C_ImageSegmentation
from Model import M_MetadataManager, M_ImageReader

class ControllerSetup:

    def __init__(self, parent):
        self.parent = parent
        self.model_reader = M_ImageReader.ImageReader()
        self.model_metadata = M_MetadataManager.MetadataManager()
        self.view = V_Setup.ViewSetup(parent)
        self.data_manager = Data_manager()
        self.pre_processing = None
        self.processing = None
        C_Metadata.ControllerMetadata(self.model_metadata, self.view)

        pub.subscribe(self.button_1_pressed, "BUTTON_1_PRESSED")
        pub.subscribe(self.button_2_pressed, "BUTTON_2_PRESSED")
        pub.subscribe(self.button_3_pressed, "BUTTON_3_PRESSED")
        pub.subscribe(self.load_image, "LOAD_IMAGE")
        pub.subscribe(self.image_loaded, "IMAGE_LOADED")

    def button_1_pressed(self):
        """
        Prints that button_1 from view has been pressed.
        """

        print("controller - Botó 1!")

    def button_2_pressed(self):
        """
        Prints that button_2 from view has been pressed and calls the function.
        load_data from Data_manager.
        """

        print("controller - Botó 2!")
        self.data_manager.load_data()

    def button_3_pressed(self, data):
        """
        Prints that button_3 from view has been pressed.
        Calls the functions to check metadata and images before saving.
        Parameters
        ----------
        data : list
           a list with all the metadata field's information written by the user
        """

        print("controller - Botó 3!")
        try:
            if self.pressure_img.loaded:
                if self.pressure_img.processed:
                    self.model_metadata.getData(data)
                else:
                    self.view.popupmsg("És necessari processar la imatge.")
            else:
                self.view.popupmsg("És necessari carregar una imatge")
        except:
            self.view.popupmsg("És necessari carregar una imatge")

    def load_image(self):
        """
        Calls the function to load a pressure injury's image.
        WARNING: For optimal visualization, images must be '560x390'
        """

        print("controller - load imatge")

        self.pressure_img.path = self.model_reader.carregar_imatge()

    def image_loaded(self, image_original, image_tk):
        """
        Defines a Pressure_img object and saves its image.
        Calls the update_image from View to update the label with the loaded image.
        Calls the function from View to show "process" button.
        Parameters
        ----------
        image_tk : PIL Image
           image ready to be loaded in a label
        """
        self.pressure_img = Pressure_img()
        self.pressure_img.img_origin = image_original
        self.pressure_img.loaded = True
        self.view.processing.update_image(image_tk)
        self.view.processing.botoImg()
        self.pre_processing = C_ImagePreSegmentation.ControllerImagePreSegmentation(self.view, self.pressure_img)
        self.processing = C_ImageSegmentation.ControllerImageSegmentation(self.view, self.pressure_img)