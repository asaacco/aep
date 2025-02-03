# modules/processing/advanced_dedupe.py
from difflib import SequenceMatcher
import hashlib

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def deduplicate(articles, title_threshold=0.9, content_threshold=0.8):
    unique = []
    hashes = set()
    
    for article in sorted(articles, key=lambda x: x['date'], reverse=True):
        title_hash = hashlib.md5(article['title'].encode()).hexdigest()
        content_hash = hashlib.md5(article['content'][:500].encode()).hexdigest()
        
        # 정확한 해시 비교
        if title_hash in hashes or content_hash in hashes:
            continue
            
        # 유사성 검사
        duplicate_found = False
        for u in unique:
            if similarity(article['title'], u['title']) > title_threshold:
                duplicate_found = True
                break
                
        if not duplicate_found:
            unique.append(article)
            hashes.update([title_hash, content_hash])
    
    print(f"중복 제거 완료: {len(articles)} → {len(unique)}")
    return unique