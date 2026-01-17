# Backend Responsibility

The backend is responsible for:

1. Receiving user text or voice transcripts
2. Converting raw language into structured logic
3. Maintaining the Logical Framework structure
4. Asking logic-strengthening follow-up questions
5. Saving versions of the LFA
6. Exporting LFA data to Excel / CSV / Text

Backend is the single source of truth.
All program logic lives here.
{
  "Goal": {
    "description": "Long-term objective of the program",
    "keywords": ["improve", "increase", "reduce", "enhance", "achieve"],
    "example": "Improve student literacy by 20% in one year"
  },
  "Outcomes": {
    "description": "Measurable changes due to outputs",
    "keywords": ["better", "higher", "improved", "change", "result"],
    "example": "Improved teaching quality and student performance"
  },
  "Outputs": {
    "description": "Tangible products or services delivered",
    "keywords": ["trained", "built", "organized", "distributed", "delivered"],
    "example": "50 teachers trained"
  },
  "Activities": {
    "description": "Tasks needed to create outputs",
    "keywords": ["organize", "conduct", "deliver", "prepare", "schedule"],
    "example": "Organize training sessions, distribute teaching materials"
  },
  "Responsibility": {
    "description": "Who is accountable for tasks/outputs",
    "keywords": ["teacher", "officer", "manager", "team", "staff"],
    "example": "Block officers, teachers"
  },
  "Monitoring": {
    "description": "How progress is checked",
    "keywords": ["review", "monitor", "track", "check", "evaluate"],
    "example": "Monthly reviews by block officers"
  },
  "Indicators": {
    "description": "How change is measured",
    "keywords": ["score", "percentage", "level", "number", "data"],
    "example": "Literacy scores from tests"
  },
  "MeansOfVerification": {
    "description": "Source of information for indicators",
    "keywords": ["report", "record", "test", "survey", "observation"],
    "example": "Test results, official reports"
  },
  "Assumptions": {
    "description": "Conditions outside control but required for success",
    "keywords": ["assume", "condition", "support", "requirement", "if"],
    "example": "Assume government support continues"
  }
}
# STEP 3B: Example sentence mapping

| Spoken Sentence                               | LFA Field                        | Reason / Mapping Logic                                      |
|-----------------------------------------------|---------------------------------|-------------------------------------------------------------|
| We will train 50 teachers by June.            | Output                           | Action delivered (training)                                 |
| Block officers will review monthly.           | Responsibility / Monitoring      | Who → Responsibility, How often → Monitoring               |
| Student literacy should improve by 20% in 1y. | Goal / Outcome                   | Long-term measurable change                                  |
| Tests will track student progress.            | Indicator / Means of Verification| How change is measured → Indicator; Source → Means of Verification |
| Assume government support continues.          | Assumptions                       | Condition outside control but required                      |
# STEP 5: Backend Workflow (Conceptual)

## 1. Receive Input
- User can send **text** or **voice**
- Voice will be converted to text using Whisper API
- Raw transcript saved in: data/transcripts/

## 2. Parse Sentences
- Break transcript into individual sentences
- Each sentence will be analyzed for keywords

## 3. Map Sentences → LFA Fields
- Use the mapping JSON (lfa-mapping.json) as reference
- Assign each sentence to the correct field:
  Goal / Outcome / Output / Activity / Responsibility / Monitoring / Indicator / MeansOfVerification / Assumption

## 4. Create Structured LFA JSON
- Example structure:
{
  "program_name": "Teacher Training",
  "goal": "Improve student literacy by 20% in 1 year",
  "outcomes": ["Improved teaching quality", "Better student performance"],
  "outputs": ["50 teachers trained"],
  "activities": ["Organize training sessions", "Distribute materials"],
  "responsibility": ["Block officers", "Teachers"],
  "monitoring": ["Monthly review"],
  "indicators": ["Test scores"],
  "means_of_verification": ["Test results, reports"],
  "assumptions": ["Government support continues"],
  "raw_transcript": "We will train 50 teachers by June..."
}

## 5. Save Structured JSON
- Save each program/session JSON in: data/lfa-json/
- Each file can be named with program name or timestamp

## 6. Prepare for Export
- Later convert JSON → Excel / CSV / Text
- Save exports in: data/exports/
# STEP 8: Logic Auditor / AI Follow-Up Questions

## Purpose
- Check structured LFA for gaps or missing links
- Ask user actionable questions to improve logic

## Audit Rules
1. Every Output must link to at least one Outcome
2. Every Activity must link to an Output
3. Every Outcome must have Indicators
4. Every Indicator must have Means of Verification
5. Every Activity/Output should have Responsibility assigned
6. Assumptions must be clearly stated

## Workflow
1. Receive structured LFA JSON
2. Check each rule above
3. Generate follow-up questions for missing / inconsistent fields
4. Return questions to frontend chat
5. Update LFA JSON after user answers
6. Repeat until all logic gaps are filled
# STEP 9: Exporting JSON → Excel / CSV / Text

## Workflow
1. Receive structured LFA JSON
2. User selects export format
3. Convert JSON → selected format
   - Excel / CSV → tabular format
   - Text → donor-ready narrative
4. Save export in: data/exports/
5. Return download link to frontend

## Excel / CSV Columns
- Goal
- Outcome
- Output
- Activity
- Responsibility
- Monitoring
- Indicator
- Means of Verification
- Assumption

## Text Narrative
- Generate professional donor-ready program description
- Include all fields in readable format
# Logic Auditor Design

1. Receives LFA JSON from mapping step.
2. Checks for:
   - Missing responsibility
   - Weak or missing monitoring
   - Unclear indicators
   - Missing means of verification
   - Empty assumptions
3. Generates AI follow-up questions for missing/weak fields.
4. Sends questions to frontend chat interface.
5. User responses update LFA JSON → saved as new version.
6. Workflow ensures completeness before export.
# Backend Export Workflow

1. User clicks "Download" in frontend.
2. Backend retrieves LFA JSON from data/lfa-json/ (specific project/version).
3. Backend converts JSON to requested format:
   - Excel → formatted LFA table
   - CSV → spreadsheet-ready columns
   - Text → donor-ready narrative
4. Save export in data/exports/ with timestamp/version.
5. Return download link to frontend.
# Frontend Live Table & Export Planning

1. Display structured LFA JSON from backend in a table.
2. Table is editable:
   - Add/remove rows
   - Inline edits for text
   - Updates sync to backend (versioning)
3. Exports:
   - Buttons for Excel, CSV, Text
   - Frontend sends request with project/version and format
   - Backend generates file and returns download link
4. Live updates can trigger logic auditor re-check if needed.
# Voice Input Integration

1. User clicks "Record" to start speaking.
2. Browser captures audio in chunks.
3. Audio sent to backend via POST or WebSocket.
4. Backend uses Whisper API to transcribe → stores transcript.
5. Transcript sent to GPT-4o → structured LFA JSON.
6. JSON returned to frontend → live LFA table updated.
7. User edits table and answers AI follow-ups.
8. Updates sent back to backend → versioned storage.
