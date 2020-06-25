import re

class Config:
	def __init__(self, comment="#", reference="<>", equality="=:"):
		self.comment = comment
		self.reference = reference
		self.equality = equality

		self.references_ex = r"({}[^\>]*?{})".format(self.reference[0], self.reference[1])
		self.equality_ex = r"[{}]".format(self.equality)

	@staticmethod
	def replace(str1, str2, start, end):
		return str1[:start]+str2+str1[end:]

	def read_section(self, section):
		for item in section:
			if sum([item.count(x) for x in self.equality]) != 1:
				raise Exception("In {} can only have one equality symbol".format(item))
		section = [re.split(self.equality_ex, item) for item in section]
		section = {item[0].strip():item[1].strip() for item in section}

		loops = 0
		while any(re.search(self.references_ex, item) for item in section.values()):
			loops += 1
			if loops > len(section)+1:
				raise Exception("Recursion error")

			for key in section:
				match = re.search(self.references_ex, section[key])
				if match.group(0)[1:-1] in section.keys() if match else False:
					section[key] = self.replace(section[key], section[match.group(1)[1:-1]], match.span()[0], match.span()[1])
					if re.search(r"<{}>".format(key), section[key]):
						raise Exception("References cannot loop")

		for key in section:
			section[key] = eval(section[key])

		return section

	def read_config(self, file_name):
		with open(file_name) as config_file:
			data = [line.strip() for line in config_file]
			#remove lines that are only whitespace
			data = [line for line in data if not re.match(r"[^\S]+", line) and len(line) > 0] 
			#group all non comment lines into one string
			data = "\n"+"".join(line+"\n" for line in data if line[0] != self.comment)

		#find headers in the file (denoted by [header name])
		headers = [*re.finditer(r"\n+\[([^{}]+)\]\n".format(self.equality), data)] 
		
		raw = [header.group(1) for header in headers]
		if not all(raw.count(header.group(1)) == 1 for header in headers):
			raise Exception("All headers must be unique")
		del raw

		#isolate each section into it's own string
		sections = {header.group(1):data[header.span()[1]:len(data)-1 if n+1 == len(headers) else headers[n+1].span()[0]].split("\n") for n, header in enumerate(headers[:])}

		config = {}
		for header in sections:
			config[header] = self.read_section(sections[header])

		self.config = config

	def __getattr__(self, attr):
		return self[attr]

	def __getitem__(self, index):
		for subsection in self.config.values():
			print(subsection.keys())
		if index in self.config.keys():
			return self.config[index]
		elif sum((list(subsection.keys()) for subsection in self.config.values()), start=[]).count(index) == 1:
			return {key:subsection[key] for subsection in self.config.values() for key in subsection.keys()}[index]
		else:
			raise Exception("'{}' not found in config file".format(index))

	def __str__(self):
		return str(self.config)

	def keys(self):
		return self.config.keys()