from typing import Union, List
from pydal import DAL, Field


class Database:

    def __init__(self) -> None:
        # Ma'lumotlar bazasiga ulanish va jadvalni aniqlash
        self.db = DAL("sqlite://database.sqlite3")
        self.db.define_table(
            "config",
            Field("key", "string", unique=True),  # Konfiguratsiya kaliti
            Field("value", "string"),  # Konfiguratsiya qiymati
            migrate=True,
        )
        self.db.commit()  # O'zgarishlarni saqlash

    def get(self, table: str) -> List[dict]:
        """
        Berilgan jadvaldan barcha ma'lumotlarni qaytaradi.
        """
        if table not in self.db.tables:
            raise ValueError(f"Jadval '{table}' mavjud emas.")
        return self.db(table).select().as_list()

    def get_config(self, key: str, default: Union[str] = None) -> Union[str, None]:
        """
        Kalit bo‘yicha konfiguratsiya qiymatini qaytaradi.
        Agar kalit mavjud bo‘lmasa, `None` qaytadi.
        """
        record = self.db(self.db.config.key == key).select().first()
        return record.value if record else default

    def update_config(self, key: str, value: str) -> bool:
        """
        Kalit bo‘yicha qiymatni yangilaydi yoki qo‘shadi.
        Muvaffaqiyatli bajarilgan bo‘lsa, `True` qaytaradi.
        """
        try:
            existing = self.db(self.db.config.key == key).select().first()
            if existing:
                self.db(self.db.config.key == key).update(value=value)
            else:
                self.db.config.insert(key=key, value=value)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Xato yuz berdi: {e}")
            return False

    def delete_config(self, key: str) -> bool:
        """
        Kalit bo‘yicha yozuvni o‘chiradi.
        Muvaffaqiyatli bajarilgan bo‘lsa, `True` qaytaradi.
        """
        try:
            self.db(self.db.config.key == key).delete()
            self.db.commit()
            return True
        except Exception as e:
            print(f"Xato yuz berdi: {e}")
            return False

    def get_all_config(self) -> List[dict]:
        """
        Barcha konfiguratsiyalarni qaytaradi.
        """
        return self.db(self.db.config).select().as_list()

    def close(self) -> None:
        """
        Ma'lumotlar bazasi ulanishini yopadi.
        """
        self.db.close()

    def __del__(self) -> None:
        """
        Sinf yo'q qilinishida ulanishni yopadi.
        """
        self.close()

