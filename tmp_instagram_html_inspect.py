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
for pat in [r'window\._sharedData\s*=\s*({.*?});</script>', r'"edge_followed_by"\s*:\s*\{\s*"count"\s*:\s*([0-9]+)\}', r'profile_pic_url_hd', r'edge_owner_to_timeline_media', r'"graphql"\s*:\s*\{']:
    m = re.search(pat, text, re.S)
    print('PAT', pat, 'match', bool(m))
    if m:
        snippet = m.group(0)
        print(snippet[:500])
        break
for label in ['Followers', 'Following', 'posts', 'Followers', 'Mobile number, username or email']:
    idx = text.find(label)
    print('label', label, 'idx', idx)
print('first 2000 chars', text[:2000].replace('\n',' '))
