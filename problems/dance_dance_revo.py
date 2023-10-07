###############################################################################
#### DO NOT EDIT THIS SECTION
###############################################################################
from typing import Dict, Any, List, Tuple, Optional
from shared_utils import set_weighted_score_data
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.student_submission import StudentSubmission
from shared_utils import grade_question_parameterized

def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = PROBLEM_CONFIG.to_json_string()

def grade(data: Dict[str, Any]) -> None:
    grade_question_parameterized(data, "subproblem_definition", grade_statement)
    set_weighted_score_data(data)

###############################################################################
#### DO NOT EDIT ABOVE HERE, ONLY EDIT BELOW
###############################################################################

statement = 'Assume you are at a middle school dance.' + ' You lock eyes with your crush across the room. What dance move will you make to impress them?'

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "You decide to" MOVE
    MOVE ->  MOVEMENT DIRECTION
    MOVEMENT -> "slide" | "jump" | "run" | "hokey pokey" | "criss cross" | EPSILON
    DIRECTION -> "up" | "down" | "left" | "right" | "away" | EPSILON
    EPSILON ->
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("MOVEMENT", "hokey pokey"):
        return False, 'If you do the hokey pokey and you turn yourself around' + \
            ' your crush will turn themselves around and go the other way.'

    if submission.does_path_exist("MOVEMENT", "jump"):
        return False, 'Unfortunately, you do not have rhythm. Jumping off beat ' + \
            ' is not the best move.'

    if submission.does_path_exist("DIRECTION", "up") and \
        submission.does_path_exist("DIRECTION", "down"):
        return False, 'Your crush is not looking you up and down with this movement'

    if submission.does_path_exist("MOVEMENT", "run") and \
        submission.does_path_exist("DIRECTION", "away"):
        return True, 'Yes, run from your crush and the dance!'

    return True, None


