from datetime import datetime
from flask import Blueprint, jsonify, request

from .models import Availability

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/test")
def test_api():
    return {"message": "CareSchedule API is working!"}

@api.route("/availability")
def get_availability():
    date_str =request.args.get("date")

    if date_str:
        selected_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

        slots = Availability.query.filter(
            Availability.is_booked == False,
            Availability.start_time >= datetime.combine(
                selected_date,
                datetime.min.time()
            ),
            Availability.start_time <= datetime.combine(
                selected_date,
                datetime.max.time()
            )
        ).all()

    else:
        slots = Availability.query.filter_by(
            is_booked=False
        ).all()

    return jsonify([
        slot.to_dict() for slot in slots
    ])