import matplotlib.pyplot as plt
import sys
import numpy
from alive_progress import alive_bar
from PIL import Image, ImageFont, ImageDraw

shift = 65
in_c = 30 * 30
out_c = 2

if __name__ == '__main__':

    # train
    print('\nTraining')
    weights = numpy.zeros((in_c, in_c))
    data = []
    with alive_bar(out_c) as bar:
        font = ImageFont.truetype("UbuntuMono-R.ttf", 30)
        for i in range(shift, shift + out_c):
            bar()
            img = Image.new("L", (int(numpy.sqrt(in_c)), int(numpy.sqrt(in_c))), (255))
            draw = ImageDraw.Draw(img)
            letter = chr(i)
            l_w, l_h = font.getsize(letter)
            draw.text((int(numpy.sqrt(in_c) / 2 - l_w / 2), int(numpy.sqrt(in_c) / 2 - l_h / 2)), letter, (0), font=font)
            draw = ImageDraw.Draw(img)
            fn = lambda x : 255 if x > 200 else 0
            img_b = img.convert('L').point(fn, mode='1')
            in_l = (numpy.asarray(img_b.convert("L")) / -255 + 1).astype(int).ravel()[numpy.newaxis].T * 2 - 1
            data.append(abs((numpy.asarray(img_b.convert("L")) / -255 + 1) - 1).astype(int).ravel().tolist())
            img_b.save('letter_' + letter + '.png')
            img.close()
            img_b.close()
            weights += in_l.T * in_l
            for i in range(len(weights)):
                weights[i][i] = 0

    # predict
    if sys.argv[1:]:
        fn = sys.argv[1]
        img = Image.open(fn)
        in_l = (numpy.asarray(img.convert("L")) / -255 + 1).astype(int).ravel()[numpy.newaxis].T * 2 - 1
        temp_out = []
        while True:
            out = []
            for i in weights.dot(in_l):
                if i >= 0:
                    out.append(1)
                else:
                    out.append(-1)
            if out == temp_out:
                break
            temp_out = out

        out_l = []
        for c, i in enumerate(out):
            if i >=0:
                out_l.append(0)
            else:
                out_l.append(1)
        print('\nLetter recognized:', chr(data.index(out_l) + shift) + '\n')
        img = Image.new('1', (int(numpy.sqrt(in_c)), int(numpy.sqrt(in_c))))
        img.putdata(out_l)
        imgplot = plt.imshow(img)
        plt.show()

