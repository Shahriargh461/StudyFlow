from __future__ import annotations

__version__ = "1.1.0"

from datetime import date, datetime, timedelta
from pathlib import Path

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText

from storage import Storage
from scheduler import SmartScheduler
from plan_analyzer import PlanAnalyzer


KV = """
MDScreen:
    md_bg_color: app.bg
    MDBoxLayout:
        orientation: "vertical"

        MDScreenManager:
            id: manager

        MDNavigationBar:
            id: nav
            on_switch_tabs: app.switch_tab(*args)

            MDNavigationItem:
                id: nav_home
                active: True
                MDNavigationItemIcon:
                    icon: "home-outline"
                MDNavigationItemLabel:
                    id: nav_home_label
                    text: "Home"

            MDNavigationItem:
                id: nav_planner
                MDNavigationItemIcon:
                    icon: "calendar-check-outline"
                MDNavigationItemLabel:
                    id: nav_planner_label
                    text: "Planner"

            MDNavigationItem:
                id: nav_progress
                MDNavigationItemIcon:
                    icon: "chart-line"
                MDNavigationItemLabel:
                    id: nav_progress_label
                    text: "Progress"

            MDNavigationItem:
                id: nav_profile
                MDNavigationItemIcon:
                    icon: "account-circle-outline"
                MDNavigationItemLabel:
                    id: nav_profile_label
                    text: "Profile"
"""


