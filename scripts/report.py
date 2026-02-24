

from pathlib import Path
from datetime import datetime
import json
import csv
from jinja2 import Template

# Default data folder (relative to repo root, works even if script moves)
DEFAULT_DATA_FOLDER = Path(__file__).parent.parent / "data"

def generate_report(
    data,
    format="json",
    output="report",
    data_folder=None
):
    """
    Generate a report in JSON, CSV, or HTML format.
    Saves to the specified data_folder (defaults to repo's data/).
    """
    # Use provided folder or fall back to default
    data_folder = data_folder or DEFAULT_DATA_FOLDER
    
    # Ensure the folder exists
    data_folder.mkdir(exist_ok=True, parents=True)
    
    # Full output path
    output_path = data_folder / f"{output}.{format}"
    
    print(f"Saving {format.upper()} report to: {output_path}")
    
    # Optional: Add metadata to every report
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "format": format,
        "output_name": output,
        "data_keys": list(data.keys())
    }
    full_data = {"metadata": metadata, "report": data}
    
    try:
        if format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(full_data, f, indent=4, ensure_ascii=False)
        
        elif format == "csv":
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Category", "SubCategory", "Value"])
                for key, val in data.items():
                    if isinstance(val, dict):
                        for sub_key, sub_val in val.items():
                            writer.writerow([key, sub_key, sub_val])
                    elif isinstance(val, list):
                        writer.writerow([key, "", ", ".join(map(str, val))])
                    else:
                        writer.writerow([key, "", str(val)])
        
        elif format == "html":
            template = Template("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Browser Tracker Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
                    h1 { color: #2c3e50; }
                    pre { background: #ecf0f1; padding: 20px; border-radius: 8px; white-space: pre-wrap; }
                    table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                    th { background: #3498db; color: white; }
                    tr:nth-child(even) { background: #f2f2f2; }
                </style>
            </head>
            <body>
                <h1>Browser Tracker Report</h1>
                <p>Generated: {{ metadata.generated_at }}</p>
                
                <h2>Summary</h2>
                <table>
                    {% for key, val in report.items() %}
                        {% if not val is mapping and not val is sequence %}
                            <tr><th>{{ key }}</th><td>{{ val }}</td></tr>
                        {% endif %}
                    {% endfor %}
                </table>
                
                <h2>Full Data</h2>
                <pre>{{ report | tojson(indent=2) }}</pre>
            </body>
            </html>
            """)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(template.render(metadata=metadata, report=data))
        
        else:
            print(f"Unsupported format: {format}. Use 'json', 'csv', or 'html'.")
            return
        
        print(f"{format.upper()} report saved successfully to: {output_path}")
    
    except Exception as e:
        print(f"Error saving {format} report: {e}")
