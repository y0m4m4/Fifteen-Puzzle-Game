#__________________________IMPORTING MODULES__________________________#
from tkinter import *
from tkinter import messagebox,simpledialog
from PIL import Image,ImageTk
from pygame import mixer
import random
mixer.init()

#______________________________FUNCTIONS______________________________#

def main_menu(b): #vytvorenie hlavného menu
    if b:
        if effects_on:
            press.play()
    canvas.delete('all')
    canvas.create_text(498,153,text='F1FT33N',font=('Century Gothic',100,'bold'),fill='darkred')
    canvas.create_text(500,150,text='F1FT33N',font=('Century Gothic',100,'bold'),fill='crimson')
    canvas.create_window(500,290,window=button_newgame)
    canvas.create_window(500,350,window=button_highscore)
    canvas.create_window(500,410,window=button_options)
    canvas.create_window(500,470,window=button_quit)

def new_game_menu(): #vytvorenie úvodného menu do novej hry
    global end,running
    if effects_on:
        press.play()
    end = True
    running = False
    try:
        pop.destroy()
    except:
        pass
    canvas.delete('all')
    canvas.create_text(500,130,text='choose difficulty:',font=('Courier',30,'bold'))
    canvas.create_window(30,30,anchor='nw',window=button_back_1)
    for i in range(3):
        canvas.create_window(250*(i+1),450,window=newgame_buttons[i])
        thumbnail = Label(root,image=thumbnails[theme][i])
        canvas.create_window(250*(i+1),300,window=thumbnail)
        thumbnail.bind('<Button-1>',lambda e,mode=i+3: new_game(mode,False))
        
def new_game(mode,b): #vytvorenie novej hry podla zvoleného módu (obtiažnosti)
    global start,end,moves,time,running
    if b:
        if effects_on:
            press.play()
    start = False
    end = False
    moves = StringVar()
    moves.set(0)
    time = 0.0
    running = False
    canvas.delete('all')
    canvas.create_window(180,120,anchor='nw',window=game_frames[mode-3])
    for widget in game_frames[mode-3].winfo_children():
        widget.destroy()
    game_screen(mode)
    create_labels(mode)

def mode_name(mode): #z číselnej hodnoty módu vráti názov módu a opačne (3='easy',4='normal',5='hard')
    if mode == 3:
        return('easy')
    if mode == 4:
        return('normal')
    if mode == 5:
        return('hard')
    if mode == 'easy':
        return(3)
    if mode == 'normal':
        return(4)
    if mode == 'hard':
        return(5)

def record(mode,type): #nájde a vráti rekordný čas alebo počet ťahov (type) v danom móde
    top = '-'
    with open('score.txt','r') as file:
        for line in file:
            if line.split()[0] == mode_name(mode):
                current = float(line.split()[1+type])
                if top == '-' or top > current:
                    top = current
    if type == 1 and top != '-':
        top = int(top)
    return(top)

def change_record_label(): #strieda zobrazenie rekordu v čase alebo počtu ťahov v ukazovateli
    global record_type
    if not end:
        record_type = (record_type+1)%2
        record_label['text'] = record(record_mode,record_type)
        if record_type == 1:
            frame_record['text'] = ' Record Moves '
        if record_type == 0:
            frame_record['text'] = ' Record Time '
        
def start_time(): #spustí časomieru
    global running
    running = True
    def count():
        if running:
            global time
            time = round(time+0.1,1)
            time_label['text'] = str(round(time,1))
            time_label.after(100,count)
    count()

def show_solved(mode): #otvorí okno s náhľadom pre poskladané puzzle
    global pop,thumbnail
    if effects_on:
        press.play()
    try:
        pop.destroy()
    except:
        pass
    pop = Toplevel(root)
    pop.title('Solved Puzzle')
    pop.iconbitmap('images/pop.ico')
    thumbnail = PhotoImage(file=f'images/thumbnails/theme_{theme}/{mode_name(mode)}.png')
    Label(pop,image=thumbnail,borderwidth=0).pack()

