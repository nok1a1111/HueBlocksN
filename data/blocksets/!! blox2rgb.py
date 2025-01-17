from PIL import Image
import os
import sys
import shutil
import datetime

print('[][][][][] blox2rgb v3 [][][][][]\n')
dirname = 'input'



# start conversion again or quit
def postConvert():
    global dirname
    dirname = input('If you wish to convert another blockset, please enter its directory name,\nor press Enter to terminate... ')
    if dirname == '':
        sys.exit()
    else:
        checkmate()



def converter():
    # create a new empty file
    try:
        # スクリプトと同じディレクトリに `block.js` を作成
        outputTxt = open('./' + dirname + '.js', 'x')
    except FileExistsError:
        input('\n[!] Warning -- "' + dirname + '.js" already exists. \nPress Enter to overwrite it... ')

    outputTxt = open('./' + dirname + '.js', 'w')

    # add timestamp
    outputTxt.write('/* generated at ' + str(datetime.datetime.now()) + ' */\n\n')

    # add starting part of a block-storing JS object
    outputTxt.write('var ' + dirname + ' = [\n')

    failedImgCnt = 0
    # cycle through the images starting from the LAST one until -1 is reached
    i = len(listImgFound) - 1
    while i >= 0:
        imgName = listImgFound[i]

        # try to open an image
        try:
            imgProc = Image.open('.' + dirname + '/' + imgName)

            # resize the image to 1px and convert to RGBA
            imgProc = imgProc.resize((1, 1), Image.Resampling.LANCZOS).convert('RGBA')
            print(imgProc)

            # load temp image and take the color of the only pixel from it
            imgTemp = imgProc.load()
            imgColor = imgTemp[0, 0]

            # append result to the block-storing JS object
            if i == 0:
                outputTxt.write('	{ id: "' + imgName + '", rgb: [' + str(imgColor[0]) + ', ' + str(imgColor[1]) + ', ' + str(imgColor[2]) + '] }\n')
            else:
                outputTxt.write('	{ id: "' + imgName + '", rgb: [' + str(imgColor[0]) + ', ' + str(imgColor[1]) + ', ' + str(imgColor[2]) + '] },\n')

        except:  
            print('[!] Warning -- "' + imgName + '" cannot be processed.')
            failedImgCnt += 1

        # substract 1 to go to the next image
        i -= 1

    # write closing part and then close the file
    outputTxt.write('];\n\nconsole.log("*beep* ' + dirname + '.js values initialized");')

    # Finally, close the file after all writes
    outputTxt.close()

    print('\n[][][][][] Conversion finished --', str(len(listImgFound) - failedImgCnt), '/', str(len(listImgFound)), 'textures converted.')
    postConvert()




def checkmate():
    # check if the directory exists
    if os.path.isdir('./' + dirname) == False:
        input('\n[!] Error -- directory "' + dirname + '" not found. \nMake sure its placed in the same directory with this script. \nPress Enter to enter another directory name... ')
        getDirname()
        return

    # get list of all .png files in the directory folder
    global listImgFound
    listImgFound = [f for f in os.listdir('./' + dirname) if f.endswith('.png')]

    # check if the list is not empty
    if listImgFound == []:
        input('\n[!] Error -- no textures found. \nPlease check if all the textures placed DIRECTLY in the "' + dirname + '" directory (not in subfolders) and have ".png" extension. \nPress Enter to enter another directory name... ')
        getDirname()
        return

    print('[i] Found', len(listImgFound), 'textures in the "' + dirname + '" directory')
    converter()



# get directory name
def getDirname():
    global dirname
    dirname = str(input("Welcome! Enter the blockset's directory name to convert and press Enter... "))
    if dirname == '':
        getDirname()
    else:
        checkmate()
getDirname()
