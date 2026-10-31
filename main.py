import os, json, random
from datetime import datetime
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
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.06, 0.08, 0.11, 1)

class MessageBubble(BoxLayout):
    def __init__(self, text, is_mine=False, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.padding = [dp(10), dp(5)]
        
        btn = Button(text=text, halign="left", valign="middle", size_hint_y=None, background_normal='', background_color=(0,0,0,0))
        btn.bind(width=lambda inst, w: setattr(inst, 'text_size', (w - dp(20), None)))
        btn.bind(texture_size=lambda inst, ts: setattr(inst, 'height', ts[1] + dp(20)))
        
        with btn.canvas.before:
            if is_mine: Color(0.1, 0.5, 0.3, 1)
            else: Color(0.15, 0.18, 0.24, 1)
            btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[dp(15)])
        btn.bind(pos=self.update_rect, size=self.update_rect)
        
        if callback: btn.bind(on_release=callback)
            
        self.add_widget(btn)
        if is_mine: self.add_widget(Widget(size_hint_x=0.2))
        else: self.add_widget(Widget(size_hint_x=0.2))

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

class MyChat(App):
    def build(self):
        self.title = "MyChat"
        self.f = os.path.join(self.user_data_dir, "data.json")
        self.d = self.load()
        self.root = ScreenManager()
        self.temp_code = ""
        self.temp_phone = ""
        
        if self.d.get("p") and self.d["p"] in self.d.get("a", {}): self.main()
        else: self.start()
        return self.root

    def load(self):
        if os.path.exists(self.f):
            try:
                with open(self.f, "r", encoding="utf-8") as f: return json.load(f)
            except: pass
        return {"a": {}, "p": "", "wallpaper": ""}

    def save(self):
        with open(self.f, "w", encoding="utf-8") as f: json.dump(self.d, f, ensure_ascii=False, indent=2)

    def u(self):
        p = self.d.get("p")
        if p and p in self.d.get("a", {}):
            a = self.d["a"][p]
            a.setdefault("n", "User"); a.setdefault("us", ""); a.setdefault("year", "")
            a.setdefault("c", {}); a.setdefault("blocked", [])
            return a
        return None

    def start(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        b.add_widget(Widget()); b.add_widget(Label(text="MyChat", font_size=dp(40), bold=True, size_hint_y=None, height=dp(60)))
        self.ph = TextInput(text="+7 ", font_size=dp(24), size_hint_y=None, height=dp(60), multiline=False, halign="center", background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1))
        b.add_widget(self.ph)
        btn = Button(text="ПОЛУЧИТЬ КОД", size_hint_y=None, height=dp(55), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.login(self.ph.text))
        b.add_widget(btn); b.add_widget(Widget()); s.add_widget(b); self.root.add_widget(s)

    def login(self, ph):
        clean = "".join(filter(str.isdigit, ph))
        if len(clean) < 10: return
        self.temp_phone = ph; self.temp_code = str(random.randint(1000, 9999)); self.code_s()

    def code_s(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        b.add_widget(Widget())
        b.add_widget(Label(text=f"Код отправлен на {self.temp_phone}", font_size=dp(16), size_hint_y=None, height=dp(30)))
        b.add_widget(Label(text=f"ВАШ КОД: {self.temp_code}", font_size=dp(30), color=(1, 0.5, 0.5, 1), bold=True, size_hint_y=None, height=dp(50)))
        self.ci = TextInput(font_size=dp(30), size_hint_y=None, height=dp(60), multiline=False, halign="center", input_type='number', background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1))
        b.add_widget(self.ci)
        btn = Button(text="ПОДТВЕРДИТЬ", size_hint_y=None, height=dp(55), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.check(self.ci.text))
        b.add_widget(btn)
        b.add_widget(Button(text="Назад", size_hint_y=None, height=dp(40), background_color=(0.3,0.1,0.1,1), on_release=lambda x: self.start()))
        b.add_widget(Widget()); s.add_widget(b); self.root.add_widget(s)

    def check(self, c):
        if c == self.temp_code:
            if self.temp_phone not in self.d["a"]: self.reg_s()
            else:
                self.d["p"] = self.temp_phone; self.save(); self.main()
        else: self.ci.text = ""

    def reg_s(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        b.add_widget(Widget()); b.add_widget(Label(text="Регистрация", font_size=dp(30), bold=True, size_hint_y=None, height=dp(50)))
        b.add_widget(Label(text="Имя", size_hint_y=None, height=dp(20), halign="left"))
        self.name_inp = TextInput(multiline=False, size_hint_y=None, height=dp(45), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(self.name_inp)
        b.add_widget(Label(text="Юзернейм (@)", size_hint_y=None, height=dp(20), halign="left"))
        self.us_inp = TextInput(multiline=False, size_hint_y=None, height=dp(45), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(self.us_inp)
        b.add_widget(Label(text="Год рождения", size_hint_y=None, height=dp(20), halign="left"))
        self.year_inp = TextInput(multiline=False, size_hint_y=None, height=dp(45), input_type='number', background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(self.year_inp)
        btn = Button(text="ЗАРЕГИСТРИРОВАТЬСЯ", size_hint_y=None, height=dp(55), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.do_reg())
        b.add_widget(btn); b.add_widget(Widget()); s.add_widget(b); self.root.add_widget(s)

    def do_reg(self):
        name = self.name_inp.text.strip(); us = self.us_inp.text.strip(); year = self.year_inp.text.strip()
        if not name or not us or not year: return
        self.d["a"][self.temp_phone] = {"n": name, "us": us, "year": year, "c": {}, "blocked": []}
        self.d["p"] = self.temp_phone; self.save(); self.main()

    def nav(self):
        n = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(5))
        for t, cb in [("Чаты", lambda x: self.main()), ("Настройки", lambda x: self.set()), ("Профиль", lambda x: self.prof())]:
            b = Button(text=t, background_color=(0.15,0.18,0.24,1)); b.bind(on_release=cb); n.add_widget(b)
        return n

    def main(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical")
        
        if self.d.get("wallpaper"):
            bg = Image(source=self.d["wallpaper"], allow_stretch=True, keep_ratio=False); m.add_widget(bg)
        else:
            m.add_widget(Widget())

        h = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(15), dp(10)], spacing=dp(10), pos_hint={'top': 1})
        h.add_widget(Label(text="Чаты", font_size=dp(22), bold=True, size_hint_x=0.25))
        self.srch = TextInput(hint_text="Поиск...", size_hint=(0.6,1), multiline=False, background_color=(0.15,0.18,0.22,0.8), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(15)])
        self.srch.bind(text=lambda i,v: self.upd_list(v)); h.add_widget(self.srch)
        
        btn_plus = Button(text="+", size_hint=(0.15, 1), background_color=(0.2,0.5,0.8,1), font_size=dp(24), bold=True)
        btn_plus.bind(on_release=lambda x: self.create_menu()); h.add_widget(btn_plus)
        m.add_widget(h)
        
        self.cl = GridLayout(cols=1, spacing=dp(5), size_hint_y=None); self.cl.bind(minimum_height=self.cl.setter('height'))
        sc = ScrollView(); sc.add_widget(self.cl); m.add_widget(sc)
        m.add_widget(self.nav()); s.add_widget(m); self.root.add_widget(s); self.upd_list()

    def create_menu(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))
        b.add_widget(Label(text="Что создать?", font_size=dp(24), bold=True))
        b.add_widget(Button(text="Группу", size_hint_y=None, height=dp(60), background_color=(0.15,0.18,0.24,1), on_release=lambda x: self.create_screen("Группа")))
        b.add_widget(Button(text="Канал", size_hint_y=None, height=dp(60), background_color=(0.15,0.18,0.24,1), on_release=lambda x: self.create_screen("Канал")))
        b.add_widget(Widget())
        b.add_widget(Button(text="Отмена", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1), on_release=lambda x: self.main()))
        s.add_widget(b); self.root.add_widget(s)

    def upd_list(self, q=""):
        self.cl.clear_widgets(); u = self.u()
        if not u: return
        
        if q.startswith("@") and len(q) > 1:
            r = BoxLayout(size_hint_y=None, height=dp(75), padding=dp(10), spacing=dp(10))
            r.add_widget(Label(text=f"Найти пользователя {q}", bold=True, size_hint_x=0.7))
            btn = Button(text="Написать", size_hint_x=None, width=dp(80), background_color=(0.2,0.5,0.8,1)); btn.bind(on_release=lambda x, name=q[1:]: self.start_chat(name)); r.add_widget(btn)
            self.cl.add_widget(r)
            
        elif q and len(q) > 2:
            r = BoxLayout(size_hint_y=None, height=dp(75), padding=dp(10), spacing=dp(10))
            r.add_widget(Label(text=f"Создать чат с {q}", bold=True, size_hint_x=0.7))
            btn = Button(text="Чат", size_hint_x=None, width=dp(60), background_color=(0.2,0.5,0.8,1)); btn.bind(on_release=lambda x, name=q: self.start_chat(name)); r.add_widget(btn)
            self.cl.add_widget(r)
        
        for n, c in u["c"].items():
            if n in u.get("blocked", []): continue
            if q and not q.startswith("@") and q.lower() not in n.lower(): continue
            t = c.get("t", "Чат")
            btn = Button(text=f"{n}\n[{t}]", size_hint_y=None, height=dp(75), background_normal='', background_color=(0.15,0.18,0.24,0.8), halign="left", valign="middle")
            btn.text_size = (Window.width - dp(40), None)
            btn.bind(on_release=lambda x, name=n: self.open_chat(name))
            self.cl.add_widget(btn)

    def start_chat(self, name):
        u = self.u()
        if name not in u["c"]: u["c"][name] = {"t": "Личный", "msgs": []}; self.save()
        self.open_chat(name)

    def create_screen(self, kind):
        self.root.clear_widgets(); s = Screen(); main = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))
        main.add_widget(Label(text=f"Настройки {kind}", font_size=dp(20), bold=True, size_hint_y=None, height=dp(40)))
        
        main.add_widget(Label(text="Название", size_hint_y=None, height=dp(20), halign="left"))
        self.c_name = TextInput(multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)]); main.add_widget(self.c_name)
        
        self.is_anon = False
        if kind == "Канал":
            self.btn_anon = Button(text="Анонимный: НЕТ", size_hint_y=None, height=dp(50), background_color=(0.3,0.3,0.3,1))
            self.btn_anon.bind(on_release=self.toggle_anon); main.add_widget(self.btn_anon)

        main.add_widget(Label(text="Добавить участников", size_hint_y=None, height=dp(20), halign="left"))
        self.members_inp = TextInput(hint_text="Имена через запятую", multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)]); main.add_widget(self.members_inp)
        
        bb = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        bc = Button(text="Отмена", background_color=(0.3,0.1,0.1,1)); bc.bind(on_release=lambda x: self.main())
        bs = Button(text="Создать", background_color=(0.2,0.5,0.8,1)); bs.bind(on_release=lambda x: self.save_create(kind))
        bb.add_widget(bc); bb.add_widget(bs); main.add_widget(bb)
        s.add_widget(main); self.root.add_widget(s)

    def toggle_anon(self, instance):
        self.is_anon = not self.is_anon
        instance.text = f"Анонимный: {'ДА' if self.is_anon else 'НЕТ'}"

    def save_create(self, kind):
        name = self.c_name.text.strip()
        if not name: return
        u = self.u()
        if name in u["c"]: return
        members = [m.strip() for m in self.members_inp.text.split(",")] if self.members_inp.text.strip() else []
        u["c"][name] = {"t": kind, "an": self.is_anon, "admins": [u["n"]], "members": members, "msgs": []}
        self.save(); self.open_chat(name)

    def open_chat(self, n):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical")
        u = self.u(); c = u["c"].get(n, {}); t = c.get("t", "Чат")
        
        if self.d.get("wallpaper"):
            bg = Image(source=self.d["wallpaper"], allow_stretch=True, keep_ratio=False); b.add_widget(bg)
            
        h = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10), pos_hint={'top': 1})
        b1 = Button(text="<", size_hint_x=None, width=dp(40), background_color=(0,0,0,0), font_size=dp(24))
        b1.bind(on_release=lambda x: self.main()); h.add_widget(b1)
        h.add_widget(Label(text=n, font_size=dp(20), bold=True))
        b2 = Button(text="...", size_hint_x=None, width=dp(40), background_color=(0.15,0.18,0.24,1), font_size=dp(20))
        b2.bind(on_release=lambda x: self.chat_settings(n)); h.add_widget(b2)
        b.add_widget(h)
        
        sc = ScrollView(); self.mb = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.mb.bind(minimum_height=self.mb.setter('height'))
        
        for idx, m in enumerate(c.get("msgs", [])):
            snd = m['snd']
            if t == "Канал" and c.get("an"): snd = n
            
            if "photo" in m:
                box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(200))
                img = Image(source=m["photo"], size_hint_y=None, height=dp(180))
                btn_img = Button(background_color=(0,0,0,0), size_hint_y=None, height=dp(180))
                btn_img.bind(on_release=lambda x, i=idx: self.msg_menu(n, i))
                box.add_widget(img); box.add_widget(btn_img)
                self.mb.add_widget(box)
            else:
                is_my_msg = (m['snd'] == u['n'])
                text = f"{m['txt']}\n{m['tm']}"
                if not is_my_msg and t != "Канал": text = f"{snd}: {m['txt']}\n{m['tm']}"
                bubble = MessageBubble(text, is_mine=is_my_msg, callback=lambda x, i=idx: self.msg_menu(n, i))
                self.mb.add_widget(bubble)
                
        sc.add_widget(self.mb); b.add_widget(sc)
        
        ib = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        btn_photo = Button(text="+", size_hint_x=None, width=dp(50), background_color=(0.15,0.18,0.24,1))
        btn_photo.bind(on_release=lambda x: self.file_chooser(n))
        ib.add_widget(btn_photo)
        
        self.inp = TextInput(multiline=False, background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        btn = Button(text=">", size_hint_x=None, width=dp(50), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.send(n))
        ib.add_widget(self.inp); ib.add_widget(btn); b.add_widget(ib)
        s.add_widget(b); self.root.add_widget(s)

    def msg_menu(self, n, idx):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))
        b.add_widget(Label(text="Действия с сообщением", font_size=dp(20), bold=True))
        
        def del_local(inst):
            c = self.u()["c"][n]
            if 0 <= idx < len(c["msgs"]): del c["msgs"][idx]
            self.save(); self.open_chat(n)
            
        def del_all(inst):
            c = self.u()["c"][n]
            if 0 <= idx < len(c["msgs"]):
                c["msgs"][idx]["txt"] = "[Удалено]"
                if "photo" in c["msgs"][idx]: del c["msgs"][idx]["photo"]
            self.save(); self.open_chat(n)
            
        b.add_widget(Button(text="Удалить у себя", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1), on_release=del_local))
        b.add_widget(Button(text="Удалить у всех", size_hint_y=None, height=dp(50), background_color=(0.6,0.1,0.1,1), on_release=del_all))
        b.add_widget(Button(text="Отмена", size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.24,1), on_release=lambda x: self.open_chat(n)))
        
        s.add_widget(b); self.root.add_widget(s)

    def file_chooser(self, n):
        content = BoxLayout(orientation="vertical")
        filechooser = FileChooserListView(path=os.path.expanduser("~"))
        content.add_widget(filechooser)
        
        buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        btn_cancel = Button(text="Отмена", background_color=(0.3,0.1,0.1,1))
        btn_select = Button(text="Выбрать", background_color=(0.2,0.5,0.8,1))
        
        popup = Popup(title="Выберите фото", content=content, size_hint=(0.9, 0.9))
        
        btn_cancel.bind(on_release=popup.dismiss)
        def select(inst):
            if filechooser.selection:
                path = filechooser.selection[0]
                u = self.u(); c = u["c"][n]; snd = u["n"]
                c.setdefault("msgs", []).append({"snd": snd, "photo": path, "tm": datetime.now().strftime("%H:%M")})
                self.save(); popup.dismiss(); self.open_chat(n)
                
        btn_select.bind(on_release=select)
        buttons.add_widget(btn_cancel); buttons.add_widget(btn_select)
        content.add_widget(buttons)
        popup.open()

    def send(self, n):
        txt = self.inp.text.strip()
        if not txt: return
        u = self.u(); c = u["c"][n]; snd = u["n"]
        if c.get("t") == "Канал" and c.get("an"): snd = "Канал"
        c.setdefault("msgs", []).append({"snd": snd, "txt": txt, "tm": datetime.now().strftime("%H:%M")})
        self.save(); self.open_chat(n)

    def chat_settings(self, n):
        self.root.clear_widgets(); s = Screen(); u = self.u(); c = u["c"][n]
        b = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        h = BoxLayout(size_hint_y=None, height=dp(50))
        bb = Button(text="< Назад", size_hint_x=None, width=dp(80), background_color=(0,0,0,0)); bb.bind(on_release=lambda x: self.open_chat(n))
        h.add_widget(bb); h.add_widget(Label(text="Управление", font_size=dp(20), bold=True)); b.add_widget(h)
        
        b.add_widget(Label(text="Название", size_hint_y=None, height=dp(20), halign="left"))
        self.name_inp = TextInput(text=n, multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(self.name_inp)
        btn_rename = Button(text="Сохранить название", si