def game_screen(mode): #vytvorí hernú plochu pre daný mód
    global record_type,record_mode,record_label,time_label
    record_type = 0
    record_mode = mode
    canvas.create_text(499,51,text='F1FT33N',font=('Century Gothic',40,'bold'),fill='darkred')
    canvas.create_text(500,50,text='F1FT33N',font=('Century Gothic',40,'bold'),fill='crimson')
    canvas.create_window(30,30,anchor='nw',window=button_back_2)
    canvas.create_rectangle(700,0,1000,600,fill='peachpuff',width=0)
    canvas.create_window(850,100,window=frame_mode)
    canvas.create_window(850,200,window=frame_record)
    canvas.create_window(850,300,window=frame_time)
    canvas.create_window(850,400,window=frame_moves)
    solved = Frame(root,width=49,height=49)
    Button(solved,text='L',font=('Webdings',22,'bold'),foreground='darkred',background='salmon',command=lambda: show_solved(mode)).place(x=0,y=0,width=49,height=49)
    canvas.create_window(160,30,anchor='nw',window=solved)
    restart = Button(root,text='Restart',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=lambda: new_game(mode,True))
    canvas.create_window(850,500,window=restart)
    for widget in frame_mode.winfo_children() + frame_record.winfo_children() + frame_time.winfo_children() + frame_moves.winfo_children():
        widget.destroy()
    Label(frame_mode,width=10,text=mode_name(mode).capitalize(),font=('Courier',26,'bold'),background='peachpuff').grid()
    record_label = Label(frame_record,width=10,text=record(mode,record_type),font=('Courier',26,'bold'),background='peachpuff')
    record_label.bind('<Button-1>',lambda e: change_record_label())
    record_label.grid()
    time_label = Label(frame_time,width=10,text=str(time),font=('Courier',26,'bold'),background='peachpuff')
    time_label.grid()
    Label(frame_moves,width=10,textvariable=moves,font=('Courier',26,'bold'),background='peachpuff').grid()

