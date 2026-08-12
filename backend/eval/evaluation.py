from langsmith import Client
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, CONCISENESS_PROMPT, HALLUCINATION_PROMPT, RAG_GROUNDEDNESS_PROMPT, RAG_HELPFULNESS_PROMPT, RAG_RETRIEVAL_RELEVANCE_PROMPT
from services.initialize import azure_eval_endpoint, azure_api_key, qa_service
from langchain_litellm import ChatLiteLLM

# Define the input and reference output pairs that you'll use to evaluate your app
client = Client()

eval_llm = ChatLiteLLM(
    model="azure/gpt-4.1",
    temperature=0,
    api_base=azure_eval_endpoint,
    api_key=azure_api_key
)

# Check if dataset already exists
existing_datasets = client.list_datasets()
# dataset_name = "small_eval_dataset"
dataset_name = "eval_dataset"

for ds in existing_datasets:
    if ds.name == dataset_name:
        dataset = ds
        break
else:
    dataset = client.create_dataset(
        dataset_name=dataset_name, description="A  dataset with simple questions."
    )

    # Export examples for use in API - only add when creating new dataset
    examples = [
        {
            "inputs": {"question": "What are the selectable output current limits?"},
            "outputs": {"answer": "The selectable output current limits are 0%, 33%, 67%, or 100% of the maximum output current."},
        },
        {
            "inputs": {"question": "Which stepping operations are possible with the PWM?"},
            "outputs": {"answer": "Full, half, and micro-stepping operations are possible with the PWM current control and logic inputs."},
        },
        {
            "inputs": {"question": "Is a special power-up sequencing required?"},
            "outputs": {"answer": "No special power-up sequencing is required."},
        },
        {
            "inputs": {"question": "What does a high and what does a low logic signal level cause?"},
            "outputs": {"answer": "A HIGH logic signal level causes load current to flow from OUTxA to OUTxB. A LOW logic level causes load current to flow from OUTxB to OUTxA."},
        },
        {
            "inputs": {"question": "What does a thermal protection circuitry do?"},
            "outputs": {"answer": "A thermal protection circuitry turns off all drivers when the junction temperature exceeds a safe operating limit of +170°C (typical)."},
        },
        {
            "inputs": {"question": "When are the power bridge and all outputs are disabled?"},
            "outputs": {"answer": "The power bridge and all outputs are disabled if VLOGIC is smaller than 4V."},
        },
        {
            "inputs": {"question": "What do the typical PCB layout guidelines include?"},
            "outputs": {"answer": "Separate power ground planes, supply decoupling capacitors close to the IC, short connections and use of maximized copper areas to improve thermal dissipation."},
        },
        {
            "inputs": {"question": "What is the MTS2916A DUAL FULL-BRIDGE STEPPER MOTOR DRIVER?"},
            "outputs": {"answer": "The MTS2916A Dual Full-Bridge Stepper Motor Driver Evaluation Board control circuitry is designed to typically operate from a 6V to 12V logic input (internally regulated down to 5V) and a 10V to 30V VLOAD input. VLOAD provides power to the motor windings. Test points are generously distributed throughout the evaluation board. This gives the user easy access and visibility, facilitating a better understanding of the MTS2916A operating details."},
        },
        {
            "inputs": {"question": "Which Power Connections does the MTS2916A use?"},
            "outputs": {"answer": "The MTS2916A Dual Full-Bridge Stepper Motor Driver Evaluation Board uses a combination of terminal blocks, test clips and one DC power jack for power connections. Connections are as follows: a) Motor Output Connections: - J2-1(A3), J2-2(A1), J2-3(B1), J2-4(B3), J2-5(TP21) - TP11(A1), TP12(A3), TP13(B1), TP14(B3). b) VLOAD (Motor Supply Power): - J4-1(PGND), J4-2(VLOAD) - TP20(PGND), TP18(VLOAD). WARNING: Do not connect more than 16V to these motor supply connections while Jumper JP2 is installed. c) VLOGIC: - J1-1(VLOGIC), J1-2(AGND) - TP2(VLOGIC), TP5(AGND)"},
        },
        {
            "inputs": {"question": "What are the steps to power the MTS2916A Dual Full-Bridge Stepper Motor Driver Evaluation Board?"},
            "outputs": {"answer": "Follow these steps to power-up the board: 1. With the supply turned OFF, connect the power to the logic portion of the evaluation board at J1 with the specified voltage (7 VDC to 12 VDC). The logic portion of the evaluation board will typically draw less than 50 mA. 2. If the user’s stepper motor requires a voltage that is compatible with the logic supply voltage and the user’s source can handle driving the stepper motor windings, install JP2. DO NOT connect power at J4. If powering up the stepper from an additional supply, DO NOT install JP2 and connect the stepper motor supply to J4. J1 power will still be required for the logic supply. 3. 4. Connect the bipolar stepper windings to J2 per the schematic diagram. Turn ON the power supplies. Power sequencing is not required due to the under- voltage lockout circuitry. 5. Toggle the Mode switch to cycle through the five modes, as indicated by the binary LED count. 6. Press the Run switch once to tell the PIC16F883 to send drive information to the MTS2916A with minimal (1V) VREF . Subsequent Run presses increase VREF by approximately 1V up to 5V maximum. This increases the current regulation threshold. 7. The Hold switch tells the PIC16F883 to command the MTS2916A to hold the motor position. 8. The Direction switch tells the PIC16F883 to command the MTS2916A to change the direction of the motor. 9. The Speed Adjust Potentiometer (R4) varies an analog voltage that is read by the PIC16F883 Analog-to-Digital Converter, and varies the speed accordingly."},
        },
    ]

    # Add the examples to the dataset only when creating new dataset
    client.create_examples(dataset_id=dataset.id, examples=examples)


