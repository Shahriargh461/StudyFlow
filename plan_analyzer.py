from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable


@dataclass(frozen=True)
class PlanIssue:
    severity: str  # info, warning, critical
    title: str
    detail: str


@dataclass(frozen=True)
class PlanReport:
    score: int
    label: str
    issues: tuple[PlanIssue, ...]


class PlanAnalyzer:
    """Deterministic, offline plan-quality evaluator for StudyFlow MVP."""

    def analyze(self, tasks, blocks, day: date | None = None, available_minutes: int = 300) -> PlanReport:
        day = day or date.today()
        issues: list[PlanIssue] = []
        score = 100

        pending = [t for t in tasks if not t.completed and t.minutes > 0]
        study_blocks = [b for b in blocks if b.kind == "study"]
        break_blocks = [b for b in blocks if b.kind == "break"]

        total_planned = sum(b.minutes for b in study_blocks)
        total_break = sum(b.minutes for b in break_blocks)

        if not pending:
            return PlanReport(100, "Excellent", (PlanIssue("info", "No pending tasks", "Your task list is already clear."),))

        # Deadline coverage: tasks that cannot fit before their deadline are the largest risk.
        covered = {b.task_id for b in study_blocks if b.task_id is not None}
        for task in pending:
            deadline = date.fromisoformat(task.deadline)
            if deadline < day:
                issues.append(PlanIssue("critical", "Overdue task", f"{task.name} is already past its deadline."))
                score -= 25
            elif task.id not in covered:
                issues.append(PlanIssue("critical", "Task not scheduled", f"{task.name} does not fit in today's available plan."))
                score -= 18

        if total_planned > available_minutes:
            over = total_planned - available_minutes
            issues.append(PlanIssue("critical", "Too much work", f"The plan exceeds available study time by about {over} minutes."))
            score -= min(30, 15 + over // 15)

        # Workload quality.
        if total_planned > 240:
            issues.append(PlanIssue("warning", "Heavy day", "More than 4 hours of planned study is demanding for one day."))
            score -= 8
        elif total_planned > 180:
            issues.append(PlanIssue("warning", "Busy day", "The study load is fairly high; keep breaks protected."))
            score -= 4

        # Break quality.
        if total_planned >= 90 and total_break < max(15, total_planned // 5):
            issues.append(PlanIssue("warning", "Not enough breaks", "Add short breaks between longer study blocks."))
            score -= 8
        if total_planned >= 45 and not break_blocks:
            issues.append(PlanIssue("warning", "No break block", "A break should follow focused study blocks."))
            score -= 6

        # Subject balance.
        subject_minutes: dict[str, int] = {}
        for b in study_blocks:
            subject_minutes[b.subject] = subject_minutes.get(b.subject, 0) + b.minutes
        if subject_minutes and total_planned:
            dominant_subject, dominant = max(subject_minutes.items(), key=lambda x: x[1])
            if len(subject_minutes) >= 2 and dominant / total_planned > 0.70:
                issues.append(PlanIssue("warning", "Unbalanced subjects", f"{dominant_subject} takes most of the planned study time."))
                score -= 6

        # Hard-task clustering.
        hard_ids = {t.id for t in pending if t.difficulty == "Hard"}
        hard_sequence = 0
        max_hard_sequence = 0
        for b in study_blocks:
            if b.task_id in hard_ids:
                hard_sequence += 1
                max_hard_sequence = max(max_hard_sequence, hard_sequence)
            else:
                hard_sequence = 0
        if max_hard_sequence >= 3:
            issues.append(PlanIssue("warning", "Hard-task cluster", "Several difficult blocks are consecutive; alternate with an easier task or break."))
            score -= 5

        # Deadline proximity.
        urgent = [t for t in pending if (date.fromisoformat(t.deadline) - day).days <= 1]
        if urgent and len(urgent) >= 2:
            issues.append(PlanIssue("warning", "Multiple urgent tasks", "Several tasks are due today or tomorrow; protect their blocks first."))
            score -= 5

        score = max(0, min(100, score))
        if score >= 85:
            label = "Excellent"
        elif score >= 70:
            label = "Good"
        elif score >= 50:
            label = "Needs adjustment"
        else:
            label = "High risk"

        if not issues:
            issues.append(PlanIssue("info", "Well balanced", "The plan fits the available time and has a healthy structure."))

        return PlanReport(score, label, tuple(issues))
