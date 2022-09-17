import ctypes
from shutil import rmtree
from tkinter import ttk, messagebox, filedialog
from tkinter import *
from tkinter.ttk import *
import os
import sys
from unicodedata import name
import zipfile
import apic as apic

path = sys.path[0]

# 打开文件浏览器，导入文件
def browseFiles():
    filePath = filedialog.askopenfilename(
        initialdir = '/',
        title = 'Select a File',
        filetypes = (('','songlist;*.ipa;*.apk'),
                    ('All','*.*')))
    if filePath.endswith('.apk'):
        unzipFile(filePath)
        processApk()
    elif filePath.endswith('.ipa'):
        unzipFile(filePath)
        processIpa()
    elif filePath.endswith('songlist'):
        processSonglist(filePath)
    else:
        pass

# 解压包体
def unzipFile(filePath):
    if not zipfile.is_zipfile(filePath):
        messagebox.showerror('并非有效的APK或IPA文件')
        return
    os.chdir(path)
    if os.path.exists('temp'):
        rmtree('temp')
    else:    
        os.mkdir('temp')
    with zipfile.ZipFile(filePath, 'r') as zippedPack:
        zippedPack.extractall(path + '/temp/')
    importFileWindow.destroy()

# 打包游戏包
def generateGamePack():
    pass

# 导出songlist
def exportSonglist():
    pass

# 打开歌曲信息编辑窗
def processSongDetail(selectedSong):
    song = {}
    for songInfo in songlist:
        if songInfo['id'] == selectedSong:
            song = songInfo
    if song == {}:
        return
    songEditWindow = Tk()

    songEditWindow.tk.call('tk', 'scaling', ScaleFactor/75)
    songEditWindow.title('ArcPackGUI')
    songEditWindow.geometry('1200x600')

    # 歌曲基础信息导入
    id = song['id']
    defaultName = song['title_localized']['en']
    artist = song['artist']
    bpm = song['bpm']
    baseBpm = song['bpm_base']
    pack = song['set']
    audioPreview = song['audioPreview']
    audioPreviewEnd = song['audioPreviewEnd']
    side = song['side']
    bg = song['bg']
    version = song['version']
    date = song['date']
    difficulties = song['difficulties']

    idLabel = Label(songEditWindow, text = '曲目id').place(relheight = 0.05, rely = 0)
    nameLabel = Label(songEditWindow, text = '曲目名').place(relheight = 0.05, rely = 0.125)
    artistLabel = Label(songEditWindow, text = '作曲').place(relheight = 0.05, rely = 0.25)
    bpmLabel = Label(songEditWindow, text = 'bpm').place(relheight = 0.05, rely = 0.375)
    baseBpmLabel = Label(songEditWindow, text = '基准bpm').place(relheight = 0.05, rely = 0.5)
    packLabel = Label(songEditWindow, text = '曲包').place(relheight = 0.05, rely = 0.625)
    audioPreviewLabel = Label(songEditWindow, text = '音频预览起始').place(relheight = 0.05, rely = 0.75)
    audioPreviewEndLabel = Label(songEditWindow, text = '音频预览停止').place(relheight = 0.05, rely = 0.875)
    sideLabel = Label(songEditWindow, text = '曲目背景侧').place(relheight = 0.05, relx = 0.3, rely = 0)
    bgLabel = Label(songEditWindow, text = '曲目背景id').place(relheight = 0.05, relx = 0.3, rely = 0.125)
    versionLabel = Label(songEditWindow, text = '曲目发布版本').place(relheight = 0.05, relx = 0.3, rely = 0.25)
    dateLabel = Label(songEditWindow, text = '曲目发布时间').place(relheight = 0.05, relx = 0.3, rely = 0.375)
    difficultiesLabel = Label(songEditWindow, text = '曲目难度列表').place(relheight = 0.05, relx = 0.3, rely = 0.5)

    idEntry = Entry(songEditWindow)
    idEntry.insert(0, id)
    idEntry.place(relheight = 0.05, rely = 0, relx = 0.1)
    nameEntry = Entry(songEditWindow)
    nameEntry.insert(0, defaultName)
    nameEntry.place(relheight = 0.05, rely = 0.125, relx = 0.1)
    artistEntry = Entry(songEditWindow)
    artistEntry.insert(0, artist)
    artistEntry.place(relheight = 0.05, rely = 0.25, relx = 0.1)
    bpmEntry = Entry(songEditWindow)
    bpmEntry.insert(0, bpm)
    bpmEntry.place(relheight = 0.05, rely = 0.375, relx = 0.1)
    baseBpmEntry = Entry(songEditWindow)
    baseBpmEntry.insert(0, baseBpm)
    baseBpmEntry.place(relheight = 0.05, rely = 0.5, relx = 0.1)
    packCombobox = Combobox(songEditWindow, values = packlist)
    packCombobox.set(pack)
    packCombobox.place(relheight = 0.05, rely = 0.625, relx = 0.1)
    audioPreviewEntry = Entry(songEditWindow)
    audioPreviewEntry.insert(0, audioPreview)
    audioPreviewEntry.place(relheight = 0.05, rely = 0.75, relx = 0.1)
    audioPreviewEndEntry = Entry(songEditWindow)
    audioPreviewEndEntry.insert(0, audioPreviewEnd)
    audioPreviewEndEntry.place(relheight = 0.05, rely = 0.875, relx = 0.1)

    sideValues = ['光', '对立', '纷争']
    sideCombobox = Combobox(songEditWindow, state = 'readonly', values = sideValues)
    sideCombobox.set(sideValues[side])
    sideCombobox.place(relheight = 0.05, rely = 0, relx = 0.45)
    bgCombobox = Combobox(songEditWindow)
    bgCombobox.set(bg)
    bgCombobox.place(relheight = 0.05, rely = 0.125, relx = 0.45)
    versionEntry = Entry(songEditWindow)
    versionEntry.insert(0, version)
    versionEntry.place(relheight = 0.05, rely = 0.25, relx = 0.45)
    dateEntry = Entry(songEditWindow)
    dateEntry.insert(0, date)
    dateEntry.place(relheight = 0.05, rely = 0.375, relx = 0.45)
    difficultiesTreeview = Treeview(songEditWindow, padding=(0,5,0,5))

    def showDiffDetail(event):
        selectedDiff = songlistTreeview.item(difficultiesTreeview.selection()[0], 'text')
        print(selectedDiff)

    difficultiesTreeview.bind('<Double-1>', showDiffDetail)

    diffTextList = ['Past', 'Present', 'Future', 'Beyond']

    for difficulty in song['difficulties']:
        difficultiesTreeview.insert('', END, text = diffTextList[difficulty['ratingClass']], open = False)

    difficultiesTreeview.place(relheight = 0.2, rely = 0.5, relx = 0.45)
    
    songEditWindow.mainloop()

