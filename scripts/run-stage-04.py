import os
import datetime

def verify_environment_fortification():
    print("🛰️ RUNNING STAGE 04: ENVIRONMENT FORTIFICATION VERIFICATION...")
    
    nix_config_path = ".idx/dev.nix"
    output_dir = "memory-vault/stage_outputs"
    success_token_path = os.path.join(output_dir, "04_env_success.txt")
    
    if not os.path.exists(nix_config_path):
        print("HALT: N/A: SOURCE FIDELITY VOID. DEV.NIX NOT FOUND IN ROOT.")
        return False
        
    try:
        with open(nix_config_path, "r") as f:
            nix_content = f.read()
            
        # Assert structural presence of newly deployed blueprint parameters
        required_signatures = [
            "pkgs.nodejs_22",
            "dbaeumer.vscode-eslint",
            "esbenp.prettier-vscode",
        ]
        
        # Check for `onCreate` in a more robust way
        has_on_create = "onCreate = {" in nix_content or "onCreate={" in nix_content
        
        for signature in required_signatures:
            if signature not in nix_content:
                print(f"HALT: ENVIRONMENT CONFIGDRIFT DETECTED. MISSING: {signature}")
                return False
                
        if not has_on_create:
            print("HALT: ENVIRONMENT CONFIGDRIFT DETECTED. MISSING: workspace.onCreate")
            return False
            
        # Generate the local verification receipt
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        receipt_payload = (
            f"=== AETHER_FORGE STAGE 04 ENVIRONMENT ATTESTATION ===\n"
            f"STATUS: VERIFIED_COMPLIANT\n"
            f"TIMESTAMP_UTC: {timestamp}\n"
            f"DEEP_LINT_ENGINES: ACTIVE\n"
            f"NIX_RUNTIME_TARGET: pkgs.nodejs_22\n"
        )
        
        with open(success_token_path, "w") as f:
            f.write(receipt_payload)
            
        print(f"✅ STAGE 04 ENVIRONMENT FORTIFICATION DEPLOYED -> {success_token_path}")
        return True
        
    except Exception as e:
        print(f"HALT: CRITICAL SYSTEM INGESTION EXCEPTION: {str(e)}")
        return False

if __name__ == "__main__":
    verify_environment_fortification()
