import shelve
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

from classes import Car
#from screenlogspage import LogsPage

class CarPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.car = None
        self.bind(size=self.update_background, pos=self.update_background)
        with self.canvas.before:
            self.bg_color = Color(0.05, 0.1, 0.2, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
    
    def update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def display_car_info(self, car):
        self.car =car
        self.clear_widgets()

        ####Information label
        detail_label =Label(
            text=f'ID: {car.id}\nMake: {car.make}\nModel: {car.model}\nYear: {car.year}\nMileage: {car.mileage}\nName: {car.name}',
            size_hint=(0.8,0.4),
            pos_hint={'x':0.1,'y':0.5}
        )
        self.add_widget(detail_label)

        ###Delete Button
        delete_button = Button(text='Delete Car', size_hint=(0.33,0.1), pos_hint={'x':0.0,'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        delete_button.bind(on_press=self.show_delete_confirmation)
        self.add_widget(delete_button)

        ###Edit Button
        edit_button = Button(text='Edit Details', size_hint=(0.33, 0.1), pos_hint={'x':0.33, 'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        edit_button.bind(on_press=self.show_edit_car_popup)
        self.add_widget(edit_button)

        ###View Logs Button
        view_logs_button = Button(text='View Logs', size_hint=(0.34,0.1), pos_hint={'x':0.66,'y':0.0},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        view_logs_button.bind(on_press=lambda instance:self.open_logs_page())
        self.add_widget(view_logs_button)

        ###Back Button
        back_button = Button(text='<-', size_hint=(0.1,0.1), pos_hint={'x':0.0,'y':0.9},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        back_button.bind(on_press=self.back)
        self.add_widget(back_button)

    def show_delete_confirmation(self, instance):
        layout = FloatLayout()
        label = Label(text='Are you sure you want to delete this car?', size_hint=(0.8,0.3),pos_hint={'x':0.1,'y':0.5})
        layout.add_widget(label)

        confirmation_popop = Popup(title="Confirm Deletion", content=layout, size_hint=(0.6,0.4),background='')
        confirmation_popop.background_color = (0.05, 0.1, 0.2, 0.8)
        confirmation_popop.title_color = [1,1,1,1]

        yes_button = Button(text='Yes', size_hint=(0.4,0.2), pos_hint={'x':0.05,'y':0.2}, background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        yes_button.bind(on_press=lambda instance: self.delete_car(confirmation_popop))
        layout.add_widget(yes_button)

        no_button = Button(text='No', size_hint=(0.4,0.2), pos_hint={'x':0.55,'y':0.2}, background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        no_button.bind(on_press=confirmation_popop.dismiss)
        layout.add_widget(no_button)

        confirmation_popop.open()

    def delete_car(self, confirmation_popup):
        """
        Delete the car from the database.
        """
        with shelve.open('car_database') as db:
            del db[self.car.id]
            print(f'Car {self.car.name} with ID {self.car.id} deleted.')

        confirmation_popup.dismiss()
        home_screen = self.manager.get_screen('Home')
        home_screen.children[0].display_home_page()
        self.manager.current = 'Home'  # Navigate back to the homepage

    def show_edit_car_popup(self, instance):
        """
        Display popup to edit car details.
        """
        layout = FloatLayout()

        INPUT_SIZE = (0.8,0.1)
        self.make_input = TextInput(text=self.car.make, size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.75}, background_color = (1,1,1, 0.7))
        self.model_input = TextInput(text=self.car.model, size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.65}, background_color = (1,1,1, 0.7))
        self.year_input = TextInput(text=self.car.year, size_hint=INPUT_SIZE, pos_hint={'x': 0.1, 'y': 0.55}, background_color = (1,1,1, 0.7))
        self.mileage_input = TextInput(text=str(self.car.mileage), size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.45}, background_color = (1,1,1, 0.7))
        self.name_input = TextInput(text=self.car.name, size_hint=INPUT_SIZE, pos_hint={'x':0.1,'y':0.35}, background_color = (1,1,1, 0.7))

        submit_button = Button(text='Save Changes', size_hint=(0.5, 0.1), pos_hint={'x': 0.25, 'y': 0.1},background_color=(0, 0.6, 0.8, 1),color=(1, 1, 1, 1))
        submit_button.bind(on_press=self.update_car_in_db)

        layout.add_widget(self.make_input)
        layout.add_widget(self.model_input)
        layout.add_widget(self.year_input)
        layout.add_widget(self.mileage_input)
        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)

        self.edit_popup = Popup(title='Edit Car', content=layout, size_hint=(0.8, 0.8), background = '')
        self.edit_popup.background_color = (0.05, 0.1, 0.2, 1)
        self.edit_popup.open()

    def update_car_in_db(self, instance):
        """
        Update car details in the database.
        """
        self.car.make = self.make_input.text
        self.car.model = self.model_input.text
        self.car.year = self.year_input.text
        self.car.mileage = self.mileage_input.text
        self.car.name = self.name_input.text

        validation_error = self.car.check()
        if validation_error:
            error_popup = Popup(
                title="Error",
                content=Label(
                    text=validation_error,
                    color=(1, 0, 0, 1),  # Red text
                    halign="center",
                    valign="middle",
                ),
                size_hint=(0.6, 0.4),
                background ='',
                background_color=(0.05, 0.1, 0.2, 1),
            )
            error_popup.open()
            return 

        with shelve.open('car_database') as db:
            db[self.car.id] = self.car
            print(f'Car {self.car.name} with ID {self.car.id} updated.')

        self.edit_popup.dismiss()
        home_screen = self.manager.get_screen('Home')
        home_screen.children[0].display_home_page()
        self.manager.current = 'Home'

    def open_logs_page(self):
        log_screen=self.manager.get_screen('Log')
        log_page = log_screen
        log_page.display_log_page(self.car)
        self.manager.transition.direction = 'left'
        self.manager.current='Log'

    def back(self, instance):
        home_screen=self.manager.get_screen('Home')
        home_screen.children[0].display_home_page()
        self.manager.transition.direction = 'right'
        self.manager.current = 'Home'

