import sqlite3
import os
from cryptography.fernet import Fernet

class Main:
	def __init__(self):
		super(self, Main).__init__()
		self.key = b'3Seh-ueR39DojWKAWjFDveOKXMsWpUrW9gTXA3A1VgU='
		self.conn = sqlite3.connect("db.sqlite3")
		self.cur = self.conn.cursor()
		self.insertQuery = """INSERT INTO FILE VALUES(?, ?)"""
		file_path = "/home/munseer/Music/Tuesday.mp3"
		file = os.path.basename(file_path)

	def encrypt(self, file):
		with open(file, "rb") as f:
			content = f.read()
			f.close()
		enc = Fernet(self.key)
		encrypted_content = enc.encrypt(enc)
		self.cur.execute(self.insertQuery, (file, encrypted_content))
		self.conn.commit()
		self.conn.close()
		os.remove(file)

if __name__ == "__main__":
	Main()