TRANSLATIONS = {
    "en": {
        "home": "Home", "planner": "Planner", "progress": "Progress", "profile": "Profile",
        "focus": "Focus", "today": "Today", "streak": "Streak", "level": "Level",
        "daily_goal": "Daily study goal", "start_focus": "Start Focus",
        "next_up": "Next up", "start_task": "Start this task", "add_task": "+ Add Task",
        "generate": "Generate Smart Plan", "evaluate": "Evaluate Current Plan",
        "completed": "Completed", "due": "due", "min": "min", "tasks_subtitle": "Tasks and your generated study plan.",
        "progress_subtitle": "Your effort, measured without clutter.",
        "profile_subtitle": "Your study preferences and room.",
        "edit_profile": "Edit Profile", "language": "Language", "english": "English", "persian": "فارسی",
        "change_language": "Switch to فارسی", "virtual_room": "Virtual Room", "customize": "Customize Room",
        "social": "Social", "social_text": "Study groups are planned for a later version. Privacy-first by default.",
        "focus_mode": "FOCUS MODE", "pause": "Pause / Resume", "finish": "Finish",
        "exit": "Exit", "skip_break": "Skip Break", "break": "Break",
        "ready": "Ready when you are", "recharge": "Recharge before the next block",
        "all_complete": "All tasks are complete 🎉", "choose_task": "Choose a task",
        "smart_plan": "Smart Plan", "plan_quality": "Plan Quality",
        "excellent": "Excellent", "good": "Good", "needs_adjustment": "Needs adjustment", "high_risk": "High risk",
        "no_pending": "No pending tasks.", "today_plan": "Today's plan",
        "study_time_today": "Study time today", "weekly_total": "Weekly total",
        "achievements": "Achievements", "keep_studying": "Keep studying to unlock your first badge.",
        "age": "Age", "goal": "Goal", "min_day": "min/day", "room_complete": "Room Complete",
        "room_complete_text": "All current decorations are unlocked.", "locked": "Locked",
        "room_updated": "Room Updated", "unlocked": "unlocked!",
        "first_focus": "First Focus", "seven_streak": "7 Day Streak", "task_master": "Task Master",
        "goal_crusher": "Goal Crusher", "daily_goal_badge": "Daily Goal",
        "add_title": "Add Task", "task_name": "Task name", "subject": "Subject",
        "deadline": "Deadline YYYY-MM-DD", "minutes_hint": "Minutes (e.g. 45)",
        "difficulty": "Difficulty: Easy / Medium / Hard", "notes": "Notes (optional)",
        "cancel": "Cancel", "save": "Save", "ok": "OK", "edit_title": "Edit Profile",
        "name": "Name", "age_hint": "Age (15+)", "daily_goal_hint": "Daily goal (minutes)",
        "invalid": "Invalid input", "saved": "Saved", "plan_problem": "Plan issue",
        "score": "Score", "suggestions": "Suggestions", "balanced": "The plan is well balanced.",
        "no_task": "Task not scheduled", "too_much": "Too much work", "break_issue": "Not enough breaks",
        "overdue": "Overdue task", "heavy": "Heavy day", "unbalanced": "Unbalanced subjects",
    },
    "fa": {
        "home": "خانه", "planner": "برنامه‌ریز", "progress": "پیشرفت", "profile": "پروفایل",
        "focus": "تمرکز", "today": "امروز", "streak": "تداوم", "level": "سطح",
        "daily_goal": "هدف مطالعه روزانه", "start_focus": "شروع تمرکز",
        "next_up": "کار بعدی", "start_task": "شروع این کار", "add_task": "+ افزودن کار",
        "generate": "ساخت برنامه هوشمند", "evaluate": "ارزیابی برنامه فعلی",
        "completed": "انجام‌شده", "due": "تا", "min": "دقیقه", "tasks_subtitle": "کارها و برنامه مطالعه ساخته‌شده.",
        "progress_subtitle": "پیشرفت شما، ساده و مرتب.", "profile_subtitle": "تنظیمات مطالعه و اتاق شما.",
        "edit_profile": "ویرایش پروفایل", "language": "زبان", "english": "English", "persian": "فارسی",
        "change_language": "تغییر به English", "virtual_room": "اتاق مجازی", "customize": "شخصی‌سازی اتاق",
        "social": "اجتماعی", "social_text": "گروه‌های مطالعه در نسخه بعدی اضافه می‌شوند. حریم خصوصی اولویت دارد.",
        "focus_mode": "حالت تمرکز", "pause": "توقف / ادامه", "finish": "پایان",
        "exit": "خروج", "skip_break": "رد کردن استراحت", "break": "استراحت",
        "ready": "هر وقت آماده‌ای شروع کن", "recharge": "قبل از بخش بعدی کمی استراحت کن",
        "all_complete": "همه کارها انجام شده‌اند 🎉", "choose_task": "انتخاب یک کار",
        "smart_plan": "برنامه هوشمند", "plan_quality": "کیفیت برنامه",
        "excellent": "عالی", "good": "خوب", "needs_adjustment": "نیازمند اصلاح", "high_risk": "پرریسک",
        "no_pending": "کارِ در انتظار وجود ندارد.", "today_plan": "برنامه امروز",
        "study_time_today": "مطالعه امروز", "weekly_total": "مجموع هفتگی",
        "achievements": "دستاوردها", "keep_studying": "برای باز کردن اولین نشان به مطالعه ادامه بده.",
        "age": "سن", "goal": "هدف", "min_day": "دقیقه/روز", "room_complete": "اتاق کامل",
        "room_complete_text": "همه دکورهای فعلی باز شده‌اند.", "locked": "قفل است",
        "room_updated": "اتاق به‌روز شد", "unlocked": "باز شد!",
        "first_focus": "اولین تمرکز", "seven_streak": "تداوم ۷ روزه", "task_master": "استاد کارها",
        "goal_crusher": "هدف روزانه", "daily_goal_badge": "هدف روزانه",
        "add_title": "افزودن کار", "task_name": "نام کار", "subject": "درس",
        "deadline": "مهلت YYYY-MM-DD", "minutes_hint": "زمان به دقیقه (مثلاً 45)",
        "difficulty": "سختی: Easy / Medium / Hard", "notes": "یادداشت (اختیاری)",
        "cancel": "لغو", "save": "ذخیره", "ok": "باشه", "edit_title": "ویرایش پروفایل",
        "name": "نام", "age_hint": "سن (حداقل ۱۵)", "daily_goal_hint": "هدف روزانه (دقیقه)",
        "invalid": "ورودی نامعتبر", "saved": "ذخیره شد", "plan_problem": "مشکل برنامه",
        "score": "امتیاز", "suggestions": "پیشنهادها", "balanced": "برنامه تعادل خوبی دارد.",
        "no_task": "کار زمان‌بندی نشده", "too_much": "حجم کار زیاد است", "break_issue": "استراحت کافی نیست",
        "overdue": "کار عقب‌افتاده", "heavy": "روز سنگین", "unbalanced": "توزیع درس‌ها نامتعادل است",
    },
}


