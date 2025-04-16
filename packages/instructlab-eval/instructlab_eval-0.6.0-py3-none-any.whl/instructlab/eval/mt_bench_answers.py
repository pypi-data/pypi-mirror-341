# SPDX-License-Identifier: Apache-2.0
# Standard
import concurrent.futures
import json
import os
import time

# Third Party
import shortuuid
import tqdm

# Local
from .logger_config import setup_logger
from .mt_bench_common import (
    bench_dir,
    chat_completion_openai,
    get_openai_client,
    load_questions,
    temperature_config,
)
from .mt_bench_model_adapter import get_conversation_template  # type: ignore

logger = setup_logger(__name__)


def reorg_answer_file(answer_file):
    """Sort by question id and de-duplication"""
    logger.debug(locals())
    with open(answer_file, "r+", encoding="utf-8") as f:
        answers = {}
        for l in f:
            qid = json.loads(l)["question_id"]
            answers[qid] = l

        # Reset to the beginning of the file and clear it
        f.seek(0)
        f.truncate()

        qids = sorted(list(answers.keys()))
        for qid in qids:
            f.write(answers[qid])


def get_answer(
    question: dict,
    model: str,
    num_choices: int,
    max_tokens: int,
    answer_file: str,
    force_temperature: float,
    openai_client,
):
    """Answer a question with the model"""
    assert force_temperature is None or question.get("required_temperature") is None
    if force_temperature is not None:
        temperature = force_temperature
    elif "required_temperature" in question.keys():
        temperature = question["required_temperature"]
    elif question["category"] in temperature_config:
        temperature = temperature_config[question["category"]]
    else:
        temperature = 0.7

    choices = []
    for i in range(num_choices):
        conv = get_conversation_template(model, "granite")

        turns = []
        for j in range(len(question["turns"])):
            conv.append_message(conv.roles[0], question["turns"][j])
            conv.append_message(conv.roles[1], None)

            output = chat_completion_openai(
                openai_client,
                model,
                conv,
                temperature,
                max_tokens,
            )

            conv.update_last_message(output)
            turns.append(output)

        choices.append({"index": i, "turns": turns})

    # Dump answers
    ans = {
        "question_id": question["question_id"],
        "answer_id": shortuuid.uuid(),
        "model_id": model,
        "choices": choices,
        "tstamp": time.time(),
    }

    os.makedirs(os.path.dirname(answer_file), exist_ok=True)
    with open(answer_file, "a", encoding="utf-8") as fout:
        fout.write(json.dumps(ans) + "\n")


def generate_answers(
    model_name,
    model_api_base,
    api_key=None,
    branch=None,
    output_dir="eval_output",
    data_dir=None,
    question_begin=None,
    question_end=None,
    force_temperature=None,
    num_choices=1,
    max_tokens=1024,
    max_workers=1,
    bench_name="mt_bench",
    http_client=None,
):
    """Generate model answers to be judged"""
    logger.debug(locals())

    openai_client = get_openai_client(model_api_base, api_key, http_client)

    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")

    data_base_dir = bench_dir(data_dir, bench_name, branch)
    output_base_dir = bench_dir(output_dir, bench_name, branch)

    question_file = os.path.join(data_base_dir, "question.jsonl")
    questions = load_questions(question_file, question_begin, question_end)

    answer_file = os.path.join(output_base_dir, "model_answer", f"{model_name}.jsonl")
    if os.path.isfile(answer_file):
        os.remove(answer_file)
        logger.debug("Removing previous answer file: %s", answer_file)

    first_n = None
    first_n_env = os.environ.get("INSTRUCTLAB_EVAL_FIRST_N_QUESTIONS")
    if first_n_env:
        first_n = int(first_n_env)
        logger.debug("INSTRUCTLAB_EVAL_FIRST_N_QUESTIONS=%s", first_n)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, question in enumerate(questions):
            if first_n is not None and i >= first_n:
                break

            future = executor.submit(
                get_answer,
                question,
                model_name,
                num_choices,
                max_tokens,
                answer_file,
                force_temperature,
                openai_client,
            )
            futures.append(future)

        for future in tqdm.tqdm(
            concurrent.futures.as_completed(futures), total=len(futures)
        ):
            future.result()

    reorg_answer_file(answer_file)
