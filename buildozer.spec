[app]

title = StudyFlow
package.name = studyflow
package.domain = org.studyflow

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,txt,md

version = 1.1.0

requirements = python3,kivy==2.3.1,kivymd==2.0.0,materialyoucolor==3.0.3,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,android

orientation = portrait
fullscreen = 0

android.ndk = 25b
android.api = 34
android.minapi = 29
android.archs = arm64-v8a

android.allow_backup = True
android.private_storage = True
android.accept_sdk_license = True
android.java_version = 17


[buildozer]

log_level = 2
warn_on_root = 1
