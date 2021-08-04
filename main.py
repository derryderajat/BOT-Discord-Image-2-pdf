import os
import glob
import discord
import random
from discord.ext import commands
import uuid
import requests
import shutil
import sys, fitz
TOKEN = ''

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.command()
async def hint(ctx):
    await ctx.send("""
command:

.save : Add image you want to add into your pdf file. ( Use this command in comment box while you are sending image)
.send pdfFileName : To send your pdf file.
.reset : to reset images that you have sent. So, you can start again to get different pdf files.
                   """)

@client.command()
async def save(ctx):
    # USAGE: use command .save in the comment box when uploading an image to save the image as a jpg
    try:
        url = ctx.message.attachments[0].url            # check for an image, call exception if none found
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
            r = requests.get(url, stream=True)
            imageName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
            with open(imageName, 'wb') as out_file:
                print('Saving image: ' + imageName)
                shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)


@client.command()
async def send(ctx,arg='file'):
    imglist = glob.glob('*.jpg')
    doc = fitz.open()                            # PDF with the pictures
    for i, f in enumerate(imglist):
        img = fitz.open(f) # open pic as document
        rect = img[0].rect                       # pic dimension
        pdfbytes = img.convertToPDF()            # make a PDF stream
        img.close()                              # no longer needed
        imgPDF = fitz.open("pdf", pdfbytes)      # open stream as PDF
        page = doc.newPage(width = rect.width,   # new page with ...
                        height = rect.height) # pic dimension
        page.showPDFpage(rect, imgPDF, 0) 
            # image fills the page
    doc.save(arg+'.pdf')
    file = discord.File(arg+".pdf")
    await ctx.send(file=file, content="Message to be sent")
    
@client.command()
async def hello(ctx, arg):
    print(arg)

@client.command()
async def reset(ctx):
    # print(ctx)
    imglist = glob.glob('*.jpg')
    pdflist = glob.glob('*.pdf')
    for img in imglist:
        os.remove(img)
    for pdf in pdflist:
        os.remove(pdf)
    print("File Removed!")
    return
  
if __name__=='__main__':
    client.run(TOKEN)
