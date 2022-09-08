import ctypes
from selectors import SelectorKey
from shutil import rmtree
from tkinter import ttk, messagebox, filedialog
from tkinter import *
from tkinter.ttk import *
import os
import sys
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
    print(song)
    songEditWindow = Tk()

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

    importFileWindow.destroy()
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

# 高DPI屏幕适配
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    ctypes.windll.user32.SetProcessDPIAware()

ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# APIC参数导入
apic.readConfigs()

messagebox.askokcancel(title = 'ArcPackGUI', message = '本软件仅适用于壳体打包或Songlist生成/修正使用，不具备软件破解功能。使用时需自负风险。')

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
