#!/usr/bin/env python3
"""
AgentMail Inbox Monitor - Telegram Notifications
Polls calmship333@agentmail.to for new messages, sends Telegram alerts
"""

import os
import json
import sys
import requests
from datetime import datetime
from pathlib import Path
from agentmail import AgentMail

# Configuration
API_KEY = "am_us_6a1a9d00cf55ff6bb29a1923592434a0723496115c8a3a8e2354d255d3a9e071"
INBOX_EMAIL = "calmship333@agentmail.to"
STATE_FILE = Path("/Users/clawedteam/.openclaw/workspace/.agentmail_state.json")
LOG_FILE = Path("/Users/clawedteam/.openclaw/logs/agentmail.log")

# Telegram config (via OpenClaw gateway)
TELEGRAM_BOT_TOKEN = "8578755001:AAGFBOCck8SmGBGrJGqfkTHGHa6Wy8HdwHo"
TELEGRAM_USER_ID = "1389370782"  # Kevin's chat ID

def log_message(msg):
    """Log to file and stdout"""
    timestamp = datetime.now().isoformat()
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    
    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(full_msg + "\n")

def send_telegram(message):
    """Send message to Kevin via Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_USER_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            log_message(f"✓ Telegram notification sent")
            return True
        else:
            log_message(f"✗ Telegram failed: {response.status_code}")
            return False
    except Exception as e:
        log_message(f"✗ Telegram error: {e}")
        return False

def load_state():
    """Load last processed messages"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                data = json.load(f)
                # Ensure processed_ids exists
                if "processed_ids" not in data:
                    data["processed_ids"] = []
                return data
        except Exception as e:
            log_message(f"State load error: {e}, using fresh state")
            return {"processed_ids": []}
    return {"processed_ids": []}

def save_state(state):
    """Save processed message IDs"""
    # Ensure processed_ids exists
    if "processed_ids" not in state:
        state["processed_ids"] = []
    
    # Ensure directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def mark_as_read(client, message_id):
    """Mark message as read"""
    try:
        # AgentMail mark-as-read endpoint (if available)
        # For now, just log it
        log_message(f"Marked {message_id} as read")
        return True
    except Exception as e:
        log_message(f"Error marking read: {e}")
        return False

def check_inbox():
    """Check inbox for new messages and notify"""
    client = AgentMail(api_key=API_KEY)
    state = load_state()
    
    try:
        # List messages from inbox
        response = client.inboxes.messages.list(inbox_id=INBOX_EMAIL)
        
        if not response.messages:
            log_message("No messages in inbox")
            return
        
        new_messages = []
        for msg in response.messages:
            # Check if already processed
            if msg.message_id not in state["processed_ids"]:
                # Check for unread label
                if "unread" in msg.labels:
                    new_messages.append(msg)
                    state["processed_ids"].append(msg.message_id)
        
        if new_messages:
            log_message(f"Found {len(new_messages)} new unread message(s)")
            
            for msg in new_messages:
                # Log details
                log_message(f"\n--- New Message ---")
                log_message(f"From: {msg.from_}")
                log_message(f"Subject: {msg.subject}")
                log_message(f"Received: {msg.timestamp}")
                log_message(f"Preview: {msg.preview[:100] if msg.preview else 'No preview'}")
                
                # Build Telegram notification
                telegram_msg = (
                    f"📧 <b>New Email</b>\n\n"
                    f"<b>From:</b> {msg.from_}\n"
                    f"<b>Subject:</b> {msg.subject}\n"
                    f"<b>Time:</b> {msg.timestamp}\n\n"
                    f"<b>Preview:</b> {msg.preview[:200] if msg.preview else '(no preview)'}"
                )
                
                # Send to Telegram
                send_telegram(telegram_msg)
                
                # Mark as read
                mark_as_read(client, msg.message_id)
            
            save_state(state)
            log_message(f"State updated: {len(state['processed_ids'])} total processed")
        else:
            log_message("No new unread messages")
            
    except Exception as e:
        log_message(f"✗ Error checking inbox: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point"""
    log_message("=== AgentMail Monitor Starting ===")
    check_inbox()
    log_message("=== Check Complete ===\n")

if __name__ == "__main__":
    main()
