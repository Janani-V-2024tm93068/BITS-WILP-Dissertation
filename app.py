from flask import Flask, jsonify
from jira_metrics import compute_metrics
from scoring import calculate_readiness

app = Flask(__name__)

@app.route("/readiness", methods=["GET"])
def readiness():
    df = compute_metrics()
    result_df = calculate_readiness(df)
    return jsonify(result_df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)