import streamlit as st
import requests
import base64
import re
from PIL import Image
from io import BytesIO
import time
import os
from datetime import datetime, timedelta
import json

class CachedResponse:
    """캐시된 응답을 위한 가짜 응답 객체"""
    def __init__(self, data):
        self.status_code = 200
        self._data = data
    
    def json(self):
        return self._data

class GitHubAPI:
    def __init__(self, token=None):
        self.headers = {
            'User-Agent': 'GitHub-README-Viewer',
            'Accept': 'application/vnd.github.v3+json'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # 캐시 초기화
        self.cache_file = 'github_cache.json'
        self.cache = self.load_cache()
        
    def load_cache(self):
        """캐시된 데이터를 로드합니다."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    # 만료된 캐시 항목 제거
                    now = datetime.now()
                    cache = {k: v for k, v in cache.items() 
                            if datetime.fromisoformat(v['expires']) > now}
                    return cache
            except Exception:
                return {}
        return {}
    
    def save_cache(self):
        """캐시를 파일에 저장합니다."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.warning(f"캐시 저장 실패: {e}")

    def cache_get(self, key):
        """캐시에서 데이터를 가져옵니다."""
        if key in self.cache:
            cache_item = self.cache[key]
            if datetime.fromisoformat(cache_item['expires']) > datetime.now():
                return cache_item['data']
        return None

    def cache_set(self, key, data, expires_in_hours=24):
        """데이터를 캐시에 저장합니다."""
        expires = datetime.now() + timedelta(hours=expires_in_hours)
        self.cache[key] = {
            'data': data,
            'expires': expires.isoformat()
        }
        self.save_cache()

    def _make_request(self, url, cache_key=None, max_retries=3):
        """API 요청을 수행하고 캐싱을 처리합니다."""
        # 캐시된 데이터가 있으면 반환
        if cache_key:
            cached_data = self.cache_get(cache_key)
            if cached_data:
                return CachedResponse(cached_data)

        for attempt in range(max_retries):
            try:
                response = self.session.get(url)
                
                if response.status_code == 200:
                    # 성공적인 응답을 캐시에 저장
                    if cache_key:
                        self.cache_set(cache_key, response.json())
                    return response
                elif response.status_code == 403:
                    rate_limit = self.check_rate_limit()
                    if rate_limit['remaining'] == 0:
                        reset_time = time.strftime('%H:%M:%S', 
                                                 time.localtime(rate_limit['reset']))
                        st.error(f"""
                        API 요청 한도를 초과했습니다. {reset_time}에 초기화됩니다.
                        GitHub 토큰을 사용하면 시간당 5,000회까지 요청할 수 있습니다.
                        """)
                        return None
                    time.sleep(2)
                    continue
                else:
                    st.error(f"API 요청 실패: {response.status_code}")
                    return None
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    st.error(f"요청 실패: {str(e)}")
                    return None
                time.sleep(1)
        
        return None

    def check_rate_limit(self):
        """GitHub API 요청 한도를 확인합니다."""
        response = self.session.get('https://api.github.com/rate_limit')
        if response.status_code == 200:
            data = response.json()
            return {
                'limit': data['rate']['limit'],
                'remaining': data['rate']['remaining'],
                'reset': data['rate']['reset']
            }
        return {'limit': 60, 'remaining': 0, 'reset': time.time() + 3600}

    def get_user_repos(self, username: str):
        """사용자의 public 저장소 목록을 가져옵니다."""
        cache_key = f"repos_{username}"
        repos_url = f"https://api.github.com/users/{username}/repos"
        response = self._make_request(repos_url, cache_key)
        return response.json() if response else []

    def get_readme_content(self, repo_full_name: str):
        """저장소의 README 내용을 가져옵니다."""
        cache_key = f"readme_{repo_full_name}"
        readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
        response = self._make_request(readme_url, cache_key)
        
        if response:
            content = response.json().get("content", "")
            if content:
                try:
                    return base64.b64decode(content).decode('utf-8')
                except Exception as e:
                    st.error(f"README 디코딩 실패: {e}")
        return None

def process_markdown_content(content: str, github_api: GitHubAPI):
    """마크다운과 HTML 내용을 처리하여 표시합니다."""
    if not content:
        return
    
    # 배지와 일반 이미지를 모두 포함하는 패턴
    image_patterns = [
        r'!\[([^\]]*)\]\((https?://[^\s<>"]+(?:jpg|jpeg|gif|png|svg))[^)]*\)',  # 일반 마크다운 이미지
        r'<img\s+src="(https?://[^\s<>"]+(?:jpg|jpeg|gif|png|svg))[^>]*>',      # HTML 이미지
        r'!\[([^\]]*)\]\((https?://img\.shields\.io/[^\s<>")]+)\)',             # shields.io 배지
        r'!\[([^\]]*)\]\((https?://(?:www\.)?badgen\.net/[^\s<>")]+)\)',        # badgen.net 배지
        r'!\[([^\]]*)\]\((https?://badge\.fury\.io/[^\s<>")]+)\)'               # badge.fury.io 배지
    ]
    
    paragraphs = content.split('\n\n')
    
    for paragraph in paragraphs:
        is_image = False
        for pattern in image_patterns:
            matches = re.finditer(pattern, paragraph)
            for match in matches:
                is_image = True
                try:
                    try:
                        img_url = match.group(1) if '![' in paragraph else match.group(1)
                        
                        # URL이 유효한지 확인
                        if not img_url.startswith(('http://', 'https://')):
                            continue
                            
                        # SVG나 배지 이미지인 경우 HTML로 직접 표시
                        if any(domain in img_url.lower() for domain in ['shields.io', 'badgen.net', 'badge.fury.io']) or img_url.lower().endswith('.svg'):
                            st.markdown(f'<img src="{img_url}" alt="badge">', unsafe_allow_html=True)
                        else:
                            # 일반 이미지
                            response = github_api._make_request(img_url)
                            if response and response.status_code == 200:
                                img = Image.open(BytesIO(response.content))
                                st.image(img, caption="", use_column_width=True)
                    except Exception as e:
                        st.warning(f"이미지 처리 실패: {img_url} ({str(e)})")
                except Exception as e:
                    st.warning(f"이미지 로딩 실패: {img_url}")
        
        if not is_image and paragraph.strip():
            # HTML 태그가 포함된 경우 unsafe_allow_html=True로 렌더링
            if re.search(r'<[^>]+>', paragraph):
                st.markdown(paragraph, unsafe_allow_html=True)
            else:
                st.markdown(paragraph)

def main():
    st.title("GitHub README Viewer")
    st.write("GitHub 사용자의 모든 public 저장소의 README 파일들을 확인해보세요!")

    # GitHub 토큰 입력 (선택사항)
    token = st.sidebar.text_input(
        "GitHub 토큰 (선택사항)", 
        type="password",
        help="API 요청 한도를 늘리려면 GitHub Personal Access Token을 입력하세요."
    )

    github_api = GitHubAPI(token)
    rate_limit = github_api.check_rate_limit()
    st.sidebar.write(f"API 요청 한도: {rate_limit['limit']}")
    st.sidebar.write(f"남은 요청 횟수: {rate_limit['remaining']}")
    
    if rate_limit['remaining'] < 10:
        st.sidebar.warning("⚠️ API 요청 횟수가 얼마 남지 않았습니다!")

    username = st.text_input("GitHub 사용자명을 입력하세요")

    if username:
        with st.spinner("저장소 정보를 가져오는 중..."):
            repos = github_api.get_user_repos(username)
        
        if repos:
            st.success(f"{len(repos)}개의 저장소를 찾았습니다!")
            
            for repo in repos:
                with st.expander(f"📁 {repo['name']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"설명: {repo.get('description', '설명 없음')}")
                    with col2:
                        st.write(f"🌟 Stars: {repo['stargazers_count']}")
                    
                    st.write(f"🔗 [저장소 링크]({repo['html_url']})")
                    
                    with st.spinner("README 파일을 불러오는 중..."):
                        readme_content = github_api.get_readme_content(repo['full_name'])
                        
                    if readme_content:
                        st.markdown("---")
                        process_markdown_content(readme_content, github_api)
                    else:
                        st.warning("이 저장소에는 README 파일이 없습니다.")

if __name__ == "__main__":
    main()