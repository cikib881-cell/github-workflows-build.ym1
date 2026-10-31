import tkinter as tk
from tkinter import messagebox, simpledialog
import random, traceback
from uuid import uuid4

BG="#17212B"; HEADER="#17212B"; BLOCK="#242F3D"
TXT="#FFFFFF"; SUB="#7D8B99"; ACC="#5288C1"
MSGME="#2B5278"; MSGOTH="#182533"; RED="#E53935"; GREEN="#4CAF50"

YOUR_PHONE = "+7 928 512 06 98"

user={"name":"","surname":"","phone":YOUR_PHONE,"username":"","reg":False}
chats={}; contacts={}
root=tk.Tk(); root.title("MyChat"); root.geometry("350x650")


def color_for(n):
    c=["#E57373","#81C784","#64B5F6","#FFB74D","#BA68C8","#4DD0E1"]
    return c[sum(ord(x) for x in n)%len(c)] if n else c[0]

def clear():
    for w in root.winfo_children(): w.destroy()

def scroll_area(parent):
    cont=tk.Frame(parent,bg=BG); cont.pack(fill=tk.BOTH,expand=True,padx=5,pady=5)
    cv=tk.Canvas(cont,bg=BG,highlightthickness=0)
    sb=tk.Scrollbar(cont,orient="vertical",command=cv.yview)
    inner=tk.Frame(cv,bg=BG)
    inner.bind("<Configure>",lambda e:cv.configure(scrollregion=cv.bbox("all")))
    cv.create_window((0,0),window=inner,anchor="nw",tags="inner")
    cv.configure(yscrollcommand=sb.set)
    cv.bind("<Configure>",lambda e:cv.itemconfig("inner",width=e.width))
    cv.pack(side=tk.LEFT,fill=tk.BOTH,expand=True); sb.pack(side=tk.RIGHT,fill=tk.Y)
    cv.bind_all("<MouseWheel>",lambda e:cv.yview_scroll(int(-e.delta/120),"units"))
    return cv,inner

def init_default_chats():
    if "Новости" not in chats:
        chats["Новости"] = {
            "type": "channel", "is_admin": True, "blocked": False,
            "anonymous": False, "members": ["Вы", "Подписчики"],
            "messages": []
        }

# ================== РЕГИСТРАЦИЯ ==================
def reg_phone():
    clear(); root.configure(bg=BG)
    tk.Label(root,text="MyChat",font=("Arial",26,"bold"),bg=HEADER,fg=ACC).pack(pady=20)
    f=tk.Frame(root,bg=BG,padx=20,pady=20); f.pack(fill=tk.BOTH,expand=True)
    tk.Label(f,text="Регистрация",font=("Arial",20,"bold"),bg=BG,fg=TXT).pack(pady=(0,5))
    tk.Label(f,text="Введите номер телефона",font=("Arial",12),bg=BG,fg=SUB).pack(pady=(0,15))
    ph=tk.Entry(f,font=("Arial",16),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0,justify="center")
    ph.pack(fill=tk.X,ipady=10); ph.insert(0,YOUR_PHONE); ph.focus_set()
    err=tk.Label(f,text="",font=("Arial",10),bg=BG,fg=RED); err.pack(pady=5)
    def go(e=None):
        d="".join(c for c in ph.get() if c.isdigit())
        if len(d)<10: err.config(text="Мин. 10 цифр"); return
        user["phone"]=ph.get().strip(); reg_code(user["phone"])
    tk.Button(f,text="Получить код",bg=ACC,fg=TXT,relief="flat",bd=0,font=("Arial",14,"bold"),command=go).pack(fill=tk.X,pady=10,ipady=8)
    ph.bind("<Return>",go)