def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate correctness of the output."""

    evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="correctness",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )
    return eval_result


def conciseness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate relevance of the output."""
    evaluator = create_llm_as_judge(
        prompt=CONCISENESS_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="conciseness",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )
    return eval_result


def hallucination_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate relevance of the output."""
    # Extract context from outputs - simple format
    context_text = ""
    if "context" in outputs and isinstance(outputs["context"], dict) and "texts" in outputs["context"]:
        context_text = "\n".join(outputs["context"]["texts"])

    evaluator = create_llm_as_judge(
        prompt=HALLUCINATION_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="hallucination",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs["answer"],
        context=context_text,
        reference_outputs=reference_outputs
    )
    return eval_result


def groundedness_evaluator(outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate relevance of the output."""
    # Extract context from outputs - simple format
    context_text = ""
    if "context" in outputs and isinstance(outputs["context"], dict) and "texts" in outputs["context"]:
        context_text = "\n".join(outputs["context"]["texts"])

    evaluator = create_llm_as_judge(
        prompt=RAG_GROUNDEDNESS_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="groundedness",
    )
    eval_result = evaluator(
        outputs=outputs["answer"],
        context=context_text,
        reference_outputs=reference_outputs
    )
    return eval_result


def relevance_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate relevance of the output."""
    # Extract context from outputs - simple format
    context_text = ""
    if "context" in outputs and isinstance(outputs["context"], dict) and "texts" in outputs["context"]:
        context_text = "\n".join(outputs["context"]["texts"])

    evaluator = create_llm_as_judge(
        prompt=RAG_RETRIEVAL_RELEVANCE_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="relevance",
    )
    eval_result = evaluator(
        inputs=inputs,
        context=context_text,
        reference_outputs=reference_outputs
    )
    return eval_result


def helpfulness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    """Define an LLM as a judge evaluator to evaluate relevance of the output."""
    evaluator = create_llm_as_judge(
        prompt=RAG_HELPFULNESS_PROMPT,
        judge=eval_llm,
        model="gpt-4.1",
        feedback_key="helpfulness",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )
    return eval_result


async def target(inputs: dict) -> dict:
    question = inputs["question"]
    try:
        answer = await qa_service.answer_question(question=question)

    except Exception as e:
        print(f"Error during question answering: {e}")
        pass

    # Extract just the text content for evaluation (no metadata needed)
    context_texts = []
    if "context" in answer and isinstance(answer["context"], dict) and "texts" in answer["context"]:
        for text_item in answer["context"]["texts"]:
            if isinstance(text_item, dict) and "content" in text_item:
                context_texts.append(text_item["content"])
            elif isinstance(text_item, str):
                context_texts.append(text_item)

    return {
        "answer": answer["answer"],
        "context": {
            "texts": context_texts
        }
    }