def create_labels(mode): #vytvorí štvorčeky v hre podľa módu, zároveň nastaví ovládanie na tlačidlo myši a klávesy
    global right_order,order,labels
    right_order = list(range(1,mode**2))+[0]
    order = list(range(1,mode**2))+[0]
    labels = (mode**2)*[0]
    for i in range(1,mode**2):
        index = order.index(i)
        lbl = label(mode,i)
        lbl.bind('<Button-1>',lambda e,n=i,m=mode: click(n,m))
        labels[index] = lbl
        lbl.grid(row=index//mode,column=index%mode,sticky='nesw')
    shuffle_labels(mode)
    root.bind('<Right>',lambda e,m=mode: right_key(m))
    root.bind('<Left>',lambda e,m=mode: left_key(m))
    root.bind('<Up>',lambda e,m=mode: up_key(m))
    root.bind('<Down>',lambda e,m=mode: down_key(m))

def label(mode,i): #vytvorí jeden štvorček podľa módu,poradia a motívu
    if theme == 0:
        lbl = Label(game_frames[mode-3],text=str(i),font=('Century Gothic',80-mode*10,'bold'),borderwidth=8-mode,relief='raised')
    if theme in (1,2,3):
        i -= 1
        color = [0,0,0]
        color[(theme-1)%3] = 255-(i//mode)*(255//(mode-1))
        color[theme%3] = 255-(i%mode)*(255//(mode-1))
        color = '#%02x%02x%02x'%tuple(color)
        lbl = Label(game_frames[mode-3],background=color,borderwidth=8-mode,relief='raised')
    if theme in (4,5,6,7):
        img = photo_labels[theme-4][mode-3][i-1]
        lbl = Label(game_frames[mode-3],image=img,borderwidth=8-mode,relief='raised')
    return lbl

def shuffle_labels(mode): #zamieša štvorčeky
    global start
    for i in range((mode**4)):
        empty = order.index(0)
        if empty == 0:
            random.choice([left,up])(mode)
        if empty == mode-1:
            random.choice([right,up])(mode)
        if empty == mode*(mode-1):
            random.choice([left,down])(mode)
        if empty == (mode*mode)-1:
            random.choice([right,down])(mode)
        elif (empty+1)%mode == 1:
            random.choice([left,up,down])(mode)
        elif (empty+1)%mode == 0:
            random.choice([right,up,down])(mode)
        elif empty//mode == mode-1:
            random.choice([right,left,down])(mode)
        elif empty//mode == 0:
            random.choice([right,left,up])(mode)
        else:
            random.choice([right,left,up,down])(mode)
    start = True
       
def right(mode): #pohyb štvorčeka vpravo
    global order,labels,moves
    empty = order.index(0)
    if (empty+1)%mode != 1:
        index = empty-1
        labels[index].grid(row=index//mode,column=index%mode+1,sticky='nesw')
        order[empty],order[index] = order[index],order[empty]
        labels[empty],labels[index] = labels[index],labels[empty]
        if start:
            if effects_on:
                move.play()
            moves.set(int(moves.get())+1)
            if not running:
                start_time()

def left(mode): #pohyb štvorčeka vľavo
    global order,labels,moves
    empty = order.index(0)
    if (empty+1)%mode != 0:
        index = empty+1
        labels[index].grid(row=index//mode,column=index%mode-1,sticky='nesw')
        order[empty],order[index] = order[index],order[empty]
        labels[empty],labels[index] = labels[index],labels[empty]
        if start:
            if effects_on:
                move.play()
            moves.set(int(moves.get())+1)
            if not running:
                start_time()

def up(mode): #pohyb štvorčeka hore
    global order,labels,moves
    empty = order.index(0)
    if empty//mode != mode-1:
        index = empty+mode
        labels[index].grid(row=index//mode-1,column=index%mode,sticky='nesw')
        order[empty],order[index] = order[index],order[empty]
        labels[empty],labels[index] = labels[index],labels[empty]
        if start:
            if effects_on:
                move.play()
            moves.set(int(moves.get())+1)
            if not running:
                start_time()

def down(mode): #pohyb štvorčeka dole
    global order,labels,moves
    empty = order.index(0)
    if empty//mode != 0:
        index = empty-mode
        labels[index].grid(row=index//mode+1,column=index%mode,sticky='nesw')
        order[empty],order[index] = order[index],order[empty]
        labels[empty],labels[index] = labels[index],labels[empty]
        if start:
            if effects_on:
                move.play()
            moves.set(int(moves.get())+1)
            if not running:
                start_time()

def click(n,mode): #funkcia pre tlačidlo myši (posúvanie štvorčekov)
    if not end:
        global order,labels
        index = order.index(n)
        try:
            if (index+1)%mode!=0 and order[index+1]==0:
                right(mode) 
        except:
            pass
        try:
            if order[index-mode]==0:
                up(mode)
        except:
            pass
        try:
            if (index+1)%mode!=1 and order[index-1]==0:
                left(mode)
        except:
            pass
        try:
            if order[index+mode]==0:
                down(mode)
        except:
            pass
        check_win(mode)

def right_key(mode): #funkcia pre klávesu šípka vpravo
    if not end:
        right(mode)
        check_win(mode)

def left_key(mode): #funkcia pre klávesu šípka vľavo
    if not end:
        left(mode)
        check_win(mode)

def up_key(mode): #funkcia pre klávesu šípka hore
    if not end:
        up(mode)
        check_win(mode)

def down_key(mode): #funkcia pre klávesu šípka dole
    if not end:
        down(mode)
        check_win(mode)

def check_win(mode): #skontroluje či sú štvorčeky usporiadané správne
    global running,end
    if order == right_order:
        if effects_on:
            win.play()
        running = False
        end = True
        name = simpledialog.askstring('Puzzle Solved', f'Congratulations! You solved the {mode_name(mode)} puzzle in:\n{time} seconds, {moves.get()} moves\nEnter your name: (max 10 characters)')
        try:
            if len(name) > 10:
                name = name[:10]
            with open('score.txt','a') as file:
                file.write('{} {} {} {}\n'.format(mode_name(mode),time,moves.get(),name))
            new_game(mode,False)
        except:
            pass

def highscore_menu(): #vytvorí menu pre zobrazenie high score
    global score_modes,score_mode,score_type
    scores = []
    score_modes = [[],[],[]]
    score_mode,score_type = 4,0
    canvas.delete('all')
    canvas.create_text(499,82,text='High Score',font=('Century Gothic',50,'bold'),fill='darkred')
    canvas.create_text(500,80,text='High Score',font=('Century Gothic',50,'bold'),fill='crimson')
    canvas.create_window(30,30,anchor='nw',window=button_back_1)
    for i in range(3):
        canvas.create_window(200+i*140,180,window=highscore_buttons[i])
    for i in range(2):
        canvas.create_window(660+i*140,180,window=highscore_buttons[3+i])
    canvas.create_window(500,520,window=button_delete)
    with open('score.txt') as file:
        for line in file:
            scores.append(tuple(line.split()))
    for (mode,time,moves,name) in scores:
        score_modes[mode_name(mode)-3].append((time,moves,name))
    show_highscore(score_mode,score_type)

def show_highscore(mode,type): #zobrazí high score pre daný mód a typ skóre
    global score_mode,score_type
    if effects_on:
        press.play()
    score_mode,score_type = mode,type
    canvas.delete('score')
    for button in highscore_buttons[:3]:
        if button == highscore_buttons[mode-3]:
            button['background'] = 'khaki'
        else:
            button['background'] = 'salmon'
    for button in highscore_buttons[3:]:
        if button == highscore_buttons[3+type]:
            button['background'] = 'khaki'
        else:
            button['background'] = 'salmon'
    for i in score_modes:
        i.sort(key=lambda tup: float(tup[type]))
    if score_modes[mode-3] == []:
        canvas.create_text(500,350,text='- no score -',font=('Courier',20),tags='score')
    else:
        for i in range(5):
            canvas.create_text(150,250+i*50,text=f'{i+1}. ',font=('Courier',20),anchor='e',tags='score')
            canvas.create_text(580,250+i*50,text=f'{i+6}. ',font=('Courier',20),anchor='e',tags='score')
            try:
                canvas.create_text(150,250+i*50,text=score_modes[mode-3][i][2]+(20-len(score_modes[mode-3][i][2])-len(score_modes[mode-3][i][type]))*'.'+score_modes[mode-3][i][type],font=('Courier',20),anchor='w',tags='score')
            except:
                canvas.create_text(150,250+i*50,text='-',font=('Courier',20),anchor='w',tags='score')
            try:
                canvas.create_text(580,250+i*50,text=score_modes[mode-3][i+5][2]+(20-len(score_modes[mode-3][i+5][2])-len(score_modes[mode-3][i+5][type]))*'.'+score_modes[mode-3][i+5][2],font=('Courier',20),anchor='w',tags='score')
            except:
                canvas.create_text(580,250+i*50,text='-',font=('Courier',20),anchor='w',tags='score')

def delete_score(): #vymaže všetky uložené skóre
    if effects_on:
        press.play()
    result = messagebox.askquestion('Delete Score', 'Are you sure you want to delete all scores?', icon='warning')
    if result == 'yes':
        with open('score.txt','w'):
            pass
        highscore_menu()

def options_menu(): # vytvorenie menu pre nastavenia hry
    if effects_on:
        press.play()
    canvas.delete('all')
    canvas.create_text(499,82,text='Options',font=('Century Gothic',50,'bold'),fill='darkred')
    canvas.create_text(500,80,text='Options',font=('Century Gothic',50,'bold'),fill='crimson')
    canvas.create_window(30,30,anchor='nw',window=button_back_1)
    canvas.create_window(90,160,anchor='nw',window=frame_themes)
    canvas.create_window(740,160,anchor='nw',window=frame_sounds)

def set_theme(n): #nastaví motív štvorčekov (podľa indexu)
    global theme
    if effects_on:
        press.play()
    themes_labels[theme].configure(borderwidth=2,relief='solid')
    themes_labels[theme].grid_configure(padx=20,pady=20)
    themes_labels[n].configure(borderwidth=12,relief='ridge')
    themes_labels[n].grid_configure(padx=0,pady=0)
    theme = n

def set_volume(sound,volume): #nastaví hlasitosť pre zvolený zvuk (hudba alebo efekty)
    global effects_volume,music_volume
    volume = int(volume)/100
    if sound == 'e':
        for sound in effect_sounds:
            sound.set_volume(volume)
    if sound == 'm':
        mixer.music.set_volume(volume)

def turn_sound(sound): #zapne alebo vypne dané zvuky (hudbu alebo efekty)
    global effects_on,music_on
    if sound == 'e':
        effects_on = not effects_on
    if sound == 'm':
        music_on = not music_on
        if music_on:
            mixer.music.play(-1)
        else:
            mixer.music.stop()


#______________________________VARIABLES______________________________#

theme = 0
effects_on,music_on = True,True

# TK, CANVAS:
root = Tk()
root.title("Fifteen Puzzle Game")
root.iconbitmap('images/game.ico')
canvas = Canvas(root,width=1000,height=600,background='beige')
canvas.pack()

#IMAGES:
thumbnails = []
for t in range(8):
    thumbnail_modes = []
    for m in range(3,6):
        img = Image.open(f'images/thumbnails/theme_{t}/{mode_name(m)}.png')
        img.thumbnail((220,220))
        thumbnail_modes.append(ImageTk.PhotoImage(img))
    thumbnails.append(thumbnail_modes)
themes = []
for i in range(8):
    img = Image.open(f'images/themes/theme_{i}.jpg')
    img.thumbnail((100,100))
    themes.append(ImageTk.PhotoImage(img))
photo_labels = []
for t in range(4,8):
    img = Image.open(f'images/themes/theme_{t}.jpg')
    img = img.resize((390,390))
    theme_labels = []
    for m in range(3,6):
        mode_labels = []
        for i in range(m**2-1):
            sizes = tuple([x*(390//m) for x in ((i%m),(i//m),(i%m+1),(i//m+1))])
            img_crop = img.crop((sizes))
            mode_labels.append(ImageTk.PhotoImage(img_crop))
        theme_labels.append(mode_labels)
    photo_labels.append(theme_labels)

#SOUNDS,MUSIC:
press = mixer.Sound('sounds/click.mp3')
move = mixer.Sound('sounds/move.mp3')
win = mixer.Sound('sounds/win.mp3')
effect_sounds = [press,move,win]
mixer.music.load('sounds/bgm.mp3')
mixer.music.set_volume(0.5)

# BUTTONS:
button_newgame = Button(root,text='New Game',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=new_game_menu)
button_highscore = Button(root,text='High Score',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=highscore_menu)
button_options = Button(root,text='Options',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=options_menu)
button_quit = Button(root,text='Quit',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=root.destroy)
button_back_1 = Button(root,text='< Back',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',command=lambda: main_menu(True))
button_back_2 = Button(root,text='< Back',font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',command=new_game_menu)
button_delete = Button(root,text='Delete Score',font=('Century Gothic',15,'bold'),foreground='darkred',background='salmon',width=15,command=delete_score)

newgame_buttons = []
highscore_buttons = []
for i in range(3,6):
    newgame_buttons.append(Button(root,text=mode_name(i).capitalize(),font=('Century Gothic',18,'bold'),foreground='darkred',background='salmon',width=15,command=lambda mode=i: new_game(mode,True)))
    highscore_buttons.append(Button(root,text=mode_name(i).capitalize(),font=('Century Gothic',15,'bold'),foreground='darkred',background='salmon',width=10,command=lambda mode=i: show_highscore(mode,score_type)))
highscore_buttons.append(Button(root,text='Time',font=('Century Gothic',15,'bold'),foreground='darkred',background='salmon',width=10,command=lambda: show_highscore(score_mode,0)))
highscore_buttons.append(Button(root,text='Moves',font=('Century Gothic',15,'bold'),foreground='darkred',background='salmon',width=10,command=lambda: show_highscore(score_mode,1)))


#LABELS,FRAMES...:
frame_easy = Frame(root,height=420,width=420,background='white',borderwidth=7,relief='solid')
for i in range(3):
    frame_easy.grid_columnconfigure(i,minsize=140)
    frame_easy.grid_rowconfigure(i,minsize=140)
frame_normal = Frame(root,height=420,width=420,background='white',borderwidth=7,relief='solid')
for i in range(4):
    frame_normal.grid_columnconfigure(i,minsize=105)
    frame_normal.grid_rowconfigure(i,minsize=105)
frame_hard = Frame(root,height=420,width=420,background='white',borderwidth=7,relief='solid')
for i in range(5):
    frame_hard.grid_columnconfigure(i,minsize=84)
    frame_hard.grid_rowconfigure(i,minsize=84)
game_frames = [frame_easy,frame_normal,frame_hard]

frame_mode = LabelFrame(root,text=' Difficulty ',font=('Century Gothic',14,'bold'),foreground='crimson',background='peachpuff')
frame_time = LabelFrame(root,text=' Time ',font=('Century Gothic',14,'bold'),foreground='crimson',background='peachpuff')
frame_moves = LabelFrame(root,text=' Moves ',font=('Century Gothic',14,'bold'),foreground='crimson',background='peachpuff')
frame_record = LabelFrame(root,text=' Record Time ',font=('Century Gothic',14,'bold'),foreground='crimson',background='peachpuff')
frame_record.bind('<Button-1>',lambda e: change_record_label())

frame_themes = LabelFrame(root,text=' Themes ',font=('Century Gothic',16,'bold'),foreground='crimson',background='beige')
frame_themes.grid_rowconfigure(2,minsize=10)
frame_themes.grid_columnconfigure(0,minsize=10)
frame_themes.grid_columnconfigure(5,minsize=10)
themes_labels = []
for i in range(8):
    if i ==0:
        lbl = Label(frame_themes,image=themes[i],borderwidth=12,relief='ridge')
        lbl.grid(row=i//4,column=i%4+1,padx=0,pady=0)
    else:
        lbl = Label(frame_themes,image=themes[i],relief='solid')
        lbl.grid(row=i//4,column=i%4+1,padx=20,pady=20)
    lbl.bind('<Button-1>',lambda e,n=i: set_theme(n))
    themes_labels.append(lbl)

frame_sounds = LabelFrame(root,text=' Sounds ',font=('Century Gothic',16,'bold'),foreground='crimson',background='beige')
frame_sounds.grid_rowconfigure(2,minsize=15)
effects_scale = Scale(frame_sounds,from_=0,to=100,length=150,font=('Courier',12,'bold'),orient=HORIZONTAL,background='beige',command=lambda v: set_volume('e',v))
effects_scale.grid(padx=10)
effects_button = Checkbutton(frame_sounds,text='Effects',font=('Courier',18,'bold'),background='beige',command=lambda: turn_sound('e'))
effects_button.grid(padx=10,sticky='W')
music_scale = Scale(frame_sounds,from_=0,to=100,length=150,font=('Courier',12,'bold'),orient=HORIZONTAL,background='beige',command=lambda v: set_volume('m',v))
music_scale.grid(row=3,padx=10)
music_button = Checkbutton(frame_sounds,text='Music',font=('Courier',18,'bold'),background='beige',command=lambda: turn_sound('m'))
music_button.grid(row=4,padx=10,sticky='W')
effects_button.select()
music_button.select()
effects_scale.set(50)
music_scale.set(50)

#_________________________RUNNING THE PROGRAM_________________________#
main_menu(False)
mixer.music.play(-1)
root.mainloop()