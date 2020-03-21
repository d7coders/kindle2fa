import arabic_reshaper
import zipfile
import os
import shutil
import sys


def main(fileName):
    bookFileName = fileName
    bookName = bookFileName.replace('.epub','')
    with zipfile.ZipFile(bookFileName,"r") as zip_ref:
        zip_ref.extractall(bookName)

    TextDir = bookName+'/OEBPS/Text'

    for root, dirs, files in os.walk(TextDir):
        for file in files:
            if file.endswith('.xhtml'):
                print (file)

                with open(TextDir+'/'+file, 'r') as myfile:
                  data = myfile.read()

                # replace non standard half-space
                data = data.replace('‏','‌')

                #reshape
                reshaped_text = arabic_reshaper.reshape(data)

                with open(TextDir+'/'+file, 'w') as myfile:
                    myfile.write(reshaped_text)

    #zip
    shutil.make_archive(bookName+'_converted', 'zip', bookName)
    #rename to .epub
    os.rename(bookName+'_converted'+'.zip', bookName+'_converted'+'.epub')

    #remove folder
    shutil.rmtree(bookName, ignore_errors=True)

    print('\n\nDone! :)\n\n')


if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
        main(fileName=file_name)
    except Exception as e:
        print('Error: Enter Book File name')
