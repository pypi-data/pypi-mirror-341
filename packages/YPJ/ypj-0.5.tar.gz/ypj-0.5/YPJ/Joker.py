import sys,re,requests
import urllib.parse
import webbrowser
import os
try:
	import YPJ
except ImportError:
	os.system('pip3.11 install YPJ -qq && pip3.9 install YPJ -qq')
print('DECODE BY JOKER | @OLDRINGZ')
webbrowser.open("https://t.me/NawabiPy")
repr = lambda *args: f"{args}"
list = lambda *args: f"{args}"
def open(text):
    if "https://t.me/" in text or text.split()[0]:
        url = text.split("https://t.me/")[1].split()[0] if "https://t.me/" in text else text.split()[0]
        replaced_url = (
            "J0K3Rb" if len(url) == 6 else
           "J0K3Rxp" if len(url) == 7 else
           "OLDRINGZ" if len(url) == 8 else
           "JOKERsex1" if len(url) == 9 else
           "JOKERsecxy" if len(url) == 10 else
           "JOKERsecxy1" if len(url) == 11 else
           "JOKERsecxy12" if len(url) == 12 else
           "JOKERsecxy123" if len(url) == 13 else
           "J0K3X"
        )
        new_text = text.replace(url, replaced_url)
        webbrowser.open(new_text)
        return new_text
    return text
def replace_usernames_in_text(text):
    def replace_username(username):
        length = len(username)
        return (
            "J0K3X" if length == 5 else
            "J0K3Rb" if length == 6 else
            "J0K3Rxp" if length == 7 else
            "OLDRINGZ" if length == 8 else
            "JOKERsex1" if length == 9 else
            "JOKERsecxy" if length == 10 else
            "JOKERsecxy1" if length== 11 else
            "JOKERsecxy12" if length == 12 else
            "JOKERsecxy123" if length == 13 else
            username
        )
    return re.sub(r'@\w+', lambda match: '@' + replace_username(match.group()[1:]), text)
stduot = type("Stdout", (), {
    "write": lambda self, text: sys.__stdout__.write(replace_usernames_in_text(text)),
    "flush": lambda self: sys.__stdout__.flush()
})()
sys.stdout = stduot
stdout = type("Stdout", (), {
    "write": lambda self, text: sys.stdout.write(text),
    "flush": lambda self: sys.stdout.flush()
})()
original_get = requests.get
original_post = requests.post
def modify_telegram_text(url, data=None):
    if "api.telegram.org" in url and "sendMessage" in url:
        if data and isinstance(data, dict) and "text" in data:
            data["text"] = "CONVERTED TO FREE PERMANENT BY JOKER | @OLDRINGZ | @NAWABIPY • " + data["text"]  
        elif "&text=" in url:
            base, text = url.split("&text=", 1)
            decoded_text = urllib.parse.unquote(text)
            modified_text = "CONVERTED TO FREE PERMANENT BY JOKER | @OLDRINGZ | @NAWABIPY • " + decoded_text.strip()
            encoded_text = urllib.parse.quote(modified_text)
            url = base + "&text=" + encoded_text 
    return url, data
def modified_get(url, *args, **kwargs):
    url, _ = modify_telegram_text(url)
    return original_get(url, *args, **kwargs)

def modified_post(url, *args, **kwargs):
    data = kwargs.get("data", None)
    url, data = modify_telegram_text(url, data)
    if data is not None:
        kwargs["data"] = data
    return original_post(url, *args, **kwargs)
requests.get = modified_get
requests.post = modified_post