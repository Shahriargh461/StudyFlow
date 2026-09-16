[app]
title = StudyFlow
package.name = studyflow
package.domain = org.studyflow
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,txt,md
version = 1.1.0
requirements = python3,kivy==2.3.1,kivymd==2.0.0,pillow,materialyoucolor==3.0.3,materialshapes,asynckivy,asyncgui,exceptiongroup,android
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 34
android.ndk = 25b
android.minapi = 29
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.private_storage = True
android.accept_sdk_license = True
android.java_version = 17
