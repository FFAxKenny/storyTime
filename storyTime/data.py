#!/usr/bin/env python
# encoding: utf-8
"""
data.py

Created by Bohdon Sayre on 2012-03-26.
Copyright (c) 2012 Moonbot Studios. All rights reserved.
"""

from audio import AudioRecording
import copy
import logging
import os

LOG = logging.getLogger('storyTime.data')


FPS_OPTIONS = {
    24:'Film (24 fps)',
    25:'PAL (25 fps)',
    30:'NTSC (30 fps)',
    48:'Show (48 fps)',
    50:'PAL Field (50 fps)',
    60:'NTSC Field (60 fps)',
}

DEFAULT_IMAGE_TYPES = [
    'jpg', 'jpeg', 'png', 'tif', 'tiff', 'tga', 'ico', 'gif',
]

class FrameRecording(object):
    """
    A recording created by Story Time. Times are stored
    in frames as Story Time is primarily a frame-based tool.
    
    FrameRecordings provide a pretty expansive interface for modification.
    This includes subscription and iteration akin to a list,
    eg. myRecording[4:12] to retrieve frames 4 through 12.
    """
    def __init__(self, fps=24):
        self.fps = fps
        self.start = 0
        self._frames = []
    
    def __repr__(self):
        return '<FrameRecording | {0.start}-{0.end}@{0.fps} | {1} frame(s)>'.format(self, len(self.frames))
    
    def __iter__(self):
        for f in self.frames:
            yield f
    
    def __getitem__(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError
        return self.frames[key]
    
    def __delitem__(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError
        del self._frames[key]
    
    def __len__(self):
        return len(self._frames)
    
    def __add__(self, other):
        if isinstance(other, FrameRecording):
            new = copy.deepcopy(self)
            for f in other:
                new.append(f.image, f.duration)
            return new
        return NotImplemented
    
    @property
    def frames(self):
        return self._frames
    
    @property
    def end(self):
        return self.start + self.duration
    
    @property
    def duration(self):
        return sum([f.duration for f in self.frames])
    
    @property
    def images(self):
        return sorted(list(set([f.image for f in self.frames])))
    
    def clear(self):
        self._frames = []
    
    def append(self, image, duration):
        f = Frame(image, duration)
        self.appendFrame(f)
    
    def appendFrame(self, f):
        if not isinstance(f, Frame):
            raise TypeError('expected a Frame, got {0}'.format(type(f).__name__))
        self._frames.append(f)
    
    def insert(self, index, image, duration):
        f = Frame(image, duration)
        self._frames.insert(index, f)
    
    def pop(self, index):
        if index < len(self.frames):
            return self._frames.pop(index)
    
    
    def relativeTime(self, time):
        """ Convert the given absolute time to a time relative to start """
        return time - self.start
    
    def absoluteTime(self, time):
        """ Convert the given relative time to an absolute time """
        return time + self.start
    
    def getIndex(self, time):
        """ Return the index of the frame at the given time """
        if len(self) == 0:
            return
        rtime = self.relativeTime(time)
        if rtime < 0:
            return 0
        elif rtime >= self.duration:
            return len(self.frames) - 1
        t = 0
        for i, f in enumerate(self.frames):
            t += f.duration
            if rtime < t:
                return i
    
    def getFrame(self, time):
        """ Return the frame at the given time """
        index = self.getIndex(time)
        if index is not None:
            return self.frames[self.getIndex(time)]
        
    def inTime(self, index):
        if index < len(self):
            rtime = sum([f.duration for f in self.frames[:index]])
            return self.absoluteTime(rtime)
        return self.absoluteTime(0)
    
    def outTime(self, index):
        if index < len(self):
            rtime = sum([f.duration for f in self.frames[:index+1]])
            return self.absoluteTime(rtime)
        return self.absoluteTime(0)
    



class Frame(object):
    """
    A specific frame within a FrameRecording. Frames only care about the
    image they represent and how long that image is displayed. Their
    cut information is stored in the recording.
    """
    def __init__(self, image, duration):
        """
        `image` - the full path to the image this frame represents
        `duration` - the frame duration of the image, min = 1
        """
        self.image = image
        self.duration = duration
    
    def __eq__(self, other):
        if isinstance(other, Frame):
            return self.image == other.image and self.duration == other.duration
        return NotImplemented
    
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    
    def __repr__(self):
        return 'Frame({0!r}, {1})'.format(os.path.basename(self.image), self.duration)
    
    def getImage(self):
        if self._image is None:
            return ''
        return self._image
    def setImage(self, value):
        if isinstance(value, (str, unicode)):
            self._image = os.path.normpath(value)
        else:
            self._image = None
    image = property(getImage, setImage)
    
    def getDuration(self):
        return self._duration
    def setDuration(self, value):
        self._duration = max(1, int(value))
    duration = property(getDuration, setDuration)
    
    def serialize(self):
        return {'image':self.image, 'duration':self.duration}
    
    @staticmethod
    def deserialize(dictonary):
        return Frame(dictonary['image'], dictonary['duration'])

class VideoRecording(object):
    pass


class RecordingCollection(object):
    """
    RecordingCollection keeps track of a FrameRecording and AudioRecording pair.
    The main Story Time model creates a list of recording collections to
    associate frame timings with audio recordings.
    """
    
    def __init__(self, name='Recording', frames=None, audio=None):
        self.name = name
        self.frames = frames if frames is not None else FrameRecording()
        self.audio = audio if audio is not None else AudioRecording()
        # self.video = video if video is not None else VideoRecording()
    
    def __repr__(self):
        return '<RecordingCollection {0!r} {1!r} {2!r}>'.format(self.name, self.frames, self.audio)
    
    def __len__(self):
        return len(self.frames)
    
    @property
    def duration(self):
        return self.frames.duration
    
    @staticmethod
    def fromString(recordingDict):
        """ Return a new RecordingCollection using the given string """
        fr = FrameRecording(recordingDict['fps'])
        for f in recordingDict['frames']:
            fr.appendFrame(Frame.deserialize(f))
        ar = AudioRecording()
        return RecordingCollection(recordingDict['name'], fr, ar)
    
    def toString(self):
        """ Return this RecordingCollection as a serialized string """
        serializedFrames = []
        for f in self.frames.frames:
            serializedFrames.append(f.serialize())
        fps = self.frames.fps
        tempFile = self.audio.tempFile
        recordingDict = {
            'frames':serializedFrames, 'fps':fps,
            'audioFile': self.audio.filename, 'name':self.name
        }
        return recordingDict


class ImageCollection(object):
    """
    A collection of images to be sample from during a Story Time recording.
    An image collection can be seeded with a directory or combination of images.
    It can then be sorted and organized for better usability.
    
    Image collections also provide a seeking interface to keep track of which
    image was last sampled and making it easy to get the previous/next frame.
    Collection seeking will loop both ways.
    """
    def __init__(self, images=None, imageTypes=DEFAULT_IMAGE_TYPES):
        self.imageTypes = imageTypes
        self._seek = 0
        self._images = images if images is not None else []
    
    def __iter__(self):
        for f in self.images:
            yield f
    
    def __getitem__(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError
        return self.images[key]
    
    def __delitem__(self, key):
        if not isinstance(key, (int, slice)):
            raise TypeError
        del self._images[key]
    
    def __len__(self):
        return len(self._images)
    
    def __repr__(self):
        return '<ImageCollection {0} image(s) | @{1.seek}>'.format(len(self.images), self)
    
    def getImages(self):
        return self._images
    def setImages(self, value):
        self._images = []
        if isinstance(value, (tuple, list)):
            for i in value:
                if isinstance(i, (str, unicode)) and self.isValidImage(i):
                    self._images.append(os.path.normpath(i))
        elif isinstance(value, (str, unicode)):
            self._images.append(os.path.normpath(value))
    images = property(getImages, setImages)
    
    def getSeek(self):
        if self._seek < 0 or self._seek >= len(self.images):
            # this desync is handled by clamping
            self._seek = max(min(self._seek, len(self.images)-1), 0)
        return self._seek
    def setSeek(self, value):
        if not isinstance(value, int):
            raise TypeError
        self._seek = self.validateIndex(value)
    seek = property(getSeek, setSeek)
    
    def validateIndex(self, value):
        if len(self._images) == 0:
            return 0
        else:
            return value % len(self._images)
    
    def isValidImage(self, image):
        types = [x.strip('.').lower() for x in self.imageTypes]
        ext = os.path.splitext(image)[1].strip('.')
        return ext.lower() in types
    
    def clear(self):
        self._images = []
    
    def index(self, image):
        """
        Return the index of the given image within the collection
        Returns None if the image is not in the collection
        """
        if os.path.normpath(image) in self:
            return self.images.index(os.path.normpath(image))
    
    def append(self, image):
        """
        Append the given image or images to the collection.
        This is like a combined append/extend functionality.
        """
        if isinstance(image, (str, unicode)):
            self._images.append(os.path.normpath(image))
        elif isinstance(image, (list, tuple)):
            self._images.extend([os.path.normpath(i) for i in image])
    
    def extend(self, images):
        self.append(images)
    
    def loadDir(self, dir_, additive=False):
        if not os.path.isdir(dir_):
            raise OSError('directory does not exist: {0}'.format(dir_))
        files = os.listdir(dir_)
        imgs = [os.path.join(dir_, i) for i in files if self.isValidImage(i)]
        if additive:
            self.images.extend(imgs)
        else:
            self.images = imgs
        self.sort()
    
    def loadSequence(self, image):
        """ Load the image sequence associated with the given image """
        LOG.warning('loadSequence not yet implemented')
        self._images = image
    
    def sort(self, cmp_=None, key=None, reverse=False):
        if cmp_ is None:
            # case insensitive sort
            cmp_ = lambda x,y: cmp(x.lower(), y.lower())
        self._images.sort(cmp=cmp_, key=key, reverse=reverse)
    
    def current(self):
        if len(self.images) == 0:
            return
        return self[self.seek]
    
    def prev(self, seek=True):
        if len(self.images) == 0:
            return
        if seek:
            self.seek -= 1
            i = self.seek
        else:
            i = self.validateIndex(self.seek - 1)
        return self[i]
    
    def next(self, seek=True):
        if len(self.images) == 0:
            return
        if seek:
            self.seek += 1
            i = self.seek
        else:
            i = self.validateIndex(self.seek + 1)
        return self[i]
    
    def seekToImage(self, image):
        """ Seek to the given image, if its in the collection. Otherwise ignore """
        index = self.index(image)
        if index is not None:
            self.seek = index

