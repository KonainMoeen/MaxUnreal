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
		
class LiveLinkUI(QWidget):

    Instance = None
    
    @staticmethod
    def getInstance():
        if( LiveLinkUI.Instance == None):
            LiveLinkUI()
        return LiveLinkUI.Instance

    # UI Widgets
    def __init__(self, parent=GetHostApp()):
        super(LiveLinkUI, self).__init__(parent)

        LiveLinkUI.Instance = self
        
        self.MaxVersion2021 = getVersion()
        self.project = pathInFile[1]
        self.content = pathInFile[2]

        self.setObjectName("LiveLinkUI")
        self.setMinimumWidth(400)
        self.setWindowTitle("3ds Max To Unreal")
        self.setWindowFlags(Qt.Window)

        self.style_ = ("""  QWidget#LiveLinkUI { background-color: #262729; } """)
        # style_ = ("QLabel {background-color: #232325; font-size: 14px;font-family: Source Sans Pro; color: #afafaf;}")

        self.MainLayout = QGridLayout()

        #Text
        self.text1 = QLabel("Unreal Project :",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text1,0,0)
            
        self.text2 = QLabel("Content Path :",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text2,1,0)
        
        self.text3 = QLabel("Asset Prefix :",alignment=Qt.AlignCenter)
        self.MainLayout.addWidget(self.text3,2,0)

        #Text fields
        self.lineEntry1 = QLineEdit(self)
        self.lineEntry1.resize(200,15)
        self.lineEntry1.setText(self.project)

        self.MainLayout.addWidget(self.lineEntry1,0,1)

        self.lineEntry2 = QLineEdit(self)
        self.lineEntry2.resize(200,15)
        self.lineEntry2.setText(self.content)
        self.MainLayout.addWidget(self.lineEntry2,1,1)

        
        self.lineEntry3 = QLineEdit(self)
        self.lineEntry3.resize(200,15)
        self.MainLayout.addWidget(self.lineEntry3,2,1)


        #Button
        self.filebutton = QPushButton("::")
        self.filebutton.clicked.connect(self.OpenfileSelector)
        self.MainLayout.addWidget(self.filebutton,0,2)
        

        self.exportbutton = QPushButton("Export Asset")
        self.exportbutton.clicked.connect(self.Execute)
        self.MainLayout.addWidget(self.exportbutton,3,1)


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
        Handler.ExportTempAssets(self.MaxVersion2021)
        Handler.EnablePythonPlugin()
        Handler.Execute()
        print("EXECUTE")

def initLiveLink():

    if LiveLinkUI.Instance != None:
        try: LiveLinkUI.Instance.close()
        except: pass

    LiveLinkUI.Instance = LiveLinkUI()
    LiveLinkUI.Instance.show()
    pref_geo = QRect(500, 300, 460, 30)
    LiveLinkUI.Instance.setGeometry(pref_geo)
    
    #return LiveLinkUI.Instance

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
    pass

def createToolbarMenu2021():
    pass 
 
 
if __name__ == "__main__":
    initLiveLink()   