# 刷新曲目列表
def packEditRefresh():
    for song in songlist:
        if not 'set' in song.keys():
            song['set'] = 'undefined'
        elif type(song['set']) != type(' '):
            song['set'] = 'undefined'
        elif song['set'].lower() not in [y.lower() for y in packlist]:
            packlist.append(song['set'])
    
    if not 'undefined' in packlist:
        packlist.append('undefined')

    d = songlistTreeview.get_children()
    for item in d:
        songlistTreeview.delete(item)
    
    for pack in packlist:
        packSong = songlistTreeview.insert('', END, text = pack, open = False)
        for song in songlist:
            if song['set'] == pack:
                songlistTreeview.insert(packSong, END, text = song['id'], open = False)
    

# 打开包体信息编辑窗
def processGamePackage(songsPath, packType):

    global songlist
    global packlist
    global songlistTreeview
    global packageEditWindow

    packageEditWindow = Tk()
    packageEditWindow.tk.call('tk', 'scaling', ScaleFactor/75)
    packageEditWindow.title('ArcPackGUI')
    packageEditWindow.geometry('400x600')
    
    songlist = apic.resolveSonglist(songsPath + 'songlist')
    packlist = []
    if packType < 2:
        packlist = apic.resolvePacklist(songsPath + 'packlist')
        exportBtn = Button(packageEditWindow, text = '打包游戏包体', command = packEditRefresh)
    else:
        exportBtn = Button(packageEditWindow, text = '导出songlist', command = exportSonglist)
    
    songlistTreeview = Treeview(packageEditWindow, padding=(0,5,0,5))
    songlistTreeview.heading('#0', text = '曲目列表(以曲包分割)')

    packEditRefresh()

    def showSongDetail(event):
        selectedSong = songlistTreeview.item(songlistTreeview.selection()[0], 'text')
        processSongDetail(selectedSong)

    songlistTreeview.bind('<Double-1>', showSongDetail)

    songlistTreeview.pack(fill=BOTH,expand=True)
    exportBtn.pack()

    packageEditWindow.mainloop()

# 解压后初次整备APK文件
def processApk():
    songsPath = path + '/temp/assets/songs/'
    if os.chdir(songsPath):
        messagebox.showerror('并非有效的APK或IPA文件')
    rmtree('../../META-INF')
    processGamePackage(songsPath, 0)

# 解压后初次整备IPA文件
def processIpa():
    songsPath = path + '/temp/Payload/Arc-mobile.app/songs/'
    if os.chdir(songsPath):
        messagebox.showerror('并非有效的APK或IPA文件')
    processGamePackage(songsPath, 1)

# 整备songlist
def processSonglist():
    processGamePackage(path, 2)

def openImportWindow():

    global importFileWindow

    importFileWindow = Tk()

    importFileWindow.call('tk', 'scaling', ScaleFactor/75)
    importFileWindow.title('ArcPackGUI')
    importFileWindow.geometry('450x300')
    importFileWindow['background'] = '#ffffff'

    uploadFileText = Label(importFileWindow, text='请加载Arcaea APK/IPA壳体文件或Songlist文件', font=('Times', 10, ''))
    uploadFileText.pack()

    browseButton = Button(importFileWindow,
                            text = '选择文件',
                            command = browseFiles)

    browseButton.pack()

    importFileWindow.mainloop()

# 高DPI屏幕适配
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    ctypes.windll.user32.SetProcessDPIAware()

ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# APIC参数导入
apic.readConfigs()

messagebox.askokcancel(title = 'ArcPackGUI', message = '本软件仅适用于壳体打包或Songlist生成/修正使用，不具备软件破解功能。使用时需自负风险。')

if os.path.exists('temp'):
    messagebox.askokcancel(title = 'ArcPackGUI', message = '发现尚未完成的工程，正在尝试打开。')
    if os.path.exists('temp/Payload'):
        processIpa()
    else:
        processApk()
