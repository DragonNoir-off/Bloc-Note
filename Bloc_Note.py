
# primary import
import os
import psutil
import time

# import of kivy and kivyMD
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.list import MDList, OneLineRightIconListItem, IconRightWidget
from kivymd.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

class File_class():
    file_path = "Bloc_Note/Notes"
    
    def Close_All_File():
        pid = os.getpid()
        process = psutil.Process(pid)

        for fichier in process.open_files():
            try:
                with open(fichier.path, "r") as f:
                    f.close()
                os.close(fichier.fd)
            except OSError:
                pass

class Init_Frame(MDApp):
    App = MDApp
    Last_File_Path = None
    Last_File = None
    
    def build(self):
        Init_Frame.App.root = Builder.load_file("UIX_kivy.kv")
        Init_Frame.App.theme_cls = ThemeManager()
        Init_Frame.Setup_List()
        Init_Frame.Alternate_Visibility(True)
        return Init_Frame.App.root
    
    def Alternate_Visibility(status):
        ids = Init_Frame.App.root.ids
        if status==False:
            ids.Label_MainFrame.opacity = 0
            ids.NewNote_MainFrame.opacity = 0
            ids.Separator_MainFrame.opacity = 0
            ids.List_MainFrame.opacity = 0
            ids.TextField_InputFrame.opacity = 1
            ids.TextField_InputFrame.disabled = False
            ids.SaveNote_InputFrame.opacity = 1
            ids.SaveNote_InputFrame.disabled = False
            ids.Exit_InputFrame.opacity = 1
            ids.Exit_InputFrame.disabled = False
        else:
            ids.Label_MainFrame.opacity = 1
            ids.NewNote_MainFrame.opacity = 1
            ids.Separator_MainFrame.opacity = 1
            ids.List_MainFrame.opacity = 1
            ids.TextField_InputFrame.opacity = 0
            ids.TextField_InputFrame.disabled = True
            ids.SaveNote_InputFrame.opacity = 0
            ids.SaveNote_InputFrame.disabled = True
            ids.Exit_InputFrame.opacity = 0
            ids.Exit_InputFrame.disabled = True
    
    def Create_NewNote(_):
        def save_note(self):
            input_text = Init_Frame.dialog.content_cls.text
            if input_text:
                if not os.path.exists("Bloc_Note/Notes/"+str(input_text)+".txt"):
                    file = open("Bloc_Note/Notes/"+str(input_text)+".txt", "x")
                    file.close()
                    Init_Frame.Setup_List()
                else:
                    error_message = Label(text="Une NOTE ne peux pas avoir le même nom qu'une autre NOTE", color=(1, 0, 0, 1))
                    popup = Popup(title="Erreur lors de la création de la NOTE",
                    content=error_message,
                    size_hint=(None, None), size=(500, 100))
                    popup.open()
                    
            Init_Frame.dialog.dismiss()
        
        def close_dialog(self):
            Init_Frame.dialog.dismiss()
            
        Init_Frame.dialog = MDDialog(
            title="Saisir le nom de la note",
            type="custom",
            content_cls=MDTextField(
                hint_text="Entrez le nom de la note ici",
                size_hint=(1, None),
                height="150dp"
            ),
            buttons=[
                MDRaisedButton(
                    text="Annuler", 
                    on_release=close_dialog
                ),
                MDRaisedButton(
                    text="Valider", 
                    on_release=save_note
                ),
            ],
        )
        Init_Frame.dialog.open()
    
    def Setup_List():
        Init_Frame.App.root.ids.File_List.clear_widgets()
            
        for i in os.listdir(File_class.file_path):
            File_Name = os.path.splitext(i)[0]
            Button_Data = OneLineRightIconListItem(
                text=File_Name,
                on_release=Init_Frame.File_Selected,
                size_hint_x=0.2,
                id=File_Name
            )
            
            Rename_Icon = IconRightWidget(icon="pencil", on_release=Init_Frame.Rename_File, id=File_Name)
            Delete_Icon = IconRightWidget(icon="delete", on_release=Init_Frame.File_Delete, id=File_Name)
            
            Button_Data.add_widget(Rename_Icon)
            Button_Data.add_widget(Delete_Icon)
            
            Init_Frame.App.root.ids.File_List.add_widget(Button_Data)
    
    def File_Selected__Save_NewText(self):
        input_text = Init_Frame.App.root.ids.TextField_InputFrame.text
        file = open(Init_Frame.Last_File_Path, "w")
        file.write(input_text)
        file.close()
        Init_Frame.File_Selected__Exit_InputFrame(None)
        Init_Frame.Last_File.close()
        
    def File_Selected__Exit_InputFrame(self):
        Init_Frame.App.root.ids.TextField_InputFrame.text = ""
        Init_Frame.Alternate_Visibility(True)
    
    def File_Selected(instance):
        Init_Frame.Last_File_Path = "Bloc_Note/Notes/"+str(instance.id)+".txt"
        Init_Frame.Last_File = open(Init_Frame.Last_File_Path, "r+")
        
        Init_Frame.Alternate_Visibility(False)
        
        Init_Frame.App.root.ids.TextField_InputFrame.text = Init_Frame.Last_File.read()
    
    def Rename_File(instance):
        def Rename(self):
            input_text = Init_Frame.dialog.content_cls.text
            if input_text:
                if not os.path.exists("Bloc_Note/Notes/"+str(input_text)+".txt"):
                    PreviousFile = open("Bloc_Note/Notes/"+str(instance.id)+".txt", "r", encoding="utf-8")
                    file = open("Bloc_Note/Notes/"+str(input_text)+".txt", "w")
                    file.write(PreviousFile.read())
                    
                    File_class.Close_All_File()
                    
                    time.sleep(2)
                    
                    os.remove("Bloc_Note/Notes/"+str(instance.id)+".txt")
                    Init_Frame.Setup_List()
                else:
                    error_message = Label(text="Une NOTE ne peux pas avoir le même nom qu'une autre NOTE", color=(1, 0, 0, 1))
                    popup = Popup(title="Erreur lors de la création de la NOTE",
                    content=error_message,
                    size_hint=(None, None), size=(500, 100))
                    popup.open()
                    
            Init_Frame.dialog.dismiss()
        
        def close_dialog(self):
            Init_Frame.dialog.dismiss()
            
        Init_Frame.dialog = MDDialog(
            title="Saisir un nouveau nom de note",
            type="custom",
            content_cls=MDTextField(
                hint_text="Entrer le nouveau nom de la note ici",
                size_hint=(1, None),
                height="150dp"
            ),
            buttons=[
                MDRaisedButton(
                    text="Annuler", 
                    on_release=close_dialog
                ),
                MDRaisedButton(
                    text="Valider", 
                    on_release=Rename
                ),
            ],
        )
        Init_Frame.dialog.open()
        
    def File_Delete(instance):
        def close_dialog(self):
            Init_Frame.dialog.dismiss()
            
        def Erase_Note(self):
            File_Path = "Bloc_Note/Notes/"+str(instance.id)+".txt"
            
            os.remove(File_Path)
            Init_Frame.Setup_List()
            close_dialog(None)
        
        Init_Frame.dialog = MDDialog(
            title="Double Validation",
            type="custom",
            text="Are you sure you want to delete "+str(instance.id)+" NOTE ?",
            buttons=[
                MDRaisedButton(
                    text="Annuler", 
                    on_release=close_dialog
                ),
                MDRaisedButton(
                    text="Valider", 
                    on_release=Erase_Note
                ),
            ],
        )
        Init_Frame.dialog.open()
    
Init_Frame().run()
