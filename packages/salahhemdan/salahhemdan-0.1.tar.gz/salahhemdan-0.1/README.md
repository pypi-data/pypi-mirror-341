# salahhemdan

مكتبة لتحميل وسائط إنستجرام باستخدام RapidAPI.

## التثبيت
```bash
pip install salahhemdan
```

## الاستخدام
```python
from salahhemdan import download_media

data = download_media("https://www.instagram.com/p/xxxxx/")
print(data)
```