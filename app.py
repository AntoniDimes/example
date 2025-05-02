from flask import Flask, render_template, request
from schedule import get_team_schedule
from team_id import get_teams

app = Flask(__name__)

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    # Get all the team from the list
    teams = get_teams()

    if request.method == "POST":
        team_name = request.form.get("team")
        if not team_name:
            return render_template("schedule.html", teams=teams, error="Please enter a team name.")

        # Auto-capitalize the first letter of each word
        team_name = team_name.title()

        schedule = get_team_schedule(team_name)

        if schedule:
            return render_template("schedule.html", schedule=schedule, teams=teams)
        else:
            return render_template("schedule.html", teams=teams, error=f"No schedule found for team '{team_name}'. Please try again.")

    return render_template("schedule.html", teams=teams)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
