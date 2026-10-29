import os
import time
import requests

# Vul hier jouw gegevens in (of stel ze in via Render Environment Variables)
GROUP_ID = "15819510"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1565342912642809968/1IHVQQsXUdoEOnUXqvVBg9oQYxF2kBDJjxhFz_Wsxt0OivrhhmcCEOrK9wgB4Draq45X"
ROBLOX_API_KEY = "xhFi0EkM5EygYsN0xX+LrkVHAAtal/rc2nTv7/KDXX2tEOwgZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SW5ob1Jta3dSV3ROTlVWNVoxbHpUakI0V0N0TWNtdFdTRUZCZEdGc0wzSmpNbTVVZGpjdlMwUllXREowUlU5M1p5SXNJbTkzYm1WeVNXUWlPaUl4TlRneE9UVXhNQ0lzSW1WNGNDSTZNVGM1TXpJNE1UUXdNeXdpYVdGMElqb3hOemt6TWpjM09EQXpMQ0p1WW1ZaU9qRTNPVE15TnpjNE1ETjkuSGl6d05jYnA0VHNHYTJ0Y2ZHSU9xdm56ei0wYXUtb2RjZVNLb0l1YU5iZndDdzN2OVJ5dWxMQm1yYjV1TGFMWVVfZnVRbWpUcGcxS3l6U2trWU50NGx6RTdROTB4ZTVJMkpKNUZSOEpOSm8tQ3N3UWpDQ3k2TF94Q0F3N0NxaEN1V1Q3a1Bvb0pWbmxCdWZPdEFNQTJOU1dhaWJoLU9pQjhJVGZHRlVGZmlpdTF6TnIxN3RjWkVQNEZUR1Foc2Rub3NHbkQxb3M2U3g3c1d3bjc0LWh2aXZlVmtLSWd2OFhCZGpCUm5JeWdCOXlMbGpYbDlqMmxxUFlvMGNlZFNrMXYtekNrbkRSVVRpWnE4T0JsVWpQT3hJVmxPT0hsR3BBcnlSZ1FKczBoaXYxVXFMRmpLVWEwWjlDNjdQWG4ydnVhbVdtS0FrMGJHMzU0Rk5pT1JzaGxB"

last_processed_sale_id = None

def get_latest_sales():
    global last_processed_sale_id
    url = f"https://apis.roblox.com/cloud/v2/groups/{GROUP_ID}/user-transactions?transactionType=Sale&maxPageSize=5"
    headers = {
        "x-api-key": ROBLOX_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            transactions = data.get("userTransactions", [])

            if not transactions:
                return

            latest_sale = transactions[0]
            sale_id = latest_sale.get("id")

            # Als dit de allereerste check is, slaan we op om oude verkopen niet te spammen
            if last_processed_sale_id is None:
                last_processed_sale_id = sale_id
                return

            # Controleer op een nieuwe verkoop
            if sale_id != last_processed_sale_id:
                details = latest_sale.get("details", {})
                item_name = details.get("itemName", "Kledingstuk")
                price = latest_sale.get("amount", "0")
                agent = latest_sale.get("agent", {})
                buyer_name = agent.get("name", "Onbekende koper")

                # Bericht sturen naar Discord Webhook
                embed = {
                    "title": "🎉 Nieuwe Groepsverkoop!",
                    "color": 65280,
                    "fields": [
                        {"name": "👕 Item", "value": str(item_name), "inline": True},
                        {"name": "💰 Prijs", "value": f"{price} Robux", "inline": True},
                        {"name": "👤 Koper", "value": str(buyer_name), "inline": False}
                    ],
                    "footer": {"text": "KVN CLOTHING Group Sales"}
                }
                
                requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
                last_processed_sale_id = sale_id

        else:
            print(f"Fout bij opvragen API: {response.status_code}")
    except Exception as e:
        print(f"Fout in script: {e}")

# Controleer elke 60 seconden op nieuwe verkopen
while True:
    get_latest_sales()
    time.sleep(60)
