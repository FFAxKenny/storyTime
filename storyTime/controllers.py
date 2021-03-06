"""
controller.py

Created by Bohdon Sayre on 2012-03-26.
Copyright (c) 2012 Moonbot Studios. All rights reserved.
"""

from models import Mappings, StoryTimeModel
from PySide.QtCore import *
from PySide.QtGui import *
import audio
import logging
import os
import utils

LOG = logging.getLogger('storyTime.controllers')


class EventEater(QObject):
    def eventFilter(self, obj, event):
        
        if event.type() == QEvent.KeyPress:
            return self.keyPressEvent(event)
            
        elif event.type() == QEvent.DragEnter:
            return self.dragEnterEvent(event)
            
        elif event.type() == QEvent.DragMove:
            return self.dragMoveEvent(event)
            
        elif event.type() == QEvent.Drop:
            return self.dropEvent(event)
        
        else:
            # standard event processing
            try:
                return QObject.eventFilter(self, obj, event)
            except:
                return False

    def keyPressEvent(self, event):
        return False
    
    def handlePaths(self, paths):
        pass
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
        return True

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
        return True

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            paths = []
            for url in event.mimeData().urls():
                paths.append(str(url.toLocalFile()))
            self.handlePaths(paths)
        return True


class StoryTimeWindow(object):
    """
    The Main Story Time Window. Loads and attaches each of the main control
    widgets (ImageView, ImageSlider, TimeSlider) and connects them to a model.
    """
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StoryTimeWindow, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    @staticmethod
    def instance():
        return StoryTimeWindow._instance
    
    def __init__(self, parent=None):
        viewPath = os.path.abspath('views/main.ui')
        print "viewPath: {0}".format(viewPath) # TESTING
        self.ui = utils.loadUi(viewPath, None)
        self.ui.setWindowTitle('Story Time')
        self.ui.setFocusPolicy(Qt.StrongFocus)
        self.ui.setAcceptDrops(True)
        if utils.getOS() == 'windows':
            self.ui.setWindowIcon(QIcon(os.path.abspath('StoryTime.ico')))
        self.ui.show()
        
        # setup model
        self._model = StoryTimeModel(self.ui)
        
        # current image
        self.curImageView = ImageView(Mappings.curImage, 1, self.ui)
        self.curImageView.setModel(self._model)
        self.ui.layoutCurImage.addWidget(self.curImageView)
        # prev image
        self.prevImageView = ImageView(Mappings.prevImage, 0, self.ui)
        self.prevImageView.setModel(self._model)
        self.ui.layoutPrevImage.addWidget(self.prevImageView)
        # prev image
        self.nextImageView = ImageView(Mappings.nextImage, 2, self.ui)
        self.nextImageView.setModel(self._model)
        self.ui.layoutNextImage.addWidget(self.nextImageView)
        
        self.setImageViewVisible('prev', False)
        self.setImageViewVisible('next', False)
        
        self.imageSlider = ImageSlider(self.ui)
        self.imageSlider.setModel(self._model)
        self.ui.layoutControls.addWidget(self.imageSlider)
        
        self.timeSlider = TimeSlider(self.ui)
        self.timeSlider.setModel(self._model)
        self.ui.layoutControls.addWidget(self.timeSlider)
        
        # setup key press eater
        self.eventEater = EventEater()
        self.eventEater.keyPressEvent = self.keyPressEvent
        self.eventEater.handlePaths = self.loadPaths
        self.ui.installEventFilter(self.eventEater)
        self.imageSlider.installEventFilter(self.eventEater)
        self.timeSlider.installEventFilter(self.eventEater)
        
        # build some dynamic menus
        self.buildAudioInputsMenu()
        self.ui.menuFPS.setEnabled(False)
        # hookup menu actions
        self.ui.menuFile.aboutToShow.connect(self.fileMenuAboutToShow)
        self.ui.actionNewRecording.triggered.connect(self.newRecording)
        self.ui.actionOpenRecording.triggered.connect(self.openRecording)
        self.ui.actionSaveRecordingAs.triggered.connect(self.saveRecordingAs)
        self.ui.actionExportMovie.triggered.connect(self.exportMovie)
        self.ui.actionExportForEditing.triggered.connect(self.exportForEditing)
        self.ui.actionOpenStoryTimeDir.triggered.connect(self.openStoryTimePath)
        self.ui.actionImportImages.triggered.connect(self.importImages)
        self.ui.actionClearImages.triggered.connect(self._model.clearImages)
        self.ui.actionNewRecording.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        self.ui.actionOpenRecording.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        self.ui.actionSaveRecordingAs.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        self.ui.actionExportMovie.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_M))
        self.ui.actionExportForEditing.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_E))
        self.ui.actionImportImages.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_I))

        # Active and reveal the window
        self.ui.activateWindow()
        self.ui.raise_()
    
    def setPrevImageViewVisible(self, visible):
        self.setImageViewVisible('prev', visible)
    
    def setNextImageViewVisible(self, visible):
        self.setImageViewVisible('next', visible)
    
    def setImageViewVisible(self, which, visible):
        if not hasattr(self, '{0}ImageView'.format(which)):
            return
        view = getattr(self, '{0}ImageView'.format(which))
        view.setVisible(visible)
        self.ui.layoutImageViews.setStretch(view.index, int(visible))
    
    def buildAudioInputsMenu(self):
        self.ui.menuAudioInputDevices.clear()
        self.ui.audioInputGroup = QActionGroup(self.ui)
        self.ui.audioInputGroup.triggered.connect(self.audioInputGroupTriggered)
        devices = audio.inputDevices()
        if len(devices) > 0:
            for d in devices:
                action = QAction(d['name'], self.ui)
                action.setData(d['index'])
                action.setCheckable(True)
                if d['index'] == self._model.audioInputDeviceIndex:
                    action.setChecked(True)
                self.ui.menuAudioInputDevices.addAction(action)
                self.ui.audioInputGroup.addAction(action)
        else:
            # no input devices found
            action = QAction('(No Input Devices)', self.ui)
            action.setEnabled(False)
            self.ui.menuAudioInputDevices.addAction(action)
        # insert separator and refresh button
        self.ui.menuAudioInputDevices.addSeparator()
        action = QAction('Refresh', self.ui)
        action.triggered.connect(self.buildAudioInputsMenu)
        self.ui.menuAudioInputDevices.addAction(action)
    
    def updateAudioInputsMenu(self):
        for action in self.ui.audioInputGroup.actions():
            checked = action.data() == self._model.audioInputDeviceIndex
            action.setChecked(checked)
    
    def audioInputGroupTriggered(self):
        value = self.ui.audioInputGroup.checkedAction().data()
        index = self._model.mappingIndex(Mappings.audioInputDeviceIndex)
        self._model.setData(index, value)
    
    def keyPressEvent(self, event):
        # set the image index data the same way a mapping would
        if event.key() in (Qt.Key_Space, Qt.Key_Period, Qt.Key_Right, Qt.Key_Down):
            # update time and frame
            self.timeSlider.updateTime()
            index = self._model.mappingIndex(Mappings.curImageIndex)
            value = self._model.curImageIndex + 1
            self._model.setData(index, value)
            return True
        if event.key() in (Qt.Key_Backspace, Qt.Key_Comma, Qt.Key_Left, Qt.Key_Up):
            # update time and frame
            self.timeSlider.updateTime()
            index = self._model.mappingIndex(Mappings.curImageIndex)
            value = self._model.curImageIndex - 1
            self._model.setData(index, value)
            return True
        
        # some time slider hotkeys
        if event.key() == Qt.Key_R:
            self.timeSlider.recordBtnAction()
            return True
        if event.key() == Qt.Key_P:
            self.timeSlider.togglePlayback()
            return True
        if event.key() == Qt.Key_B:
            self.timeSlider.toFirst()
            return True
        if event.key() == Qt.Key_E:
            self.timeSlider.toLast()
            return True
        if event.key() == Qt.Key_N:
            self.newRecording()
            return True
        if event.key() == Qt.Key_BracketRight:
            self.imageSlider.ui.NextImageCheck.toggle()
            return True
        if event.key() == Qt.Key_BracketLeft:
            self.imageSlider.ui.PrevImageCheck.toggle()
            return True
        
        return False
    
    def fileMenuAboutToShow(self):
        hasRecording = len(self._model.curRecording) > 0
        self.ui.actionSaveRecordingAs.setEnabled(hasRecording)
        self.ui.actionExportMovie.setEnabled(hasRecording)
        self.ui.actionExportForEditing.setEnabled(hasRecording)
    
    def openStoryTimePath(self):
        dir_ = self._model.getStoryTimePath()
        if os.path.isdir(dir_):
            utils.openDir(dir_)
    
    def loadPaths(self, paths):
        self._model.loadPaths(paths)
    
    def newRecording(self):
        self._model.newRecording()
        LOG.debug('New recording')
    
    def openRecording(self):
        caption = 'Open Story Time Recording...'
        f = QFileDialog.getOpenFileName(
            self.ui,
            caption=caption,
            dir=self._model.getStoryTimePath(),
            filter='XML files (*.xml)',
        )[0]
        self._model.openRecording(f)
    
    def saveRecordingAs(self):
        caption = 'Save Story Time Recording...'
        f = self.getSaveDestination(caption)
        if f is not None:
            self._model.saveRecording(f)
            utils.openDir(os.path.dirname(f))
    
    def exportMovie(self):
        caption = 'Export Movie...'
        file = self.getSaveDestination(caption, filter='MOV files (*.mov)')
        if file is not None:
            progress = QProgressDialog('Exporting Movie...', 'Cancel', 0, 100, self.ui)
            progress.setWindowModality(Qt.WindowModal)
            self._model.exportMovie(file, progress=progress)
    
    def exportForEditing(self):
        caption = 'Export XML for Editing...'
        # get platform
        msgBox = QMessageBox(self.ui)
        msgBox.setText("Export XML for Editing...")
        msgBox.setInformativeText("Which platform?")
        winButton = msgBox.addButton('Windows', QMessageBox.ActionRole)
        macButton = msgBox.addButton('Mac', QMessageBox.ActionRole)
        abortButton = msgBox.addButton(QMessageBox.Cancel)

        msgBox.exec_()
        btn = msgBox.clickedButton()
        if btn == winButton:
            platform = 'win32'
        elif btn == macButton:
            platform = 'darwin'
        else:
            return
        
        file = self.getSaveDestination(caption)
        if file is not None:
            self._model.exportRecording(file, platform)
            utils.openDir(os.path.dirname(file))
    
    def importImages(self):
        caption = 'Import Image(s)'
        files = QFileDialog.getOpenFileNames(
            self.ui,
            caption=caption,
        )
        if len(files) > 0 and len(files[0]) > 0:
            self.loadPaths(files[0])
            LOG.debug('Imported {0}'.format(files[0]))
        self.ui.activateWindow()
    
    def getSaveDestination(self, caption, filter='XML files (*.xml)', **kwargs):
        files = QFileDialog.getSaveFileName(
            self.ui,
            caption=caption,
            filter=filter,
            **kwargs
        )
        return files[0] if len(files[0]) > 0 else None
    
    def featureNotDone(self):
        msgBox = QMessageBox(self.ui)
        msgBox.setText('This feature is not done yet...')
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()


