from config.config_loader import Config
from scrapers.instagram_scraper import InstagramScraper

print('IG_LOGIN_ENABLED', Config.IG_LOGIN_ENABLED)
print('IG_USERNAME set', bool(Config.IG_USERNAME))
print('IG_PASSWORD set', bool(Config.IG_PASSWORD))

scraper = InstagramScraper(headless=False)
try:
    ok = scraper.login(Config.IG_USERNAME, Config.IG_PASSWORD)
    print('login result', ok)
    print('current_url', scraper.driver.current_url)
    try:
        profile = scraper.scrape_profile('instagram')
        print('profile result', profile)
    except Exception as e:
        print('scrape_profile error', repr(e))
finally:
    scraper.close()
