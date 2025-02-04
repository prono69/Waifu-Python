# WAIFU-PYTHON

A project born out of boredom, designed to simplify and reduce the code related to the Waifu API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **waifu-python**.

```bash
pip install waifu-python
```

## API Included

- [Anilist](https://anilist.co/)
- [Danborru](https://danbooru.donmai.us/)
- [Waifu.im](https://www.waifu.im/)
- [Waifu.pics](https://waifu.pics/)  
- [Nekos.best](https://nekos.best/) 
- [Pic.re](https://pic.re/)  
- [Purrbot.site](https://purrbot.site/)  
- [N-sfw.com](https://n-sfw.com/)
- [Safeborru](https://safebooru.org/)

## Usage

```python
import asyncio
from waifu_python import WaifuIm

async def main():

    image_data1 = await WaifuIm.fetch_sfw_images()
    #support for tags in args 
    image_data2 = await WaifuIm.fetch_sfw_images('raiden-shogun')
    #retrive tags for the API
    tags = await WaifuIm.get_tags()

    print(f"Random Image{image_data1}\n\nRaiden Shogun{image_data2}\n\nTags{tags}")

asyncio.run(main())
```

## Anilist Usage

```python
import asyncio
from waifu_python import AniList

async def main():
    try:
        random_waifu = await AniList.get_random_waifus()  
        if random_waifu:
            waifu = random_waifu[0]  
            print(f"Name: {waifu['name']}")
            print(f"Anime: {waifu['anime']}")
            print(f"Image: {waifu['image']}")
            print(f"Age: {waifu['age']}")
            print(f"Gender: {waifu['gender']}")
            print(f"Description: {waifu['description']}")
        else:
            print("No waifus found.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Example 1

```python
import asyncio
from waifu_python import WaifuIm
from waifu_python import NekosBest
from waifu_python import WaifuPics
from waifu_python import PicRe
from waifu_python import PurrBot
from waifu_python import NSFWBot
from waifu_python import AniList
from waifu_python import SafeBooru
from waifu_python import Danbooru


async def main():

#-----------------SFW-----------------


    image_data1 = await WaifuIm.fetch_sfw_images()
    image_data2 = await NekosBest.fetch_sfw_images()
    image_data3 = await WaifuPics.fetch_sfw_images()
    image_data4 = await PicRe.fetch_sfw_images()
    image_data5 = await NSFWBot.fetch_sfw_images()
    image_data6 = await PurrBot.fetch_sfw_images()
    image_data7 = await SafeBooru.get_random_image() #check safeborru site for tags


#-----------------NSFW -----------------


    image_data11 = await WaifuIm.fetch_nsfw_images()
    image_data33 = await WaifuPics.fetch_nsfw_images()
    image_data55 = await NSFWBot.fetch_nsfw_images()
    image_data66 = await PurrBot.fetch_nsfw_gif()
    image_data77 = await Danbooru.get_random_image() #check danborru site for tags


#---------------Anilist-----------------


#         Refer to Anilist Usage


#------------------TAGS-----------------


    image_data111 = await WaifuIm.get_tags()
    image_data222 = await NekosBest.get_tags()
    image_data333 = await WaifuPics.get_tags()
    image_data444 = await PicRe.get_tags()
    image_data555 = await NSFWBot.get_tags()
    image_data666 = await PurrBot.get_tags()


#-------------------GIF-------------------


# WAIFU.PICS
# NEKO.BEST
# PURRBOT


    print(f"SFW\n\n{image_data1}\n{image_data2}\n{image_data3}\n{image_data4}\n{image_data5}\n{image_data6}\n\nNSFW\n\n{image_data11}\n{image_data33}\n{image_data55}\n{image_data66}")
    #\n\nTAGS\n\n{image_data111}\n\n{image_data222}\n\n{image_data333}\n\n{image_data444}\n\n{image_data555}\n\n{image_data666}") 

#---TAGs mightbe overwhelming....

asyncio.run(main())
```

## Example 3 (TELEGRAM BOT)

Check Example 1 for more functions And Anilist Usage for anilist

```python
from pyrogram import Client, filters
from waifu_python import AniList
from waifu_python import SafeBooru
from waifu_python import Danbooru

app = Client("Raiden", api_id="API_ID", api_hash="API_HASH", bot_token="BOT_TOKEN")

@app.on_message(filters.command("sfw"))
async def send_sfw_image(client, message):
#Safeborru
    command = message.text.split()
    tag = command[1] if len(command) > 1 else None
    try:
        image_url = await SafeBooru.get_random_image(tag)
        if image_url:
            await message.reply_photo(image_url)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

@app.on_message(filters.command("nsfw"))
#Danborru
async def send_nsfw_image(client, message):
    command = message.text.split()
    tag = command[1] if len(command) > 1 else None
    try:
        image_url = await Danbooru.get_random_image(tag)
        if image_url:
            await message.reply_photo(image_url)
    except Exception as e:
        await message.reply(f"Error: {str(e)}")

#-----------------------------------Anilist--------------------------------------

@app.on_message(filters.command("waifu"))
#optional name (female) or random female character
async def send_nsfw_images(client, message):
    command = message.text.split(maxsplit=1)
    search = command[1] if len(command) > 1 else None

    try:
        waifus = await AniList.get_random_waifus(count=1, search=search)  
        if not waifus:
            await message.reply("No waifus found.")
            return

        waifu = waifus[0]  
        
        description = waifu['description'][:500] + "..." if len(waifu['description']) > 500 else waifu['description']
        caption = (
            f"**Name:** {waifu['name']}\n"
            f"**Anime:** {waifu['anime']}\n"
            f"**Age:** {waifu['age']}\n"
            f"**Gender:** {waifu['gender']}\n\n"
            f"{description}"
        )
        await message.reply_photo(waifu['image'], caption=caption)
    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("character"))
#optional name or random, male and female character
async def send_characters(client, message):
    command = message.text.split(maxsplit=1)
    search = command[1] if len(command) > 1 else None

    try:
        characters = await AniList.get_random_characters(count=1, search=search)  
        if not characters:
            await message.reply("No characters found.")
            return

        character = characters[0]  
        
        description = character['description'][:500] + "..." if len(character['description']) > 500 else character['description']
        caption = (
            f"**Name:** {character['name']}\n"
            f"**Anime:** {character['anime']}\n"
            f"**Age:** {character['age']}\n"
            f"**Gender:** {character['gender']}\n\n"
            f"{description}"
        )
        await message.reply_photo(character['image'], caption=caption)
    except Exception as e:
        await message.reply(f"Error: {e}")


if __name__ == "__main__":
    app.run()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