class ImageView(QWidget):
    """
    The image viewing widget for Story Time. Contains three graphics views
    for displaying the current, previous, and next images.
    """
    def __init__(self, pixmapMapping, index, parent=None):
        super(ImageView, self).__init__(parent)
        viewPath = os.path.abspath('views/imageView.ui')
        print "ImageView viewPath: {0}".format(viewPath) # TESTING
        self.ui = utils.loadUi(viewPath, self)
        self._dataMapper = QDataWidgetMapper()
        self.pixmapMapping = pixmapMapping
        # for use when adjusting layout stretch
        self.index = index
        self.ui.GraphicsView.setStyleSheet( 'QGraphicsView { border-style: none; }' )
    
    def getPixmap(self):
        return self.ui.GraphicsPixmapItem.pixmap()
    def setPixmap(self, data):
        self.ui.GraphicsPixmapItem.setPixmap(data)
        self.resizeEvent()
    pixmap = Property("QPixmap", getPixmap, setPixmap)
    
    def addPixmapItem(self, graphicsView):
        item = QGraphicsPixmapItem()
        scene = QGraphicsScene()
        scene.addItem(item)
        graphicsView.setScene(scene)
        return item

    def setModel(self, model):
        self._model = model
        self._dataMapper.setModel(model)
        self.ui.GraphicsPixmapItem = self.addPixmapItem(self.ui.GraphicsView)
        self._dataMapper.addMapping(self, self.pixmapMapping, 'pixmap')
        self._dataMapper.toFirst()
    
    def resizeEvent(self, event=None):
        self.ui.GraphicsView.fitInView(self.ui.GraphicsView.scene().itemsBoundingRect(), Qt.KeepAspectRatio)



