import os, json
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

Window.clearcolor = (0.06, 0.08, 0.11, 1)

class MyChat(App):
    def build(self):
        self.title = "MyChat"
        self.f = os.path.join(self.user_data_dir, "data.json")
        self.d = self.load()
        self.root = ScreenManager()
        
        if self.d.get("p") and self.d["p"] in self.d.get("a", {}): 
            self.main()
        else: 
            self.start()
        return self.root

    def load(self):
        if os.path.exists(self.f):
            try:
                with open(self.f, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return {"a": {}, "p": ""}

    def save(self):
        with open(self.f, "w", encoding="utf-8") as f: json.dump(self.d, f, ensure_ascii=False, indent=2)

    def u(self):
        p = self.d.get("p")
        if p and p in self.d.get("a", {}):
            a = self.d["a"][p]
            a.setdefault("n", "User")
            a.setdefault("c", {})
            return a
        return None

    def start(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        b.add_widget(Widget())
        b.add_widget(Label(text="MyChat", font_size=dp(40), bold=True, size_hint_y=None, height=dp(60)))
        self.ph = TextInput(text="+7 ", font_size=dp(24), size_hint_y=None, height=dp(60), multiline=False, halign="center")
        b.add_widget(self.ph)
        btn = Button(text="ВОЙТИ", size_hint_y=None, height=dp(55), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.login(self.ph.text))
        b.add_widget(btn); b.add_widget(Widget()); s.add_widget(b); self.root.add_widget(s)

    def login(self, ph):
        if len("".join(filter(str.isdigit, ph))) < 10: return
        if ph not in self.d["a"]: self.d["a"][ph] = {"n": "User", "c": {}}
        self.d["p"] = ph
        self.save()
        self.main()

    def main(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical")
        h = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(15), dp(10)])
        h.add_widget(Label(text="Чаты", font_size=dp(22), bold=True, size_hint_x=0.5))
        btn_plus = Button(text="+ Создать", size_hint=(0.5, 1), background_color=(0.2,0.5,0.8,1))
        btn_plus.bind(on_release=lambda x: self.create_screen()); h.add_widget(btn_plus)
        m.add_widget(h)
        self.cl = GridLayout(cols=1, spacing=dp(5), size_hint_y=None); self.cl.bind(minimum_height=self.cl.setter('height'))
        sc = ScrollView(); sc.add_widget(self.cl); m.add_widget(sc)
        n = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(5))
        b = Button(text="Профиль", background_color=(0.15,0.18,0.24,1)); b.bind(on_release=lambda x: self.prof()); n.add_widget(b)
        m.add_widget(n)
        s.add_widget(m); self.root.add_widget(s); self.upd_list()

    def upd_list(self):
        self.cl.clear_widgets(); u = self.u()
        if not u: return
        for n, c in u["c"].items():
            btn = Button(text=n, size_hint_y=None, height=dp(75), background_color=(0.15,0.18,0.24,1))
            btn.bind(on_release=lambda x, name=n: self.open_chat(name))
            self.cl.add_widget(btn)

    def create_screen(self):
        self.root.clear_widgets(); s = Screen(); main = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        main.add_widget(Label(text="Создать Группу", font_size=dp(20), bold=True, size_hint_y=None, height=dp(40)))
        self.c_name = TextInput(hint_text="Название", multiline=False, size_hint_y=None, height=dp(50))
        main.add_widget(self.c_name)
        bb = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        bc = Button(text="Отмена", background_color=(0.3,0.1,0.1,1)); bc.bind(on_release=lambda x: self.main())
        bs = Button(text="Создать", background_color=(0.2,0.5,0.8,1)); bs.bind(on_release=lambda x: self.save_create())
        bb.add_widget(bc); bb.add_widget(bs); main.add_widget(bb)
        s.add_widget(main); self.root.add_widget(s)

    def save_create(self):
        name = self.c_name.text.strip()
        if not name: return
        self.u()["c"][name] = {"msgs": []}
        self.save(); self.main()

    def open_chat(self, n):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical")
        c = self.u()["c"].get(n, {})
        h = BoxLayout(size_hint_y=None, height=dp(60))
        b1 = Button(text="<", size_hint_x=None, width=dp(40)); b1.bind(on_release=lambda x: self.main()); h.add_widget(b1)
        h.add_widget(Label(text=n, font_size=dp(20), bold=True))
        b.add_widget(h)
        sc = ScrollView(); self.mb = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.mb.bind(minimum_height=self.mb.setter('height'))
        for m in c.get("msgs", []):
            self.mb.add_widget(Label(text=f"{m['snd']}: {m['txt']}", halign="left", size_hint_y=None, height=dp(40)))
        sc.add_widget(self.mb); b.add_widget(sc)
        ib = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.inp = TextInput(multiline=False)
        btn = Button(text=">", size_hint_x=None, width=dp(50), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.send(n))
        ib.add_widget(self.inp); ib.add_widget(btn); b.add_widget(ib)
        s.add_widget(b); self.root.add_widget(s)

    def send(self, n):
        txt = self.inp.text.strip()
        if not txt: return
        c = self.u()["c"][n]
        c.setdefault("msgs", []).append({"snd": self.u()["n"], "txt": txt})
        self.save(); self.open_chat(n)

    def prof(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical")
        m.add_widget(Label(text=self.u()["n"], font_size=dp(30), bold=True, size_hint_y=None, height=dp(60)))
        m.add_widget(Label(text=f"Тел: {self.d['p']}", size_hint_y=None, height=dp(30)))
        b_out = Button(text="Выйти", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1))
        b_out.bind(on_release=lambda x: self.logout()); m.add_widget(b_out)
        n = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(5))
        b = Button(text="Назад", background_color=(0.15,0.18,0.24,1)); b.bind(on_release=lambda x: self.main()); n.add_widget(b)
        m.add_widget(n)
        s.add_widget(m); self.root.add_widget(s)

    def logout(self):
        self.d["p"] = ""; self.save(); self.start()

if __name__ == "__main__":
    MyChat().run()
