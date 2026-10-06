import subprocess
import json
import time

SESMO_ADDR = "0x120ae397B38E9E1E4C5377597C393F9DC4373eBB"
CONSUMER_ADDR = "0xDd8CD2Be680B14bBf07d3DB59372720e67C6E67A"
PASSWORD = "sesmopassword"
MY_ACCOUNT = "0x798BB9c649751CCB2E589c3d04c736fC23AD17DD" # from task 106 logs

def run_genlayer_call(contract, method, *args):
    cmd = ["genlayer.cmd", "call", contract, method]
    if args:
        cmd.extend(["--args"])
        cmd.extend(str(a) for a in args)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Call failed: {result.stderr}")
    
    # parse the JSON output from genlayer CLI
    output = result.stdout.strip()
    try:
        # genlayer call outputs 'Result:\n<value>' or JSON
        if "Result:" in output:
            res = output.split("Result:\n")[1].strip()
            # replace single quotes with double quotes for json parsing if it's a dict/array
            try:
                import ast
                return ast.literal_eval(res)
            except:
                return res
        return output
    except Exception as e:
        return output

def run_genlayer_write(contract, method, *args):
    print(f"Executing {method}...")
    cmd = ["genlayer.cmd", "write", contract, method]
    if args:
        cmd.extend(["--args"])
        cmd.extend(str(a) for a in args)
    
    result = subprocess.run(cmd, input=PASSWORD + "\n", capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Write failed: {result.stderr}\n{result.stdout}")
    
    output = result.stdout
    print(output)
    return output

print("Getting action hash...")
action_hash = run_genlayer_call(
    CONSUMER_ADDR, "preview_grant_action_hash",
    MY_ACCOUNT, 100, "Live Test Grant"
)
print("Action hash:", action_hash)

print("\nCreating SESMO...")
run_genlayer_write(
    SESMO_ADDR, "create_sesmo",
    CONSUMER_ADDR, 
    "Live Test Title", 
    "Activation of service order SESMO-DEMO-001",
    "Classify SATISFIED only if the public source explicitly states that order SESMO-DEMO-001 is active. Classify FAILED if it explicitly states that the order failed, was rejected, or was cancelled. Otherwise return INCONCLUSIVE.",
    action_hash,
    '["https://example.com/service-status"]',
    1, 0, 600, 60
)

sesmo_id = 1
while True:
    try:
        run_genlayer_call(SESMO_ADDR, "get_sesmo", sesmo_id)
        sesmo_id += 1
    except Exception:
        break
sesmo_id -= 1  # the last one that succeeded
print("Created SESMO ID:", sesmo_id)

print("\nGetting definition hash...")
sesmo_record = run_genlayer_call(SESMO_ADDR, "get_sesmo", sesmo_id)
definition_hash = sesmo_record["definition_hash"]
print("Definition Hash:", definition_hash)

print("\nStaging Grant on Consumer...")
run_genlayer_write(
    CONSUMER_ADDR, "stage_grant",
    sesmo_id, definition_hash, MY_ACCOUNT, 100, "Live Test Grant"
)

print("\nWaiting for 10 seconds to allow observation window and consensus...")
time.sleep(10)

print("\nResolving SESMO...")
run_genlayer_write(SESMO_ADDR, "resolve_sesmo", sesmo_id)

print("\nChecking final SESMO state...")
final_sesmo = run_genlayer_call(SESMO_ADDR, "get_sesmo", sesmo_id)
print("SESMO State Name:", final_sesmo["state_name"])
print("Resolution Outcome:", final_sesmo["resolution_outcome"])

print("\nChecking final Consumer Grant state...")
grant_record = run_genlayer_call(CONSUMER_ADDR, "get_grant", 1)  # Assuming grant_id is 1
print("Grant State Name:", grant_record["state_name"])

print("\nChecking usable credit...")
credit = run_genlayer_call(CONSUMER_ADDR, "get_usable_credit", MY_ACCOUNT)
print("Usable credit:", credit)

print("\nLive test complete.")
