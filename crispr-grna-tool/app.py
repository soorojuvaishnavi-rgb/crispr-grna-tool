from flask import Flask, render_template, request

app = Flask(__name__)


def find_grnas(sequence):
    sequence = sequence.upper().replace(" ", "").replace("\n", "")
    results = []

    for i in range(len(sequence) - 22):
        guide = sequence[i:i + 20]
        pam_seq = sequence[i + 20:i + 23]

        if pam_seq[1:] == "GG":
            results.append({
                "position": i + 1,
                "guide": guide,
                "pam": pam_seq
            })

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    sequence = ""

    if request.method == "POST":
        sequence = request.form.get("sequence", "")
        results = find_grnas(sequence)

    return render_template(
        "index.html",
        results=results,
        sequence=sequence
    )


if __name__ == "__main__":
    app.run(debug=True)