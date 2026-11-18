from flask import Flask, render_template, request
from scanner import scan_ports
import time
import csv
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    target = ""
    scan_time = 0

    if request.method == "POST":
        target = request.form["target"]

        start = time.time()
        results = scan_ports(target)
        end = time.time()

        scan_time = round(end - start, 2)

        # Create reports folder if it doesn't exist
        os.makedirs("reports", exist_ok=True)

        # Save scan results to CSV
        csv_file = os.path.join("reports", "scan_results.csv")

        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Host",
                "Port",
                "Service",
                "Product",
                "Version",
                "Status"
            ])

            for row in results:
                if "error" not in row:
                    writer.writerow([
                        row.get("host", ""),
                        row.get("port", ""),
                        row.get("service", ""),
                        row.get("product", ""),
                        row.get("version", ""),
                        row.get("status", "")
                    ])

    return render_template(
        "index.html",
        results=results,
        target=target,
        scan_time=scan_time
    )

if __name__ == "__main__":
    app.run(debug=True)
    