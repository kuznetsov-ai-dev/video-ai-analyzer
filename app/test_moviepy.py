import sys
import os

print("🔍 PYTHON:", sys.executable)
print("🔍 sys.path:")
for p in sys.path:
    print("   ", p)

print("\n🔍 Проверка наличия moviepy:")
try:
    import moviepy
    print("✅ moviepy импортирован")
    print("📁 Путь:", moviepy.__file__)
except ImportError as e:
    print("❌", e)

print("\n🔍 Проверка наличия moviepy.editor:")
try:
    from moviepy import editor
    print("✅ editor импортирован")
except ImportError as e:
    print("❌", e)