class ImageSlider(QWidget):
    """
    The ImageSlider widget for Story Time. Contains a slider that controls
    which image is currently displayed, as well as labels providing information
    about the current image path as well as how many images there are.
    """
    def __init__(self, parent=None):
        super(ImageSlider, self).__init__(parent)
        #self.setupUi(self)
        viewPath = os.path.abspath('views/imageSlider.ui')
        print "ImageSlider viewPath: {0}".format(viewPath) # TESTING
        self.ui = utils.loadUi(viewPath, self)
        self._dataMapper = QDataWidgetMapper()
        
        self.ui.ImageSlider.valueChanged.connect(self._dataMapper.submit)
        self.ui.PrevImageCheck.toggled.connect(StoryTimeWindow.instance().setPrevImageViewVisible)
        self.ui.NextImageCheck.toggled.connect(StoryTimeWindow.instance().setNextImageViewVisible)
    
    def getSliderMaximum(self):
        return self.ui.ImageSlider.maximum()
    def setSliderMaximum(self, value):
        self.ui.ImageSlider.setMaximum(max(value - 1, 0))
        self.ui.ImageSliderProgress.repaint()
    sliderMaximum = Property('int', getSliderMaximum, setSliderMaximum)
    
    def setModel(self, model):
        self._model = model
        self.ui.CacheImagesBtn.clicked.connect(self._model.cacheAllImages)
        self.ui.ClearCacheBtn.clicked.connect(self._model.clearCache)
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.ImagePath, Mappings.curImagePath, 'text')
        self._dataMapper.addMapping(self.ui.ImageSlider, Mappings.curImageIndex, 'sliderPosition')
        self._dataMapper.addMapping(self, Mappings.imageCount, 'sliderMaximum')
        self._dataMapper.addMapping(self.ui.ImageSliderLabel, Mappings.curImageIndexLabel, 'text')
        self._dataMapper.toFirst()
        
    
    def installEventFilter(self, filter):
        # install the event filter on all appropriate objects
        self.ui.ImageSlider.installEventFilter(filter)
        self.ui.CacheImagesBtn.installEventFilter(filter)
        self.ui.ClearCacheBtn.installEventFilter(filter)