def reg_code(phone):
    clear(); root.configure(bg=BG)
    tk.Label(root,text="Подтверждение",font=("Arial",20,"bold"),bg=HEADER,fg=TXT).pack(pady=20)
    f=tk.Frame(root,bg=BG,padx=20,pady=20); f.pack(fill=tk.BOTH,expand=True)
    tk.Label(f,text=f"Код на {phone}",font=("Arial",12),bg=BG,fg=SUB).pack()
    tk.Label(f,text="(демо: 1234)",font=("Arial",10),bg=BG,fg=ACC).pack(pady=(0,15))
    ce=tk.Entry(f,font=("Arial",20),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0,justify="center")
    ce.pack(fill=tk.X,ipady=10); ce.focus_set()
    err=tk.Label(f,text="",font=("Arial",10),bg=BG,fg=RED); err.pack(pady=5)
    def v(e=None):
        if ce.get().strip()=="1234": reg_name()
        else: err.config(text="Неверный код")
    tk.Button(f,text="Подтвердить",bg=ACC,fg=TXT,relief="flat",bd=0,font=("Arial",14,"bold"),command=v).pack(fill=tk.X,pady=10,ipady=8)
    ce.bind("<Return>",v)

def reg_name():
    clear(); root.configure(bg=BG)
    tk.Label(root,text="Последний шаг",font=("Arial",20,"bold"),bg=HEADER,fg=TXT).pack(pady=20)
    f=tk.Frame(root,bg=BG,padx=20,pady=20); f.pack(fill=tk.BOTH,expand=True)
    tk.Label(f,text="Имя",font=("Arial",14),bg=BG,fg=TXT).pack(anchor="w")
    ne=tk.Entry(f,font=("Arial",14),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0)
    ne.pack(fill=tk.X,ipady=8,pady=(0,15)); ne.focus_set()
    tk.Label(f,text="Фамилия",font=("Arial",14),bg=BG,fg=TXT).pack(anchor="w")
    se=tk.Entry(f,font=("Arial",14),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0)
    se.pack(fill=tk.X,ipady=8,pady=(0,15))
    err=tk.Label(f,text="",font=("Arial",10),bg=BG,fg=RED); err.pack(pady=5)
    def fin():
        n=ne.get().strip(); s=se.get().strip()
        if not n: err.config(text="Введите имя"); return
        user["name"]=n; user["surname"]=s
        en_name = "".join(c for c in n.lower() if c.isascii() and c.isalpha()) or "user"
        user["username"]=f"@{en_name}{random.randint(100,999)}"
        user["reg"]=True
        init_default_chats()
        show_chats()
    tk.Button(f,text="Завершить",bg=GREEN,fg=TXT,relief="flat",bd=0,font=("Arial",14,"bold"),command=fin).pack(fill=tk.X,pady=10,ipady=8)

# ================== НАВИГАЦИЯ ==================
def nav_bar(active):
    n=tk.Frame(root,bg=BLOCK,pady=10); n.pack(fill=tk.X,side=tk.BOTTOM)
    for t,k,c in [("Чаты","chats",show_chats),("Контакты","contacts",show_contacts),("Настройки","settings",show_settings),("Профиль","profile",show_profile)]:
        col = ACC if k==active else SUB
        tk.Button(n,text=t,bg=BLOCK,fg=col,relief="flat",bd=0,highlightthickness=0,font=("Arial",9,"bold"),command=c).pack(side=tk.LEFT,expand=True,fill=tk.X)

