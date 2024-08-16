import os
import sys
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.network.urlrequest import UrlRequest
import json
from fontTools.ttLib import TTFont
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock




kivy.require('1.11.1')

class BookingScreen(Screen):
    def __init__(self, **kwargs):
        super(BookingScreen, self).__init__(**kwargs)

        background = Image(source='img.jpg', allow_stretch=True)

        input_layout = FloatLayout()

        # Example of changing font and font size for labels in BookingScreen
        self.app_name_label = Label(text="[font=Cascadia]Park-EazyGo[/font]",
                                    markup=True,
                                    size_hint=(None, None), 
                                    pos_hint={'center_x': 0.5, 'top': 0.85}, 
                                    font_size=65, color=(8,8,0,2),
                                    font_name="Cascadia.ttf")

        self.name_label = Label(text="Name of the User", size_hint=(None, None), 
                                pos_hint={'x': 0.37, 'center_y': 0.60}, 
                                font_size=30, color=(0, 0, 0, 1),
                                font_name="Acme-Regular.ttf")

        self.name_input = TextInput(hint_text="Enter your name", multiline=False, size_hint=(None, None), width=300, height=50, font_size=24, pos_hint={'center_x': 0.5, 'center_y': 0.53})
        self.book_button = Button(text="Book Now", size_hint=(None, None), background_color=(0, 0.8, 0.3, 1), size=(300, 60), pos_hint={'center_x': 0.5, 'y': 0.25})
        self.book_button.bind(on_press=self.book)

        input_layout.add_widget(self.book_button)
        input_layout.add_widget(self.name_input)
        input_layout.add_widget(self.app_name_label)
        input_layout.add_widget(self.name_label)

        main_layout = FloatLayout()
        main_layout.add_widget(background)
        main_layout.add_widget(input_layout)
        self.add_widget(main_layout)

    def book(self, instance):
        name = self.name_input.text.strip()
        if name:
            confirmation_message = f"Booking confirmed for {name}"
            self.manager.get_screen("payment").booking_confirmation = confirmation_message
            self.manager.current = "slot_list"
        else:
            self.show_error_popup("Please fill in all fields.")

    def show_error_popup(self, message):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=message))
        ok_button = Button(text="OK", size_hint=(None, None), background_color=(0, 0.7, 0.3, 1))
        popup = Popup(title="Error", content=content, size_hint=(0.3, 0.3))
        content.add_widget(ok_button)

        ok_button.bind(on_press=popup.dismiss)
        popup.open()

    def reset_fields(self):
        self.name_input.text = ""

class SlotListScreen(Screen):
    def __init__(self, **kwargs):
        super(SlotListScreen, self).__init__(**kwargs)

        background = Image(source='img.jpg', allow_stretch=True)

        slot_list_layout = FloatLayout()
        app_image = Image(source='upi-twitter.jpg', 
                          allow_stretch=True, 
                          size_hint=(None, None), 
                          size=(200, 200), 
                          pos_hint={'center_x': 0.5, 'y': 0.7})

        self.slot_list_label = Label(text="Available Slots: Loading...", 
                                     size_hint=(None, None), 
                                     pos_hint={'x': 0.45, 'y': 0.6},
                                     font_size=35, 
                                     color=(0, 0, 0, 1),
                                     font_name="KronaOne-Regular.ttf")

        self.price_label = Label(text="Price per hour: ₹40", 
                                 size_hint=(None, None), 
                                 pos_hint={'x': 0.45, 'y': 0.5}, 
                                 font_size=30, 
                                 color=(0, 0, 0, 1),
                                 font_name="Poppins-Regular.ttf")

        self.go_to_payment_button = Button(text="Go to Payment", size_hint=(None, None), background_color=(0.9, 0.4, 0.0, 1), size=(300, 60), pos_hint={'center_x': 0.5, 'y': 0.2})
        self.go_to_payment_button.bind(on_press=self.go_to_payment)

        # Add a restart button
        self.restart_button = Button(text="Refresh Slot", size_hint=(None, None), background_color=(0.7, 0.4, 0.7, 1), size=(150, 40), pos_hint={'right': 0.57, 'top': 0.1})
        self.restart_button.bind(on_press=self.restart_app)
        
        
        slot_list_layout.add_widget(self.slot_list_label)
        slot_list_layout.add_widget(self.price_label)
        slot_list_layout.add_widget(self.go_to_payment_button)
        slot_list_layout.add_widget(self.restart_button)  # Add the restart button

        main_layout = FloatLayout()
        main_layout.add_widget(background)
        main_layout.add_widget(slot_list_layout)
        self.add_widget(main_layout)

    def go_to_payment(self, instance):
        self.manager.current = "payment"

    def restart_app(self, instance):
        # Restart the app by re-running it
        os.execv(sys.executable, ['python'] + sys.argv)

