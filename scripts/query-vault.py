import os
import sys
import re

def search_obsidian_vault(query_term):
    vault_path = "memory-vault/obsidian-vault"
    print(f"🔍 SCANNING OBSIDIAN VAULT CORE FOR KNOWLEDGE VECTOR: '{query_term}'...")
    
    if not os.path.exists(vault_path):
        print("HALT: N/A: SOURCE FIDELITY VOID. KNOWLEDGE GRAPH SEVERED.")
        return
        
    found_matches = 0
    # Walk through your local markdown knowledge files
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith(".md"):
                full_file_path = os.path.join(root, file)
                with open(full_file_path, "r", errors="ignore") as f:
                    for line_num, line_content in enumerate(f, 1):
                        if re.search(query_term, line_content, re.IGNORECASE):
                            found_matches += 1
                            relative_path = os.path.relpath(full_file_path, vault_path)
                            print(f"📌 [{relative_path} : Line {line_num}]: {line_content.strip()}")
                            
    if found_matches == 0:
        print("⚠️ ZERO SEMANTIC MATCHES IDENTIFIED IN ACTIVE RECORDINGS.")
    else:
        print(f"✅ COMPLETED. LOCATED {found_matches} CONTEXTUAL GRAPH REFERENCES.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/query-vault.py <search_term>")
    else:
        search_obsidian_vault(sys.argv[1])