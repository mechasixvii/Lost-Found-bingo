installpath = r"C:\FIX\ME\Bingo"

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import random
import os

spacing = 56
standardsize = 412
used = []
textcolor = (52, 68, 52)
lightcolor = (157,205,156)

shortmodes = r"Resources\Modes"
shortlogo = r"Resources\Lostfound.png"
shortfreespace = r"Resources\free.png"
shortfontu = r"Resources\GOTHAM-BLACK.TTF"

modes = os.path.join(installpath, shortmodes)
logo = os.path.join(installpath, shortlogo)
freespace = os.path.join(installpath, shortfreespace)
fontu = os.path.join(installpath, shortfontu)

try:
    lostandfound = [f for f in os.listdir(modes) if f.endswith(".png")]
except FileNotFoundError:
    print(f"Error: Folder '{modes}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    font = ImageFont.truetype(fontu, 80)
    smallfont = ImageFont.truetype(fontu, 35)
except IOError:
    print ("whoopsy! no font")

playarea = Image.new('RGBA', (2400,2400), 'white')
canvas = Image.new('RGBA', (2400,3080), 'white')

for xloop in range(5):
    for yloop in range (5):

        if xloop == 2 and yloop == 2:
            free = Image.open(freespace).convert("RGBA")
            truex = spacing*(xloop+1)+standardsize*xloop
            truey = spacing*(yloop+1)+standardsize*yloop
            playarea.paste(free, (truex,truey), free)
        
        else:
            
            while True:
                index = [random.randint(0,11), random.randint(0,11)]
                if index not in used:
                    break
            used.append(index)
            for bloop in range (2):
                

                offsetx=0
                offsety=0

                fullpath = os.path.join(modes,lostandfound[index[bloop]])
                
                mode = Image.open(fullpath).convert("RGBA")

                if bloop == 1:
                    offsety = random.randint (-5,5)
                    offsetx = random.randint (-5,5)
                    offangle = random.randint (-2,2)
                    mode = mode.rotate(offangle, expand=True)
                    enhancer = ImageEnhance.Brightness(mode)
                    mode = enhancer.enhance(1.5)

                truex = spacing*(xloop+1)+standardsize*xloop
                truey = spacing*(yloop+1)+standardsize*yloop

                playarea.paste(mode, (truex+offsetx,truey+offsety), mode)
            
            draw=ImageDraw.Draw(playarea)
            
            texttowrite= lostandfound[index[0]].split("-", 1)[0] + "\n\n+\n\n" + lostandfound[index[1]].split("-", 1)[0]
            smalltext=  lostandfound[index[0]].rsplit(".", 1)[0].split("-", 1)[1] + "\n\n\n\n" + lostandfound[index[1]].rsplit(".", 1)[0].split("-", 1)[1]
            squarecentrex = truex +(standardsize/2)
            squarecentrey = truey +(standardsize/2)
            bound = draw.textbbox((0,0), texttowrite, font=font, align="center")
            text_width = bound[2]-bound[0]
            text_height = bound[3]-bound[1]
            textx = squarecentrex -(text_width/2)
            texty = squarecentrey -(text_height/2)

            draw.multiline_text((textx+3, texty+3), texttowrite, fill=lightcolor, font=font, align="center")
            draw.multiline_text((textx, texty), texttowrite, fill=textcolor, font=font, align="center")

            bound = draw.textbbox((0,0), smalltext, font=smallfont, align="center")
            text_width = bound[2]-bound[0]
            text_height = bound[3]-bound[1]
            textx = squarecentrex -(text_width/2)
            texty = squarecentrey -(text_height/2)

            draw.multiline_text((textx+3, texty+3), smalltext, fill=lightcolor, font=smallfont, align="center")
            draw.multiline_text((textx, texty), smalltext, fill=textcolor, font=smallfont, align="center")

lostfoundlogo = Image.open(logo).convert("RGBA")

canvas.paste (lostfoundlogo, (0,0),lostfoundlogo)
canvas.paste (playarea, (0,680), playarea)
canvas.save(r"C:\Users\Alex\Desktop\Bingo\output.png")
