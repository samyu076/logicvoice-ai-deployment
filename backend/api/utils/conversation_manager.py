# backend/utils/conversation_manager.py

import re

class ConversationManager:
    def __init__(self):
        self.clients = {}

    def create_client(self, client_id):
        self.clients[client_id] = {
            "transcripts": [],
            "lfa_draft": {
                "Goal": "",
                "Outcomes": [],
                "Outputs": [],
                "Activities": [],
                "Indicators": [],
                "Assumptions": []
            },
            "pending_questions": [],
        }

    def add_transcript(self, client_id, transcript_text):
        if client_id not in self.clients:
            self.create_client(client_id)
        self.clients[client_id]["transcripts"].append(transcript_text)
        self.update_lfa_from_transcript(client_id, transcript_text)

    def update_lfa_from_transcript(self, client_id, transcript_text):
        """
        Free version: simple keyword-based extraction for LFA.
        Generates follow-up questions for missing fields.
        """
        client = self.clients[client_id]
        lfa = client["lfa_draft"]
        pending = client["pending_questions"]

        # Very simple rule-based mapping
        # Look for keywords in transcript to assign fields
        if "goal" in transcript_text.lower():
            lfa["Goal"] = transcript_text
        if "outcome" in transcript_text.lower():
            lfa["Outcomes"].append(transcript_text)
        if "output" in transcript_text.lower():
            lfa["Outputs"].append(transcript_text)
        if "activity" in transcript_text.lower():
            lfa["Activities"].append(transcript_text)
        if "indicator" in transcript_text.lower():
            lfa["Indicators"].append(transcript_text)
        if "assumption" in transcript_text.lower():
            lfa["Assumptions"].append(transcript_text)

        # Simple logic auditor
        if not lfa["Goal"]:
            pending.append("Please specify the main Goal of the program.")
        if not lfa["Outcomes"]:
            pending.append("Mention at least one Outcome for the program.")
        if not lfa["Outputs"]:
            pending.append("Mention at least one Output for the program.")
        if not lfa["Activities"]:
            pending.append("List at least one Activity to achieve the Output.")
        if not lfa["Indicators"]:
            pending.append("Provide measurable Indicators for Outcomes/Outputs.")
        if not lfa["Assumptions"]:
            pending.append("List key Assumptions underlying this program.")

        # Save back
        client["lfa_draft"] = lfa
        client["pending_questions"] = pending

    def get_client_state(self, client_id):
        if client_id not in self.clients:
            self.create_client(client_id)
        return self.clients[client_id]
