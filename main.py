import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')

btn_dir = QPushButton('Папка') 
pic_list = QListWidget()
pic = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_blur = QPushButton('Заблюрить')
btn_right = QPushButton('Право')
btn_mir = QPushButton('Зеркало')
btn_rez = QPushButton('Резкость')
btn_wb = QPushButton('Ч/Б')

v1 = QVBoxLayout()
v1.addWidget(btn_dir)
v1.addWidget(pic_list)

h1 = QHBoxLayout()
h1.addWidget(btn_left)
h1.addWidget(btn_right)
h1.addWidget(btn_mir)
h1.addWidget(btn_rez)
h1.addWidget(btn_wb)
h1.addWidget(btn_blur)

v2 = QVBoxLayout()
v2.addWidget(pic)
v2.addLayout(h1)

h2 = QHBoxLayout()
h2.addLayout(v1, 20)
h2.addLayout(v2, 80)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    f_list = filter(os.listdir(workdir), extensions)
    pic_list.clear()
    for f in f_list:
        pic_list.addItem(f)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.save_dir = 'modifite/'

    def loadimage(self, dir, filename):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pic.hide()
        pixmapimage = QPixmap(path)
        w, h = pic.width(), pic.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        pic.setPixmap(pixmapimage)
        pic.show()

    def do_wb(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def blure_img(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def zerk_img(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rot_90_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rot_90_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def rezk_img(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    



workimage = ImageProcessor()

def showChosenImage():
    if pic_list.currentRow() >= 0:
        filename = pic_list.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

pic_list.currentRowChanged.connect(showChosenImage)
btn_blur.clicked.connect(workimage.blure_img)
btn_wb.clicked.connect(workimage.do_wb)
btn_mir.clicked.connect(workimage.zerk_img)
btn_left.clicked.connect(workimage.rot_90_left)
btn_right.clicked.connect(workimage.rot_90_right)
btn_rez.clicked.connect(workimage.rezk_img)

win.setLayout(h2)
win.show()
app.exec()