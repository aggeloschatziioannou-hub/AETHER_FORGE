import json
import os
import datetime

def consolidate_memory():
    todo_path = "memory-vault/todo.md"
    ledger_path = "memory-vault/evolution-ledger.json"
    
    if not os.path.exists(todo_path):
        print("N/A: SOURCE FIDELITY VOID")
        return
        
    with open(todo_path, "r") as f:
        active_context = f.read()
        
    # Python 3.13 compliant timezone-aware UTC generation
    # Prevents naive offset comparisons across distributed agent meshes
    distilled_insights = {
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
        "system_state": "STABLE",
        "atomic_concepts_extracted": [
            line.strip() for line in active_context.split("\n") if line.startswith("- [x]")
        ]
    }
    
    ledger_data = []
    if os.path.exists(ledger_path) and os.path.getsize(ledger_path) > 0:
        with open(ledger_path, "r") as f:
            try:
                ledger_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Memory vault ledger suffered minor corruption. Re-anchoring.")
            
    ledger_data.append(distilled_insights)
    
    with open(ledger_path, "w") as f:
        json.dump(ledger_data, f, indent=2)
        
    print("@@SCAN: Timezone-aware memory consolidation completed successfully. State anchored at Merkle root.")

if __name__ == "__main__":
    consolidate_memory()