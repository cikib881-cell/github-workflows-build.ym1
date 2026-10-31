from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

class MyChat(App):
    def build(self):
        self.root = ScreenManager()
        self.show_login()
        return self.root

    def show_login(self):
        screen = Screen(name="login")
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        layout.add_widget(Label(text="MyChat", font_size=40))
        
        self.phone_input = TextInput(hint_text="Введите номер", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.phone_input)
        
        btn = Button(text="Войти", size_hint_y=None, height=50)
        btn.bind(on_release=self.do_login)
        layout.add_widget(btn)
        
        screen.add_widget(layout)
        self.root.add_widget(screen)

    def do_login(self, instance):
        self.root.current = "main"

    def on_start(self):
        screen = Screen(name="main")
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Добро пожаловать в чат!", font_size=24))
        
        btn = Button(text="Выйти", size_hint_y=None, height=50)
        btn.bind(on_release=lambda x: setattr(self.root, 'current', 'login'))
        layout.add_widget(btn)
        
        screen.add_widget(layout)
        self.root.add_widget(screen)

if __name__ == '__main__':
    MyChat().run()
