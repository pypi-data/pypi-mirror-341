def Naprawa(code):
    """
    Automatycznie analizuje cały kod i naprawia błędy nawiasów.
    """
    try:
        # Próbujemy skompilować kod
        compile(code, "<string>", "exec")
        print("ErrFix | Kod poprawny, nie wymaga naprawy.")
    except SyntaxError as e:
        if "unexpected EOF while parsing" in e.msg:
            print("ErrFix | Wykryto niezakończony kod. Sprawdzam nawiasy...")
            # Liczymy nawiasy otwierające i zamykające
            count_open = code.count("(")
            count_close = code.count(")")
            if count_open > count_close:
                print("ErrFix | Dodaję brakujące nawiasy zamykające...")
                code += ")" * (count_open - count_close)  # Dodaj brakujące zamknięcia nawiasów
            elif count_close > count_open:
                print("ErrFix | Usuwam niepotrzebne nawiasy zamykające...")
                for _ in range(count_close - count_open):
                    # Usuń nadmiarowe zamykające nawiasy
                    code = code.replace(")", "", 1)
            print("ErrFix | Kod naprawiony.")
        else:
            print(f"ErrFix | Nieznany błąd: {e.msg}")
            print("ErrFix | Nie udało się naprawić tego błędu automatycznie.")
    except Exception as ex:
        print(f"ErrFix | Wystąpił błąd: {str(ex)}")
    return code



# Analiza - sprawdzanie kodu pod kątem błędów
def Analiza(code):
    """
    Analizuje kod linia po linii i wypisuje znalezione błędy.
    """
    lines = code.split("\n")
    for index, line in enumerate(lines, start=1):
        try:
            compile(line, "<string>", "exec")
            print(f"ErrFix | Linia {index}: Kod poprawny.")
        except SyntaxError as e:
            print(f"ErrFix | Linia {index}: Znaleziono błąd: {e.msg}")
    return


# OnOff - automatyczna kontrola uruchamiania kodu
def OnOff():
    """
    Automatyczna kontrola uruchamiania kodu:
    - Informuje o pomyślnym włączeniu.
    - Informuje o wyłączeniu programu z podaniem przyczyny.
    """
    try:
        # Symulacja włączenia kodu
        print("ErrFix | Włączono Kod Pomyślnie.")
        # Tu umieść logikę swojego programu, np. przetwarzanie kodu
        compile("print('Test')", "<string>", "exec")  # Przykład działania
    except Exception as e:
        print(f"ErrFix | Kod Wyłączony Pomyślnie Przez: Błąd ({str(e)})")
    else:
        print("ErrFix | Kod działa bez błędów.")
    finally:
        print("ErrFix | Proces zakończony.")