class TimeSlider(QWidget):
    """
    The TimeSlider widget for Story Time. Controls/displays the current
    playback state of the current recording.
    """
    def __init__(self, parent=None):
        super(TimeSlider, self).__init__(parent)
        #self.setupUi(self)
        viewPath = os.path.abspath('views/timeSlider.ui')
        print "TimeSlider viewPath: {0}".format(viewPath) # TESTING
        self.ui = utils.loadUi(viewPath, self)
        self._dataMapper = QDataWidgetMapper()
        
        # used to keep track of playback time
        self.time = QElapsedTimer()
        self.timer = QTimer()
        self.timer.timerEvent = self.updateTime
        
        # add context menu to audio
        action = QAction('Open Audio Folder...', self.ui)
        action.triggered.connect(self.openAudioFolder)
        self.ui.AudioCheck.addAction(action)
        
        # hide hidden controls
        self.ui.IsRecordingCheck.setVisible(False)
        self.ui.IsPlayingCheck.setVisible(False)
        
        self.ui.RecordingIndex.valueChanged.connect(self.recordingIndexChanged)
        self.ui.TimeSlider.valueChanged.connect(self.timeSliderValueChanged)
        self.ui.IsPlayingCheck.toggled.connect(self.updateIsPlaying)
        self.ui.IsRecordingCheck.toggled.connect(self.updateIsRecording)
        self.ui.AudioCheck.toggled.connect(self.audioCheckToggled)
        self.ui.PlayBtn.clicked.connect(self.play)
        self.ui.RecordBtn.clicked.connect(self.recordBtnAction)
        self.ui.NewBtn.clicked.connect(StoryTimeWindow.instance().newRecording)
    
    @property
    def timerInterval(self):
        return (1 / self._model.recordingFps) * 1000
    
    def setSliderMaximum(self, value):
        self.ui.TimeSlider.setMaximum(value)
        self.ui.TimeSliderProgress.repaint()
        
    def getSliderMaximum(self):
        return self.ui.TimeSlider.maximum()
    sliderMaximum = Property('int', getSliderMaximum, setSliderMaximum)
    
    def audioCheckToggled(self):
        self._dataMapper.submit()
    
    def openAudioFolder(self):
        dir_ = self._model.getStoryTimePath()
        if os.path.isdir(dir_):
            utils.openDir(dir_)
    
    def recordingIndexChanged(self):
        if self.isPlaying and not self.isRecording:
            self.play()
        # submit the data directly
        index = self._model.mappingIndex(Mappings.recordingIndex)
        value = self.ui.RecordingIndex.value()
        self._model.setData(index, value)
    
    def timeSliderValueChanged(self):
        index = self._model.mappingIndex(Mappings.curTime)
        value = self.ui.TimeSlider.value()
        self._model.setData(index, value)
    
    def updateIsPlaying(self, isPlaying):
        # record button state
        img = 'images/{0}.png'.format('stopBtn' if isPlaying else 'recordBtn')
        self.ui.RecordBtn.setIcon(QIcon(img))
        # enable/disable controls
        setVisuallyEnabled(self.ui.PlayBtn, not isPlaying)
        setVisuallyEnabled(self.ui.NewBtn, not isPlaying)
        setVisuallyEnabled(self.ui.AudioCheck, not isPlaying)
        setVisuallyEnabled(self.ui.RecordingName, not isPlaying)
        setVisuallyEnabled(self.ui.RecordingImageCount, not isPlaying)
        setVisuallyEnabled(self.ui.RecordingImageCountLabel, not isPlaying)
        setVisuallyEnabled(self.ui.RecordingDurationDisplay, not isPlaying)
    
    def updateIsRecording(self, isRecording):
        # bg color
        style = 'background-color: rgb{0};'.format( (60, 25, 25) if isRecording else (40, 40, 40) )
        self.ui.MainFrame.setStyleSheet(style)
        # enable/disable controls
        self.ui.TimeSlider.setEnabled(not isRecording)
        setVisuallyEnabled(self.ui.RecordingIndex, not isRecording)
    
    def recordBtnAction(self):
        if self.isRecording or self.isPlaying:
            self.stop()
        else:
            self.record()
    
    
    def getIsRecording(self):
        return self.ui.IsRecordingCheck.checkState() == Qt.Checked
    def setIsRecording(self, value):
        self.ui.IsRecordingCheck.setCheckState(Qt.Checked if value else Qt.Unchecked)
        index = self._model.mappingIndex(Mappings.isRecording)
        self._model.setData(index, value)
    isRecording = property(getIsRecording, setIsRecording)
    
    def getIsPlaying(self):
        return self.ui.IsPlayingCheck.checkState() == Qt.Checked
    def setIsPlaying(self, value):
        self.ui.IsPlayingCheck.setCheckState(Qt.Checked if value else Qt.Unchecked)
        index = self._model.mappingIndex(Mappings.isPlaying)
        self._model.setData(index, value)
    isPlaying = property(getIsPlaying, setIsPlaying)
    
    def record(self):
        if len(self._model.images) > 0:
            self.isRecording = True
            self.play()
    
    def play(self, time=0):
        self.isPlaying = True
        self.time.restart()
        self.timer.start(self.timerInterval)
    
    def stop(self):
        self.isRecording = False
        self.isPlaying = False
        self.timer.stop()
    
    def togglePlayback(self):
        if self.isRecording or self.isPlaying:
            self.stop()
        else:
            self.play()
    
    def toFirst(self):
        if not self.isPlaying and not self.isRecording:
            self.ui.TimeSlider.setSliderPosition(0)
            self._dataMapper.submit()
    
    def toLast(self):
        if not self.isPlaying and not self.isRecording:
            self.ui.TimeSlider.setSliderPosition(self._model.recordingDuration)
            self._dataMapper.submit()
    
    def updateTime(self, event=None):
        if not (self.isPlaying or self.isRecording):
            return
        sec = self.time.elapsed() * 0.001
        frames = int(sec * self._model.recordingFps)
        self.ui.TimeSlider.setSliderPosition(frames)
        # determine whether to loop or not
        if not self.isRecording and frames >= self._model.recordingDuration:
            # reached the end of playback
            self.stop()
        self.timeSliderValueChanged()
    
    def setModel(self, model):
        self._model = model
        self.ui.TimeDisplay.clicked.connect(self._model.toggleTimeDisplay)
        self._dataMapper.setModel(model)
        self._dataMapper.addMapping(self.ui.RecordingIndex, Mappings.recordingIndex, 'value')
        self._dataMapper.addMapping(self.ui.RecordingName, Mappings.recordingName, 'text')
        self._dataMapper.addMapping(self.ui.RecordingImageCount, Mappings.recordingImageCount, 'text')
        self._dataMapper.addMapping(self.ui.RecordingDurationDisplay, Mappings.recordingDurationDisplay, 'text')
        self._dataMapper.addMapping(self, Mappings.recordingDuration, 'sliderMaximum')
        self._dataMapper.addMapping(self.ui.AudioCheck, Mappings.audioEnabled, 'checked')
        self._dataMapper.addMapping(self.ui.IsRecordingCheck, Mappings.isRecording, 'checked')
        self._dataMapper.addMapping(self.ui.IsPlayingCheck, Mappings.isPlaying, 'checked')
        self._dataMapper.addMapping(self.ui.TimeSlider, Mappings.curTime, 'sliderPosition')
        self._dataMapper.addMapping(self.ui.TimeDisplay, Mappings.timeDisplay, 'text')
        self._dataMapper.toFirst()
        
    
    def installEventFilter(self, filter):
            # install the event filter on all appropriate objects
        self.ui.TimeSlider.installEventFilter(filter)
        self.ui.TimeDisplay.installEventFilter(filter)
        self.ui.AudioCheck.installEventFilter(filter)
        self.ui.PlayBtn.installEventFilter(filter)
        self.ui.RecordingIndex.installEventFilter(filter)
        self.ui.RecordBtn.installEventFilter(filter)
        self.ui.NewBtn.installEventFilter(filter)



