[app]
# (str) Title of your application
 title = StudyFlow
# (str) Package name (ASCII only, one word)
 package.name = studyflow
# (str) Package domain; together with package.name forms the Android application ID
 package.domain = org.studyflow
# (str) Source directory
 source.dir = .
# (list) Valid file extensions to include in the APK
 source.include_exts = py,kv,png,jpg,jpeg,txt,md
# (str) Application version
 version = 1.1.0
# Current Buildozer guidance for modern Ubuntu runners.
 p4a.branch = develop
# (list) Python packages/recipes required by the app
 requirements = python3,kivy==2.3.1,kivymd==2.0.0,pillow,materialyoucolor==3.0.3,materialshapes,asynckivy,asyncgui,exceptiongroup,pycairo,android
# (str) Supported orientations
 orientation = portrait
# (bool) Fullscreen
 fullscreen = 0
# (str) Presplash image (optional)
# presplash.filename = %(source.dir)s/assets/presplash.png
# (str) Icon (optional)
# icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
# (int) Log level (0 = error only, 2 = normal, 3 = verbose)
 log_level = 2
# (bool) Warn when running as root
 warn_on_root = 1

[android]
# Target Android API. API 36 follows current Buildozer guidance for modern Android builds.
 android.api = 36
 android.ndk = 29
# Minimum Android API. Android 8.0+ is the intended supported baseline for the MVP.
 android.minapi = 26
# Build both common ARM ABIs for wider device compatibility.
 android.archs = arm64-v8a,armeabi-v7a
# Let Android back up app data when supported by the OS.
 android.allow_backup = True
# Keep app-private storage inside the app sandbox.
 android.private_storage = True
# Automatically accept the Android SDK licenses in CI.
 android.accept_sdk_license = True
# Keep Java target aligned with the current Buildozer Android toolchain recommendation.
 android.java_version = 17
# Do not request network/location/etc. permissions: the MVP is offline-first.
# android.permissions =

# Optional: keep the debug package clearly identifiable during local testing.
# android.debug_artifact = apk
