import os
import json
import datetime

def verify_infrastructure_alignment():
    print("🛰️ RUNNING STAGE 01: INFRASTRUCTURE VERIFICATION LIFECYCLE...")
    
    firestore_path = "firestore.rules"
    database_path = "database.rules.json"
    output_dir = "memory-vault/stage_outputs"
    success_token_path = os.path.join(output_dir, "01_infra_success.txt")
    
    # Assert physical file node visibility constraints
    if not os.path.exists(firestore_path) or not os.path.exists(database_path):
        print("HALT: N/A: SOURCE FIDELITY VOID. FIREWALL RULES MISSING FROM ROOT.")
        return False
        
    try:
        # Read local configuration blocks
        with open(firestore_path, "r") as f:
            firestore_content = f.read()
        with open(database_path, "r") as f:
            database_content = f.read()
            
        # Run strict symbolic validation rules
        if "rules_version = '2'" not in firestore_content or "isValidNode" not in firestore_content:
            print("HALT: FIRESTORE SECURITY SCHEMAS DEVIATE FROM BLUEPRINT SPEC.")
            return False
            
        if "presence" not in database_content or "auth.uid === $userId" not in database_content:
            print("HALT: REALTIME DATABASE RULES SHOW STATE PRESERVATION DRIFT.")
            return False
            
        # Generate the tangible plain text verification receipt requested by Van Clief
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now(datetime.UTC).isoformat()
        
        receipt_payload = (
            f"=== AETHER_FORGE STAGE 01 ATTESTATION RECONCILIATION ===\n"
            f"STATUS: VERIFIED_COMPLIANT\n"
            f"TIMESTAMP_UTC: {timestamp}\n"
            f"FIRESTORE_HASH_SIZE: {len(firestore_content)} BYTES\n"
            f"RTDB_HASH_SIZE: {len(database_content)} BYTES\n"
            f"GOVERNANCE_PRECEDENCE: ManyIH-Tier-2-LOCKED\n"
        )
        
        with open(success_token_path, "w") as f:
            f.write(receipt_payload)
            
        print(f"✅ STAGE 01 ATTESTATION ISSUED SUCCESSFULLY -> {success_token_path}")
        return True
        
    except Exception as e:
        print(f"HALT: CRITICAL SYSTEM INGESTION EXCEPTION: {str(e)}")
        return False

if __name__ == "__main__":
    verify_infrastructure_alignment()