# src/backend/aho_corasick.py

from collections import deque

def build_trie(keywords: list[str]) -> dict:
    trie = {}
    for keyword in keywords:
        node = trie
        for char in keyword:
            node = node.setdefault(char, {})
        node.setdefault('_output', []).append(keyword)
    return trie

def build_failure_links(trie: dict):
    queue = deque()
    for char, node in trie.items():
        if char != '_output':
            node['_failure'] = trie
            queue.append(node)
    
    while queue:
        current_node = queue.popleft()
        for char, next_node in current_node.items():
            if char == '_output' or char == '_failure':
                continue

            failure_node = current_node['_failure']
            while char not in failure_node and failure_node is not trie:
                failure_node = failure_node['_failure']

            if char in failure_node:
                next_node['_failure'] = failure_node[char]
            else:
                next_node['_failure'] = trie
            
            output = next_node['_failure'].get('_output', [])
            next_node.setdefault('_output', []).extend(output)
            queue.append(next_node)

def aho_corasick(text:str, keywords: list[str]) -> dict:
    if not keywords:
        return {}
    
    trie = build_trie(keywords)
    build_failure_links(trie)

    results = {keyword: 0 for keyword in keywords}
    current_node = trie

    for char in text:
        while char not in current_node and current_node is not trie:
            current_node = current_node['_failure']
        
        if char in current_node:
            current_node = current_node[char]
        else:
            current_node = trie
        
        if '_output' in current_node:
            for keyword in current_node['_output']:
                results[keyword] += 1
    return results

if __name__ == '__main__':
    text_sample = "he said his new shell is a hell"
    keywords_sample = ["he", "she", "his", "hers", "hell"]
    
    print(f"Text: '{text_sample}'")
    print(f"Keywords: {keywords_sample}")
    
    matches = aho_corasick(text_sample, keywords_sample)
    
    print("\nHasil Pencarian:")
    for keyword, count in matches.items():
        if count > 0:
            print(f"- '{keyword}' ditemukan sebanyak {count} kali.")