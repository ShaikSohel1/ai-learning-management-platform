"""
Calendar Service Module.

Generates structured study plans, learning milestones, and exports iCalendar (.ics) calendar files.
"""

from datetime import datetime, timedelta, UTC
from typing import Dict, Any, List


class CalendarService:
    """Generates study plans and iCalendar (.ics) exports."""

    def generate_study_plan(self, course_title: str, weeks: int = 4) -> Dict[str, Any]:
        start_date = datetime.now(UTC)
        weekly_sessions: List[Dict[str, Any]] = []

        for w in range(1, weeks + 1):
            session_date = start_date + timedelta(days=(w - 1) * 7 + 1)
            weekly_sessions.append({
                "week": w,
                "title": f"Week {w}: {course_title} Mastery",
                "date": session_date.strftime("%Y-%m-%d"),
                "duration_minutes": 90,
                "agenda": f"Complete Module {w} video lessons and practical lab exercises."
            })

        return {
            "course_title": course_title,
            "total_weeks": weeks,
            "total_sessions": len(weekly_sessions),
            "sessions": weekly_sessions
        }

    def export_ics_calendar(self, course_title: str, user_name: str) -> str:
        """Generates RFC 5545 compliant iCalendar string."""
        now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        start = (datetime.now(UTC) + timedelta(days=1)).strftime("%Y%m%dT100000Z")
        end = (datetime.now(UTC) + timedelta(days=1, hours=2)).strftime("%Y%m%dT120000Z")

        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI LMS Enterprise Action Assistant//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "BEGIN:VEVENT",
            f"UID:lms-session-{now}@ailms.enterprise",
            f"DTSTAMP:{now}",
            f"DTSTART:{start}",
            f"DTEND:{end}",
            f"SUMMARY:📚 AI LMS Study Session: {course_title}",
            f"DESCRIPTION:Scheduled learning session for {user_name} on course '{course_title}'.",
            "STATUS:CONFIRMED",
            "END:VEVENT",
            "END:VCALENDAR"
        ]

        return "\r\n".join(ics_lines)


calendar_service = CalendarService()
