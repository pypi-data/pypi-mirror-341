from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse, HTMLResponse
from starlette.routing import Route
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTask
from urllib.parse import unquote
# import asyncio
import uvicorn
import os
import pathlib
import contextlib
# import json

from musicbox_mpd.musicplayer import MusicPlayer
from musicbox_mpd import data
from musicbox_mpd import __about__
from musicbox_mpd import startup


def get_static_path():
    return os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")


def status_json(status, message=""):
    return {"status": status, "message": message}


def homepage(request):
    with open(os.path.join(get_static_path(), "ui.html")) as f:
        html = f.read()
        return HTMLResponse(html.replace("{ver}", __about__.__version__))


async def get_version(request):
    stats = await player.get_stats()
    response = {'musicbox': __about__.__version__, 'mpd': await player.get_mpd_version()}
    response["stats"] = stats
    return JSONResponse(response)


async def status(request):
    status = await player.status()
    uri = status.get("file")
    if uri == None:
        status["libraryid"] = 0
    else:
        status["libraryid"] = data.get_id(con, uri)
    return JSONResponse(status)


async def play(request):
    params = await request.json()
    songpos = params.get("songpos")
    if songpos == None:
        songpos = 0
    status = await player.play(songpos)
    if status == False:
        return JSONResponse(status_json("Error", await player.error_message))
    return JSONResponse(status_json("OK"))


async def stop(request):
    await player.stop()
    return JSONResponse(status_json("OK"))


async def search(request):
    search_text = request.query_params["search"]
    result = data.search(con, search_text)

    # If no results and no search filters, try to cache the library and search again
    if len(result) == 0 and search_text == "":
        print("Library empty - Caching library and retrying search")
        await player.cache_library(con)
        result = data.search(con, search_text)

    return JSONResponse(result)


async def queuestatus(request):
    result = await player.get_queue()
    return JSONResponse({"queueCount": len(result), "queueLength": sum([float(x.get("duration")) for x in result if x.get("duration") != None])})


async def coverart(request):
    id = request.path_params["id"]
    uri = data.get_uri(con, id)
    default_image = os.path.join(get_static_path(), "default.gif")

    if uri == None:
        return FileResponse(default_image)

    image_folder = os.environ.get("SNAP_COMMON")
    if image_folder == None:
        image_folder = config.get("image_folder")
    else:
        image_folder = os.path.join(image_folder, "coverart")
    cover = await player.get_cover_art(uri, image_folder)

    if cover == None:
        return FileResponse(default_image)

    if not cover == None:
        path = os.path.dirname(cover)
        filename = os.path.basename(cover)
        return FileResponse(os.path.join(path, filename))


def album(request):
    search = unquote(request.query_params["search"])
    result = data.get_album(con, search)

    return JSONResponse(result)


async def add(request):
    id = request.path_params["id"]
    uri = data.get_uri(con, id)
    await player.add_to_queue(uri)

    return JSONResponse(status_json("OK"))


async def remove(request):
    id = request.path_params["id"]
    await player.remove_from_queue(id)

    return JSONResponse(status_json("OK"))


async def remove_all(request):
    await player.clear_queue()
    return JSONResponse(status_json("OK"))


async def queue(request):
    result = await player.get_queue()
    return JSONResponse(result)


async def skip(request):
    result = await player.skip()
    if result == False:
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(status_json("OK"))


async def pause(request):
    await player.pause()
    return JSONResponse(status_json("OK"))


async def volume(request):
    vol = request.path_params["vol"]
    result = await player.volume(vol)
    return JSONResponse(status_json(result))


def get_path(path):
    if path.endswith("/"):
        return path[:-1]
    return path


async def queuealbum(request):
    params = await request.json()
    uri = get_path(params["path"])
    await player.add_to_queue(uri)

    return JSONResponse(status_json("OK"))


async def playsong(request):
    json = await request.json()
    uri = json.get("uri")
    if uri == None:
        return JSONResponse(status_json("Error", "No URI provided"))

    status = await player.status()
    if status.get("state") == "play":
        result = await player.play_next(uri, status)
        if not result:
            return JSONResponse(status_json("Error", player.error_message))
        return JSONResponse(status_json("next"))

    await player.clear_queue()
    await player.add_to_queue(uri)
    if not await player.play():
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(status_json("OK"))

# Use for scanning QR codes TODO: Implement


async def playalbum(request):
    status = await player.status()
    json = await request.json()
    uri = get_path(json["path"])

    if status.get("state") == "play":
        return JSONResponse(status_json("notplay"))

    await player.clear_queue()
    await player.add_to_queue(uri)
    await player.play()

    return JSONResponse(status_json("OK"))


async def random_queue(request):
    num = request.path_params["num"]
    for song in data.get_random_songs(con, num):
        await player.add_to_queue(song["file"])
    return JSONResponse(status_json("OK"))


async def get_mixtapes(request):
    result = await player.get_playlists()
    return JSONResponse(result)


async def load_mixtape(request):
    name = request.path_params["name"]
    await player.load_playlist(name)
    return JSONResponse(status_json("OK"))


