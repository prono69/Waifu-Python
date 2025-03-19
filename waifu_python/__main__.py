import sys
from waifu_python import Danbooru, WaifuIm, Safebooru  # Import modules as needed

def main():
    if len(sys.argv) < 2:
        print("Usage: python-waifu <api>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "danbooru":
        # Example: Fetch a random image from Danbooru
        import asyncio
        image = asyncio.run(Danbooru.fetch_images())
        print(f"Danbooru image: {image}")
    elif command == "waifuim":
        import asyncio
        image = asyncio.run(WaifuIm.fetch_sfw_images())
        print(f"Waifu.im image: {image}")
    elif command == "safebooru":
        import asyncio
        image = asyncio.run(Safebooru.fetch_images())
        print(f"Safebooru image: {image}")
    else:
        print(f"Unknown command: {command}")
        print("Usage: python-waifu <api>")
        sys.exit(1)

if __name__ == "__main__":
    main()