class StudyFlowApp(MDApp):
    bg = StringProperty("#F7F8FC")
    card = StringProperty("#FFFFFF")
    text = StringProperty("#161823")
    secondary = StringProperty("#707483")
    primary = StringProperty("#6C4CF1")
    green = StringProperty("#39B77A")
    orange = StringProperty("#F3A83B")
    focus_bg = StringProperty("#F2F0FA")

    xp = NumericProperty(0)
    level = NumericProperty(1)
    streak = NumericProperty(0)
    timer = NumericProperty(1500)
    running = BooleanProperty(False)
    timer_text = StringProperty("25:00")
    focus_title = StringProperty("Focus")
    focus_subject = StringProperty("Ready when you are")
    name = StringProperty("Student")
    daily_goal = NumericProperty(120)
    today_minutes = NumericProperty(0)
    language = StringProperty("en")

    dialog = None
    ticker = None
    session_id = None
    active_task_id = None
    actual = 0
    paused = False
    kind = "study"
    timer_label = None
    focus_title_label = None
    focus_subject_label = None

    def t(self, key):
        return TRANSLATIONS.get(self.language, TRANSLATIONS["en"]).get(key, key)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.storage = Storage()
        self.analyzer = PlanAnalyzer()
        self.refresh_state()

        root = Builder.load_string(KV)
        self._build_screens(root.ids.manager)
        self._apply_language()
        self._set_tab("Home")
        return root

    def _build_screens(self, manager):
        manager.clear_widgets()
        self.home = MDScreen(name="Home")
        self.planner = MDScreen(name="Planner")
        self.progress = MDScreen(name="Progress")
        self.profile = MDScreen(name="Profile")
        self.focus = MDScreen(name="Focus")
        for screen in (self.home, self.planner, self.progress, self.profile, self.focus):
            manager.add_widget(screen)

        self.render_home()
        self.render_planner()
        self.render_progress()
        self.render_profile()
        self.render_focus()

    def refresh_state(self):
        p = self.storage.get_profile()
        pr = self.storage.get_progress()
        self.name = p["name"]
        self.daily_goal = p["daily_goal"]
        self.language = p.get("language", "en") or "en"
        self.xp = pr["xp"]
        self.streak = pr["streak"]
        self.level = self.xp // 250 + 1
        self.today_minutes = self.storage.total_study_seconds(date.today(), date.today()) // 60

    def label(self, txt, size=None, color=None, bold=False, h=None):
        w = MDLabel(
            text=str(txt),
            theme_text_color="Custom",
            text_color=color or self.text,
            bold=bold,
            size_hint_y=None,
            halign="right" if self.language == "fa" else "left",
            valign="middle",
        )
        if size:
            w.font_size = dp(size)
        if h:
            w.height = dp(h)
        return w

    def card(self, children, height=None):
        c = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            radius=[dp(20)] * 4,
            elevation=0,
            md_bg_color=self.card,
            size_hint_y=None,
        )
        if height:
            c.height = dp(height)
        for child in children:
            c.add_widget(child)
        return c

    def button(self, text, callback, style="filled", icon=None):
        b = MDButton(style=style)
        if icon:
            b.add_widget(MDButtonIcon(icon=icon))
        b.add_widget(MDButtonText(text=text))
        b.bind(on_release=callback)
        return b

    def page(self, title, subtitle=None):
        box = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
        )
        box.bind(minimum_height=box.setter("height"))
        box.add_widget(self.label(title, bold=True, h=42))
        if subtitle:
            box.add_widget(self.label(subtitle, color=self.secondary, h=30))
        return box

    def _set_content(self, screen, box):
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        scroll.add_widget(box)
        screen.clear_widgets()
        screen.add_widget(scroll)

    def _apply_language(self):
        if not hasattr(self, "root") or not self.root:
            return
        ids = self.root.ids
        ids.nav_home_label.text = self.t("home")
        ids.nav_planner_label.text = self.t("planner")
        ids.nav_progress_label.text = self.t("progress")
        ids.nav_profile_label.text = self.t("profile")

    def switch_tab(self, bar, item, item_icon, item_text):
        mapping = {
            self.root.ids.nav_home: "Home",
            self.root.ids.nav_planner: "Planner",
            self.root.ids.nav_progress: "Progress",
            self.root.ids.nav_profile: "Profile",
        }
        self._set_tab(mapping.get(item, "Home"))

    def _set_tab(self, screen_name):
        self.root.ids.manager.current = screen_name
        if screen_name == "Home":
            self.render_home()
            self.root.ids.nav.set_active_item(self.root.ids.nav_home)
        elif screen_name == "Planner":
            self.render_planner()
            self.root.ids.nav.set_active_item(self.root.ids.nav_planner)
        elif screen_name == "Progress":
            self.render_progress()
            self.root.ids.nav.set_active_item(self.root.ids.nav_progress)
        elif screen_name == "Profile":
            self.render_profile()
            self.root.ids.nav.set_active_item(self.root.ids.nav_profile)

    def render_home(self):
        self.refresh_state()
        b = self.page(
            f'Hi, {self.name} 👋' if self.language == "en" else f"سلام، {self.name} 👋",
            "A calm place to plan, focus, and make progress." if self.language == "en" else "جایی آرام برای برنامه‌ریزی، تمرکز و پیشرفت.",
        )

        stats = MDBoxLayout(size_hint_y=None, height=dp(86), spacing=dp(10))
        for title, val in [
            (self.t("today"), f"{self.today_minutes} {self.t('min')}"),
            (self.t("streak"), f"{self.streak}"),
            (self.t("level"), f"{self.level}"),
        ]:
            stats.add_widget(
                self.card(
                    [self.label(title, color=self.secondary, h=22), self.label(val, bold=True, h=28)],
                    86,
                )
            )
        b.add_widget(stats)

        goal = self.card(
            [
                self.label(self.t("daily_goal"), color=self.secondary, h=24),
                self.label(f"{self.today_minutes} / {self.daily_goal} {self.t('min')}", bold=True, h=30),
                self.button(self.t("start_focus"), self.open_focus_picker, icon="timer-play-outline"),
            ],
            150,
        )
        b.add_widget(goal)

        tasks = self.storage.list_tasks(True)
        if tasks:
            t = tasks[0]
            b.add_widget(
                self.card(
                    [
                        self.label(self.t("next_up"), color=self.secondary, h=22),
                        self.label(t.name, bold=True, h=28),
                        self.label(f"{t.subject} • {t.minutes} {self.t('min')} • {self.t('due')} {t.deadline}", color=self.secondary, h=24),
                        self.button(self.t("start_task"), lambda *_a, tid=t.id: self.start_focus(tid), style="tonal", icon="play"),
                    ],
                    132,
                )
            )
        self._set_content(self.home, b)

    def render_planner(self):
        b = self.page(self.t("planner"), self.t("tasks_subtitle"))
        b.add_widget(self.button(self.t("add_task"), self.add_task_dialog, icon="plus"))
        tasks = self.storage.list_tasks(False)

        for task in tasks:
            status = self.t("completed") if task.completed else f"{task.minutes} {self.t('min')} • {self.t('due')} {task.deadline}"
            row = self.card(
                [
                    self.label(task.name, bold=True, h=26),
                    self.label(f"{task.subject} • {task.difficulty}", color=self.secondary, h=22),
                    self.label(status, color=self.secondary, h=22),
                ],
                116,
            )
            if not task.completed:
                row.add_widget(
                    self.button(
                        self.t("start_focus"),
                        lambda *_a, tid=task.id: self.start_focus(tid),
                        style="tonal",
                        icon="play",
                    )
                )
            else:
                row.opacity = 0.65
            b.add_widget(row)

        b.add_widget(self.button(self.t("generate"), self.generate_plan, style="tonal", icon="auto-fix"))
        b.add_widget(self.button(self.t("evaluate"), self.evaluate_current_plan, style="outlined", icon="chart-box-outline"))
        self._set_content(self.planner, b)

    def text_field(self, hint, text=""):
        field = MDTextField(mode="outlined")
        field.add_widget(MDTextFieldHintText(text=hint))
        field.text = text
        return field

    def add_task_dialog(self, *_):
        fields = [
            self.text_field(self.t("task_name")),
            self.text_field(self.t("subject")),
            self.text_field(self.t("deadline")),
            self.text_field(self.t("minutes_hint")),
            self.text_field(self.t("difficulty")),
            self.text_field(self.t("notes")),
        ]
        body = MDDialogContentContainer(*fields, orientation="vertical", spacing=dp(8))
        buttons = MDDialogButtonContainer(
            Widget(),
            self.button(self.t("cancel"), lambda *_: self.dialog.dismiss(), "text"),
            self.button(self.t("save"), lambda *_: self._save_task(fields), "filled"),
        )
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=self.t("add_title")),
            body,
            buttons,
            width_offset=dp(32),
        )
        self.dialog.open()

    def _save_task(self, fields):
        name = fields[0].text.strip() or ("New Task" if self.language == "en" else "کار جدید")
        subject = fields[1].text.strip() or ("General" if self.language == "en" else "عمومی")
        deadline = fields[2].text.strip() or date.today().isoformat()

        try:
            parsed_deadline = date.fromisoformat(deadline)
            if parsed_deadline < date.today() - timedelta(days=365):
                raise ValueError
        except ValueError:
            return self.show_message(self.t("invalid"), self.t("deadline"))

        try:
            minutes = max(5, min(600, int(fields[3].text)))
        except ValueError:
            minutes = 30

        difficulty = fields[4].text.strip().title()
        if difficulty not in ("Easy", "Medium", "Hard"):
            difficulty = "Medium"

        self.storage.add_task(name, subject, deadline, minutes, difficulty, fields[5].text.strip())
        self.dialog.dismiss()
        self.render_planner()

    def _plan_report(self):
        tasks = self.storage.list_tasks(True)
        blocks = SmartScheduler(day=date.today()).generate(tasks)
        available = 300
        return blocks, self.analyzer.analyze(tasks, blocks, date.today(), available)

    def generate_plan(self, *_):
        blocks, report = self._plan_report()
        lines = []
        for block in blocks:
            if block.kind == "study":
                lines.append(f"{block.start:%H:%M}–{block.end:%H:%M}  📚 {block.title}")
            else:
                lines.append(f"{block.start:%H:%M}–{block.end:%H:%M}  ☕ {self.t('break')}")
        schedule = "\n".join(lines) or self.t("no_pending")
        self.show_plan_dialog(schedule, report)

    def evaluate_current_plan(self, *_):
        _, report = self._plan_report()
        self.show_plan_report(report)

    def show_plan_dialog(self, schedule, report):
        score = f"{self.t('plan_quality')}: {report.score}/100 — {self._report_label(report.label)}"
        content = MDLabel(
            text=score + "\n\n" + schedule,
            theme_text_color="Custom",
            text_color=self.text,
            size_hint_y=None,
            height=dp(max(160, 36 + 28 * max(1, len(schedule.splitlines())))),
            halign="right" if self.language == "fa" else "left",
            valign="top",
        )
        body = MDDialogContentContainer(content, orientation="vertical")
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=self.t("smart_plan")),
            body,
            MDDialogButtonContainer(
                Widget(),
                self.button(self.t("ok"), lambda *_: self.dialog.dismiss(), "filled"),
            ),
            width_offset=dp(32),
        )
        self.dialog.open()

        # Offer detailed evaluation after the plan dialog is closed via a second explicit action.
        self._last_plan_report = report

    def show_plan_report(self, report):
        issue_lines = []
        for issue in report.issues:
            icon = "⚠️" if issue.severity == "warning" else ("🔴" if issue.severity == "critical" else "ℹ️")
            issue_lines.append(f"{icon} {issue.title}: {issue.detail}")
        message = (
            f"{self.t('score')}: {report.score}/100 — {self._report_label(report.label)}\n\n"
            + "\n".join(issue_lines)
        )
        self.show_message(self.t("plan_quality"), message)

    def _report_label(self, label):
        return {
            "Excellent": self.t("excellent"),
            "Good": self.t("good"),
            "Needs adjustment": self.t("needs_adjustment"),
            "High risk": self.t("high_risk"),
        }.get(label, label)

    def open_focus_picker(self, *_):
        tasks = self.storage.list_tasks(True)
        if not tasks:
            return self.show_message(self.t("focus"), self.t("all_complete"))

        content = MDBoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        for task in tasks[:8]:
            content.add_widget(
                self.button(
                    f"{task.name} • {task.minutes} {self.t('min')}",
                    lambda *_a, tid=task.id: self._pick_focus_task(tid),
                    "tonal",
                    "play",
                )
            )
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=self.t("choose_task")),
            MDDialogContentContainer(content, orientation="vertical"),
            MDDialogButtonContainer(
                Widget(),
                self.button(self.t("cancel"), lambda *_: self.dialog.dismiss(), "text"),
            ),
            width_offset=dp(32),
        )
        self.dialog.open()

    def _pick_focus_task(self, task_id):
        if self.dialog:
            self.dialog.dismiss()
        Clock.schedule_once(lambda *_: self.start_focus(task_id), 0.05)

    def start_focus(self, task_id):
        task = self.storage.get_task(task_id)
        if not task or task.completed:
            return
        self._stop_timer()
        self.active_task_id = task.id
        self.focus_title = task.name
        self.focus_subject = task.subject
        self.kind = "study"
        self.timer = min(45 * 60, max(60, task.minutes * 60))
        self.actual = 0
        self.paused = False
        self.session_id = self.storage.start_session(self.active_task_id, "study", self.timer)
        self.running = True
        self.root.ids.manager.current = "Focus"
        self.render_focus()
        self._render_timer()
        self.ticker = Clock.schedule_interval(self._tick, 1)

    def start_break(self):
        self._stop_timer()
        self.active_task_id = None
        self.session_id = None
        self.kind = "break"
        self.timer = 15 * 60
        self.focus_title = self.t("break")
        self.focus_subject = self.t("recharge")
        self.actual = 0
        self.paused = False
        self.running = True
        self.root.ids.manager.current = "Focus"
        self.render_focus()
        self._render_timer()
        self.ticker = Clock.schedule_interval(self._tick, 1)

    def _tick(self, dt):
        if not self.running or self.paused:
            return
        self.timer = max(0, self.timer - 1)
        self.actual += 1
        self._render_timer()

        if self.timer == 0:
            if self.kind == "study":
                self.finish_focus(True)
            else:
                self.finish_break()

    def _render_timer(self):
        self.timer_text = f"{self.timer // 60:02d}:{self.timer % 60:02d}"
        if self.timer_label:
            self.timer_label.text = self.timer_text

    def pause(self, *_):
        if self.running:
            self.paused = not self.paused

    def finish_focus(self, natural=False, *_):
        if not self.running or self.kind != "study":
            if self.kind == "break":
                self.finish_break()
            return

        self._stop_timer()
        actual = self.actual
        session_id = self.session_id
        self.running = False
        self.session_id = None

        if session_id is not None:
            self.storage.finish_session(session_id, actual, natural)

        if actual >= 60:
            self.storage.add_xp(10)
            self.storage.register_activity()
            task = self.storage.get_task(self.active_task_id)
            threshold = max(60, int((task.minutes if task else 60) * 60 * 0.5))
            if natural or actual >= threshold:
                self.storage.set_completed(self.active_task_id, True)
                self.storage.add_xp(25)
            self._award_daily_goal_if_reached()

        self.refresh_state()
        self.start_break()

    def finish_break(self, *_):
        self._stop_timer()
        self.running = False
        self.session_id = None
        self.kind = "study"
        self.root.ids.manager.current = "Home"
        self.render_home()

    def skip_break(self, *_):
        if self.kind != "break":
            return
        self._stop_timer()
        self.running = False
        self.session_id = None
        self.kind = "study"
        self.root.ids.manager.current = "Home"
        self.render_home()

    def render_focus(self):
        b = MDBoxLayout(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(14),
            size_hint_y=None,
            height=dp(500),
            md_bg_color=self.focus_bg,
        )

        b.add_widget(self.label(self.t("focus_mode"), color=self.secondary, bold=True, h=30))
        self.focus_title_label = self.label(self.focus_title, bold=True, h=50)
        self.focus_subject_label = self.label(self.focus_subject, color=self.secondary, h=34)
        self.timer_label = self.label(self.timer_text, bold=True, h=140)
        b.add_widget(self.focus_title_label)
        b.add_widget(self.focus_subject_label)
        b.add_widget(self.timer_label)

        controls = MDBoxLayout(size_hint_y=None, height=dp(54), spacing=dp(8))
        controls.add_widget(self.button(self.t("pause"), self.pause, "tonal", "pause"))
        controls.add_widget(self.button(self.t("finish"), lambda *_: self.finish_focus(False), "filled", "check"))
        controls.add_widget(self.button(self.t("exit"), self.exit_focus, "outlined", "close"))
        b.add_widget(controls)

        if self.kind == "break":
            b.add_widget(self.button(self.t("skip_break"), self.skip_break, "tonal", "skip-forward"))

        self._set_content(self.focus, b)

    def exit_focus(self, *_):
        self._stop_timer()
        if self.running and self.kind == "study" and self.session_id is not None:
            self.storage.finish_session(self.session_id, self.actual, False)
        self.running = False
        self.session_id = None
        self.kind = "study"
        self.root.ids.manager.current = "Home"
        self.render_home()

    def render_progress(self):
        self.refresh_state()
        b = self.page(self.t("progress"), self.t("progress_subtitle"))
        xp_in = self.xp % 250
        b.add_widget(self.card([self.label(f"{self.t('level')} {self.level}", bold=True, h=30), self.label(f"{xp_in} / 250 XP", color=self.secondary, h=24)], 92))
        weekly = self.storage.total_study_seconds(date.today() - timedelta(days=6), date.today()) // 60
        b.add_widget(
            self.card(
                [
                    self.label(self.t("study_time_today"), color=self.secondary, h=22),
                    self.label(f"{self.today_minutes} {self.t('min')}", bold=True, h=30),
                    self.label(self.t("weekly_total"), color=self.secondary, h=22),
                    self.label(f"{weekly} {self.t('min')}", bold=True, h=30),
                ],
                130,
            )
        )
        b.add_widget(self.card([self.label(self.t("achievements"), bold=True, h=26), self.label(self._achievement_text(), color=self.secondary, h=60)], 110))

        subjects = self.storage.subject_minutes(date.today() - timedelta(days=6), date.today())
        for subject, minutes in subjects[:5]:
            b.add_widget(self.card([self.label(subject, bold=True, h=24), self.label(f"{minutes} {self.t('min')}", color=self.secondary, h=24)], 72))
        self._set_content(self.progress, b)

    def _award_daily_goal_if_reached(self):
        self.refresh_state()
        if self.today_minutes >= self.daily_goal and "Daily Goal" not in self.storage.achievements():
            self.storage.add_xp(50)
            self.storage.unlock_achievement("Daily Goal")

        if self.storage.completed_count() >= 5:
            self.storage.unlock_achievement("Task Master")

        if self.streak >= 7 and "7 Day Streak" not in self.storage.achievements():
            self.storage.add_xp(100)
            self.storage.unlock_achievement("7 Day Streak")
        self.refresh_state()

    def _achievement_text(self):
        achievements = self.storage.achievements()
        unlocked = []
        if self.storage.total_study_seconds() > 0:
            unlocked.append(self.t("first_focus"))
        if self.streak >= 7:
            unlocked.append(self.t("seven_streak"))
        if self.storage.completed_count() >= 5:
            unlocked.append(self.t("task_master"))
        if self.today_minutes >= self.daily_goal:
            unlocked.append(self.t("goal_crusher"))

        for key in (
            "First Focus",
            "7 Day Streak" if self.streak >= 7 else "",
            "Task Master" if self.storage.completed_count() >= 5 else "",
            "Goal Crusher" if self.today_minutes >= self.daily_goal else "",
        ):
            if key:
                self.storage.unlock_achievement(key)

        return " • ".join(unlocked or [self.t("keep_studying")])

    def render_profile(self):
        self.refresh_state()
        profile = self.storage.get_profile()
        b = self.page(self.t("profile"), self.t("profile_subtitle"))

        b.add_widget(
            self.card(
                [
                    self.label(profile["name"], bold=True, h=28),
                    self.label(f'{self.t("age")} {profile["age"]} • {self.t("goal")} {profile["daily_goal"]} {self.t("min_day")}', color=self.secondary, h=24),
                    self.label(f'{self.t("language")}: {self.t("persian") if self.language == "fa" else self.t("english")}', color=self.secondary, h=24),
                ],
                118,
            )
        )

        b.add_widget(
            self.card(
                [
                    self.label(self.t("virtual_room"), bold=True, h=26),
                    self.label(self.room_text(), color=self.secondary, h=44),
                    self.button(self.t("customize"), self.customize_room, "tonal", "home-edit-outline"),
                ],
                140,
            )
        )
        b.add_widget(
            self.card(
                [
                    self.label(self.t("social"), bold=True, h=25),
                    self.label(self.t("social_text"), color=self.secondary, h=52),
                ],
                116,
            )
        )
        b.add_widget(self.button(self.t("edit_profile"), self.edit_profile, "outlined", "pencil"))
        b.add_widget(self.button(self.t("change_language"), self.toggle_language, "tonal", "translate"))
        self._set_content(self.profile, b)

    def room_text(self):
        decorations = self.storage.decorations()
        names = {
            "desk": "Desk" if self.language == "en" else "میز",
            "chair": "Chair" if self.language == "en" else "صندلی",
            "lamp": "Lamp" if self.language == "en" else "چراغ",
            "books": "Books" if self.language == "en" else "کتاب",
            "plant": "Plant" if self.language == "en" else "گیاه",
            "poster": "Poster" if self.language == "en" else "پوستر",
        }
        unlocked = [value for key, value in names.items() if decorations.get(key)]
        suffix = " • Earn XP to unlock more." if self.language == "en" else " • برای باز کردن موارد بیشتر XP بگیر."
        return " • ".join(unlocked) + suffix

    def customize_room(self, *_):
        self.refresh_state()
        order = ["lamp", "books", "plant", "poster"]
        decorations = self.storage.decorations()
        locked = next((key for key in order if not decorations.get(key)), None)
        if not locked:
            return self.show_message(self.t("room_complete"), self.t("room_complete_text"))

        costs = {"lamp": 100, "books": 200, "plant": 300, "poster": 400}
        if self.xp < costs[locked]:
            return self.show_message(self.t("locked"), f"{locked.title()} → {costs[locked]} XP")

        self.storage.unlock_decoration(locked)
        self.show_message(self.t("room_updated"), f"{locked.title()} {self.t('unlocked')}")
        self.render_profile()

    def edit_profile(self, *_):
        profile = self.storage.get_profile()
        fields = [
            self.text_field(self.t("name"), profile["name"]),
            self.text_field(self.t("age_hint"), str(profile["age"])),
            self.text_field(self.t("daily_goal_hint"), str(self.daily_goal)),
        ]
        body = MDDialogContentContainer(*fields, orientation="vertical", spacing=dp(8))
        buttons = MDDialogButtonContainer(
            Widget(),
            self.button(self.t("cancel"), lambda *_: self.dialog.dismiss(), "text"),
            self.button(self.t("save"), lambda *_: self._save_profile(fields), "filled"),
        )
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=self.t("edit_title")),
            body,
            buttons,
            width_offset=dp(32),
        )
        self.dialog.open()

    def _save_profile(self, fields):
        try:
            age = max(15, min(100, int(fields[1].text)))
            goal = max(15, min(600, int(fields[2].text)))
        except ValueError:
            return self.show_message(self.t("invalid"), self.t("daily_goal_hint"))

        self.storage.update_profile(
            fields[0].text.strip() or "Student",
            age,
            goal,
            self.storage.get_profile()["subjects"],
            self.language,
        )
        self.dialog.dismiss()
        self.refresh_state()
        self.render_profile()
        self.render_home()

    def toggle_language(self, *_):
        self.language = "fa" if self.language == "en" else "en"
        profile = self.storage.get_profile()
        self.storage.update_profile(profile["name"], profile["age"], profile["daily_goal"], profile["subjects"], self.language)
        self._apply_language()
        self.render_home()
        self.render_planner()
        self.render_progress()
        self.render_profile()

    def show_message(self, title, message):
        if self.dialog:
            try:
                self.dialog.dismiss()
            except Exception:
                pass

        content = MDDialogSupportingText(text=str(message))
        self.dialog = MDDialog(
            MDDialogHeadlineText(text=str(title)),
            content,
            MDDialogButtonContainer(
                Widget(),
                self.button(self.t("ok"), lambda *_: self.dialog.dismiss(), "filled"),
            ),
            width_offset=dp(32),
        )
        self.dialog.open()


if __name__ == "__main__":
    StudyFlowApp().run()
