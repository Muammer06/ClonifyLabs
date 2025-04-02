#!/usr/bin/env python3

import git
import os
import datetime
import sys
from pathlib import Path

# GitHub repository dizini
repo_path = os.getcwd()
repo = git.Repo(repo_path)

# Son committen itibaren değişiklikleri al
latest_commit = repo.head.commit
previous_commit = list(repo.iter_commits(max_count=2))[1] if len(list(repo.iter_commits(max_count=2))) > 1 else None

if previous_commit:
    # Değişiklikleri alır
    diffs = previous_commit.diff(latest_commit)
    
    # Değişiklik özeti oluştur
    summary = f"## {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Tarihli Kod Değişiklikleri\n\n"
    summary += f"Commit: {latest_commit.hexsha[:7]} - {latest_commit.message.strip()}\n\n"
    
    # Değiştirilen dosyaları listele
    summary += "### Değiştirilen Dosyalar\n\n"
    
    for diff_item in diffs:
        if diff_item.a_path.endswith(('.py', '.cpp', '.h', '.hpp', '.c', '.js', '.ts')):
            summary += f"- `{diff_item.a_path}`\n"
            
            # Değişiklik türünü belirle
            if diff_item.new_file:
                summary += "  - Yeni dosya oluşturuldu\n"
            elif diff_item.deleted_file:
                summary += "  - Dosya silindi\n"
            elif diff_item.renamed:
                summary += f"  - Dosya yeniden adlandırıldı: `{diff_item.a_path}` -> `{diff_item.b_path}`\n"
            else:
                # Kod değişikliklerini basitçe analiz et
                try:
                    # Eklenen/silinen satırları say
                    if diff_item.diff:
                        added = len([line for line in diff_item.diff.decode('utf-8').split('\n') if line.startswith('+')])
                        removed = len([line for line in diff_item.diff.decode('utf-8').split('\n') if line.startswith('-')])
                        summary += f"  - {added} satır eklendi, {removed} satır silindi\n"
                except:
                    summary += "  - Değişiklikler analiz edilemedi\n"
    
    print(summary)
else:
    print("## İlk Commit\n\nHenüz karşılaştırılacak önceki commit yok.")