def show_chats(q=""):
    if not user["reg"]: return reg_phone()
    clear(); root.configure(bg=BG)
    h=tk.Frame(root,bg=HEADER,pady=15,padx=10); h.pack(fill=tk.X)
    tk.Label(h,text="MyChat",font=("Arial",22,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT)
    tk.Button(h,text="+",bg=HEADER,fg=ACC,relief="flat",bd=0,font=("Arial",24,"bold"),command=create_page).pack(side=tk.RIGHT,padx=5)
    
    sf=tk.Frame(root,bg=BLOCK,pady=5,padx=10); sf.pack(fill=tk.X,padx=10,pady=5)
    se=tk.Entry(sf,bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0,font=("Arial",12))
    se.pack(side=tk.LEFT,fill=tk.X,expand=True); se.insert(0,q)
    se.bind("<Return>",lambda e:show_chats(se.get().strip()))
    tk.Button(sf,text="🔍",bg=BLOCK,fg=SUB,relief="flat",bd=0,command=lambda:show_chats(se.get().strip())).pack(side=tk.RIGHT)
    
    cv,inner=scroll_area(root)
    ql=q.lower(); found=False
    for name,data in chats.items():
        if ql and (ql not in name.lower() or data.get("anonymous")): continue
        found=True
        row=tk.Frame(inner,bg=BG,pady=2); row.pack(fill=tk.X,pady=2)
        c=tk.Frame(row,bg=BG); c.pack(fill=tk.X,padx=5,pady=5)
        tk.Label(c,text=name[0].upper() if name else "?",font=("Arial",14,"bold"),bg=color_for(name),fg="white",width=2).pack(side=tk.LEFT,padx=(0,10))
        tf=tk.Frame(c,bg=BG); tf.pack(side=tk.LEFT,fill=tk.X,expand=True)
        title=name+(" 🔒" if data.get("blocked") else "")+(" 🕵" if data.get("anonymous") else "")
        tk.Label(tf,text=title,font=("Arial",14,"bold"),bg=BG,fg=TXT,anchor="w").pack(fill=tk.X)
        last="Нет сообщений"
        for m in reversed(data["messages"]):
            if "me" not in m.get("deleted_for",set()): last=m["text"]; break
        tk.Label(tf,text=last,font=("Arial",12),bg=BG,fg=SUB,anchor="w").pack(fill=tk.X)
        def ba(w,n=name):
            w.bind("<Button-1>",lambda e:show_chat(n))
            w.bind("<Button-3>",lambda e:manage_chat(n))
            for ch in w.winfo_children(): ba(ch,n)
        ba(row)
    if not found: tk.Label(inner,text="Ничего не найдено",bg=BG,fg=SUB,font=("Arial",12)).pack(pady=20)
    nav_bar("chats")

# ================== ЧАТ ==================
def show_chat(name):
    if not user["reg"]: return reg_phone()
    cd=chats.get(name)
    if cd is None: return show_chats()
    clear(); root.configure(bg=BG)
    h=tk.Frame(root,bg=HEADER,pady=10,padx=10); h.pack(fill=tk.X)
    tk.Button(h,text="<",bg=HEADER,fg=TXT,relief="flat",bd=0,font=("Arial",20),command=show_chats).pack(side=tk.LEFT)
    tk.Label(h,text=name,font=("Arial",14,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT,padx=10)
    
    tk.Button(h,text="⚙",bg=HEADER,fg=SUB,relief="flat",bd=0,font=("Arial",16),command=lambda:manage_chat(name)).pack(side=tk.RIGHT,padx=5)
    
    cv,inner=scroll_area(root)
    for m in cd["messages"]:
        if "me" in m.get("deleted_for",set()): continue
        is_me=m["sender"]=="me"
        bg=MSGME if is_me else MSGOTH
        mf=tk.Frame(inner,bg=bg,pady=5,padx=10); mf.pack(anchor="e" if is_me else "w",pady=3,padx=5)
        lb=tk.Label(mf,text=m["text"],font=("Arial",12),bg=bg,fg=TXT,wraplength=250,justify="left"); lb.pack()
        def oc(e,msg=m): msg_actions(name,msg)
        for w in (mf,lb): w.bind("<Button-1>",oc)
    root.update_idletasks(); cv.yview_moveto(1.0)
    
    bp=tk.Frame(root,bg=BG,pady=5,padx=5); bp.pack(fill=tk.X,side=tk.BOTTOM)
    ip=tk.Frame(bp,bg=BLOCK,pady=5,padx=5); ip.pack(side=tk.LEFT,fill=tk.X,expand=True)
    en=tk.Entry(ip,font=("Arial",12),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0,highlightthickness=0)
    en.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=5)
    if cd.get("blocked"):
        en.config(state="disabled"); en.insert(0,"Чат заблокирован"); en.config(fg=SUB)
    else:
        def send(e=None):
            t=en.get().strip()
            if not t: return
            cd["messages"].append({"id":str(uuid4()),"text":t,"sender":"me","deleted_for":set()})
            show_chat(name)
        en.bind("<Return>",send)
        tk.Button(ip,text=">",bg=ACC,fg=TXT,relief="flat",bd=0,font=("Arial",16,"bold"),width=3,command=send).pack(side=tk.RIGHT,padx=(2,5),ipady=8)
        en.focus_set()

def msg_actions(cn,msg):
    c=chats[cn]; can=msg["sender"]=="me" or c.get("is_admin",False)
    w=tk.Toplevel(root); w.title("Сообщение"); w.configure(bg=HEADER); w.resizable(False,False)
    def dm(): msg.setdefault("deleted_for",set()).add("me"); w.destroy(); show_chat(cn)
    def da(): 
        try: c["messages"].remove(msg)
        except ValueError: pass
        w.destroy(); show_chat(cn)
    tk.Button(w,text="Удалить у себя",bg=BLOCK,fg=TXT,relief="flat",bd=0,font=("Arial",12),command=dm).pack(pady=8,fill=tk.X,padx=20,ipady=4)
    if can: tk.Button(w,text="Удалить у всех",bg=RED,fg=TXT,relief="flat",bd=0,font=("Arial",12),command=da).pack(pady=8,fill=tk.X,padx=20,ipady=4)
    tk.Button(w,text="Отмена",bg=BLOCK,fg=SUB,relief="flat",bd=0,font=("Arial",12),command=w.destroy).pack(pady=8,fill=tk.X,padx=20,ipady=4)

def manage_chat(name):
    c=chats.get(name)
    if not c: return
    w=tk.Toplevel(root); w.title("Управление чатом"); w.configure(bg=HEADER); w.resizable(False,False)
    def dc():
        if messagebox.askyesno("Удалить",f"Удалить '{name}'?"): del chats[name]; w.destroy(); show_chats()
    def tg(): c["blocked"]=not c["blocked"]; w.destroy(); show_chat(name)
    
    tk.Button(w,text=("Разблокировать" if c["blocked"] else "Заблокировать"),bg=BLOCK,fg=TXT,relief="flat",bd=0,font=("Arial",12),command=tg).pack(pady=5,fill=tk.X,padx=20,ipady=4)
    if c.get("is_admin"):
        tk.Button(w,text="Удалить чат",bg=RED,fg=TXT,relief="flat",bd=0,font=("Arial",12),command=dc).pack(pady=5,fill=tk.X,padx=20,ipady=4)
    tk.Button(w,text="Отмена",bg=BLOCK,fg=SUB,relief="flat",bd=0,font=("Arial",12),command=w.destroy).pack(pady=5,fill=tk.X,padx=20,ipady=4)

# ================== СОЗДАНИЕ ЧАТА ==================
def create_page():
    clear(); root.configure(bg=BG)
    h=tk.Frame(root,bg=HEADER,pady=15,padx=10); h.pack(fill=tk.X)
    tk.Button(h,text="<",bg=HEADER,fg=TXT,relief="flat",bd=0,font=("Arial",18),command=show_chats).pack(side=tk.LEFT,padx=10)
    tk.Label(h,text="Создать",font=("Arial",20,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT)
    st={"bg":BLOCK,"fg":TXT,"relief":"flat","bd":0,"font":("Arial",14),"pady":15}
    tk.Button(root,text="Создать группу",command=lambda:create_chat(False),**st).pack(fill=tk.X,padx=20,pady=10)
    tk.Button(root,text="Создать канал",command=lambda:create_chat(True),**st).pack(fill=tk.X,padx=20,pady=10)

def create_chat(is_channel):
    clear(); root.configure(bg=BG)
    members=["Вы (создатель)"]
    h=tk.Frame(root,bg=HEADER,pady=10,padx=10); h.pack(fill=tk.X)
    tk.Button(h,text="Отмена",bg=HEADER,fg=ACC,relief="flat",bd=0,font=("Arial",12),command=create_page).pack(side=tk.LEFT)
    tk.Label(h,text=("Новый канал" if is_channel else "Новая группа"),font=("Arial",18,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT,padx=20)
    c=tk.Frame(root,bg=BG,pady=10,padx=15); c.pack(fill=tk.BOTH,expand=True)
    tk.Label(c,text="Название",bg=BG,fg=ACC,font=("Arial",12)).pack(anchor="w")
    et=tk.Entry(c,font=("Arial",14),bg=BLOCK,fg=TXT,insertbackground=TXT,relief="flat",bd=0)
    et.pack(fill=tk.X,pady=5,ipady=8); et.insert(0,"Введите название...")
    tk.Label(c,text="Участники",bg=BG,fg=ACC,font=("Arial",12)).pack(anchor="w",pady=(10,0))
    lm=tk.Label(c,text=", ".join(members),bg=BLOCK,fg=TXT,anchor="w",padx=10,pady=10); lm.pack(fill=tk.X,pady=5)
    def add():
        nm=simpledialog.askstring("Участник","Имя:")
        if nm and nm.strip() and nm.strip() not in members: members.append(nm.strip()); lm.config(text=", ".join(members))
    tk.Button(c,text="+ Добавить",bg=BLOCK,fg=TXT,relief="flat",bd=0,font=("Arial",12),command=add).pack(fill=tk.X,pady=5,ipady=5)
    av=tk.BooleanVar()
    if is_channel: tk.Checkbutton(c,text="Анонимный",variable=av,bg=BG,fg=TXT,selectcolor=BLOCK,activebackground=BG,activeforeground=TXT,bd=0).pack(anchor="w",pady=10)
    def fin():
        t=et.get().strip()
        if not t or t=="Введите название...": messagebox.showwarning("Ошибка","Введите название!"); return
        if t in chats: messagebox.showerror("Ошибка","Чат уже существует"); return
        chats[t]={"type":"channel" if is_channel else "group","is_admin":True,"blocked":False,"anonymous":av.get() if is_channel else False,"members":members[:],"messages":[]}
        show_chats()
    tk.Button(root,text="Создать",bg=ACC,fg=TXT,relief="flat",bd=0,font=("Arial",16,"bold"),command=fin).pack(fill=tk.X,side=tk.BOTTOM,pady=20,padx=20,ipady=10)

# ================== КОНТАКТЫ И ПРОФИЛИ ==================
def show_contacts():
    if not user["reg"]: return reg_phone()
    clear(); root.configure(bg=BG)
    h=tk.Frame(root,bg=HEADER,pady=15,padx=10); h.pack(fill=tk.X)
    tk.Label(h,text="Контакты",font=("Arial",22,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT)
    tk.Button(h,text="+",bg=HEADER,fg=ACC,relief="flat",bd=0,font=("Arial",24,"bold"),command=add_contact).pack(side=tk.RIGHT,padx=5)
    
    cv,inner=scroll_area(root)
    for orig,info in contacts.items():
        row=tk.Frame(inner,bg=BG,pady=2); row.pack(fill=tk.X,pady=2)
        c=tk.Frame(row,bg=BG); c.pack(fill=tk.X,padx=5,pady=5)
        d=info["display_name"]
        tk.Label(c,text=d[0].upper() if d else "?",font=("Arial",14,"bold"),bg=color_for(d),fg="white",width=2).pack(side=tk.LEFT,padx=(0,10))
        tf=tk.Frame(c,bg=BG); tf.pack(side=tk.LEFT,fill=tk.X,expand=True)
        tk.Label(tf,text=d,font=("Arial",14,"bold"),bg=BG,fg=TXT,anchor="w").pack(fill=tk.X)
        tk.Label(tf,text=info.get("phone","") or f"Оригинал: {orig}",font=("Arial",10),bg=BG,fg=SUB,anchor="w").pack(fill=tk.X)
        def ba(w,o=orig):
            w.bind("<Button-1>",lambda e:view_profile(o, is_contact=True))
            for ch in w.winfo_children(): ba(ch,o)
        ba(row)
    nav_bar("contacts")

def add_contact():
    o=simpledialog.askstring("Контакт","Имя в системе:")
    if not o or not o.strip(): return
    o=o.strip(); p=simpledialog.askstring("Контакт","Телефон (необязательно):") or ""
    contacts[o]={"display_name":o,"phone":p.strip()}; show_contacts()

# ================== ПРОСМОТР ПРОФИЛЯ (Собеседник) ==================
def view_profile(name, is_contact=True):
    clear(); root.configure(bg=BG)
    info = contacts.get(name) if is_contact else None
    disp_name = info["display_name"] if info else name
    
    h=tk.Frame(root,bg=HEADER,pady=15,padx=10); h.pack(fill=tk.X)
    tk.Button(h,text="<",bg=HEADER,fg=TXT,relief="flat",bd=0,font=("Arial",20),command=show_contacts if is_contact else show_chats).pack(side=tk.LEFT)
    
    tk.Label(root,text=disp_name[0].upper() if disp_name else "?",font=("Arial",32,"bold"),bg=color_for(disp_name),fg="white",width=3,height=1).pack(pady=30)
    tk.Label(root,text=disp_name,font=("Arial",18,"bold"),bg=BG,fg=TXT).pack()
    if info and info.get("phone"): tk.Label(root,text=info["phone"],font=("Arial",12),bg=BG,fg=SUB).pack(pady=5)
    
    f=tk.Frame(root,bg=BG,padx=20,pady=20); f.pack(fill=tk.BOTH,expand=True)
    
    def change_name():
        new_name = simpledialog.askstring("Имя", "Как сохранить имя для этого контакта?", initialvalue=disp_name)
        if new_name and new_name.strip():
            if is_contact: contacts[name]["display_name"] = new_name.strip()
            view_profile(name, is_contact)
            
    def delete_contact():
        if messagebox.askyesno("Удалить", "Удалить контакт?"):
            if is_contact and name in contacts: del contacts[name]
            show_contacts()

    if is_contact:
        tk.Button(f,text="✏️ Поменять имя",bg=BLOCK,fg=TXT,relief="flat",bd=0,font=("Arial",13),command=change_name).pack(fill=tk.X,pady=5,ipady=8)
        tk.Button(f,text="🗑️ Удалить контакт",bg=RED,fg=TXT,relief="flat",bd=0,font=("Arial",13),command=delete_contact).pack(fill=tk.X,pady=5,ipady=8)

# ================== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ (Мой) ==================
def show_profile():
    if not user["reg"]: return reg_phone()
    clear(); root.configure(bg=BG)
    tk.Label(root,text=user["name"][0].upper() if user["name"] else "?",font=("Arial",32,"bold"),bg=color_for(user["name"]),fg="white",width=3,height=1).pack(pady=20)
    tk.Label(root,text=f"{user['name']} {user['surname']}".strip(),font=("Arial",18,"bold"),bg=BG,fg=TXT).pack()
    tk.Label(root,text=user["phone"],font=("Arial",11),bg=BG,fg=SUB).pack(pady=5)
    tk.Label(root,text=user["username"],font=("Arial",11),bg=BG,fg=ACC).pack()
    nav_bar("profile")

def show_settings():
    if not user["reg"]: return reg_phone()
    clear(); root.configure(bg=BG)
    h=tk.Frame(root,bg=HEADER,pady=15,padx=10); h.pack(fill=tk.X)
    tk.Label(h,text="Настройки",font=("Arial",22,"bold"),bg=HEADER,fg=TXT).pack(side=tk.LEFT)
    f=tk.Frame(root,bg=BG,padx=20,pady=20); f.pack(fill=tk.BOTH,expand=True)
    def lo():
        if messagebox.askyesno("Выход","Выйти из аккаунта?"):
            user.update({"name":"","surname":"","phone":YOUR_PHONE,"username":"","reg":False})
            chats.clear(); contacts.clear(); reg_phone()
    tk.Button(f,text="Выйти из аккаунта",bg=RED,fg=TXT,relief="flat",bd=0,font=("Arial",13,"bold"),command=lo).pack(fill=tk.X,pady=10,ipady=8)
    nav_bar("settings")

try:
    show_chats()
    root.mainloop()
except Exception as e:
    traceback.print_exc()
    try: messagebox.showerror("Ошибка",f"{type(e).__name__}: {e}")
    except Exception: pass
