import os
import pandas as pd
import numpy as np
import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from Config.settings import BASE_DIR,MEDIA_ROOT


class PDFExtractor3:
    """Данный класс реализует методы для работы с pdf файлами. """

    def __init__(self, filename, dpi=500):
        self.dpi = dpi
        self.filename = filename
        self.frame = pd.DataFrame()
        self.pagelist = []
        self.directory = os.path.join(MEDIA_ROOT, 'output_files')
        self.output_fname = ''
        print(self.directory)

    def image_list(self):

        self.pagelist.append(self.filename)
        self.output_fname = self.filename
        # print(self.filename)

    # конвертирование pdf в jpeg с разбивкой по страницам
    def convert_to_jpg(self):
        """
        Метод предназначен для конвертирования pdf в jpg
        Каждая страница pdf документа сохраняется в отдельный файл jpg.
        Имя файла заносится в параметр pagelist.
        """

        print('Конвертируем pdf в jpeg...')
        output_dir = self.directory + '/'+ self.filename.split('/')[-1].split('.')[0]
        os.mkdir(output_dir)
        convert_from_path(self.filename, self.dpi, output_folder=output_dir, fmt='jpg')
        print(os.listdir(output_dir))
        self.pagelist = list(map(lambda x: output_dir + '/' + x,os.listdir(output_dir)))


    def parse_page(self):
        """
        Распознает текст с изображения с помощью tessract.
        Открывает изображение в градациях серого, убирает мелкие шумы, бинаризует с некоторым порогом,
        распознает текст, заносит информацию в DataFrame о позиции текста на изображении и его токен.
        """

        recong = pd.DataFrame()
        print('Распознаем текст на изображениях...')
        # custom_config = r'-c tessedit_char_blacklist=0123456789 -l rus --oem 2 --psm 6'

        for i, p in enumerate(self.pagelist):
            im = cv2.imread(p)
            img_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            img_grey = cv2.medianBlur(img_grey, 3)
            img_grey = cv2.threshold(img_grey, 25, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            df_page = pytesseract.image_to_data(img_grey, lang='rus', output_type='data.frame')
            df_page = df_page[df_page['text'].notna()]
            df_page['page_num'] = i
            self.frame = pd.concat([self.frame, df_page])

        self.frame.reset_index(inplace=True)
        self.frame['text'].replace(regex=True, inplace=True, to_replace=r'[^а-яА-Я]', value=r'')

        self.frame.drop((self.frame[self.frame['text'] == ''].index) | (self.frame[self.frame['text'] == ' '].index),
                        inplace=True, axis=0)
        self.frame.reset_index(inplace=True)

        return self.frame

    def img2pdf(self):
        """
        Метод собирает pdf файл из отдельных страниц.
        """
        print('Сохраняем конечный файл pdf...')
        image_list = []

        self.output_fname = self.directory + '/' + 'out_' + self.filename.split("/")[-1]
        for index, filename in enumerate(self.pagelist):
            image_list.append(Image.open(filename))

        image_list[0].save(self.output_fname, "PDF", resolution=100.0, save_all=True, append_images=image_list[1:], )

        return self.output_fname

    def delete_temp_files(self):
        """
        Удаляем временные файлы
        """
        for f in self.pagelist:
            os.remove(f)

    def report(self):
        """
        Отчет о количестве найденных сущностей
        """
        class1 = len(self.frame[self.frame['flag'] == 1])
        class0 = len(self.frame[self.frame['flag'] == 0])
        # Negative  #Positive    #Total
        return (class0, class1, class0 + class1)


class Hide_PD:
    """
docdsdfsdfcxvx    Класс предназначен для закрашивания участка документа с персональными данными
    """

    def __init__(self, filename_list):
        self.filename_list = filename_list

    def open_image(self, filename):
        """Открывает изображение"""
        image = cv2.imread(filename)
        return image

    def blur_image(self, image, x, y, w, h, ks1=71, ks2=71):
        """Размывает изображение"""
        temp_im = image[y:y + h, x:x + w, :]
        blurred = cv2.GaussianBlur(temp_im, (ks1, ks2), 0)
        image[y:y + h, x:x + w, :] = blurred
        return image

    def fill_rect(self, image, x, y, w, h):
        image[y:y + h, x:x + w, :] = 0

        return image

    def fill_image(self, df):
        """Открывает изображение и берет из dataframe координаты токена и вызывает функцию размывания изображения и сохраняет его"""

        for index, filename in enumerate(self.filename_list):
            print('Размываем текст на странице {0}...'.format(index))
            image = self.open_image(filename)
            df_temp = df[['left', 'top', 'width', 'height']][df.page_num == index]
            if len(df_temp) > 0:
                df_temp.reset_index(inplace=True)
                for n in range(len(df_temp)):
                    x = df_temp['left'][n]
                    y = df_temp['top'][n]
                    w = df_temp['width'][n]
                    h = df_temp['height'][n]
                    image = self.blur_image(image, x, y, w, h, ks1=101, ks2=101)
                    # image = self.fill_rect(image, x,y,w,h)
            cv2.imwrite(filename, image)
