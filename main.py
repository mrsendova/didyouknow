#!/usr/bin/python2
# coding: utf-8
# Copyright (c) 2015 Raphaël M-P
#
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.




from PIL import Image, ImageDraw, ImageFont
import time

#Settings
heading = "Did you know?"

# 1. Image selection
originalFilename = raw_input('Input file: ')
darkFactor = float(raw_input('Dark Factor: '))
destination = raw_input('Output File: ')
svtext = raw_input('Text: ')

img = Image.open(originalFilename)

# 2. Crop
y = img.size[0]
x = img.size[1]
if (y*0.75 < x): #If image length is larger/equal to its height
    print("image ratio is too big. not supported at this time")
else:
    g = x * (1024.0/768.0)#1.3333
    z = y-g
    cut = z/2
    roundcut = int(round(cut))
    second = roundcut + int(round(g))
    #Crop
    img_cropped = img.crop((roundcut, 0, second, x))
    del img

# 2.5 Resize the image to 1024x768
img = img_cropped.resize((1024,768))

# 3. Darken Image
img_darkened = img.point(lambda p: p * darkFactor)
del img

# 4. Add the HEADING
# Defines the fonts
fonthead = ImageFont.truetype(size=100, filename='fonts/oswald/Oswald-Heavy.ttf')
fontbody = ImageFont.truetype(size=65, filename='fonts/oswald/Oswald-DemiBold.ttf')

drw = ImageDraw.Draw(img_darkened)
pos_he = img_darkened.size[0] - fonthead.getsize(heading)[0]
pos_h = pos_he/2 #Center the heading
drw.text([pos_h,45], heading, font=fonthead, fill="white")

#4.5 Calculate each line's width to make it fit properly.
final_list = []
list = svtext.split()
empty = 'false'
x = 0
maketext = ''

while (empty == 'false'):
    if not list:
        empty = 'true'
    else:
        for word in list:
            maketext = maketext + word + ' '
            textsize = drw.textsize(maketext, font=fontbody)
            length = textsize[0]
            if (length > 690 or len(list) <= 1):
                break
            else:
                pass
            x = x + 1
        final_list.append(maketext)
        to_rm = maketext.split()
        for word in to_rm:
            list.remove(word)
            #print('Removed ' + word)
        maketext = ''


print(final_list)
base_height = 200
for line in final_list:
    print(line)
    lineu = unicode(line, "utf-8")
    pos_he = img_darkened.size[0] - fontbody.getsize(lineu)[0]
    pos_h = pos_he/2 #Centers the line
    drw.text([pos_h,base_height], lineu, font=fontbody, fill=(254,218,41))
    base_height = base_height + fontbody.getsize(line)[1] + 10
del drw
img = img_darkened
# 5. Save the image
img.save('output/' + str(time.time()) + '-' + destination)