class PaymentScreen(Screen):
    def __init__(self, **kwargs):
        super(PaymentScreen, self).__init__(**kwargs)

        background = Image(source='img.jpg', allow_stretch=True)

        payment_layout = FloatLayout()
        app_image1 = Image(source='upis.png', 
                          allow_stretch=True, 
                          size_hint=(None, None), 
                          size=(300, 300), 
                          pos_hint={'center_x': 0.5, 'y': 0.3})
        # app_image2 = Image(source='gpay.png', 
        #                   allow_stretch=True, 
        #                   size_hint=(None, None), 
        #                   size=(200, 200), 
        #                   pos_hint={'center_x': 0.2, 'y': 0.4})
        # app_image3 = Image(source='paytm.png', 
        #                   allow_stretch=True, 
        #                   size_hint=(None, None), 
        #                   size=(200, 200), 
        #                   pos_hint={'center_x': 0.2, 'y': 0.6})
        # app_image4 = Image(source='phonepay.png', 
        #                   allow_stretch=True, 
        #                   size_hint=(None, None), 
        #                   size=(200, 200), 
        #                   pos_hint={'center_x': 0.8, 'y': 0.6})
        # app_image5 = Image(source='bharatpe.png', 
        #                   allow_stretch=True, 
        #                   size_hint=(None, None), 
        #                   size=(200, 200), 
        #                   pos_hint={'center_x': 0.8, 'y': 0.4})
        self.confirmation_label = Label(size_hint=(None, None), 
                                        size=(400, 40), 
                                        pos_hint={'center_x': 0.5, 'y': 0.6}, 
                                        font_size=30, 
                                        color=(0, 0, 0, 1))
        self.payment_button = Button(text="Make Payment", 
                                     
                                     size_hint=(None, None), 
                                     background_color=(0.9, 0.4, 0.0, 1), 
                                     size=(300, 60), 
                                     pos_hint={'center_x': 0.5, 'y': 0.3})
        self.payment_button.bind(on_press=self.make_payment)

        self.return_button = Button(text="Return to Booking Screen", 
                                    size_hint=(None, None), 
                                    background_color=(0.2, 0.6, 0.9, 1), 
                                    size=(300, 60), 
                                    pos_hint={'center_x': 0.5, 'y': 0.2})
        self.return_button.bind(on_press=self.return_to_booking)

        payment_layout.add_widget(app_image1)
    
        payment_layout.add_widget(self.confirmation_label)
        payment_layout.add_widget(self.payment_button)
        payment_layout.add_widget(self.return_button)

        main_layout = FloatLayout()
        main_layout.add_widget(background)
        main_layout.add_widget(payment_layout)
        self.add_widget(main_layout)
        self.booking_confirmation = ""

    def make_payment(self, instance):
        confirmation_message = self.booking_confirmation + "\n\nPayment Successful!"
        self.confirmation_label.text = confirmation_message
        

    def return_to_booking(self, instance):
        booking_screen = self.manager.get_screen("booking")
        booking_screen.reset_fields()

        self.reset_fields()

        self.manager.current = "booking"

    def reset_fields(self):
        self.confirmation_label.text = ""

class MyApp(App):
    def build(self):
        Window.size = (360, 600)
        sm = ScreenManager()

        # Create instances of your screens
        booking_screen = BookingScreen(name="booking")
        payment_screen = PaymentScreen(name="payment")
        slot_list_screen = SlotListScreen(name="slot_list")

        # Add the screens to the ScreenManager
        sm.add_widget(booking_screen)
        sm.add_widget(payment_screen)
        sm.add_widget(slot_list_screen)

        # Perform an intro animation before displaying the booking screen
        Clock.schedule_once(lambda dt: self.intro_animation(booking_screen), 0.5)

        return sm

    def intro_animation(self, screen):
        # You can define your intro animation here
        # For example, let's animate the opacity and size of the screen
        animation = Animation(opacity=0, size=(0, 0))  # Define your animation properties
        animation += Animation(opacity=1, size=(360, 600), duration=1.5)  # Add sequential animation properties

        # Bind the transition to move to the booking screen after the animation completes
        animation.bind(on_complete=self.change_to_booking_screen)

        # Start the animation on the specified screen
        animation.start(screen)

    def change_to_booking_screen(self, *args):
        # Change the current screen to the booking screen after animation completion
        self.root.current = "booking"

    def on_start(self):
        api_url = "http://127.0.0.1:5000"  # Replace with your API URL
        UrlRequest(api_url, on_success=self.on_data_received)

    def on_data_received(self, req, result):
        if req.resp_status == 200:
            free_slots = result  # The result is already in JSON format, so no need to decode it
            slot_list_screen = self.root.get_screen("slot_list")
            slot_list_screen.slot_list_label.text = f"Available Slots: {', '.join(map(str, free_slots))}"
        else:
            slot_list_screen = self.root.get_screen("slot_list")
            slot_list_screen.slot_list_label.text = "Error: Unable to fetch free slots"

if __name__ == '__main__':
    MyApp().run()
