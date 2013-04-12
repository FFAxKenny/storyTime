"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import inspect
import os
import stat
import shutil
from py2app.util import copy_file, find_app
from subprocess import call
from PySide import QtCore

uiDir = 'storyTime/views'
uiFiles = [os.path.join(uiDir, ui) for ui in os.listdir(uiDir)]
imgDir = 'storyTime/images'
imgFiles = [os.path.join(imgDir, i) for i in os.listdir(imgDir)]

setup(
    app = ['run.py'],
    name = 'StoryTime',
    data_files = [
    	('views', uiFiles),
    	('images', imgFiles),
    	('bin/windows', ["storyTime/bin/windows/ffmpeg.exe"]),
    	('bin/mac', ["storyTime/bin/mac/ffmpeg"]),
    	('bin/linux', ["storyTime/bin/linux/ffmpeg"]),
    ],
    options = {'py2app': {
        'dist_dir':"dist_mac",
        'argv_emulation': True,
        'includes':['PySide.QtXml'],
        'iconfile':'storyTime/images/StoryTime.icns',
        }
    },
    setup_requires = ['py2app'],
)

def makeExecutable(path):
    print "Making {0} executable".format(path)
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

# Make ffmpeg executable
scriptFolder = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
makeExecutable(os.path.join(scriptFolder, "dist_mac/StoryTime.app/Contents/Resources/bin/mac/ffmpeg"))
makeExecutable(os.path.join(scriptFolder, "dist_mac/StoryTime.app/Contents/Resources/bin/linux/ffmpeg"))

# Copy the qt plugins so we can use jpegs
# if os.path.isdir('dist_mac/StoryTime.app/Contents/plugins'):
#     shutil.rmtree('dist_mac/StoryTime.app/Contents/plugins')
# shutil.copytree(os.path.abspath('storyTime/bin/mac/plugins'), 'dist_mac/StoryTime.app/Contents/plugins')



appPath = "dist_mac/StoryTime.app/Contents"
plugins = os.path.join(unicode(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.PluginsPath)), "imageformats")
qtLibPath = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.LibrariesPath)
print "qtLibPath: {0}".format(qtLibPath) # TESTING
dest = os.path.abspath("dist_mac/StoryTime.app/Contents/Resources/qt_plugins/imageformats")
os.makedirs(dest)
for lib in ("libqgif.dylib", "libqjpeg.dylib", "libqtiff.dylib"):
    src_file = os.path.join(plugins, lib)
    if os.path.isfile(src_file):
        print "dest_file: {0}".format(dest) # TESTING
        print "lib: {0}".format(lib) # TESTING
        print "src_file: {0}".format(src_file) # TESTING
        dest_file = os.path.join(dest, lib)
        print "dest_file: {0}".format(dest_file) # TESTING
        
        copy_file(src_file, dest_file)
        srcQtCore = os.path.join(qtLibPath, "QtCore.framework/Versions/4/QtCore")
        srcQtGui = os.path.join(qtLibPath, "QtGui.framework/Versions/4/QtGui")
        call(["install_name_tool", "-change", srcQtCore, "@executable_path/../Frameworks/QtCore.framework/Versions/4/QtCore", dest_file])
        call(["install_name_tool", "-change", srcQtGui, "@executable_path/../Frameworks/QtGui.framework/Versions/4/QtGui", dest_file])