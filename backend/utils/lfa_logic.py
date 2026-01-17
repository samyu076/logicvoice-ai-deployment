from typing import Dict, List

LFA_SCHEMA = {
    "goal": [],
    "outcome": [],
    "outputs": [],
    "activities": [],
    "indicators": [],
    "assumptions": []
}

def classify_sentence(sentence: str) -> str:
    s = sentence.lower()

    # GOAL – long-term change
    if any(x in s for x in ["overall goal", "primary goal", "aim is to", "goal is to", "long term"]):
        return "goal"

    # OUTCOME – end-state change
    if any(x in s for x in ["by the end", "will result in", "children will", "students will"]):
        return "outcome"

    # OUTPUT – tangible deliverables
    if any(x in s for x in ["will deliver", "program will provide", "sessions", "workshops", "materials"]):
        return "outputs"

    # ACTIVITY – actions taken
    if any(x in s for x in ["we will conduct", "we will do", "teaching", "training", "sessions per week"]):
        return "activities"

    # INDICATOR – measurement
    if any(x in s for x in ["measured by", "tracked by", "assessment", "attendance", "scores", "monitoring"]):
        return "indicators"

    # ASSUMPTION – external dependency
    if any(x in s for x in ["assume", "assuming", "depends on", "availability of", "cooperation of"]):
        return "assumptions"

    return None


def update_lfa(lfa: Dict[str, List[str]], sentence: str):
    category = classify_sentence(sentence)
    if not category:
        return lfa  # ignore unclassified noise

    if sentence not in lfa[category]:
        lfa[category].append(sentence)

    return lfa
