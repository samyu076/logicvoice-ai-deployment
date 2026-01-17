import re

def generate_lfa_json(full_transcript):
    """
    Tier-1 Logic Engine: Processes full session context to build 
    Indicators, Accountability, and a formal Narrative.
    """
    if not full_transcript:
        return {"lfa": [], "indicators": [], "audit": [], "accountability": [], "narrative": ""}

    text = full_transcript.lower()
    extracted = []
    indicators = []
    accountability = []

    # 1. ENTITY & LOGIC EXTRACTION
    patterns = {
        "Goal": [r"aims? to (.*?)(?=\.|$)", r"means to (.*?)(?=\.|$)"],
        "Outcome": [r"result in (.*?)(?=\.|$)", r"leads to (.*?)(?=\.|$)"],
        "Activities": [r"by (organizing .*?)(?=\.|$|and)", r"setting up (.*?)(?=\.|$|and)", r"plan to (.*?)(?=\.|$)"],
        "Assumptions": [r"assume that (.*?)(?=\.|$)", r"assumptions? (.*?)(?=\.|$)"]
    }

    for category, regex_list in patterns.items():
        for pattern in regex_list:
            matches = re.findall(pattern, text)
            for m in matches:
                if len(m) > 8:
                    extracted.append({"type": category, "text": m.strip().capitalize()})

    # 2. SECTOR-SPECIFIC M&E INDICATOR SUGGESTIONS
    if any(word in text for word in ["water", "drinking", "wells", "desalination"]):
        indicators = [
            "Liters of potable water provided per household/day",
            "% decrease in water-borne diseases in target villages",
            "Functional status of desalination units (Target: >95%)"
        ]
    elif any(word in text for word in ["school", "education", "coding", "computer"]):
        indicators = [
            "Student-to-computer ratio (Target 1:1 during labs)",
            "% of students passing post-assessment coding exams",
            "Teacher-led session attendance rate"
        ]

    # 3. ACCOUNTABILITY MAPPING (RACI Style)
    actors = {
        "panchayat": "Infrastructure Support & Land Provision",
        "ngo": "Project Implementation & Monitoring",
        "youth": "Maintenance & Operational Oversight",
        "municipality": "Regulatory Compliance & Permissions"
    }
    for actor, role in actors.items():
        if actor in text:
            accountability.append({"actor": actor.capitalize(), "role": role})

    # 4. LOGIC AUDITOR (Mentor Follow-ups)
    audit = []
    if not any(i['type'] == 'Assumptions' for i in extracted):
        audit.append("❓ What are the key risks or external assumptions for this project?")
    if "water" in text and "panchayat" not in text:
        audit.append("❓ You mentioned water units; has the local Panchayat agreed to the location?")

    # 5. GENERATE PROFESSIONAL NARRATIVE
    narrative = generate_professional_writeup(extracted)

    return {
        "lfa": extracted,
        "indicators": indicators,
        "audit": audit,
        "accountability": accountability,
        "narrative": narrative
    }

def generate_professional_writeup(lfa_list):
    """Converts LFA items into a donor-ready proposal narrative."""
    if not lfa_list: return ""
    goal = next((i['text'] for i in lfa_list if i['type'] == 'Goal'), "the stated objectives")
    activities = [i['text'].lower() for i in lfa_list if i['type'] == 'Activities']
    
    writeup = f"STRATEGIC PROPOSAL SUMMARY\n\n"
    writeup += f"Strategic Objective: The program is designed to {goal.lower()}.\n\n"
    writeup += f"Methodology: The implementation strategy focuses on {', '.join(activities)}. "
    writeup += "This approach ensures sustainable impact through community-led maintenance and rigorous stakeholder alignment."
    return writeup