		
#inserire immagine dentro ad una GraphicView denominata ConnStatus_2
		self.iconStatus=QtGui.QGraphicsScene(self)
		self.ui.connStatus_2.setScene(self.iconStatus)
		pixMap = QtGui.QPixmap('gui/img/redLed.png')
		item=self.iconStatus.addPixmap(pixMap)
		self.ui.connStatus_2.fitInView(item)
		self.ui.connStatus_2.show()

#set image to a label
	pixMap = QtGui.QPixmap(url)
	label.setPixmap(pixMap)
	label.show()