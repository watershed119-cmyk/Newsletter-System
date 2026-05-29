from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeedSource:
    country: str
    source: str
    url: str
    priority: str = "high"


# Google News RSS — domain + keyword based collection (no API key required)
FEED_SOURCES: tuple[FeedSource, ...] = (
    FeedSource("USA", "US EPA", "https://news.google.com/rss/search?q=site:epa.gov+(water+quality+OR+PFAS+OR+watershed)&hl=en-US&gl=US&ceid=US:en"),
    FeedSource("USA", "USGS", "https://news.google.com/rss/search?q=site:usgs.gov+water+quality&hl=en-US&gl=US&ceid=US:en"),
    FeedSource("EU", "European Environment Agency", "https://news.google.com/rss/search?q=site:eea.europa.eu+water&hl=en-US&gl=US&ceid=US:en"),
    FeedSource("EU", "EC Environment", "https://news.google.com/rss/search?q=site:environment.ec.europa.eu+water&hl=en-US&gl=US&ceid=US:en"),
    FeedSource("Japan", "環境省", "https://news.google.com/rss/search?q=site:env.go.jp+(水質+OR+水環境)&hl=ja&gl=JP&ceid=JP:ja"),
    FeedSource("Japan", "NIES", "https://news.google.com/rss/search?q=site:nies.go.jp+水環境&hl=ja&gl=JP&ceid=JP:ja"),
    FeedSource("Korea", "환경부", "https://news.google.com/rss/search?q=site:me.go.kr+(수질+OR+수환경+OR+유역)&hl=ko&gl=KR&ceid=KR:ko"),
    FeedSource("Korea", "국립환경과학원", "https://news.google.com/rss/search?q=site:nier.go.kr+(수질+OR+수생태)&hl=ko&gl=KR&ceid=KR:ko"),
    FeedSource("Australia", "DCCEEW", "https://news.google.com/rss/search?q=site:dcceew.gov.au+water+quality&hl=en-US&gl=AU&ceid=AU:en"),
    FeedSource("Australia", "CSIRO", "https://news.google.com/rss/search?q=site:csiro.au+water&hl=en-US&gl=AU&ceid=AU:en"),
    FeedSource("Academic", "Water Research", "https://news.google.com/rss/search?q=water+quality+site:sciencedirect.com&hl=en-US&gl=US&ceid=US:en"),
)

INCLUDE_KEYWORDS = (
    "water quality",
    "water pollution",
    "watershed",
    "nonpoint",
    "aquatic ecosystem",
    "pfas",
    "microplastic",
    "수질",
    "수환경",
    "유역",
    "비점",
    "수생태",
    "水質",
    "水環境",
    "流域",
)

EXCLUDE_KEYWORDS = (
    "drinking water pipe",
    "sewer pipe",
    "flood warning",
    "drought emergency",
    "ocean plastic gyre",
    "marine debris island",
    "정수장 배관",
    "하수관로",
)

TIER1_DOMAINS = (
    "epa.gov",
    "eea.europa.eu",
    "environment.ec.europa.eu",
    "env.go.jp",
    "nies.go.jp",
    "me.go.kr",
    "nier.go.kr",
    "dcceew.gov.au",
    "who.int",
    "sciencedirect.com",
    "acs.org",
)

MONTHLY_SECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "수질 기준 및 규제 변화": ("standard", "regulation", "rule", "기준", "규제", "規制", "基準"),
    "신규 오염물질 (PFAS·미세플라스틱)": ("pfas", "microplastic", "emerging contaminant", "미세플라스틱", "신규오염"),
    "수생태계 모니터링 및 복원": ("ecosystem", "restoration", "수생태", "생태계", "복원"),
    "유역관리 및 비점원오염 저감": ("watershed", "nonpoint", "runoff", "유역", "비점"),
    "기후변화와 물환경": ("climate", "기후", "drought", "가뭄"),
}
