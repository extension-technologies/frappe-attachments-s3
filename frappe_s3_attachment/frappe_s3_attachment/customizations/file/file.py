import frappe
import urllib.request
import tempfile
import shutil
from frappe import _
from PIL import ImageFile
from frappe.utils.file_manager import safe_b64decode
from frappe.core.doctype.file.file import File

exclude_from_linked_with = True
ImageFile.LOAD_TRUNCATED_IMAGES = True
URL_PREFIXES = ("http://", "https://")

def decode_file_content(content: bytes) -> bytes:
	if isinstance(content, str):
		content = content.encode("utf-8")
	if b"," in content:
		content = content.split(b",")[1]
	return safe_b64decode(content)

class customFile(File):
	def get_content(self) -> bytes:
		if self.is_folder:
			frappe.throw(_("Cannot get file contents of a Folder"))

		if self.get("content"):
			self._content = self.content
			if self.decode:
				self._content = decode_file_content(self._content)
				self.decode = False
			# self.content = None # TODO: This needs to happen; make it happen somehow
			return self._content

		if self.file_url:
			self.validate_file_url()
			tmp_file = None
			if(self.file_url.startswith(URL_PREFIXES)):
				with urllib.request.urlopen(self.file_url) as response:
					with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
						shutil.copyfileobj(response, tmp_file)
				tmp_file = tmp_file.name
		file_path = self.get_full_path()

		# read the file
		with open(tmp_file or file_path, mode="rb") as f:
			self._content = f.read()
			try:
				# for plain text files
				self._content = self._content.decode()
			except UnicodeDecodeError:
				# for .png, .jpg, etc
				pass

		return self._content