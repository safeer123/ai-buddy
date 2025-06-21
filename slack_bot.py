from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from dotenv import load_dotenv
from fastapi import Request, HTTPException
from vector_store import load_vector_store
from gemini_helper import ask_gemini

import os
import json

load_dotenv()
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
verifier = SignatureVerifier(os.getenv("SLACK_SIGNING_SECRET"))

vectorstore = load_vector_store()
retriever = vectorstore.as_retriever()

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

    if event.get("type") == "app_mention":
        text = event.get("text", "")
        user_question = text.split(">", 1)[-1].strip()
        channel = event.get("channel")

        # Print to confirm message content
        print("📨 User Question:", user_question)

        docs = retriever.get_relevant_documents(user_question)
        context = "\n\n".join([doc.page_content for doc in docs[:3]])
        print("📚 Context Sent to Gemini:", context)

        answer = ask_gemini(context, user_question)
        print("🤖 Gemini Reply:", answer)

        slack_client.chat_postMessage(channel=channel, text=answer)

    return {"ok": True}
