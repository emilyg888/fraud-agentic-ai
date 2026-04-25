# Air-lab Fraud Agentic AI User Test Cases

Use these five test cases for analyst-style user testing of the current dashboard build.

## Test Case 1: High-Risk Investigation Happy Path

**Objective**  
Verify that a user can investigate a strong fraud case end to end.

**Case**  
`A-1001`

**Steps**

1. Open the dashboard.
2. Select `A-1001` from the case queue.
3. Review the case overview and threshold information.
4. Click `Run Investigation`.
5. Review evidence, governance, and candidate signal output.

**Expected Result**

- The user can understand why the alert is risky.
- Evidence and retrieved typologies are visible.
- A candidate signal is generated.
- The workflow pauses for human review when required.

## Test Case 2: Human Approval Flow

**Objective**  
Verify that a reviewer can approve a pending candidate signal from the dashboard.

**Case**  
Use the pending run generated from `A-1001`.

**Steps**

1. Open `Signal Review`.
2. Confirm the run is marked `pending_human_review`.
3. Select the signal.
4. Enter reviewer name `fraud_analyst_demo`.
5. Click `Approve Signal`.

**Expected Result**

- The approval is recorded successfully.
- The run status changes from pending to approved.
- The decision appears in the audit trail.
- The final report reflects the approval outcome.

## Test Case 3: Threshold Interpretation And Analyst Skepticism

**Objective**  
Verify that the dashboard does not overstate a below-threshold alert.

**Case**  
`A-1002`

**Steps**

1. Select `A-1002`.
2. Review the case overview before running the investigation.
3. Confirm the threshold summary wording.
4. Run the investigation and inspect the evidence summary.

**Expected Result**

- The UI shows that score `0.67` did not exceed threshold `0.70`.
- The evidence summary does not incorrectly say the threshold was exceeded.
- The user can still inspect retrieved typologies and supporting evidence.

## Test Case 4: Governance-Sensitive Rejection Path

**Objective**  
Verify that a reviewer can identify governance concerns and reject a candidate signal.

**Case**  
`A-1003`

**Steps**

1. Select `A-1003`.
2. Run the investigation.
3. Review evidence, governance findings, and restricted/stale feature context.
4. Open `Signal Review`.
5. Reject the candidate signal.

**Expected Result**

- The user can identify the governance issue from the dashboard.
- The signal is rejected rather than promoted.
- The rejection is written to the audit log and reflected in the report.

## Test Case 5: Report, Trace, And Monitoring Validation

**Objective**  
Verify that the app produces downloadable artifacts and post-approval monitoring output.

**Case**  
Any approved `A-1001` run.

**Steps**

1. Open `Report & Export`.
2. Confirm the markdown report is visible.
3. Download the report and run trace.
4. Open `Signal Layer Monitor`.
5. Review approved-signal monitoring fields.

**Expected Result**

- The report is non-empty and readable.
- The JSON run trace is available.
- The monitor tab shows coverage, fraud lift, drift, decay score, and next review recommendation.
- The monitor tab clearly labels these metrics as sample-data proxy outputs.
