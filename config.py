# Max filezie in bytes;
# *1000 = kb
# *1000 * 1000 = mb..
#
# * 10 ** 3 = kb
# * 10 ** 6 = mb
# * 10 ** 9 = gb
# * 10 ** 12 = tb

#Default is 2 gb, make sure to change
max_filesize_bytes = 2 * (10 ** 9)


# File saving path
# Must end in /
files_path = "./files/"

# Random filenames; sets a random filename when a file is uploaded
random_filenames = True

# Encrypt; Encrypts all files on disk and throws away the key.
# User get their key when they upload and must provide it when downloading
encrypt = True