import os
import subprocess
import base64
import shutil
import sys


repo_encoded = "aHR0cHM6Ly9naXRodWIuY29tL2FsaTQxNGE0NGFsaS9tYXRyaXg"

# يقرأ اسم الفرع من متغير البيئة BRANCH
# وإذا ما موجود يستخدم main
branch = os.getenv("BRANCH", "main")


def run(cmd):
    print(f"⌭ تنفيذ: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def decode_repo_url(encoded):
    try:
        clean_encoded = encoded.strip().replace(" ", "")
        clean_encoded += "=" * (-len(clean_encoded) % 4)
        return base64.b64decode(clean_encoded).decode("utf-8")
    except Exception as e:
        print("❌ فشل فك تشفير الرابط:", e)
        sys.exit(1)


def _run_git_clone():
    print("• جـاري تحميل سورس ماتركـس.....")
    print(f"⌭ سيتم استخدام الفرع: {branch}")

    repo_url = decode_repo_url(repo_encoded)

    if os.path.exists("source_temp"):
        print("⌭ حذف النسخة القديمة...")
        shutil.rmtree("source_temp")

    try:
        run(f"git clone -b {branch} --single-branch {repo_url} source_temp")
        os.chdir("source_temp")
    except subprocess.CalledProcessError:
        print("❌ فشل تحميل الفرع المحدد من GitHub")
        sys.exit(1)


def _install_requirements():
    print("⌭ تثبيت مكاتب ماتركـس ⌭")
    run("pip install -r requirements.txt")


def _start_project():
    print("⌭ البدء بتشغيل ماتركـس ⌭")

    server_process = subprocess.Popen(
        ["python3", "server.py"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    matrix_process = subprocess.Popen(
        ["python3", "-m", "Matrix"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )

    server_process.wait()
    matrix_process.wait()


if __name__ == "__main__":
    _run_git_clone()
    _install_requirements()
    _start_project()
