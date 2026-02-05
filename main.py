import subprocess

def main():
    print("=== TwinLex 統一入口 ===")
    print("啟動 Streamlit 前端 ...")
    subprocess.run(["streamlit", "run", "src/ui/app.py"])

if __name__ == "__main__":
    main()