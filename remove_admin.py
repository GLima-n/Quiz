import json
import os
import re

arquivo = 'ranking.json'

if os.path.exists(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        ranking = json.load(f)
    
    print(f"Total entries before: {len(ranking)}")
    
    # Filter out admin
    cleaned_ranking = []
    
    for item in ranking:
        nome_norm = re.sub(r'\s+', ' ', item['nome'].strip()).lower()
        
        # Check if it is admin
        if nome_norm == 'alef gomes#':
            print(f"Removing admin entry: {item['nome']}")
        else:
            cleaned_ranking.append(item)
            
    print(f"Total entries after: {len(cleaned_ranking)}")
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(cleaned_ranking, f, indent=2, ensure_ascii=False)
    
    print("Ranking cleaned successfully!")
else:
    print("Ranking file not found.")
