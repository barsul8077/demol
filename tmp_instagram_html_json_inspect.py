import requests
import re
url = 'https://www.instagram.com/instagram/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
resp = requests.get(url, headers=headers, timeout=30)
print('status', resp.status_code)
text = resp.text
print('len', len(text))
for pat in [r'id="__NEXT_DATA__"', r'script type="application/json"', r'window\.__additionalDataLoaded', r'window\._sharedData', r'"edge_followed_by"', r'"graphql"\s*:\s*\{', r'"profile_pic_url_hd"']:
    print('pat', pat, 'found', bool(re.search(pat, text)))
for name in ['__NEXT_DATA__','instagram', 'edge_followed_by', 'edge_owner_to_timeline_media', 'profile_pic_url_hd', 'window.__additionalDataLoaded']:
    idx = text.find(name)
    print('name', name, 'idx', idx)
    if idx != -1:
        print(text[max(0,idx-120):idx+240].replace('\n',' '))
        print('---')
