import argparse
import sqlite3
import os
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--encrypt", help="Encrypt the files", action="store_true")
parser.add_argument("-d", "--decrypt", help="Decrypt the files", action="store_true")
parser.add_argument("-f", "--file", help="Name of the file")
args = parser.parse_args()

class Main:
	def __init__(self):
		self.key = b'3Seh-ueR39DojWKAWjFDveOKXMsWpUrW9gTXA3A1VgU='
		self.conn = sqlite3.connect("db.sqlite3")
		self.cur = self.conn.cursor()
		table = """CREATE TABLE IF NOT EXISTS FILE(
			FileName VARCHAR,
			Content BLOB
		);"""
		self.cur.execute(table)
		self.conn.commit()
		if args.file:
			if args.decrypt:
				self.decrypt(args.file)
			elif args.encrypt:
				self.encrypt(args.file)
			else:
				print("Select an option to encrypt of decrypt")
		else:
			print("Enter file name by using -f or --file")

	def encrypt(self, file):
		with open(file, "rb") as f:
			content = f.read()
			f.close()
		enc = Fernet(self.key)
		encrypted_content = enc.encrypt(content)
		name = os.path.basename(file)
		insertQuery = """INSERT INTO FILE VALUES(?, ?)"""
		self.cur.execute(insertQuery, (name, encrypted_content))
		self.conn.commit()
		self.conn.close()
		os.remove(file)

	def decrypt(self, file):
		file = os.path.basename(file)
		self.cur.execute(f"SELECT * FROM FILE WHERE FileName LIKE '%{file}%'")
		_files = self.cur.fetchall()
		dec = Fernet(self.key)
		for _file in _files:
			decrypted_content = dec.decrypt(_file[1])
			with open(_file[0], "wb") as f:
				f.write(decrypted_content)
				f.close()

if __name__ == "__main__":
	Main()
