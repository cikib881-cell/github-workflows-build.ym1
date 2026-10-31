import os, json
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
            a.setdefault("blocked", [])
            return a
        return None

    def start(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(20))
        b.add_widget(Widget())
        b.add_widget(Label(text="MyChat", font_size=dp(40), bold=True, size_hint_y=None, height=dp(60)))
        self.ph = TextInput(text="+7 ", font_size=dp(24), size_hint_y=None, height=dp(60), multiline=False, halign="center", background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1))
        b.add_widget(self.ph)
        btn = Button(text="ВОЙТИ", size_hint_y=None, height=dp(55), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.login(self.ph.text))
        b.add_widget(btn); b.add_widget(Widget()); s.add_widget(b); self.root.add_widget(s)

    def login(self, ph):
        if len("".join(filter(str.isdigit, ph))) < 10: return
        if ph not in self.d["a"]: self.d["a"][ph] = {"n": "User", "c": {}, "blocked": []}
        self.d["p"] = ph; self.save(); self.main()

    def nav(self):
        n = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(5))
        for t, cb in [("Чаты", lambda x: self.main()), ("Настройки", lambda x: self.set()), ("Профиль", lambda x: self.prof())]:
            b = Button(text=t, background_color=(0.15,0.18,0.24,1)); b.bind(on_release=cb); n.add_widget(b)
        return n

    def main(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical")
        
        h = BoxLayout(size_hint_y=None, height=dp(60), padding=[dp(15), dp(10)], spacing=dp(10))
        h.add_widget(Label(text="Чаты", font_size=dp(22), bold=True, size_hint_x=0.25))
        self.srch = TextInput(hint_text="Поиск...", size_hint=(0.6,1), multiline=False, background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), hint_text_color=(0.5,0.5,0.5,1), cursor_color=(1,1,1,1), padding=[dp(10), dp(15)])
        self.srch.bind(text=lambda i,v: self.upd_list(v)); h.add_widget(self.srch)
        btn_plus = Button(text="+", size_hint=(0.15, 1), background_color=(0.2,0.5,0.8,1), font_size=dp(24), bold=True)
        btn_plus.bind(on_release=lambda x: self.create_screen("Группа")); h.add_widget(btn_plus)
        m.add_widget(h)
        
        self.cl = GridLayout(cols=1, spacing=dp(5), size_hint_y=None); self.cl.bind(minimum_height=self.cl.setter('height'))
        sc = ScrollView(); sc.add_widget(self.cl); m.add_widget(sc)
        m.add_widget(self.nav()); s.add_widget(m); self.root.add_widget(s); self.upd_list()

    def upd_list(self, q=""):
        self.cl.clear_widgets(); u = self.u()
        if not u: return
        if q and len(q) > 2 and q not in u["c"]:
            r = BoxLayout(size_hint_y=None, height=dp(75), padding=dp(10), spacing=dp(10))
            r.add_widget(Label(text=f"Начать чат с {q}", bold=True, size_hint_x=0.7))
            btn = Button(text="Чат", size_hint_x=None, width=dp(60), background_color=(0.2,0.5,0.8,1)); btn.bind(on_release=lambda x, name=q: self.start_chat(name)); r.add_widget(btn)
            self.cl.add_widget(r)
        for n, c in u["c"].items():
            if n in u.get("blocked", []): continue
            if q and q.lower() not in n.lower(): continue
            t = c.get("t", "Чат")
            btn = Button(text=f"{n}\n[{t}]", size_hint_y=None, height=dp(75), background_normal='', background_color=(0.15,0.18,0.24,1), halign="left", valign="middle")
            btn.text_size = (Window.width - dp(40), None)
            btn.bind(on_release=lambda x, name=n: self.open_chat(name))
            self.cl.add_widget(btn)

    def start_chat(self, name):
        u = self.u()
        if name not in u["c"]: u["c"][name] = {"t": "Личный", "msgs": []}; self.save()
        self.open_chat(name)

    def create_screen(self, kind):
        self.root.clear_widgets(); s = Screen(); main = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        main.add_widget(Label(text=f"Создать {kind}", font_size=dp(20), bold=True, size_hint_y=None, height=dp(40)))
        main.add_widget(Label(text="Название", size_hint_y=None, height=dp(20)))
        self.c_name = TextInput(multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)]); main.add_widget(self.c_name)
        self.is_anon = False
        if kind == "Канал":
            self.btn_anon = Button(text="Анонимный: НЕТ", size_hint_y=None, height=dp(50), background_color=(0.3,0.3,0.3,1))
            self.btn_anon.bind(on_release=self.toggle_anon); main.add_widget(self.btn_anon)
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
        u["c"][name] = {"t": kind, "an": self.is_anon, "admins": [u["n"]], "members": [], "msgs": []}
        self.save(); self.open_chat(name)

    def open_chat(self, n):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical")
        u = self.u(); c = u["c"].get(n, {}); t = c.get("t", "Чат")
        h = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        b1 = Button(text="<", size_hint_x=None, width=dp(40), background_color=(0,0,0,0), font_size=dp(24))
        b1.bind(on_release=lambda x: self.main()); h.add_widget(b1)
        h.add_widget(Label(text=n, font_size=dp(20), bold=True))
        b2 = Button(text="Настройки", size_hint_x=None, width=dp(90), background_color=(0.15,0.18,0.24,1), font_size=dp(14))
        b2.bind(on_release=lambda x: self.chat_settings(n)); h.add_widget(b2)
        b.add_widget(h)
        sc = ScrollView(); self.mb = GridLayout(cols=1, spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.mb.bind(minimum_height=self.mb.setter('height'))
        for m in c.get("msgs", []):
            self.mb.add_widget(Label(text=f"{m['snd']}: {m['txt']}\n{m['tm']}", halign="left", size_hint_y=None, height=dp(50)))
        sc.add_widget(self.mb); b.add_widget(sc)
        ib = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.inp = TextInput(multiline=False, background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        btn = Button(text=">", size_hint_x=None, width=dp(50), background_color=(0.2,0.5,0.8,1))
        btn.bind(on_release=lambda x: self.send(n))
        ib.add_widget(self.inp); ib.add_widget(btn); b.add_widget(ib)
        s.add_widget(b); self.root.add_widget(s)

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
        btn_rename = Button(text="Сохранить название", size_hint_y=None, height=dp(50), background_color=(0.2,0.5,0.8,1))
        btn_rename.bind(on_release=lambda x: self.rename_chat(n, self.name_inp.text)); b.add_widget(btn_rename)
        inf = f"Тип: {c['t']}\nАдмины: {', '.join(c.get('admins',[]))}\nУчастники: {', '.join(c.get('members',[]))}"
        b.add_widget(Label(text=inf, size_hint_y=None, height=dp(80), halign="left"))
        b1 = Button(text="Добавить участника", size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.24,1))
        b1.bind(on_release=lambda x: self.member_menu(n, "add")); b.add_widget(b1)
        b2 = Button(text="Сделать админом", size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.24,1))
        b2.bind(on_release=lambda x: self.member_menu(n, "admin")); b.add_widget(b2)
        b3 = Button(text="Удалить из чата", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1))
        b3.bind(on_release=lambda x: self.member_menu(n, "remove")); b.add_widget(b3)
        b4 = Button(text="Заблокировать чат", size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.24,1))
        b4.bind(on_release=lambda x: self.block_chat(n)); b.add_widget(b4)
        b5 = Button(text="Удалить чат", size_hint_y=None, height=dp(50), background_color=(0.6,0.1,0.1,1))
        b5.bind(on_release=lambda x: self.del_chat(n)); b.add_widget(b5)
        s.add_widget(b); self.root.add_widget(s)

    def rename_chat(self, old_n, new_n):
        if not new_n.strip(): return
        u = self.u()
        if new_n in u["c"]: return
        u["c"][new_n] = u["c"].pop(old_n)
        self.save(); self.open_chat(new_n)

    def member_menu(self, n, action):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))
        b.add_widget(Label(text="Введите имя пользователя:", size_hint_y=None, height=dp(40)))
        f = TextInput(multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(f)
        btn = Button(text="Готово", size_hint_y=None, height=dp(50), background_color=(0.2,0.5,0.8,1))
        def do_action(inst):
            name = f.text.strip()
            if not name: return
            ch = self.u()["c"][n]
            if action == "add": ch.setdefault("members", []).append(name)
            elif action == "admin": ch.setdefault("admins", []).append(name)
            elif action == "remove":
                if name in ch.get("members", []): ch["members"].remove(name)
                if name in ch.get("admins", []): ch["admins"].remove(name)
            self.save()
            self.chat_settings(n)
        btn.bind(on_release=do_action)
        b.add_widget(btn)
        b.add_widget(Button(text="Отмена", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1), on_release=lambda x: self.chat_settings(n)))
        s.add_widget(b); self.root.add_widget(s)

    def block_chat(self, n):
        u = self.u()
        u.setdefault("blocked", []).append(n)
        self.save()
        self.main()

    def del_chat(self, n):
        u = self.u()
        if n in u["c"]: del u["c"][n]
        self.save(); self.main()

    def prof(self):
        self.root.clear_widgets(); s = Screen(); u = self.u(); m = BoxLayout(orientation="vertical")
        m.add_widget(Widget(size_hint_y=None, height=dp(30)))
        av = Button(text=u["n"][:1].upper(), size_hint=(None,None), size=(dp(100),dp(100)), background_color=(0.2,0.4,0.7,1), font_size=dp(40), pos_hint={'center_x':0.5})
        m.add_widget(av)
        br = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10), padding=[dp(15), 0])
        b2 = Button(text="Изменить", background_color=(0.15,0.18,0.24,1)); b2.bind(on_release=lambda x: self.ask_name())
        b3 = Button(text="Настройки", background_color=(0.15,0.18,0.24,1)); b3.bind(on_release=lambda x: self.set())
        br.add_widget(b2); br.add_widget(b3); m.add_widget(br)
        m.add_widget(Widget(size_hint_y=None, height=dp(20)))
        m.add_widget(Label(text=f"Тел: {self.d['p']}", font_size=dp(18), size_hint_y=None, height=dp(30)))
        m.add_widget(Label(text=f"Имя: {u['n']}", font_size=dp(18), size_hint_y=None, height=dp(30)))
        m.add_widget(Widget(size_hint_y=None, height=dp(30)))
        b_out = Button(text="Выйти", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1))
        b_out.bind(on_release=lambda x: self.logout()); m.add_widget(b_out)
        m.add_widget(Widget())
        m.add_widget(self.nav()); s.add_widget(m); self.root.add_widget(s)

    def ask_name(self):
        self.root.clear_widgets(); s = Screen(); b = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))
        b.add_widget(Widget())
        b.add_widget(Label(text="Введите новое имя:", size_hint_y=None, height=dp(40)))
        f = TextInput(multiline=False, size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.22,1), background_normal='', foreground_color=(1,1,1,1), padding=[dp(10), dp(10)])
        b.add_widget(f)
        btn = Button(text="Сохранить", size_hint_y=None, height=dp(50), background_color=(0.2,0.5,0.8,1))
        def save(inst):
            if f.text.strip():
                self.u()["n"] = f.text.strip(); self.save(); self.prof()
        btn.bind(on_release=save); b.add_widget(btn)
        b.add_widget(Button(text="Отмена", size_hint_y=None, height=dp(50), background_color=(0.3,0.1,0.1,1), on_release=lambda x: self.prof()))
        b.add_widget(Widget())
        s.add_widget(b); self.root.add_widget(s)

    def logout(self):
        self.d["p"] = ""; self.save(); self.start()

    def set(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical")
        h = BoxLayout(size_hint_y=None, height=dp(60))
        h.add_widget(Widget()); h.add_widget(Label(text="Настройки", font_size=dp(24), bold=True)); h.add_widget(Widget())
        m.add_widget(h)
        b_acc = Button(text="Аккаунт", size_hint_y=None, height=dp(60), background_color=(0.15,0.18,0.24,1)); b_acc.bind(on_release=lambda x: self.prof()); m.add_widget(b_acc)
        m.add_widget(Widget(size_hint_y=None, height=dp(10)))
        b_lang = Button(text="Заблокированные чаты", size_hint_y=None, height=dp(60), background_color=(0.15,0.18,0.24,1)); b_lang.bind(on_release=lambda x: self.show_blocked()); m.add_widget(b_lang)
        m.add_widget(Widget())
        m.add_widget(self.nav()); s.add_widget(m); self.root.add_widget(s)

    def show_blocked(self):
        self.root.clear_widgets(); s = Screen(); m = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        b = BoxLayout(size_hint_y=None, height=dp(50))
        bb = Button(text="<", size_hint_x=None, width=dp(40), background_color=(0,0,0,0)); bb.bind(on_release=lambda x: self.set())
        b.add_widget(bb); b.add_widget(Label(text="Заблокированные", font_size=dp(20), bold=True)); m.add_widget(b)
        sc = ScrollView(); ct = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(5)); ct.bind(minimum_height=ct.setter('height'))
        u = self.u()
        for n in u.get("blocked", []):
            btn = Button(text=f"Разблокировать {n}", size_hint_y=None, height=dp(50), background_color=(0.15,0.18,0.24,1))
            btn.bind(on_release=lambda x, name=n: self.unblock(name))
            ct.add_widget(btn)
        sc.add_widget(ct); m.add_widget(sc)
        s.add_widget(m); self.root.add_widget(s)

    def unblock(self, n):
        u = self.u()
        if n in u.get("blocked", []): u["blocked"].remove(n)
        self.save(); self.show_blocked()

if __name__ == "__main__":
    MyChat().run()
