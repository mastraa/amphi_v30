from PyQt4 import QtGui
from PyQt4.phonon import Phonon# -*- coding: utf-8 -*-

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.media = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget(self)
        Phonon.createPath(self.media, self.video)
        self.video.setMinimumSize(400, 400)
        
        self.media.stateChanged.connect(self.handleStateChanged)
        
        self.button = QtGui.QPushButton('Choose File', self)
        self.play = QtGui.QPushButton('play',self)
        self.stop = QtGui.QPushButton('stop',self)
        self.button.clicked.connect(self.handleButton)
        self.play.clicked.connect(self.playVideo)
        self.stop.clicked.connect(self.stopVideo)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.video, 1)
        layout.addWidget(self.button)
        layout.addWidget(self.play)
        layout.addWidget(self.stop)
        
    def handleButton(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.button.text())
            if path:
                self.media.setCurrentSource(Phonon.MediaSource(path))
                #self.media.play()
                
    def handleStateChanged(self, newstate, oldstate):
        print newstate
    
    def playVideo(self):
        self.media.play()
        
    def stopVideo(self):
        self.media.stop()
        
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Phonon Player')
    window = Window()
    window.show()
    sys.exit(app.exec_())