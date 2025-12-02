import os
import math
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for

# =========================================================
# BASIC FLASK SETUP
# =========================================================
app = Flask(__name__)
app.secret_key = "change_this_to_any_random_string"

# =========================================================
# PATHS – POINTING TO YOUR DESKTOP FILES
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FORMULA_PATH = os.path.join(BASE_DIR, "static", "data", "County-level formula_cleaned.xlsx")
CHARTS_DIR = os.path.join(BASE_DIR, "static", "charts")
MAPS_DIR = os.path.join(BASE_DIR, "static", "maps")

# =========================================================
# LOAD FORMULA TABLE (ONCE AT STARTUP)
# =========================================================
if not os.path.exists(FORMULA_PATH):
    raise FileNotFoundError(f"Cannot find Excel file: {FORMULA_PATH}")

df_formulas = pd.read_excel(FORMULA_PATH)

# Create a cleaned lowercase county column for matching
df_formulas["County_clean"] = (
    df_formulas["County"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# =========================================================
# SAFE FORMULA EVALUATOR
# =========================================================
def evaluate_formula(formula_str, x_value):
    """
    Takes a formula like 'y = 0.0148*x^3 + 2*x^2 + 3'
    and returns y for a given x_value.

    Supports:
      - ^ (Excel) → ** (Python)
      - exp(), log(), sqrt()
    """
    if not isinstance(formula_str, str):
        return None

    # Only keep part after "y ="
    parts = formula_str.split("=")
    if len(parts) < 2:
        return None

    expr = parts[1].strip()  # expression after '='
    expr = expr.replace("^", "**")  # Excel to Python power operator

    allowed_names = {
        "x": x_value,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt
    }

    try:
        return float(eval(expr, {"__builtins__": {}}, allowed_names))
    except Exception:
        return None


# =========================================================
# HELPER – FIND PNG BY COUNTY
# =========================================================
def find_image_for_county(directory, county_name):
    """
    Look in directory for a PNG containing the county name.
    """
    if not os.path.isdir(directory):
        return None

    target = county_name.replace(" ", "_").lower()
    for fname in os.listdir(directory):
        if fname.lower().endswith(".png") and target in fname.lower():
            return fname
    return None


# =========================================================
# SERVE CHART & MAP IMAGES
# =========================================================
@app.route("/chart/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHARTS_DIR, filename)


@app.route("/map/<path:filename>")
def serve_map(filename):
    return send_from_directory(MAPS_DIR, filename)


# =========================================================
# MAIN PAGE
# =========================================================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    chart_filename = None
    map_filename = None
    county_display = None
    ev_formula = None
    adopt_formula = None

    if request.method == "POST":
        county_input = request.form.get("county", "").strip()
        x_input = request.form.get("superchargers", "").strip()

        if not county_input:
            flash("Please enter a county name.")
            return redirect(url_for("index"))

        # Lookup county
        county_clean = county_input.lower()
        match = df_formulas[df_formulas["County_clean"] == county_clean]

        if match.empty:
            flash(f"County '{county_input}' not found in Excel file.")
            return redirect(url_for("index"))

        row = match.iloc[0]
        county_display = row["County"]

        ev_formula = row.get("EVs_vs_SC_Formula")
        adopt_formula = row.get("Adopt_vs_SC_Formula")

        # Evaluate formulas if x provided
        if x_input:
            try:
                x_val = float(x_input)
            except ValueError:
                flash("Superchargers (x) must be a number.")
                return redirect(url_for("index"))

            ev_y = evaluate_formula(ev_formula, x_val)
            adopt_y = evaluate_formula(adopt_formula, x_val)

            if ev_y is None or adopt_y is None:
                flash("Could not evaluate one or both formulas.")
                return redirect(url_for("index"))

            result = {
                "x": x_val,
                "ev_y": ev_y,
                "adopt_y": adopt_y,
            }

        # Find PNG chart & map
        chart_filename = find_image_for_county(CHARTS_DIR, county_display)
        map_filename = find_image_for_county(MAPS_DIR, county_display)

        if chart_filename is None:
            flash(f"No chart image found for county: {county_display}")
        if map_filename is None:
            flash(f"No map image found for county: {county_display}")

    return render_template(
        "index.html",
        result=result,
        county=county_display,
        ev_formula=ev_formula,
        adopt_formula=adopt_formula,
        chart_filename=chart_filename,
        map_filename=map_filename,
    )


# =========================================================
# RUN FLASK
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
