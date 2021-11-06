import pandas as pd
from api.services.recognizer.utils import docx_docs as docs, pdf2 as pdf, tf_fio
import os


ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']

#Передаем путь для изображения

def recogn_image(file_name, dpi = 300):
    """Метод для распознавания изображений"""

    extractor_im = pdf.PDFExtractor3(file_name, dpi = dpi)
    extractor_im.image_list()
    df_recogn = extractor_im.parse_page()
    model = tf_fio.Predictor()
    l = list(df_recogn.text)
    predict = model.bst_predict(l)
    df_recogn['flag'] = pd.Series(predict)
    hide = pdf.Hide_PD(extractor_im.pagelist)
    hide.fill_image(df_recogn[df_recogn.flag == 1])
    report = extractor_im.report()
    print('Всего: {2}, Найдено персональных данных: {1}. Найдено не персональных данных: {0}'
          .format(report[0], report[1], report[2] ))
    print('Output file {0}'.format(extractor_im.output_fname))

    return extractor_im.output_fname


#Передаем путь для docx
def recogn_doc(file_name):
    """Метод для распознавания docx"""

    doc = docs.Docs(file_name)
    doc.recogn_doc()
    report = doc.report()
    print('Всего: {2}, Найдено персональных данных: {1}. Найдено не персональных данных: {0}'
          .format(report[0], report[1], report[2]))
    print('Output file {0}'.format(doc.output_fname))
    return doc.output_fname


#Передаем путь для pdf
def recogn_pdf(file_name, dpi = 300):
    """Метод для распознавания pdf"""

    extractor = pdf.PDFExtractor3(file_name, dpi = dpi)
    extractor.convert_to_jpg()
    df_recogn = extractor.parse_page()
    model = tf_fio.Predictor()
    l = list(df_recogn.text)
    predict = model.bst_predict(l)
    df_recogn['flag'] = pd.Series(predict)
    df_recogn.to_csv(os.curdir + '/files/recogn.csv')
    hide = pdf.Hide_PD(extractor.pagelist)
    hide.fill_image(df_recogn[df_recogn.flag == 1])
    extractor.img2pdf()
    report = extractor.report()

    print('Всего: {2}, Найдено персональных данных: {1}. Найдено не персональных данных: {0}'
          .format(report[0], report[1], report[2] ))
    print('Output file {0}'.format(extractor.output_fname))
    extractor.delete_temp_files()

    return extractor.output_fname


def recognizer(f_name):
    format = f_name.split('.')[-1]
    if format == 'pdf':
        recogn_pdf(f_name)
    elif format == 'docx':
        recogn_doc(f_name)
    elif format in ALLOWED_EXTENSIONS:
        recogn_image(f_name)

