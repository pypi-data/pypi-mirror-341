from setuptools import setup, find_packages

setup(
    name="worldchange",  # 모듈 이름
    version="0.1.0",  # 버전
    packages=find_packages(),  # 패키지 자동 검색
    install_requires=[  # 필요한 외부 라이브러리 (있다면)
        # "requests",  # 예시: requests 라이브러리 추가
    ],
    author="Your Name",  # 작성자 이름
    author_email="your-email@example.com",  # 작성자 이메일
    description="A module to change the weather.",  # 간단한 설명
)
