"""Monitor Hyperliquid positions and alert on margin thresholds."""
import subprocess, json

MARGIN_ALERT_PCT = 80  # alert if margin used exceeds this

def get_positions():
    """Get current Hyperliquid positions via openbroker CLI."""
    try:
        result = subprocess.run(["openbroker", "positions"], 
                                capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def get_account():
    """Get account balance and margin info."""
    try:
        result = subprocess.run(["openbroker", "account", "list"],
                                capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

def check_margin_alert(positions_data):
    """Parse margin usage and return alert if above threshold."""
    # Parse margin percentage from output
    for line in positions_data.split("\n"):
        if "margin" in line.lower() and "%" in line:
            try:
                pct = float(line.split("%")[0].split()[-1])
                if pct > MARGIN_ALERT_PCT:
                    return f"⚠️ MARGIN ALERT: {pct:.1f}% used (threshold: {MARGIN_ALERT_PCT}%)"
            except: pass
    return None

if __name__ == "__main__":
    positions = get_positions()
    print(positions)
    alert = check_margin_alert(positions)
    if alert:
        print(alert)
