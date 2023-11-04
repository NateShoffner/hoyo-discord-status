import asyncio
import genshin
import os
from dotenv import load_dotenv
from pypresence import AioPresence

load_dotenv()


async def update_starrail_stats(rpc: AioPresence):
    client = genshin.Client()
    client.set_browser_cookies("chromium") # change this to your browser of choice

    client.default_game = genshin.types.Game.STARRAIL

    cards = await client.get_record_cards(os.getenv("HOYOLAB_ID"))
    card = cards[1]

    starrail_uid = card.uid
    starrail_name = card.nickname
    starrail_level = card.level
    starrail_server = card.server_name

    moc_data = await client.get_starrail_challenge(starrail_uid)
    import pprint

    pprint.pprint(moc_data)
    max_floor = moc_data.max_floor
    total_stars = moc_data.total_stars

    profile_url = f"https://act.hoyolab.com/app/community-game-records-sea/index.html?user_id={os.getenv('HOYOLAB_ID')}&utm_source=share&uid={os.getenv('HOYOLAB_ID')}#/hsr"

    state = ""
    state += f"Memory of Chaos: Floor {0 if not max_floor else max_floor} | {total_stars} Stars\n"
    await rpc.update(
        large_image="hsr",
        details=f"{starrail_name} (UID: {starrail_uid}) | TB {starrail_level}",
        state=state,
        buttons=[
            {"label": "View Profile", "url": profile_url},
        ],
    )


async def update_genshin_stats(rpc: AioPresence):
    client = genshin.Client()
    # cookies = genshin.utility.get_browser_cookies("chromium")
    client.set_browser_cookies("chromium")

    client.default_game = genshin.types.Game.GENSHIN

    cards = await client.get_record_cards(os.getenv("HOYOLAB_ID"))
    card = cards[0]

    genshin_uid = card.uid
    genshin_name = card.nickname
    genshin_level = card.level
    genshin_server = card.server_name

    abyss_data = await client.get_genshin_spiral_abyss(genshin_uid)
    max_floor = abyss_data.max_floor
    total_stars = abyss_data.total_stars

    notes = await client.get_genshin_notes(genshin_uid)
    current_resin = notes.current_resin
    max_resin = notes.max_resin

    current_realm_currency = notes.current_realm_currency
    max_realm_currency = notes.max_realm_currency

    profile_url = f"https://act.hoyolab.com/app/community-game-records-sea/index.html?&user_id={os.getenv('HOYOLAB_ID')}&utm_source=share&uid={os.getenv('HOYOLAB_ID')}"

    state = ""
    """
    state += f"Resin: {current_resin}/{max_resin}"
    if (current_resin >= max_resin):
        state += " (Full)"
    state += "\n"
    state += f"Realm Currency: {current_realm_currency}/{max_realm_currency}\n"
    """
    state += f"Spiral Abyss: Floor {max_floor} | {total_stars} Stars\n"

    await rpc.update(
        large_image="genshin",
        details=f"{genshin_name} (UID: {genshin_uid}) | AR {genshin_level}",
        state=state,
        buttons=[
            {"label": "View Profile", "url": profile_url},
        ],
    )


async def main():
    loop = asyncio.get_event_loop()

    rpc = AioPresence(os.getenv("CLIENT_ID"), loop=loop)
    await rpc.connect()

    # switch between showing genshin stats and starrail stats every 15 seconds
    while True:
        await update_genshin_stats(rpc)
        await asyncio.sleep(15)
        await update_starrail_stats(rpc)
        await asyncio.sleep(15)


if __name__ == "__main__":
    # if sys.platform == "win32":
    #    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