async def save_mixtape(request):
    name = request.path_params["name"]
    await player.update_playlist(name)
    return JSONResponse(status_json("OK"))


async def create_mixtape(request):
    name = request.path_params["name"]
    result = await player.save_playlist(name)
    if result:
        return JSONResponse(status_json("OK"))
    else:
        return JSONResponse(status_json("Error", player.error_message))


async def delete_mixtape(request):
    name = request.path_params["name"]
    await player.delete_playlist(name)
    return JSONResponse(status_json("OK"))


async def get_mixtape(request):
    name = unquote(request.path_params["name"])
    result = await player.list_playlist(name)
    return JSONResponse(result)


async def update(request):
    task = BackgroundTask(player.wait_for_update, con)
    result = await player.update(con)
    return JSONResponse(result, background=task)


async def setting(request):
    name = request.path_params["name"]
    value = request.path_params["value"]
    await player.set_setting(name, value)
    return JSONResponse(status_json("OK"))


async def replaygain(request):
    result = await player.get_replay_gain_status()
    if result == None:
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(status_json("OK", result))


async def set_replaygain(request):
    json = await request.json()
    value = json["mode"]
    result = await player.set_replay_gain_mode(value)
    if result == False:
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(status_json("OK", result))


async def shuffle(request):
    result = await player.shuffle()
    if result == False:
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(status_json("OK", result))


async def history(request):
    result = await player.play_history()
    if result == None:
        return JSONResponse(status_json("Error", player.error_message))
    return JSONResponse(result)


async def get_config(request):
    return JSONResponse(config)


async def set_config(request):
    new_config = await request.json()
    config["mpd_host"] = new_config.get("mpdHost", config["mpd_host"])
    config["mpd_port"] = new_config.get("mpdPort", config["mpd_port"])
    pwd = new_config.get("password", config.get("password"))
    if pwd != None:
        config["password"] = pwd
        player.password = config["password"]
    config["host"] = new_config.get("host", config["host"])
    config["port"] = new_config.get("port", config["port"])
    player.disconnect()
    player.host = config["mpd_host"]
    player.port = config["mpd_port"]

    try:
        startup.save_config(config)
        return JSONResponse(status_json("OK"))
    except Exception as e:
        return JSONResponse(status_json("Error", str(e)))


@contextlib.asynccontextmanager
async def lifespan(app):
    print("Run at startup!")
    await startup.try_cache_library(player, con, config_exists)
    startup.add_radio_stations(con, config.get("stations"))
    yield
    print("Run on shutdown!")

app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/remove/{id}', remove, methods=['DELETE']),
    Route('/version', get_version),
    Route('/status', status),
    Route('/queuestatus', queuestatus),
    Route('/play', play, methods=['POST']),
    Route('/stop', stop, methods=['POST']),
    Route('/search', search),
    Route('/coverart/{id}', coverart),
    Route('/album', album),
    Route('/add/{id}', add, methods=['POST']),
    Route('/all', remove_all, methods=['DELETE']),
    Route('/queue', queue),

    Route('/playalbum', playalbum, methods=['POST']),
    Route('/queuealbum', queuealbum, methods=['POST']),
    Route('/playsong', playsong, methods=['POST']),
    Route('/rand/{num}', random_queue, methods=['POST']),
    Route('/mix', get_mixtapes),
    Route('/loadmix/{name}', load_mixtape, methods=['POST']),
    Route('/savemix/{name}', save_mixtape, methods=['POST']),
    Route('/mix/{name}', create_mixtape, methods=['POST']),
    Route('/mix/{name}', delete_mixtape, methods=['DELETE']),
    Route('/mix/{name}', get_mixtape, methods=['GET']),
    Route('/update', update, methods=['POST']),
    Route('/setting/{name}/{value}', setting, methods=['POST']),
    Route('/replaygain', replaygain, methods=['GET']),
    Route('/replaygain', set_replaygain, methods=['POST']),
    Route('/shuffle', shuffle, methods=["POST"]),
    Route('/history', history, methods=["GET"]),
    Route('/config', get_config, methods=["GET"]),
    Route('/config', set_config, methods=["POST"]),

    Route('/skip', skip, methods=['POST']),
    Route('/pause', pause, methods=['POST']),
    Route('/volume/{vol}', volume, methods=['POST']),


    Mount('/ui', app=StaticFiles(directory=get_static_path()), name="ui"),
], lifespan=lifespan)

args = startup.get_args()
config, config_exists = startup.get_config(args.configfile)
con = data.in_memory_db()
player = MusicPlayer(config["mpd_host"],
                     config["mpd_port"], config.get("password"))


def start():
    if args.service:
        startup.create_service()
        return

    if args.version:
        print(f"Musicbox MPD version {__about__.__version__}")
        return

    if args.create_config:
        startup.get_default_config(True)
        print("Config file 'musicbox-mpd.conf.json' created")
        return

    uvicorn.run("musicbox_mpd.main:app",
                host=config["host"], port=config["port"], reload=False)
