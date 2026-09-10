from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appointments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Appointment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable=True)
  date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
  start_time = db.Column(db.String(5), nullable=False)  # HH:MM
  end_time = db.Column(db.String(5), nullable=False)  # HH:MM
  status = db.Column(
      db.String(20), default="Scheduled"
  )  # Scheduled, Completed, Cancelled


def seed_data():
  """Seeds sample appointments if database is empty."""
  if Appointment.query.count() == 0:
    samples = [
        Appointment(
            title="Sprint Planning",
            description="Discuss Q3 goals and milestones",
            date="2026-09-15",
            start_time="10:00",
            end_time="11:00",
            status="Scheduled",
        ),
        Appointment(
            title="Client Review Call",
            description="Review dashboard deliverables",
            date="2026-09-15",
            start_time="14:00",
            end_time="15:00",
            status="Completed",
        ),
        Appointment(
            title="Architecture Sync",
            description="API design review",
            date="2026-09-16",
            start_time="11:30",
            end_time="12:30",
            status="Cancelled",
        ),
    ]
    db.session.bulk_save_objects(samples)
    db.session.commit()


def check_time_conflict(date, start_time, end_time, exclude_id=None):
  """Checks if overlapping active appointment exists."""
  query = Appointment.query.filter(
      Appointment.date == date, Appointment.status != "Cancelled"
  )
  if exclude_id:
    query = query.filter(Appointment.id != exclude_id)

  for appt in query.all():
    # Two intervals [s1, e1) and [s2, e2) overlap if s1 < e2 and s2 < e1
    if start_time < appt.end_time and appt.start_time < end_time:
      return True
  return False


@app.route("/")
def index():
  filter_date = request.args.get("date", "").strip()
  filter_status = request.args.get("status", "").strip()

  query = Appointment.query
  if filter_date:
    query = query.filter(Appointment.date == filter_date)
  if filter_status:
    query = query.filter(Appointment.status == filter_status)

  appointments = query.order_by(
      Appointment.date.asc(), Appointment.start_time.asc()
  ).all()
  return render_template(
      "index.html",
      appointments=appointments,
      filter_date=filter_date,
      filter_status=filter_status,
  )


@app.route("/appointment/add", methods=["POST"])
def add_appointment():
  title = request.form.get("title", "").strip()
  description = request.form.get("description", "").strip()
  date = request.form.get("date", "").strip()
  start_time = request.form.get("start_time", "").strip()
  end_time = request.form.get("end_time", "").strip()

  if not (title and date and start_time and end_time):
    flash("All required fields must be filled.", "error")
    return redirect(url_for("index"))

  if end_time <= start_time:
    flash("End time must be after the start time.", "error")
    return redirect(url_for("index"))

  if check_time_conflict(date, start_time, end_time):
    flash("Selected slot conflicts with an existing appointment.", "error")
    return redirect(url_for("index"))

  new_appt = Appointment(
      title=title,
      description=description,
      date=date,
      start_time=start_time,
      end_time=end_time,
      status="Scheduled",
  )
  db.session.add(new_appt)
  db.session.commit()
  flash("Appointment scheduled successfully!", "success")
  return redirect(url_for("index"))


@app.route("/appointment/<int:id>/edit", methods=["POST"])
def edit_appointment():
  appt = Appointment.query.get_or_404(id)
  title = request.form.get("title", "").strip()
  description = request.form.get("description", "").strip()
  date = request.form.get("date", "").strip()
  start_time = request.form.get("start_time", "").strip()
  end_time = request.form.get("end_time", "").strip()

  if not (title and date and start_time and end_time):
    flash("All required fields must be filled.", "error")
    return redirect(url_for("index"))

  if end_time <= start_time:
    flash("End time must be after the start time.", "error")
    return redirect(url_for("index"))

  if (
      appt.status != "Cancelled"
      and check_time_conflict(date, start_time, end_time, exclude_id=appt.id)
  ):
    flash("Selected slot conflicts with an existing appointment.", "error")
    return redirect(url_for("index"))

  appt.title = title
  appt.description = description
  appt.date = date
  appt.start_time = start_time
  appt.end_time = end_time
  db.session.commit()
  flash("Appointment updated successfully.", "success")
  return redirect(url_for("index"))


@app.route("/appointment/<int:id>/complete", methods=["POST"])
def complete_appointment(id):
  appt = Appointment.query.get_or_404(id)
  if appt.status == "Cancelled":
    flash("Cannot mark a cancelled appointment as completed.", "error")
  else:
    appt.status = "Completed"
    db.session.commit()
    flash("Appointment marked as completed!", "success")
  return redirect(url_for("index"))


@app.route("/appointment/<int:id>/cancel", methods=["POST"])
def cancel_appointment(id):
  appt = Appointment.query.get_or_404(id)
  appt.status = "Cancelled"
  db.session.commit()
  flash(
      "Appointment cancelled. Slot is now available for other bookings.",
      "success",
  )
  return redirect(url_for("index"))


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    seed_data()
  app.run(debug=True)