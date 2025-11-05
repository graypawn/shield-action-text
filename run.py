import re
import requests
from urllib.parse import urlparse

def get_final_url(url: str) -> str:
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        return response.url
    except requests.RequestException as e:
        return f"Error: {e}"

def get_url():
    return clean_url(get_final_url("https://jusocon.com/bbs/link.php?bo_table=nav3&wr_id=5&no=1"))

def clean_url(url):
    parsed = urlparse(url)
    cleaned_url = parsed.netloc + parsed.path
    return cleaned_url.rstrip('/')

def increment_number_in_url(url: str) -> str:
    match = re.search(r'(\d+)(?!.*\d)', url)
    if match:
        num_str = match.group(1)
        incremented = str(int(num_str) + 1)
        return url[:match.start()] + incremented + url[match.end():]
    else:
        return url

def build_filter_lines(url: str) -> list:
    """
    URL 하나를 받아서 대응하는 필터 라인 리스트를 반환
    """
    return [
        f"{url}##div[id*=\"-banner-\"] > div[class*=\" \"] > div[class*=\" \"][style*=\" \"]",
        f"{url}###hd_pop",
        f"{url}##img[src^=\"/tokinbtoki/\"]",
        f"{url}#?#ul[class] > li:has(> a[href*=\"tokkiweb.com\"])"
    ]

def main():
    try:
        url = get_url()
        url_plus1 = increment_number_in_url(url)

        # 두 URL에 대한 라인 생성
        lines = build_filter_lines(url) + build_filter_lines(url_plus1)  # 중간에 빈 줄 추가

        with open('toki_filter.txt', 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + "\n")

        print("toki_filter.txt 파일이 성공적으로 생성되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
