import requests
from pprint import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'X-IG-App-ID': '936619743392459',
    'Referer': 'https://www.instagram.com/',
    'Accept-Language': 'en-US,en;q=0.9',
}
for username in ['instagram', 'natgeo']:
    url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'
    print('URL:', url)
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print('status', r.status_code)
        print('content-type', r.headers.get('content-type'))
        text = r.text[:2000]
        print('text snippet:', text)
        if r.headers.get('content-type', '').startswith('application/json'):
            data = r.json()
            pprint(data.keys())
            pprint(data.get('data', {}).get('user', {}).get('edge_followed_by'))
    except Exception as e:
        import traceback
        traceback.print_exc()
    print('---')
