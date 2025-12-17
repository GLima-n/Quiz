import json
import os
import re

arquivo = 'ranking.json'

if os.path.exists(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as f:
        ranking = json.load(f)
    
    print(f"Total entries before: {len(ranking)}")
    
    unique_ranking = {}
    
    for item in ranking:
        nome_norm = re.sub(r'\s+', ' ', item['nome'].strip()).lower()
        
        if nome_norm in unique_ranking:
            existing = unique_ranking[nome_norm]
            # Update if current has better score
            if item['pontuacao'] > existing['pontuacao']:
                unique_ranking[nome_norm] = item
            # Or same score but better time
            elif item['pontuacao'] == existing['pontuacao'] and item['tempo_total'] < existing['tempo_total']:
                unique_ranking[nome_norm] = item
        else:
            unique_ranking[nome_norm] = item
            
    final_ranking = list(unique_ranking.values())
    print(f"Total entries after: {len(final_ranking)}")
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(final_ranking, f, indent=2, ensure_ascii=False)
    
    print("Ranking cleaned successfully!")
else:
    print("Ranking file not found.")
