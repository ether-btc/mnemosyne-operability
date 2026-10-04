# Stage 2/3 Codebook — Avoidable Reminder Labeling

## Stage 2: Agent Action

### agent_action
- **used_correctly**: Assistant used the right tool/capability for the task
- **not_selected**: Assistant did not use any tool/capability (answered directly or asked for clarification)
- **selected_wrong**: Assistant used the wrong tool/capability for the task

### correct_use
- **true**: The tool/capability was used correctly (proper parameters, correct sequence)
- **false**: The tool/capability was used incorrectly (wrong parameters, wrong sequence, or failed)

### task_outcome
- **correct**: The task was completed successfully
- **incomplete**: The task was not completed (partial, failed, or abandoned)
- **unknown**: Cannot determine from the response

## Stage 3: Reminder Outcome

### avoidable_reminder
- **true**: The user had to remind the assistant about something it should have known or done (capability, context, correction)
- **false**: No avoidable reminder was needed

### reminder_type
- **capability**: User reminded assistant about a tool/skill/capability it should have used
- **context**: User reminded assistant about context it should have remembered
- **correction**: User corrected a mistake the assistant made
- **none**: No reminder needed

## Operationalization

An "avoidable reminder" is when the user has to tell the assistant something it should have known or done without being told. This includes:
- Reminding the assistant to use a specific tool/skill
- Reminding the assistant about context from earlier in the conversation
- Correcting a mistake the assistant made that it should have avoided

A reminder is NOT avoidable if:
- The user provides new information that was not previously available
- The user asks for clarification on something ambiguous
- The user changes their mind about what they want

## Labeling Procedure

1. Read the user message (task start)
2. Read the assistant response
3. Label Stage 2 fields (agent_action, correct_use, task_outcome)
4. Label Stage 3 fields (avoidable_reminder, reminder_type)
5. If avoidable_reminder is true, provide a brief explanation

## Intra-rater Agreement

After ≥48h, re-rate a random 20% sample of the labeled items. Report Cohen's kappa or simple agreement percentage.
