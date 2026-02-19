## Report Generation

import json
import csv

from jinja2 import Template

def generate_report(data, format="json", output="report"):
    if format == "json":
        with open(f"{output}.json", "w") as f:
            json.dump(data, f, indent=4)
    elif format == "csv":
        # Flatten data for CSV
        with open(f"{output}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Details"])
            for key, val in data.items():
                writer.writerow([key, str(val)])
    elif format == "html":
        template = Template("""
        <html><body>
        <h1>Browser Tracker Report</h1>
        <pre>{{ data | tojson(indent=2) }}</pre>
        </body></html>
        """)
        with open(f"{output}.html", "w") as f:
            f.write(template.render(data=data))

