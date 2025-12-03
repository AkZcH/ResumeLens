import re
from helpers.regex_patterns import EMAIL_REGEX, PHONE_REGEX

class RegexExtractors:
    @staticmethod
    def extract_email(text: str) -> str:
        match = re.search(EMAIL_REGEX, text)
        return match.group(0) if match else ""
    
    @staticmethod
    def extract_phone(text: str) -> str:
        match = re.search(PHONE_REGEX, text)
        return match.group(0) if match else ""
    
    @staticmethod
    def extract_urls(text: str) -> list:
        url_regex = r'https?://[^\s]+'
        return re.findall(url_regex, text)