def setVisuallyEnabled(control, enabled):
    style = '' if enabled else 'color: rgb(120, 120, 120);'
    control.setEnabled(enabled)
    control.setStyleSheet(style)



class StoryTimeControl(object):
    
    #audioHandler = AudioHandler()
    UPDATE_INTERVAL = 500
    
    
    def ctl_process_export(self, caption, operatingSystem):
        """
        Export the current application state to a Final Cut Pro XML file.
        
        `caption` -- the caption of the file browsing dialog
        `operatingSystem` -- the operating system to export the file to
        """
        if len(self.images.get()) > 0:
            path = self.view_browse_save_as(caption)
            if path is not None and path != '':
                fcpkw = {
                    'name':os.path.splitext(os.path.split(path)[1])[0],
                    'images':zip(self.images.get(), self.create_frames_list()),
                    'audioPath':self.audioPath.get(),
                    'fps':self.fps.get(),
                    'ntsc':(self.fps.get() % 30 == 0),
                    'OS':operatingSystem
                }
                with open(path, 'w') as exportFile:
                    exportFile.write(FcpXml(**fcpkw).getStr())
                self.ctl_make_audio_path()
    
    def to_xml(self):
        """Create a StoryTime XML string from the current application state"""
        xmlDoc = xml.dom.minidom.Document()
        stElement = xmlDoc.createElement('storyTime')
        xmlDoc.appendChild(stElement)
        fpsElement = xmlDoc.createElement('fps')
        stElement.appendChild(fpsElement)
        fpsText = xmlDoc.createTextNode(str(self.fps.get()))
        fpsElement.appendChild(fpsText)
        audioElement = xmlDoc.createElement('audio')
        stElement.appendChild(audioElement)
        audioText = xmlDoc.createTextNode(self.audioPath.get())
        audioElement.appendChild(audioText)
        framesElement = xmlDoc.createElement('frames')
        stElement.appendChild(framesElement)
        for i in range(0, len(self.timing_data.get())):
            frameElement = xmlDoc.createElement('frame')
            framesElement.appendChild(frameElement)
            pathElement = xmlDoc.createElement('path')
            frameElement.appendChild(pathElement)
            pathText = xmlDoc.createTextNode(self.timing_data.get()[i]['image'])
            pathElement.appendChild(pathText)
            msElement = xmlDoc.createElement('ms')
            frameElement.appendChild(msElement)
            msText = xmlDoc.createTextNode(str(self.timing_data.get()[i]['timing']))
            msElement.appendChild(msText)
        return xmlDoc.toprettyxml('\t', '\n')
    
    def from_xml(self, xmlStr):
        """Update the application state based on a StoryTime XML string"""
        xmlStr = xmlStr.replace('\n', '')
        xmlStr = xmlStr.replace('\t', '')
        xmlDoc = xml.dom.minidom.parseString(xmlStr)
        mainElement = xmlDoc.getElementsByTagName('storyTime')[0]
        fps = int(mainElement.getElementsByTagName('fps')[0].childNodes[0].nodeValue)
        audioPath = mainElement.getElementsByTagName('audio')[0].childNodes[0].nodeValue
        framesElement = mainElement.getElementsByTagName('frames')[0]
        images = []
        times = []
        for frameElement in framesElement.childNodes:
            images.append(frameElement.childNodes[0].childNodes[0].nodeValue)
            times.append(int(frameElement.childNodes[1].childNodes[0].nodeValue))
        self.fps.set(fps)
        self.images.set(images)
        self.times.set(times)
        self.audioPath.set(audioPath)       