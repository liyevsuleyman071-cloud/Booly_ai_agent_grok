import os,webbrowser
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
if not os.path.exists("data"):
    os.makedirs("data")
root_dir = "C:/Booly_1/data"
@tool
def youtube_search(query: str):
    """YouTube-da axtarış linki yaradır."""
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        webbrowser.open(url,new=2)
        return f"Buyur, axtardığın '{query}' üçün YouTube linki: {url}\n"
    except Exception as e:
        return f"Xəta baş verdi: {str(e)}"
@tool
def read_local_file(file_name: str):
    """Məlumatları oxumaq üçün lokal faylı açır. Fayl adını daxil et."""
    path = os.path.join(root_dir, file_name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def write_to_local_file(file_name: str, content: str):
    """Məlumatları lokal fayla yazır və ya yeni fayl yaradır."""
    path = os.path.join(root_dir, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Fayl '{file_name}' uğurla yazıldı."

@tool
def list_my_files(query: str = ""):
    """Lokal qovluqdakı bütün faylların siyahısını göstərir."""
    return os.listdir(root_dir)

@tool
def get_current_time(query: str = ""):
    """Hazırkı saat və tarixi qaytarır."""
    import datetime
    return str(datetime.datetime.now())
@tool
def python_executor(code: str):
    """
    Python kodu icra etmək üçün bu alətdən istifadə et. 
    Mürəkkəb hesablamalar, data analizi və ya məntiqi tapşırıqlar üçün idealdır.
    Giriş yalnız təmiz Python kodu olmalıdır.
    """
    try:
        result = PythonREPL().run(code)
        return f"İcra nəticəsi:\n{result}"
    except Exception as e:
        return f"Kod icra edilərkən xəta baş verdi: {str(e)}"