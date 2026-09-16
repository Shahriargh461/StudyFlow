# StudyFlow

StudyFlow is an offline-first Kivy/KivyMD study planner for Android.

## MVP features

- Home, Planner, Focus, Progress and Profile
- SQLite task and focus-session persistence
- Smart scheduling with study blocks and breaks
- XP, levels, streaks, achievements and virtual room decorations
- English / فارسی language switch with persisted preference
- Offline Plan Quality Analyzer with a 0–100 score and actionable issues
- Android build via Buildozer and GitHub Actions

## Android

The current build targets modern Android with API 36 and supports Android 8.0+ (`minapi 26`). The project uses Java 17 and the current Buildozer GitHub Action workflow.

## Local validation

```bash
python3 -m compileall -q .
```

For Android:

```bash
buildozer -v android debug
```

The first Android build downloads the SDK/NDK toolchain and can take a while.
