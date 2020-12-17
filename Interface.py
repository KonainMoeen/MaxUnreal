import sys
from os import path
sys.path.append( path.dirname( path.abspath(__file__) ) )
        
import Handler

try:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
except:
    try:
        from PySide.QtGui import *
        from PySide.QtCore import *
    except:
        try:
            from PyQt5.QtGui import *
            from PyQ5.QtCore import *
            from PyQ5.QtWidgets import *
        except:
            try:
                from PyQt4.QtGui import *
                from PyQ4.QtCore import *
            except:
                pass

pathInFile = Handler.FetchPath()

def GetHostApp():
    try:
        mainWindow = QApplication.activeWindow()
        while True:
            lastWin = mainWindow.parent()
            if lastWin:
                mainWindow = lastWin
            else:
                break
        return mainWindow
    except:
        pass
		
  
stylesheet_ = ("""

""")

class PluginUI(QWidget):

    Instance = []
    # UI Widgets
    def __init__(self, parent=GetHostApp()):
        super(PluginUI, self).__init__(parent)

        PluginUI.Instance = self
        
        self.MaxVersion2021 = getVersion()
        self.project = pathInFile[1]
        self.content = pathInFile[2]

        self.setObjectName("PluginUI")
        self.setStyleSheet("""
                           QApplication { background-color: red;}
                           QLineEdit {background-color: rgb(255, 255, 255); color:rgb(0,0,0); border-radius: 1px;}
                           QPushButton {background-color: #0e3461; border: 0.5px solid black;}
                           """)
        self.setMinimumWidth(450)
        self.setWindowTitle("3ds Max To Unreal")
        self.setWindowFlags(Qt.Window)

        self.MainLayout = QGridLayout()

        #Text
        self.text1 = QLabel("Unreal Project :",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text1,0,0)
            
        self.text2 = QLabel("Content Path :",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text2,1,0)
        
        self.text3 = QLabel(" Asset Prefix : ",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text3,1,2)

        #Text fields
        self.lineEntry1 = QLineEdit(self)
        self.lineEntry1.resize(200,15)
        self.lineEntry1.setText(self.project)
        self.MainLayout.addWidget(self.lineEntry1,0,1,1,3)

        self.lineEntry2 = QLineEdit(self)
        self.lineEntry2.resize(200,15)
        self.lineEntry2.setText(self.content)
        self.MainLayout.addWidget(self.lineEntry2,1,1)

        self.lineEntry3 = QLineEdit(self)
        self.lineEntry3.resize(200,15)
        self.MainLayout.addWidget(self.lineEntry3,1,3)

        #Button
        self.filebutton = QPushButton("::")
        self.filebutton.clicked.connect(self.OpenfileSelector)
        self.filebutton.setFixedSize(22,22)
        self.MainLayout.addWidget(self.filebutton,0,4)
        

        self.exportbutton = QPushButton("Export Asset")
        self.exportbutton.clicked.connect(self.Execute)
        self.exportbutton.setMinimumWidth(250)
        self.exportbutton.setFixedHeight(28)
        self.MainLayout.addWidget(self.exportbutton,3,1,2,3)


        self.setLayout(self.MainLayout)

    def tr(self, text):
        return QObject.tr(self, text)

    def OpenfileSelector(self):
        project = QFileDialog.getOpenFileName(self,self.tr("Open Unreal Project"), self.tr("~/Desktop/"), self.tr("Unreal Project (*.uproject)"))
        if project[0]:
            self.lineEntry1.setText(project[0])

    def Execute(self):
        self.project = self.lineEntry1.text()
        self.content = self.lineEntry2.text()

        # Fetch Asset Prefix
        Handler.fetchAssetPrefix(self.lineEntry3.text())

        # Save the project path in file
        Handler.savePathInFile("Project Path =" + self.project + '\n', 1)
        Handler.savePathInFile("Content Path =" + self.content + '\n', 2)
        
        Handler.SendPaths(self.project)
        Handler.DeleteTempAssets()
        if Handler.ExportTempAssets(self.MaxVersion2021):
            Handler.EnablePythonPlugin()
            Handler.Execute()

def initPlugin():
    if PluginUI.Instance != None:
        try: PluginUI.Instance.close()
        except: pass

    PluginUI.Instance = PluginUI()
    PluginUI.Instance.show()
    pref_geo = QRect(500, 300, 460, 80)
    PluginUI.Instance.setGeometry(pref_geo)
    
    return PluginUI.Instance

def getVersion():

    try:
        import pymxs
        if 2021 != pymxs.runtime.maxversion()[7]:
            createToolbarMenu()
            return False
        else :
            createToolbarMenu2021()
            return True
    except:
        createToolbarMenu()
        return False
	
def createToolbarMenu():
    import MaxPlus
    name = "MaxToUnreal"
    if MaxPlus.MenuManager.MenuExists(name):
        MaxPlus.MenuManager.UnregisterMenu(name)

    mb = MaxPlus.MenuBuilder(name)

    mb.AddItem(MaxPlus.ActionFactory.Create('initPlugin', 'MTU Plugin', initPlugin))
    mb.AddSeparator()
    mb.Create(MaxPlus.MenuManager.GetMainMenu())

def createToolbarMenu2021():
    import pymxs
    pymxs.runtime.execute(" global myfunc = 0 ")
    pymxs.runtime.myfunc = initPlugin
    pymxs.runtime.execute("""
-- Sample menu extension script
-- If this script is placed in the "stdplugs\stdscripts"
-- folder, then this will add the new items to MAX's menu bar
-- when MAX starts.
-- A sample macroScript that we will attach to a menu item
macroScript MaxToUnreal
category: "MyPlugin"
tooltip: "MTU Plugin"
(
on execute do myfunc()
)


-- This example adds a new sub-menu to MAX's main menu bar.
-- It adds the menu just before the "Help" menu.
if menuMan.registerMenuContext 0x1ee76d8d then
(
-- Get the main menu bar
local mainMenuBar = menuMan.getMainMenuBar()
-- Create a new menu
local subMenu = menuMan.createMenu "MaxToUnreal"
-- create a menu item that calls the sample macroScript
local subItem = menuMan.createActionItem "MaxToUnreal" "MyPlugin"
-- Add the item to the menu
subMenu.addItem subItem -1
-- Create a new menu item with the menu as it's sub-menu
local subMenuItem = menuMan.createSubMenuItem "MaxToUnreal" subMenu
-- compute the index of the next-to-last menu item in the main menu bar
local subMenuIndex = mainMenuBar.numItems() - 1
-- Add the sub-menu just at the second to last slot
mainMenuBar.addItem subMenuItem subMenuIndex
-- redraw the menu bar with the new item
menuMan.updateMenuBar()
)"""
    )
 
 
if __name__ == "__main__":
    initPlugin()   

