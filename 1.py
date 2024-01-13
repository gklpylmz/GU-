from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import pypyodbc
from datetime import datetime
from plaka_algoritma import plaka_Konum
from plakatanimasistemi import plakaTani

db =pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-IPR9NU0\SQLEXPRESS;'
    'Database=DB_Otopark;'
    'Trusted_Connection=True'
)
imlec = db.cursor()

#########Sorgular################
def plakaBilgiSorgu():
    imlec.execute("SELECT * FROM Tbl_Plaka")
    veriler = imlec.fetchall()

    columns3 = ("ID",'Plaka','Plaka Sahibi','İletişim')
    treeview3 = ttk.Treeview(tk, columns=columns3,height=7, show='headings',)
    for col in columns3:
        treeview3.heading(col, text=col)
        treeview3.column(col, anchor='center',width=120)
    for item in veriler:
        treeview3.insert('',index=0,values=item)

    treeview3.place(x=750,y=550)

def girisBilgiSorgu():
    imlec.execute("SELECT logID,plakaDeger,logSaat,logDurum FROM Tbl_Log INNER JOIN Tbl_Plaka ON Tbl_Log.plakaID=Tbl_Plaka.plakaID WHERE logDurum='Giriş'")
    girisbilgi = imlec.fetchall()
    columns = ("ID",'Plaka', 'Saat','Durum')
    treeview = ttk.Treeview(tk, columns=columns,height=10, show='headings',)
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor='center',width=120)
    
    for item in girisbilgi:
        treeview.insert('',index=0,values=item)

    treeview.place(x=750,y=30)

def cikisBilgiSorgu():
    imlec.execute("SELECT logID,plakaDeger,logSaat,logDurum FROM Tbl_Log INNER JOIN Tbl_Plaka ON Tbl_Log.plakaID=Tbl_Plaka.plakaID WHERE logDurum='Çıkış'")
    cikisbilgi = imlec.fetchall()
    columns2 = ("ID",'Plaka', 'Saat','Durum')
    treeview2 = ttk.Treeview(tk, columns=columns2,height=10, show='headings',)
    for col in columns2:
        treeview2.heading(col, text=col)
        treeview2.column(col, anchor='center',width=120)

    for item in cikisbilgi:
        treeview2.insert('',index=0,values=item)

    treeview2.place(x=750,y=300)





tk = Tk()
tk.title("Otopark Sistemi")
tk.geometry("1280x720")




#Fonksiyonlar

def buton(bilgiler):
    selected_value = selected_option.get()
    for item in bilgiler:
        labelPlaka.config(text="Plaka Bilgisi : "+item[1])
        labelPlakaSahip.config(text="Araç Sahibi : "+item[2])

def girisYap():
    selected_value = selected_option.get()
    if selected_value=="Giriş":
        insertGiris="INSERT INTO Tbl_Log (logSaat,logDurum,plakaID) VALUES (?,?,?)"
        saatdeger=datetime.now()
        saat=saatdeger.strftime("%H:%M")
        durum="Giriş"
        print(plakaid)
        plaka=plakaid
        print(plaka)
        imlec.execute(insertGiris,(saat,durum,plaka))
        db.commit()
        girisBilgiSorgu()
    elif selected_value == "Çıkış":
        insertGiris="INSERT INTO Tbl_Log (logSaat,logDurum,plakaID) VALUES (?,?,?)"
        saatdeger=datetime.now()
        saat=saatdeger.strftime("%H:%M")
        durum="Çıkış"
        plaka=plakaid
        imlec.execute(insertGiris,(saat,durum,plaka))
        db.commit()
        cikisBilgiSorgu()


    



def dosya_sec():
    dosya_yolu = filedialog.askopenfilename(title="Dosya Seç", filetypes=[("Tüm Dosyalar", "*.*")])
    global plakaid
    if dosya_yolu:
        print("Seçilen resim:", dosya_yolu)
        isim =dosya_yolu[36:]#Normalveriseti path len6
        img = cv2.imread("veriseti/"+isim)
        img = cv2.resize(img,(500,500))

        plaka,resim = plaka_Konum(img)
        plakaImg, plakaKarakter = plakaTani(img, plaka)

        print("Resimdeki plaka:", plakaKarakter)
        pil_img = Image.fromarray(resim)
        pil_img = pil_img.resize((400, 400), Image.LANCZOS)
        foto_tk = ImageTk.PhotoImage(pil_img)
        lmain.config(image=foto_tk)
        lmain.image = foto_tk

        plakastring ="".join(plakaKarakter)
        print(plakastring)
        imlec.execute(f"SELECT * FROM Tbl_Plaka WHERE plakaDeger='{plakastring}'")
        bilgiler=imlec.fetchall()
        print(bilgiler)
        if bilgiler==[]:
            labelPlaka.config(text="Plaka : Plaka Kayıtlı Değil "+plakastring)
        else:
            plakaid=bilgiler[0][0]
            labelPlaka.config(text="Plaka : "+plakastring)
        buton(bilgiler)   


#Kamera Label
lmain = Label(tk,width=400,height=400)
lmain.place(x=10,y=50)




#Treewiew Giriş
labelGiris = Label(tk,text="Giriş ")
labelGiris.place(x=750,y=10)
girisBilgiSorgu()

#Treewiew Çıkış
labelCikis = Label(tk,text="Çıkış")
labelCikis.place(x=750,y=270)
cikisBilgiSorgu()

#Treewiew Bilgiler
labelBilgi = Label(tk,text="Araç Bilgileri")
labelBilgi.place(x=750,y=530)
plakaBilgiSorgu()




btnPTS = Button(tk,
            text="Fotoğraf Seç",
            padx="80",pady="5",
            command=dosya_sec)
btnPTS.place(x=20,y=10)


selected_option = StringVar()
radio_button1 = ttk.Radiobutton(tk, text="Giriş", variable=selected_option, value="Giriş")
radio_button1.place(x=20,y=500)

radio_button2 = ttk.Radiobutton(tk, text="Çıkış", variable=selected_option, value="Çıkış")
radio_button2.place(x=200,y=500)

labelPlaka = Label(tk,text="Plaka :")
labelPlaka.place(x=20,y=550)

labelPlakaSahip = Label(tk,text="Araç Sahibi:")
labelPlakaSahip.place(x=20,y=580)


btnKaydet = Button(tk,
            text="Giriş/Çıkış",
            padx="20",pady="20",
            command=girisYap)
btnKaydet.place(x=60,y=630)


tk.mainloop()
db.close()
