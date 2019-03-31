HONORIFICS = [
	r"^mr\.?$",
	r"^mister$",
	r"^master$",
	r"^ms\.?$",
	r"^mz\.?$",
	r"^miss\.?$",
	r"^mrs\.?$",
	r"^mx\.?$",
	r"^sir$",
	r"^madam$",
	r"^ma'am$",
	r"^dame$",
	r"^lord$",
	r"^lady$",
	r"^esq\.?$",
	r"^esquire$",
	r"^adv\.?$",
	r"^advocate$",
	r"^dr\.?$",
	r"^doctor$",
	r"^prof\.?$",
	r"^professor$",
	r"^alderman$",
	r"^br\.?$",
	r"^brother$",
	r"^fr\.?$",
	r"^father$",
	r"^rev\.?$",
	r"^reverend$",
	r"^pr\.?$",
	r"^pastor$",
	r"^elder$",
	r"^rabbi$",
	r"^captain-general$",
	r"^sergeant-major-general$",
	r"^major-general$",
	r"^brigadier-general$",
	r"^colonel-commandant$",
	r"^colonel$",
	r"^col\.?$",
	r"^brigadier$",
	r"^sergeant-major'?s-major$",
	r"^major$",
	r"^captain$",
	r"^captain-lieutenant$",
	r"^ensign$",
	r"^second-lieutenant$",
	r"^cornet$",
	r"^lieutenant$",
	r"^lt\.?$"
]

TITLES = [
	r"^dean$",
	r"^chanter$",
	r"^duke$",
	r"^duchess$",	
	r"^marquess$",
	r"^marchioness$",
	r"^earl$",
	r"^countess$",
	r"^viscount$",
	r"^viscountess$",
	r"^baron$",
	r"^baroness$",
	r"^baronet$",
	r"^baronetess$",
	r"^knight$",
	r"^bishop$",
	r"^archdeacon$",
	r"^king$"
]

LOCATIONS = [
	r"(?i)of (st )?[^ ]+"
]

NORMALS = [
	(r"(of)([A-Z])", r"\1 \2"),
	(r"&", r"and"),
	(r"(Xpher)", r"Christopher"),
	(r"(Xpofer)", r"Christopher"),	
	(r"(Xopher)", r"Christopher"),
	(r"(Xtopher)", r"Christopher"),
	(r"(?i)(fitz) ([^ ]*)", r"\1\2"),
	(r"(?i)(captain) (general)", r"\1-\2"),
	(r"(?i)(major) (general)", r"\1-\2"),
	(r"(?i)(brigadier) (general)", r"\1-\2"),
	(r"(?i)(colonel) (commandant)", r"\1-\2"),
	(r"(?i)(sergeant) (major)", r"\1-\2"),	
	(r"(?i)(captain) (lieutenant)", r"\1-\2"),
	(r"(?i)(second) (lieutenant)", r"\1-\2"),
	(r"(?i)(sergeant-major) (major)", r"\1-\2"),
	(r"(?i)(sergeant-major'?s) (major)", r"\1-\2"),
]