from typing import List, Tuple

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.run.workflow import WorkflowRunOutput
from dotenv import load_dotenv
from agno.workflow import Workflow, WorkflowExecutionInput, Step, StepOutput, Loop, StepInput

from agents.log import LogLine, LogRecord, Entity
from pathlib import Path
import json

load_dotenv()

RETURN_COUNT = 1000


labels_agent = Agent(
    model=OpenAIResponses(id="gpt-5.2", temperature=0.9),
    instructions="""
    You are a synthetic label generator with an expert knowledge of NLP Token Classification.
    Your task is to generate NER labels for a given log line.
    Each line is may be made up of 0 or more entities.
    There is a 1 in 3 chance that a LogLine has an entity.
    An entity is a single word or phrase that has been identified as belonging to a particular label.
    It is very unlikely that more than 2 labels will exist for the line, and for the vast majority of labels, there will only be one.
    Note, there are many different ways to display phone numbers, national insurance numbers, postcodes etc.
    Make sure to use lots of different representations of these entities in your output.
    If using a national insurance number don't use a space and the NINO cannot be QQ123456C or AB123456D.
    Choose labels with equal weight to each one.
    Text string can in 3/8 cases be unclean
    """,
    markdown=True,
    output_schema=LogLine
)

log_agent = Agent(
    model=OpenAIResponses(id="gpt-5.2", temperature=0.9),
    instructions="""
    You are a synthetic log generator with expert knowledge of NLP Token Classification and on PII in logs.
    Your task is to map the LogLine entities into the LogRecord log line.
    Each LogLine is made up of 0 or more entities.
    If there are one or more entities, each of those entities text items should appear character for character somewhere in the log line in a natural way.
    It will usually be in the message, but can sometimes (1/10 times) be in the endpoint.
    The labels in the LogLine are various forms of personally identifiable information (PII).
    The label in it's raw uppercase form will never be in the log line and it will more often than not be omitted from the log line.
    The log line may only contain the labelled entities if they are present in the input, otherwise it must be free from any PII.
    If labels exist, they must be included in the log line, but not duplicated.
    The entity text will never be duplicated in the log line, unless the entity is duplicated in the input.
    label=text type messages should not be created.
    """,
    input_schema=LogLine,
    output_schema=LogRecord,
    markdown=True
)

labels_step = Step(agent=labels_agent, name="Label generator", description="Generate labels for a log line.")
log_step = Step(agent=log_agent, name="Log generator", description="Generate a log line from the labels.")

labels_list = []
logs_list = []

labels_path = Path("../data/labels.jsonl")
logs_path = Path("../data/logs.jsonl")

def aggregate_loop_run(step_input: StepInput) -> StepOutput:
    labels = step_input.get_step_content("Label generator")
    logs = step_input.get_step_content("Log generator")
    labels_list.append(labels)
    logs_list.append(logs)

    with labels_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(map_log_line_to_entity(labels)) + "\n")


    with logs_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(map_log_records_to_labels(logs)) + "\n")

    return StepOutput(
        step_name="aggregator",
        content=None,
        success=True
    )

aggregate_loop_run_step = Step(executor=aggregate_loop_run, name="Aggregator", description="Aggregate loop outputs.")

def aggregate_loop_results(step_input: StepInput) -> StepOutput:
    # Access specific step outputs from the loop by name
    # loop_step_content = step_input.get_step_content("Log generation loop")
    print("labels list", len(labels_list), "logs list", len(logs_list))
    return StepOutput(
        step_name="aggregator",
        content=(labels_list, logs_list),
        success=True
    )

aggregate_loop_results_step = Step(executor=aggregate_loop_results, name="Aggregator", description="Aggregate loop outputs.")

# End condition function
def log_evaluator(outputs: List[StepOutput]) -> bool:
    """
    Evaluate if research results are sufficient
    Returns True to break the loop, False to continue
    """
    # Check if any outputs are present
    if not outputs:
        return False

    output_length = len(labels_list)
    if output_length >= RETURN_COUNT:
        print(f"Log generation complete - generated {len(outputs)} logs")
        return True

    print(f"Generated {output_length} of {RETURN_COUNT} logs - continuing to generate more logs...")
    return False

workflow = Workflow(
    name="Log generation workflow",
    description="Generate synthetic logs with PII until conditions are met, then return content",
    steps=[
        Loop(
            name="Log generation loop",
            steps=[labels_step, log_step, aggregate_loop_run_step],
            end_condition=log_evaluator,
            max_iterations=RETURN_COUNT,  # Maximum 3 iterations
        ),
        aggregate_loop_results_step
    ],
)


def map_log_line_to_entity(log_line: LogLine) -> List[List[Tuple[str, str]]]:
    return [entity.model_dump(mode="json") for entity in log_line.entities]

def map_log_records_to_labels(log_record: LogRecord) -> dict:
    return log_record.model_dump(mode="json")

if __name__ == "__main__":
    response: WorkflowRunOutput = workflow.run(
        input="Generate logs and labels",
        markdown=True,
    )
    # result = workflow.print_response("Generate logs and labels", stream=True)
    log_line_labels, log_records = response.content
    print(f"{len(log_line_labels)} log lines, {len(log_records)} log records")

    labels = [map_log_line_to_entity(log_line) for log_line in log_line_labels]
    with open("../data/labels.jsonl", "w", encoding="utf-8") as f:
        for label in labels:
            f.write(json.dumps(label) + "\n")

    logs = [map_log_records_to_labels(log_record) for log_record in log_records]
    with open("../data/logs.jsonl", "w", encoding="utf-8") as f:
        for log in logs:
            f.write(json.dumps(log) + "\n")

    print(labels)
    print(logs)