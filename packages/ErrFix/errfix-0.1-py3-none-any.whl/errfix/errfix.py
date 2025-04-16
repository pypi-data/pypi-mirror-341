import subprocess

def check_file_for_errors(file_path):
    """Sprawdza błędy składniowe w pliku Python."""
    try:
        result = subprocess.run(
            ["python", "-m", "py_compile", file_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            print("ErrFix | Znalezione Błędy:")
            print(result.stderr.strip())
        else:
            print("ErrFix | Uruchomiono Poprawnie")
    except Exception as e:
        print("ErrFix | Nie Udało Się Uruchomić")
        print(f"Błąd: {str(e)}")

def evaluate_code(code):
    """Ocena kodu w locie."""
    try:
        compile(code, "<string>", "exec")
        print("ErrFix | Uruchomiono Poprawnie")
    except SyntaxError as e:
        print("ErrFix | Znalezione Błędy:")
        print(f"Linia {e.lineno}: {e.msg}")
    except Exception as e:
        print("ErrFix | Nie Udało Się Uruchomić")
        print(f"Błąd: {str(e)}")