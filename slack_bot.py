from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from gemini_helper import ask_gemini

import os
import json

load_dotenv()
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(os.getenv("SLACK_SIGNING_SECRET"))

async def handle_slack_event(req: Request):
    body = await req.body()
    print("🔵 Raw Body:", body)

    if not verifier.is_valid_request(body, req.headers):
        raise HTTPException(status_code=403, detail="Invalid Slack signature")

    payload = await req.json()
    print("🟡 Parsed Payload:", json.dumps(payload, indent=2))

    if "challenge" in payload:
        return {"challenge": payload["challenge"]}

    event = payload.get("event", {})
    print("🟢 Slack Event:", event)

    if event.get("type") == "app_mention" or event.get("channel_type") == "im":
        user_id = event.get("user")
        bot_user_id = payload.get("authorizations", [{}])[0].get("user_id")

        # ✅ Prevent infinite loop
        if user_id == bot_user_id:
            print("⛔ Ignoring bot's own message to avoid loop")
            return {"ok": True}

        text = event.get("text", "")
        user_question = text.split(">", 1)[-1].strip()
        channel = event.get("channel")

        # Print to confirm message content
        print("📨 User Question:", user_question)

        context = """New Year's. Day	1 Jan 2025	Fixed Holiday	
        Holi	14 Mar 2025	Fixed Holiday	Friday
        Ramzan Id/Eid-ul-Fitar	31 Mar 2025	Fixed Holiday	Monday
        Baisakhi	14 Apr 2025	Fixed Holiday	Monday
        May Day (Labour Day)	1 May 2025	Fixed Holiday	Thursday"""
        print("📚 Context Sent to Gemini:", context)

        answer = ask_gemini(context, user_question)
        print("🤖 Gemini Reply:", answer)

        slack_client.chat_postMessage(channel=channel, text=answer)

    return {"ok": True}
