import asyncio
from waifu_python.waifu_im import WaifuIm
from waifu_python.nekos_best import NekosBest
from waifu_python.waifu_pics import WaifuPics
from waifu_python.pics_re import PicRe
from waifu_python.purr_bot import PurrBot
from waifu_python.nsfwbot import NSFWBot


async def main():

#-----------------SFW-----------------


    image_data1 = await WaifuIm.fetch_sfw_images()
    image_data2 = await NekosBest.fetch_sfw_images()
    image_data3 = await WaifuPics.fetch_sfw_images()
    image_data4 = await PicRe.fetch_sfw_images()
    image_data5 = await NSFWBot.fetch_sfw_images()
    image_data6 = await PurrBot.fetch_sfw_images()

#-----------------NSFW -----------------


    image_data11 = await WaifuIm.fetch_nsfw_images()
    image_data33 = await WaifuPics.fetch_nsfw_images()
    image_data55 = await NSFWBot.fetch_nsfw_images()
    image_data66 = await PurrBot.fetch_nsfw_gif()


#-------------------TAGS-----------------

    image_data111 = await WaifuIm.get_tags()
    image_data222 = await NekosBest.get_tags()
    image_data333 = await WaifuPics.get_tags()
    image_data444 = await PicRe.get_tags()
    image_data555 = await NSFWBot.get_tags()
    image_data666 = await PurrBot.get_tags()


#-------------------GIF------------- ----


# WAIFU.PICS
# NEKO.BEST
# PURRBOT

    print(f"SFW\n\n{image_data1}\n{image_data2}\n{image_data3}\n{image_data4}\n{image_data5}\n{image_data6}\n\nNSFW\n\n{image_data11}\n{image_data33}\n{image_data55}\n{image_data66}")
    #\n\nTAGS\n\n{image_data111}\n\n{image_data222}\n\n{image_data333}\n\n{image_data444}\n\n{image_data555}\n\n{image_data666}") 

#---TAGs mightbe overwhelming....

asyncio.run(main())


