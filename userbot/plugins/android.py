# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
# J
""" Userbot module containing commands related to android"""
import json
import re

from bs4 import BeautifulSoup
from requests import get

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/devices.json"
)


@bot.on(admin_cmd(pattern=r"magisk"))
@bot.on(sudo_cmd(pattern=r"magisk", allow_sudo=True))
async def kakashi(magisk):
    reply_to_id = magisk.message
    MAGISK = "https://telegra.ph/file/a4b88cbc8da9c562fdb44.jpg"
    """magisk latest releases"""
    releases = (
        "__**Latest Magisk Releases:**__\n\n"
        f"**Stable : **[APK v8.0.2](https://github.com/topjohnwu/Magisk/releases/download/manager-v8.0.2/MagiskManager-v8.0.2.apk) | [ZIP v20.4](https://github.com/topjohnwu/Magisk/releases/download/v20.4/Magisk-v20.4.zip) | [Uninstaller](https://github.com/topjohnwu/Magisk/releases/download/v20.4/Magisk-uninstaller-20200323.zip)\n"
        f"**Beta : **[APK v8.0.2](https://github.com/topjohnwu/Magisk/releases/download/manager-v8.0.2/MagiskManager-v8.0.2.apk) | [ZIP v21.0](https://github.com/topjohnwu/Magisk/releases/download/v21.0/Magisk-v21.0.zip) | [Uninstaller](https://github.com/topjohnwu/Magisk/releases/download/v21.0/Magisk-uninstaller-20201003.zip)\n"
        f"**Canary : **[APK v4e0a3f5e](https://github.com/topjohnwu/magisk_files/blob/canary/app-debug.apk) | [ZIP v4e0a3f5e](https://github.com/topjohnwu/magisk_files/blob/canary/magisk-debug.zip) | [Uninstaller](https://github.com/topjohnwu/magisk_files/blob/canary/magisk-uninstaller.zip)"
    )
    await bot.send_file(
        magisk.chat_id,
        MAGISK,
        caption=releases,
        reply_to=reply_to_id,
        link_preview=False,
        allow_cache=True,
    )
    await magisk.delete()


@bot.on(admin_cmd(outgoing=True, pattern=r"device(?: |$)(\S*)"))
@bot.on(sudo_cmd(pattern=r"device(?: |$)(\S*)", allow_sudo=True))
async def device_info(request):
    """get android device basic info from its codename"""
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await edit_or_reply(request, "`Usage: .device <codename> / <model>`")
        return
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await edit_or_reply(request, reply)


@bot.on(admin_cmd(outgoing=True, pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)"))
@bot.on(sudo_cmd(pattern=r"codename(?: |)([\S]*)(?: |)([\s\S]*)", allow_sudo=True))
async def codename_info(request):
    """search for android codename"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await edit_or_reply(request, "`Usage: .codename <brand> <device>`")
        return

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}  # Lower brand names in JSON
    devices = devices_lower.get(brand)
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Search results for {brand} {device}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Device**: {item['device']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await edit_or_reply(request, reply)


@bot.on(admin_cmd(outgoing=True, pattern=r"aspecs(?: |)([\S]*)(?: |)([\s\S]*)"))
@bot.on(sudo_cmd(pattern=r"aspecs(?: |)([\S]*)(?: |)([\s\S]*)", allow_sudo=True))
async def devices_specifications(request):
    """Mobile devices specifications"""
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await edit_or_reply(request, "`Usage: .aspecs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content, "lxml"
        )
        .find("div", {"class": "brand-listing-container-news"})
        .findAll("a")
    )
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await edit_or_reply(request, f"`{brand} is unknown brand!`")
        return
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await edit_or_reply(request, f"`can't find {device}!`")
        return
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n" + info.title.text.split("-")[0].strip() + "\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await edit_or_reply(request, reply)


@bot.on(admin_cmd(outgoing=True, pattern=r"twrp(?: |$)(\S*)"))
@bot.on(sudo_cmd(pattern=r"twrp(?: |$)(\S*)", allow_sudo=True))
async def twrp(request):
    """get android device twrp"""
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await edit_or_reply(request, "`Usage: .twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await edit_or_reply(request, reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await edit_or_reply(request, reply)


CMD_HELP.update(
    {
        "android": "__**PLUGIN NAME :** Android__\
\n\n📌** CMD ➥** `.magisk`\
\n**USAGE   ➥  **Get latest Magisk releases\
\n\n📌** CMD ➥** `.device` <codename>\
\n**USAGE   ➥  **Get info about android device codename or model.\
\n\n📌** CMD ➥** `.codename` <brand> <device>\
\n**USAGE   ➥  **Search for android device codename.\
\n\n📌** CMD ➥** `.aspecs` <brand> <device>\
\n**USAGE   ➥  **Get device specifications info.\
\n\n📌** CMD ➥** `.twrp` <codename>\
\n**USAGE   ➥  **Get latest twrp download for android device."
    }
)
