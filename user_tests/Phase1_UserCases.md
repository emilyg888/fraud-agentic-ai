Setup
Start the app:

cd /Users/emilygao/LocalDocuments/Projects/fraud-agentic-ai
source .venv/bin/activate
streamlit run streamlit_app/fraud_case_dashboard.py
Moderator Script
Tell the tester:

“Imagine you are a fraud analyst reviewing ML-flagged cases. Please use the dashboard to investigate a case, review the evidence, and decide whether a candidate signal should be promoted. Think out loud as you go.”

Task 1
Ask them to select A-1001 and explain, in their own words, why the case looks risky
alerts
.csv
(line 2)
.

Success signal:
They can find model score, threshold, triggered features, and start the run without help.

Task 2
Ask them to click Run Investigation and describe what the system is doing as they move through the tabs
fraud_case_dashboard
.py
(lines 34-122)
.

Watch for:
Whether the workflow/audit view makes sense.
Whether they understand the difference between evidence, governance, and signal review.

Task 3
Ask them to open Evidence Explorer and answer:
“What evidence supports account takeover?”
“What evidence weakens the fraud hypothesis?”

Success signal:
They use retrieved typologies plus transaction/behaviour summaries, not just the alert score.

Task 4
Ask them to use Case Copilot with:
“Why was this case flagged?”
“Are there data quality or lineage concerns?”
“What should the analyst do next?”
service
.py
(lines 37-63)

Watch for:
Whether they trust the answers.
Whether evidence references and limitations are clear enough.

Task 5
Ask them to open Signal Review and decide whether to approve or reject the candidate signal.
Then ask why they made that choice.

Success signal:
They notice this is a human decision boundary, not an automated fraud decision
workflow
.py
(lines 98-147)
.

Task 6
Ask them to check Governance & Audit and Report & Export and confirm they can see the decision trail and final report.

Success signal:
They can explain what happened without needing the CLI.

Follow-up Questions
Ask these after the tasks:

What part of the workflow felt most clear?
What part felt confusing or too technical?
Did you trust the evidence shown? Why or why not?
Did the approval step feel appropriately controlled?
What was missing that you would expect in an analyst tool?
If you used this again, what would you want on the first screen?
What To Capture
Record:

Time to complete each task
Places where they hesitate
Tabs they ignore
Terms they misunderstand
Whether they understand the dashboard is calling a governed workflow, not making direct decisions
Whether they can explain the candidate signal and governance status
If you want, I can also turn this into a one-page user test checklist you can paste into Notion or Google Docs.

19:20
yes go ahead
19:20

User Test Checklist

Session Info

Tester name:
Date:
Role/background:
Moderator:
Duration:
Build used:
Setup

Open dashboard
Select case A-1001
Confirm tester understands the scenario: fraud analyst reviewing an ML-flagged case
Task 1: Find The Case Context

Can the tester find:
case ID
model score
threshold
triggered features
Notes:
Completed without help: Yes / No
Task 2: Run The Investigation

Tester clicks Run Investigation
Can they explain what the system is doing?
Do they understand the workflow status?
Notes:
Completed without help: Yes / No
Task 3: Review Evidence

Tester opens Evidence Explorer
Can they answer:
What evidence supports fraud risk?
What evidence weakens the fraud hypothesis?
Notes:
Completed without help: Yes / No
Task 4: Use The Copilot
Ask tester to enter:

Why was this case flagged?
Are there data quality or lineage concerns?
What should the analyst do next?
Capture:

Did the answer feel useful?
Did the answer feel trustworthy?
Did they notice evidence references and limitations?
Notes:
Task 5: Review Candidate Signal

Tester opens Signal Review
Can they explain:
what the candidate signal means
whether it should be approved or rejected
why
Decision made: Approve / Reject
Notes:
Completed without help: Yes / No
Task 6: Check Governance And Audit

Tester opens Governance & Audit
Can they explain what controls were applied?
Can they find the human decision in the audit trail?
Notes:
Completed without help: Yes / No
Task 7: Review Report

Tester opens Report & Export
Can they understand the final report?
Can they find the recommendation quickly?
Notes:
Completed without help: Yes / No
Post-Test Questions

What part felt most clear?
What part felt confusing?
What information felt missing?
Did the approval step feel appropriately controlled?
Would you trust this as an analyst support tool? Why or why not?
What should be improved first?
Metrics To Capture

Time to complete each task
Number of moderator prompts needed
Tabs skipped
Confusing labels or terms
Trust concerns
Suggestions repeated by multiple testers
Severity Scale

P1: blocked task
P2: major confusion or low trust
P3: minor friction
P4: cosmetic issue
If you want, I can format this next as:

a Notion-friendly template
a Google Docs interview sheet
a CSV table for tracking multiple testers
