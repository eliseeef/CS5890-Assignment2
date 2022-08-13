from flask import Flask, request, render_template, redirect
import importlib

app = Flask(__name__)

@app.route("/")
def redirect_to_problem():
    return render_template("dp_intro.html")

@app.route("/<problem_name>/problem")
def display_problem(problem_name: str) -> str:
    problem = importlib.import_module("problems." + problem_name)

    data = {"params": {}}
    problem.generate(data)

    return render_template(
        'problem.html',
        statement=problem.statement,
        cfg=data["params"]["subproblem_definition_cfg"]
    )

@app.route("/<problem_name>/submit", methods=["POST"])
def handle_submit(problem_name: str) -> str:
    problem = importlib.import_module("problems." + problem_name)

    tokenized_sentence = request.get_json()
    data = {
        "submitted_answers": {"subproblem_definition": tokenized_sentence},
        "partial_scores": {},
        "feedback": {},
    }

    problem.grade(data)

    return data["feedback"].get("subproblem_definition", "Good job!")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
