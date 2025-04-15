r"""Wrapper for std.h

Generated with:
/home/rstudio/.local/bin/ctypesgen -DANSI -llibxux64.so std.h xu.h -o xux64.py

Do not modify this file.
"""

__docformat__ = "restructuredtext"

# Begin preamble for Python

import ctypes
import sys
from ctypes import *  # noqa: F401, F403
import numpy as np

def nptr(dtype=np.double,ndim=1, flags='CONTIGUOUS',p=np.ctypeslib.ndpointer):
	return p(dtype=dtype,ndim=ndim,flags=flags)

#convert numpy 2D-array:`m` of ctype:`t` to `**m` in C
def np2ct2(m,t=c_double): return (POINTER(t)*len(m))(*(np.ctypeslib.as_ctypes(j) for j in m))

#convert numpy 1D-array:`v`  to `*v` in C
def np2ct(v): return np.ctypeslib.as_ctypes(v)

#convert list 2D-array:`m` of ctype:`t` to `**m` in C
def v2ct2(m,t=c_double): return (POINTER(t)*len(m))(*((c_double*len(x))(*x) for x in m))

#convert list 1D-array:`v` of ctype `t`  to `*v` in C
def v2ct(s,t=c_double): return (t*len(s))(*s)

#convert list of string-array:`vs` of ctype `t`  to `**vs` in C
def vs2ct(vs,t=c_char_p): return (t*len(vs))(*(t(x.encode('utf-8')) for x in vs))

_int_types = (ctypes.c_int16, ctypes.c_int32)
if hasattr(ctypes, "c_int64"):
	# Some builds of ctypes apparently do not have ctypes.c_int64
	# defined; it's a pretty good bet that these builds do not
	# have 64-bit pointers.
	_int_types += (ctypes.c_int64,)
for t in _int_types:
	if ctypes.sizeof(t) == ctypes.sizeof(ctypes.c_size_t):
		c_ptrdiff_t = t
del t
del _int_types



class UserString:
	def __init__(self, seq):
		if isinstance(seq, bytes):
			self.data = seq
		elif isinstance(seq, UserString):
			self.data = seq.data[:]
		else:
			self.data = str(seq).encode()

	def __bytes__(self):
		return self.data

	def __str__(self):
		return self.data.decode()

	def __repr__(self):
		return repr(self.data)

	def __int__(self):
		return int(self.data.decode())

	def __long__(self):
		return int(self.data.decode())

	def __float__(self):
		return float(self.data.decode())

	def __complex__(self):
		return complex(self.data.decode())

	def __hash__(self):
		return hash(self.data)

	def __le__(self, string):
		if isinstance(string, UserString):
			return self.data <= string.data
		else:
			return self.data <= string

	def __lt__(self, string):
		if isinstance(string, UserString):
			return self.data < string.data
		else:
			return self.data < string

	def __ge__(self, string):
		if isinstance(string, UserString):
			return self.data >= string.data
		else:
			return self.data >= string

	def __gt__(self, string):
		if isinstance(string, UserString):
			return self.data > string.data
		else:
			return self.data > string

	def __eq__(self, string):
		if isinstance(string, UserString):
			return self.data == string.data
		else:
			return self.data == string

	def __ne__(self, string):
		if isinstance(string, UserString):
			return self.data != string.data
		else:
			return self.data != string

	def __contains__(self, char):
		return char in self.data

	def __len__(self):
		return len(self.data)

	def __getitem__(self, index):
		return self.__class__(self.data[index])

	def __getslice__(self, start, end):
		start = max(start, 0)
		end = max(end, 0)
		return self.__class__(self.data[start:end])

	def __add__(self, other):
		if isinstance(other, UserString):
			return self.__class__(self.data + other.data)
		elif isinstance(other, bytes):
			return self.__class__(self.data + other)
		else:
			return self.__class__(self.data + str(other).encode())

	def __radd__(self, other):
		if isinstance(other, bytes):
			return self.__class__(other + self.data)
		else:
			return self.__class__(str(other).encode() + self.data)

	def __mul__(self, n):
		return self.__class__(self.data * n)

	__rmul__ = __mul__

	def __mod__(self, args):
		return self.__class__(self.data % args)

	# the following methods are defined in alphabetical order:
	def capitalize(self):
		return self.__class__(self.data.capitalize())

	def center(self, width, *args):
		return self.__class__(self.data.center(width, *args))

	def count(self, sub, start=0, end=sys.maxsize):
		return self.data.count(sub, start, end)

	def decode(self, encoding=None, errors=None):  # XXX improve this?
		if encoding:
			if errors:
				return self.__class__(self.data.decode(encoding, errors))
			else:
				return self.__class__(self.data.decode(encoding))
		else:
			return self.__class__(self.data.decode())

	def encode(self, encoding=None, errors=None):  # XXX improve this?
		if encoding:
			if errors:
				return self.__class__(self.data.encode(encoding, errors))
			else:
				return self.__class__(self.data.encode(encoding))
		else:
			return self.__class__(self.data.encode())

	def endswith(self, suffix, start=0, end=sys.maxsize):
		return self.data.endswith(suffix, start, end)

	def expandtabs(self, tabsize=8):
		return self.__class__(self.data.expandtabs(tabsize))

	def find(self, sub, start=0, end=sys.maxsize):
		return self.data.find(sub, start, end)

	def index(self, sub, start=0, end=sys.maxsize):
		return self.data.index(sub, start, end)

	def isalpha(self):
		return self.data.isalpha()

	def isalnum(self):
		return self.data.isalnum()

	def isdecimal(self):
		return self.data.isdecimal()

	def isdigit(self):
		return self.data.isdigit()

	def islower(self):
		return self.data.islower()

	def isnumeric(self):
		return self.data.isnumeric()

	def isspace(self):
		return self.data.isspace()

	def istitle(self):
		return self.data.istitle()

	def isupper(self):
		return self.data.isupper()

	def join(self, seq):
		return self.data.join(seq)

	def ljust(self, width, *args):
		return self.__class__(self.data.ljust(width, *args))

	def lower(self):
		return self.__class__(self.data.lower())

	def lstrip(self, chars=None):
		return self.__class__(self.data.lstrip(chars))

	def partition(self, sep):
		return self.data.partition(sep)

	def replace(self, old, new, maxsplit=-1):
		return self.__class__(self.data.replace(old, new, maxsplit))

	def rfind(self, sub, start=0, end=sys.maxsize):
		return self.data.rfind(sub, start, end)

	def rindex(self, sub, start=0, end=sys.maxsize):
		return self.data.rindex(sub, start, end)

	def rjust(self, width, *args):
		return self.__class__(self.data.rjust(width, *args))

	def rpartition(self, sep):
		return self.data.rpartition(sep)

	def rstrip(self, chars=None):
		return self.__class__(self.data.rstrip(chars))

	def split(self, sep=None, maxsplit=-1):
		return self.data.split(sep, maxsplit)

	def rsplit(self, sep=None, maxsplit=-1):
		return self.data.rsplit(sep, maxsplit)

	def splitlines(self, keepends=0):
		return self.data.splitlines(keepends)

	def startswith(self, prefix, start=0, end=sys.maxsize):
		return self.data.startswith(prefix, start, end)

	def strip(self, chars=None):
		return self.__class__(self.data.strip(chars))

	def swapcase(self):
		return self.__class__(self.data.swapcase())

	def title(self):
		return self.__class__(self.data.title())

	def translate(self, *args):
		return self.__class__(self.data.translate(*args))

	def upper(self):
		return self.__class__(self.data.upper())

	def zfill(self, width):
		return self.__class__(self.data.zfill(width))


class MutableString(UserString):
	"""mutable string objects

	Python strings are immutable objects.  This has the advantage, that
	strings may be used as dictionary keys.  If this property isn't needed
	and you insist on changing string values in place instead, you may cheat
	and use MutableString.

	But the purpose of this class is an educational one: to prevent
	people from inventing their own mutable string class derived
	from UserString and than forget thereby to remove (override) the
	__hash__ method inherited from UserString.  This would lead to
	errors that would be very hard to track down.

	A faster and better solution is to rewrite your program using lists."""

	def __init__(self, string=""):
		self.data = string

	def __hash__(self):
		raise TypeError("unhashable type (it is mutable)")

	def __setitem__(self, index, sub):
		if index < 0:
			index += len(self.data)
		if index < 0 or index >= len(self.data):
			raise IndexError
		self.data = self.data[:index] + sub + self.data[index + 1 :]

	def __delitem__(self, index):
		if index < 0:
			index += len(self.data)
		if index < 0 or index >= len(self.data):
			raise IndexError
		self.data = self.data[:index] + self.data[index + 1 :]

	def __setslice__(self, start, end, sub):
		start = max(start, 0)
		end = max(end, 0)
		if isinstance(sub, UserString):
			self.data = self.data[:start] + sub.data + self.data[end:]
		elif isinstance(sub, bytes):
			self.data = self.data[:start] + sub + self.data[end:]
		else:
			self.data = self.data[:start] + str(sub).encode() + self.data[end:]

	def __delslice__(self, start, end):
		start = max(start, 0)
		end = max(end, 0)
		self.data = self.data[:start] + self.data[end:]

	def immutable(self):
		return UserString(self.data)

	def __iadd__(self, other):
		if isinstance(other, UserString):
			self.data += other.data
		elif isinstance(other, bytes):
			self.data += other
		else:
			self.data += str(other).encode()
		return self

	def __imul__(self, n):
		self.data *= n
		return self


class String(MutableString, ctypes.Union):

	_fields_ = [("raw", ctypes.POINTER(ctypes.c_char)), ("data", ctypes.c_char_p)]

	def __init__(self, obj=b""):
		if isinstance(obj, (bytes, UserString)):
			self.data = bytes(obj)
		else:
			self.raw = obj

	def __len__(self):
		return self.data and len(self.data) or 0

	def from_param(cls, obj):
		# Convert None or 0
		if obj is None or obj == 0:
			return cls(ctypes.POINTER(ctypes.c_char)())

		# Convert from String
		elif isinstance(obj, String):
			return obj

		# Convert from bytes
		elif isinstance(obj, bytes):
			return cls(obj)

		# Convert from str
		elif isinstance(obj, str):
			return cls(obj.encode())

		# Convert from c_char_p
		elif isinstance(obj, ctypes.c_char_p):
			return obj

		# Convert from POINTER(ctypes.c_char)
		elif isinstance(obj, ctypes.POINTER(ctypes.c_char)):
			return obj

		# Convert from raw pointer
		elif isinstance(obj, int):
			return cls(ctypes.cast(obj, ctypes.POINTER(ctypes.c_char)))

		# Convert from ctypes.c_char array
		elif isinstance(obj, ctypes.c_char * len(obj)):
			return obj

		# Convert from object
		else:
			return String.from_param(obj._as_parameter_)

	from_param = classmethod(from_param)


def ReturnString(obj, func=None, arguments=None):
	return String.from_param(obj)


# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to ctypes.c_void_p.
def UNCHECKED(type):
	if hasattr(type, "_type_") and isinstance(type._type_, str) and type._type_ != "P":
		return type
	else:
		return ctypes.c_void_p


# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
	def __init__(self, func, restype, argtypes, errcheck):
		self.func = func
		self.func.restype = restype
		self.argtypes = argtypes
		if errcheck:
			self.func.errcheck = errcheck

	def _as_parameter_(self):
		# So we can pass this variadic function as a function pointer
		return self.func

	def __call__(self, *args):
		fixed_args = []
		i = 0
		for argtype in self.argtypes:
			# Typecheck what we can
			fixed_args.append(argtype.from_param(args[i]))
			i += 1
		return self.func(*fixed_args + list(args[i:]))


def ord_if_char(value):
	"""
	Simple helper used for casts to simple builtin types:  if the argument is a
	string type, it will be converted to it's ordinal value.

	This function will raise an exception if the argument is string with more
	than one characters.
	"""
	return ord(value) if (isinstance(value, bytes) or isinstance(value, str)) else value

# End preamble

_libs = {}
_libdirs = []

# Begin loader

"""
Load libraries - appropriately for all our supported platforms
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#	notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#	notice, this list of conditions and the following disclaimer in
#	the documentation and/or other materials provided with the
#	distribution.
#  * Neither the name of pyglet nor the names of its
#	contributors may be used to endorse or promote products
#	derived from this software without specific prior written
#	permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import ctypes
import ctypes.util
import glob
import os.path
import platform
import re
import sys


def _environ_path(name):
	"""Split an environment variable into a path-like list elements"""
	if name in os.environ:
		return os.environ[name].split(":")
	return []


class LibraryLoader:
	"""
	A base class For loading of libraries ;-)
	Subclasses load libraries for specific platforms.
	"""

	# library names formatted specifically for platforms
	name_formats = ["%s"]

	class Lookup:
		"""Looking up calling conventions for a platform"""

		mode = ctypes.DEFAULT_MODE

		def __init__(self, path):
			super(LibraryLoader.Lookup, self).__init__()
			self.access = dict(cdecl=ctypes.CDLL(path, self.mode))

		def get(self, name, calling_convention="cdecl"):
			"""Return the given name according to the selected calling convention"""
			if calling_convention not in self.access:
				raise LookupError(
					"Unknown calling convention '{}' for function '{}'".format(
						calling_convention, name
					)
				)
			return getattr(self.access[calling_convention], name)

		def has(self, name, calling_convention="cdecl"):
			"""Return True if this given calling convention finds the given 'name'"""
			if calling_convention not in self.access:
				return False
			return hasattr(self.access[calling_convention], name)

		def __getattr__(self, name):
			return getattr(self.access["cdecl"], name)

	def __init__(self):
		self.other_dirs = []

	def __call__(self, libname):
		"""Given the name of a library, load it."""
		paths = self.getpaths(libname)

		for path in paths:
			# noinspection PyBroadException
			try:
				return self.Lookup(path)
			except Exception:  # pylint: disable=broad-except
				pass

		raise ImportError("Could not load %s." % libname)

	def getpaths(self, libname):
		"""Return a list of paths where the library might be found."""
		if os.path.isabs(libname):
			yield libname
		else:
			# search through a prioritized series of locations for the library

			# we first search any specific directories identified by user
			for dir_i in self.other_dirs:
				for fmt in self.name_formats:
					# dir_i should be absolute already
					yield os.path.join(dir_i, fmt % libname)

			# check if this code is even stored in a physical file
			try:
				this_file = __file__
			except NameError:
				this_file = None

			# then we search the directory where the generated python interface is stored
			if this_file is not None:
				for fmt in self.name_formats:
					yield os.path.abspath(os.path.join(os.path.dirname(__file__), fmt % libname))

			# now, use the ctypes tools to try to find the library
			for fmt in self.name_formats:
				path = ctypes.util.find_library(fmt % libname)
				if path:
					yield path

			# then we search all paths identified as platform-specific lib paths
			for path in self.getplatformpaths(libname):
				yield path

			# Finally, we'll try the users current working directory
			for fmt in self.name_formats:
				yield os.path.abspath(os.path.join(os.path.curdir, fmt % libname))

	def getplatformpaths(self, _libname):  # pylint: disable=no-self-use
		"""Return all the library paths available in this platform"""
		return []


# Darwin (Mac OS X)


class DarwinLibraryLoader(LibraryLoader):
	"""Library loader for MacOS"""

	name_formats = [
		"lib%s.dylib",
		"lib%s.so",
		"lib%s.bundle",
		"%s.dylib",
		"%s.so",
		"%s.bundle",
		"%s",
	]

	class Lookup(LibraryLoader.Lookup):
		"""
		Looking up library files for this platform (Darwin aka MacOS)
		"""

		# Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
		# of the default RTLD_LOCAL.  Without this, you end up with
		# libraries not being loadable, resulting in "Symbol not found"
		# errors
		mode = ctypes.RTLD_GLOBAL

	def getplatformpaths(self, libname):
		if os.path.pathsep in libname:
			names = [libname]
		else:
			names = [fmt % libname for fmt in self.name_formats]

		for directory in self.getdirs(libname):
			for name in names:
				yield os.path.join(directory, name)

	@staticmethod
	def getdirs(libname):
		"""Implements the dylib search as specified in Apple documentation:

		http://developer.apple.com/documentation/DeveloperTools/Conceptual/
			DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

		Before commencing the standard search, the method first checks
		the bundle's ``Frameworks`` directory if the application is running
		within a bundle (OS X .app).
		"""

		dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
		if not dyld_fallback_library_path:
			dyld_fallback_library_path = [
				os.path.expanduser("~/lib"),
				"/usr/local/lib",
				"/usr/lib",
			]

		dirs = []

		if "/" in libname:
			dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
		else:
			dirs.extend(_environ_path("LD_LIBRARY_PATH"))
			dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
			dirs.extend(_environ_path("LD_RUN_PATH"))

		if hasattr(sys, "frozen") and getattr(sys, "frozen") == "macosx_app":
			dirs.append(os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks"))

		dirs.extend(dyld_fallback_library_path)

		return dirs


# Posix


class PosixLibraryLoader(LibraryLoader):
	"""Library loader for POSIX-like systems (including Linux)"""

	_ld_so_cache = None

	_include = re.compile(r"^\s*include\s+(?P<pattern>.*)")

	name_formats = ["lib%s.so", "%s.so", "%s"]

	class _Directories(dict):
		"""Deal with directories"""

		def __init__(self):
			dict.__init__(self)
			self.order = 0

		def add(self, directory):
			"""Add a directory to our current set of directories"""
			if len(directory) > 1:
				directory = directory.rstrip(os.path.sep)
			# only adds and updates order if exists and not already in set
			if not os.path.exists(directory):
				return
			order = self.setdefault(directory, self.order)
			if order == self.order:
				self.order += 1

		def extend(self, directories):
			"""Add a list of directories to our set"""
			for a_dir in directories:
				self.add(a_dir)

		def ordered(self):
			"""Sort the list of directories"""
			return (i[0] for i in sorted(self.items(), key=lambda d: d[1]))

	def _get_ld_so_conf_dirs(self, conf, dirs):
		"""
		Recursive function to help parse all ld.so.conf files, including proper
		handling of the `include` directive.
		"""

		try:
			with open(conf) as fileobj:
				for dirname in fileobj:
					dirname = dirname.strip()
					if not dirname:
						continue

					match = self._include.match(dirname)
					if not match:
						dirs.add(dirname)
					else:
						for dir2 in glob.glob(match.group("pattern")):
							self._get_ld_so_conf_dirs(dir2, dirs)
		except IOError:
			pass

	def _create_ld_so_cache(self):
		# Recreate search path followed by ld.so.  This is going to be
		# slow to build, and incorrect (ld.so uses ld.so.cache, which may
		# not be up-to-date).  Used only as fallback for distros without
		# /sbin/ldconfig.
		#
		# We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

		directories = self._Directories()
		for name in (
			"LD_LIBRARY_PATH",
			"SHLIB_PATH",  # HP-UX
			"LIBPATH",  # OS/2, AIX
			"LIBRARY_PATH",  # BE/OS
		):
			if name in os.environ:
				directories.extend(os.environ[name].split(os.pathsep))

		self._get_ld_so_conf_dirs("/etc/ld.so.conf", directories)

		bitage = platform.architecture()[0]

		unix_lib_dirs_list = []
		if bitage.startswith("64"):
			# prefer 64 bit if that is our arch
			unix_lib_dirs_list += ["/lib64", "/usr/lib64"]

		# must include standard libs, since those paths are also used by 64 bit
		# installs
		unix_lib_dirs_list += ["/lib", "/usr/lib"]
		if sys.platform.startswith("linux"):
			# Try and support multiarch work in Ubuntu
			# https://wiki.ubuntu.com/MultiarchSpec
			if bitage.startswith("32"):
				# Assume Intel/AMD x86 compat
				unix_lib_dirs_list += ["/lib/i386-linux-gnu", "/usr/lib/i386-linux-gnu"]
			elif bitage.startswith("64"):
				# Assume Intel/AMD x86 compatible
				unix_lib_dirs_list += [
					"/lib/x86_64-linux-gnu",
					"/usr/lib/x86_64-linux-gnu",
				]
			else:
				# guess...
				unix_lib_dirs_list += glob.glob("/lib/*linux-gnu")
		directories.extend(unix_lib_dirs_list)

		cache = {}
		lib_re = re.compile(r"lib(.*)\.s[ol]")
		# ext_re = re.compile(r"\.s[ol]$")
		for our_dir in directories.ordered():
			try:
				for path in glob.glob("%s/*.s[ol]*" % our_dir):
					file = os.path.basename(path)

					# Index by filename
					cache_i = cache.setdefault(file, set())
					cache_i.add(path)

					# Index by library name
					match = lib_re.match(file)
					if match:
						library = match.group(1)
						cache_i = cache.setdefault(library, set())
						cache_i.add(path)
			except OSError:
				pass

		self._ld_so_cache = cache

	def getplatformpaths(self, libname):
		if self._ld_so_cache is None:
			self._create_ld_so_cache()

		result = self._ld_so_cache.get(libname, set())
		for i in result:
			# we iterate through all found paths for library, since we may have
			# actually found multiple architectures or other library types that
			# may not load
			yield i


# Windows


class WindowsLibraryLoader(LibraryLoader):
	"""Library loader for Microsoft Windows"""

	name_formats = ["%s.dll", "lib%s.dll", "%slib.dll", "%s"]

	class Lookup(LibraryLoader.Lookup):
		"""Lookup class for Windows libraries..."""

		def __init__(self, path):
			super(WindowsLibraryLoader.Lookup, self).__init__(path)
			self.access["stdcall"] = ctypes.windll.LoadLibrary(path)


# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
	"darwin": DarwinLibraryLoader,
	"cygwin": WindowsLibraryLoader,
	"win32": WindowsLibraryLoader,
	"msys": WindowsLibraryLoader,
}

load_library = loaderclass.get(sys.platform, PosixLibraryLoader)()


def add_library_search_dirs(other_dirs):
	"""
	Add libraries to search paths.
	If library paths are relative, convert them to absolute with respect to this
	file's directory
	"""
	for path in other_dirs:
		if not os.path.isabs(path):
			path = os.path.abspath(path)
		load_library.other_dirs.append(path)


del loaderclass

# End loader

add_library_search_dirs(["/apps/fafa/pyx/anPy/afa/"])

# Begin libraries
_libs["libxux64.so"] = load_library("libxux64.so")

# 1 libraries
# End libraries

# No modules

__off_t = c_long# /usr/include/x86_64-linux-gnu/bits/types.h: 152

__off64_t = c_long# /usr/include/x86_64-linux-gnu/bits/types.h: 153

# /usr/include/x86_64-linux-gnu/bits/types/__sigset_t.h: 8
class struct_anon_6(Structure):
	pass

struct_anon_6.__slots__ = [
	'__val',
]
struct_anon_6._fields_ = [
	('__val', c_ulong * int((1024 / (8 * sizeof(c_ulong))))),
]

__sigset_t = struct_anon_6# /usr/include/x86_64-linux-gnu/bits/types/__sigset_t.h: 8

# /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h: 49
class struct__IO_FILE(Structure):
	pass

FILE = struct__IO_FILE# /usr/include/x86_64-linux-gnu/bits/types/FILE.h: 7

# /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h: 36
class struct__IO_marker(Structure):
	pass

# /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h: 37
class struct__IO_codecvt(Structure):
	pass

# /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h: 38
class struct__IO_wide_data(Structure):
	pass

_IO_lock_t = None# /usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h: 43

struct__IO_FILE.__slots__ = [
	'_flags',
	'_IO_read_ptr',
	'_IO_read_end',
	'_IO_read_base',
	'_IO_write_base',
	'_IO_write_ptr',
	'_IO_write_end',
	'_IO_buf_base',
	'_IO_buf_end',
	'_IO_save_base',
	'_IO_backup_base',
	'_IO_save_end',
	'_markers',
	'_chain',
	'_fileno',
	'_flags2',
	'_old_offset',
	'_cur_column',
	'_vtable_offset',
	'_shortbuf',
	'_lock',
	'_offset',
	'_codecvt',
	'_wide_data',
	'_freeres_list',
	'_freeres_buf',
	'__pad5',
	'_mode',
	'_unused2',
]
struct__IO_FILE._fields_ = [
	('_flags', c_int),
	('_IO_read_ptr', String),
	('_IO_read_end', String),
	('_IO_read_base', String),
	('_IO_write_base', String),
	('_IO_write_ptr', String),
	('_IO_write_end', String),
	('_IO_buf_base', String),
	('_IO_buf_end', String),
	('_IO_save_base', String),
	('_IO_backup_base', String),
	('_IO_save_end', String),
	('_markers', POINTER(struct__IO_marker)),
	('_chain', POINTER(struct__IO_FILE)),
	('_fileno', c_int),
	('_flags2', c_int),
	('_old_offset', __off_t),
	('_cur_column', c_ushort),
	('_vtable_offset', c_char),
	('_shortbuf', c_char * int(1)),
	('_lock', POINTER(_IO_lock_t)),
	('_offset', __off64_t),
	('_codecvt', POINTER(struct__IO_codecvt)),
	('_wide_data', POINTER(struct__IO_wide_data)),
	('_freeres_list', POINTER(struct__IO_FILE)),
	('_freeres_buf', POINTER(None)),
	('__pad5', c_size_t),
	('_mode', c_int),
	('_unused2', c_char * int((((15 * sizeof(c_int)) - (4 * sizeof(POINTER(None)))) - sizeof(c_size_t)))),
]

# /usr/include/stdio.h: 326
if _libs["libxux64.so"].has("fprintf", "cdecl"):
	_func = _libs["libxux64.so"].get("fprintf", "cdecl")
	_restype = c_int
	_errcheck = None
	_argtypes = [POINTER(FILE), String]
	fprintf = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /usr/include/x86_64-linux-gnu/bits/mathcalls.h: 95
for _lib in _libs.values():
	if not _lib.has("exp", "cdecl"):
		continue
	exp = _lib.get("exp", "cdecl")
	exp.argtypes = [c_double]
	exp.restype = c_double
	break

# /usr/include/x86_64-linux-gnu/bits/mathcalls.h: 104
for _lib in _libs.values():
	if not _lib.has("log", "cdecl"):
		continue
	log = _lib.get("log", "cdecl")
	log.argtypes = [c_double]
	log.restype = c_double
	break

# /usr/include/x86_64-linux-gnu/bits/mathcalls.h: 140
for _lib in _libs.values():
	if not _lib.has("pow", "cdecl"):
		continue
	pow = _lib.get("pow", "cdecl")
	pow.argtypes = [c_double, c_double]
	pow.restype = c_double
	break

# /usr/include/x86_64-linux-gnu/bits/mathcalls.h: 162
for _lib in _libs.values():
	if not _lib.has("fabs", "cdecl"):
		continue
	fabs = _lib.get("fabs", "cdecl")
	fabs.argtypes = [c_double]
	fabs.restype = c_double
	break

# /usr/include/x86_64-linux-gnu/bits/mathcalls.h: 165
for _lib in _libs.values():
	if not _lib.has("floor", "cdecl"):
		continue
	floor = _lib.get("floor", "cdecl")
	floor.argtypes = [c_double]
	floor.restype = c_double
	break

__jmp_buf = c_long * int(8)# /usr/include/x86_64-linux-gnu/bits/setjmp.h: 31

# /usr/include/setjmp.h: 33
class struct___jmp_buf_tag(Structure):
	pass

struct___jmp_buf_tag.__slots__ = [
	'__jmpbuf',
	'__mask_was_saved',
	'__saved_mask',
]
struct___jmp_buf_tag._fields_ = [
	('__jmpbuf', __jmp_buf),
	('__mask_was_saved', c_int),
	('__saved_mask', __sigset_t),
]

jmp_buf = struct___jmp_buf_tag * int(1)# /usr/include/setjmp.h: 45

# /apps/fafa/pyx/anPy/afa/std.h: 35
try:
	prog = (String).in_dll(_libs["libxux64.so"], "prog")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 36
try:
	_GSTR = (String).in_dll(_libs["libxux64.so"], "_GSTR")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 37
try:
	_DBHOST = (String).in_dll(_libs["libxux64.so"], "_DBHOST")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 38
try:
	Fout = (POINTER(FILE)).in_dll(_libs["libxux64.so"], "Fout")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 39
try:
	Ferr = (POINTER(FILE)).in_dll(_libs["libxux64.so"], "Ferr")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 40
for _lib in _libs.values():
	try:
		FAFA_HOME = (String).in_dll(_lib, "FAFA_HOME")
		break
	except:
		pass

# /apps/fafa/pyx/anPy/afa/std.h: 41
for _lib in _libs.values():
	try:
		ZXY_DIR = (String).in_dll(_lib, "ZXY_DIR")
		break
	except:
		pass

# /apps/fafa/pyx/anPy/afa/std.h: 42
try:
	_xprfcn = (POINTER(CFUNCTYPE(UNCHECKED(c_int), ))).in_dll(_libs["libxux64.so"], "_xprfcn")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 43
try:
	xprintf = (POINTER(CFUNCTYPE(UNCHECKED(c_int), ))).in_dll(_libs["libxux64.so"], "xprintf")
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 44
try:
	Jumper = (jmp_buf).in_dll(_libs["libxux64.so"], "Jumper")
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 96
if _libs["libxux64.so"].has("commFctD", "cdecl"):
	commFctD = _libs["libxux64.so"].get("commFctD", "cdecl")
	commFctD.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(c_double)), POINTER(c_double)]
	commFctD.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 97
if _libs["libxux64.so"].has("extDbl", "cdecl"):
	extDbl = _libs["libxux64.so"].get("extDbl", "cdecl")
	extDbl.argtypes = [c_int, c_int, POINTER(POINTER(c_double)), c_double, c_int]
	extDbl.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 98
if _libs["libxux64.so"].has("alcDbl", "cdecl"):
	alcDbl = _libs["libxux64.so"].get("alcDbl", "cdecl")
	alcDbl.argtypes = [c_int, POINTER(POINTER(c_double))]
	alcDbl.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 99
if _libs["libxux64.so"].has("_alloc", "cdecl"):
	_alloc = _libs["libxux64.so"].get("_alloc", "cdecl")
	_alloc.argtypes = [String, c_size_t, POINTER(c_size_t), c_size_t]
	_alloc.restype = POINTER(c_ubyte)
	_alloc.errcheck = lambda v,*a : cast(v, c_void_p)

# /apps/fafa/pyx/anPy/afa/xu.h: 100
if _libs["libxux64.so"].has("_cfree", "cdecl"):
	_cfree = _libs["libxux64.so"].get("_cfree", "cdecl")
	_cfree.argtypes = [POINTER(POINTER(None))]
	_cfree.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 101
if _libs["libxux64.so"].has("alloc_vec", "cdecl"):
	alloc_vec = _libs["libxux64.so"].get("alloc_vec", "cdecl")
	alloc_vec.argtypes = [c_int, POINTER(c_double), POINTER(c_int)]
	alloc_vec.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 102
if _libs["libxux64.so"].has("_firr_csp", "cdecl"):
	_firr_csp = _libs["libxux64.so"].get("_firr_csp", "cdecl")
	_firr_csp.argtypes = [c_double, POINTER(c_double), c_int, POINTER(c_double), c_double, c_double, POINTER(c_double)]
	_firr_csp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 104
if _libs["libxux64.so"].has("_fnpv_csp", "cdecl"):
	_fnpv_csp = _libs["libxux64.so"].get("_fnpv_csp", "cdecl")
	_fnpv_csp.argtypes = [c_double, POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double)]
	_fnpv_csp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 105
if _libs["libxux64.so"].has("_fnfv_csp", "cdecl"):
	_fnfv_csp = _libs["libxux64.so"].get("_fnfv_csp", "cdecl")
	_fnfv_csp.argtypes = [c_double, POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double)]
	_fnfv_csp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 106
if _libs["libxux64.so"].has("_firr_sp_1", "cdecl"):
	_firr_sp_1 = _libs["libxux64.so"].get("_firr_sp_1", "cdecl")
	_firr_sp_1.argtypes = [c_double, c_double, POINTER(c_double), c_int, c_double, c_double, c_double, POINTER(c_double)]
	_firr_sp_1.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 108
if _libs["libxux64.so"].has("_fnpv_sp_1", "cdecl"):
	_fnpv_sp_1 = _libs["libxux64.so"].get("_fnpv_sp_1", "cdecl")
	_fnpv_sp_1.argtypes = [c_double, c_double, POINTER(c_double), c_int, c_double, POINTER(c_double)]
	_fnpv_sp_1.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 109
if _libs["libxux64.so"].has("_fnfv_sp_1", "cdecl"):
	_fnfv_sp_1 = _libs["libxux64.so"].get("_fnfv_sp_1", "cdecl")
	_fnfv_sp_1.argtypes = [c_double, c_double, POINTER(c_double), c_int, c_double, POINTER(c_double)]
	_fnfv_sp_1.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 110
if _libs["libxux64.so"].has("_fttr_sp_1", "cdecl"):
	_fttr_sp_1 = _libs["libxux64.so"].get("_fttr_sp_1", "cdecl")
	_fttr_sp_1.argtypes = [c_double, c_double, POINTER(c_double), c_int, c_double, c_double, c_double, c_double, POINTER(c_double)]
	_fttr_sp_1.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 112
if _libs["libxux64.so"].has("_firr_sp", "cdecl"):
	_firr_sp = _libs["libxux64.so"].get("_firr_sp", "cdecl")
	_firr_sp.argtypes = [c_double, POINTER(c_double), c_int, c_double, c_double, c_double, POINTER(c_double)]
	_firr_sp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 114
if _libs["libxux64.so"].has("_fnpv_sp", "cdecl"):
	_fnpv_sp = _libs["libxux64.so"].get("_fnpv_sp", "cdecl")
	_fnpv_sp.argtypes = [c_double, POINTER(c_double), c_int, c_double, POINTER(c_double)]
	_fnpv_sp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 115
if _libs["libxux64.so"].has("_fnfv_sp", "cdecl"):
	_fnfv_sp = _libs["libxux64.so"].get("_fnfv_sp", "cdecl")
	_fnfv_sp.argtypes = [c_double, POINTER(c_double), c_int, c_double, POINTER(c_double)]
	_fnfv_sp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 116
if _libs["libxux64.so"].has("_fttr_sp", "cdecl"):
	_fttr_sp = _libs["libxux64.so"].get("_fttr_sp", "cdecl")
	_fttr_sp.argtypes = [c_double, POINTER(c_double), c_int, c_double, c_double, c_double, c_double, POINTER(c_double)]
	_fttr_sp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 118
if _libs["libxux64.so"].has("_firr", "cdecl"):
	_firr = _libs["libxux64.so"].get("_firr", "cdecl")
	_firr.argtypes = [c_double, POINTER(c_double), c_int, c_double, c_double, c_double, c_double]
	_firr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 119
if _libs["libxux64.so"].has("_irr", "cdecl"):
	_irr = _libs["libxux64.so"].get("_irr", "cdecl")
	_irr.argtypes = [c_double, POINTER(c_double), c_int, c_double]
	_irr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 120
if _libs["libxux64.so"].has("_fnpv", "cdecl"):
	_fnpv = _libs["libxux64.so"].get("_fnpv", "cdecl")
	_fnpv.argtypes = [c_double, POINTER(c_double), c_int, c_double, c_double]
	_fnpv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 121
if _libs["libxux64.so"].has("_npv", "cdecl"):
	_npv = _libs["libxux64.so"].get("_npv", "cdecl")
	_npv.argtypes = [c_double, POINTER(c_double), c_int]
	_npv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 122
if _libs["libxux64.so"].has("_fnfv", "cdecl"):
	_fnfv = _libs["libxux64.so"].get("_fnfv", "cdecl")
	_fnfv.argtypes = [c_double, POINTER(c_double), c_int, c_double]
	_fnfv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 123
if _libs["libxux64.so"].has("_nfv", "cdecl"):
	_nfv = _libs["libxux64.so"].get("_nfv", "cdecl")
	_nfv.argtypes = [c_double, POINTER(c_double), c_int]
	_nfv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 124
if _libs["libxux64.so"].has("_shell_sort", "cdecl"):
	_shell_sort = _libs["libxux64.so"].get("_shell_sort", "cdecl")
	_shell_sort.argtypes = [POINTER(c_double), POINTER(c_int), c_int]
	_shell_sort.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 125
if _libs["libxux64.so"].has("_yes_no", "cdecl"):
	_yes_no = _libs["libxux64.so"].get("_yes_no", "cdecl")
	_yes_no.argtypes = [POINTER(FILE)]
	_yes_no.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 126
if _libs["libxux64.so"].has("_factorial", "cdecl"):
	_factorial = _libs["libxux64.so"].get("_factorial", "cdecl")
	_factorial.argtypes = [c_int]
	_factorial.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 127
if _libs["libxux64.so"].has("_dvec_transform", "cdecl"):
	_dvec_transform = _libs["libxux64.so"].get("_dvec_transform", "cdecl")
	_dvec_transform.argtypes = [c_int, POINTER(c_double), c_double, c_double, POINTER(c_double)]
	_dvec_transform.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 128
if _libs["libxux64.so"].has("_dvec_copy", "cdecl"):
	_dvec_copy = _libs["libxux64.so"].get("_dvec_copy", "cdecl")
	_dvec_copy.argtypes = [c_int, POINTER(c_double), POINTER(c_double)]
	_dvec_copy.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 129
if _libs["libxux64.so"].has("_dvec_plus", "cdecl"):
	_dvec_plus = _libs["libxux64.so"].get("_dvec_plus", "cdecl")
	_dvec_plus.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_dvec_plus.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 130
if _libs["libxux64.so"].has("_dvec_minus", "cdecl"):
	_dvec_minus = _libs["libxux64.so"].get("_dvec_minus", "cdecl")
	_dvec_minus.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_dvec_minus.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 131
if _libs["libxux64.so"].has("_dvec_multiply", "cdecl"):
	_dvec_multiply = _libs["libxux64.so"].get("_dvec_multiply", "cdecl")
	_dvec_multiply.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_dvec_multiply.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 132
if _libs["libxux64.so"].has("_dvec_devide", "cdecl"):
	_dvec_devide = _libs["libxux64.so"].get("_dvec_devide", "cdecl")
	_dvec_devide.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_dvec_devide.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 133
if _libs["libxux64.so"].has("_dvec_step", "cdecl"):
	_dvec_step = _libs["libxux64.so"].get("_dvec_step", "cdecl")
	_dvec_step.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double)]
	_dvec_step.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 134
if _libs["libxux64.so"].has("_dvec_ext", "cdecl"):
	_dvec_ext = _libs["libxux64.so"].get("_dvec_ext", "cdecl")
	_dvec_ext.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double)]
	_dvec_ext.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 135
if _libs["libxux64.so"].has("_phase", "cdecl"):
	_phase = _libs["libxux64.so"].get("_phase", "cdecl")
	_phase.argtypes = [c_int, c_double, c_double, POINTER(c_double)]
	_phase.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 136
for _lib in _libs.values():
	if not _lib.has("_phasek", "cdecl"):
		continue
	_phasek = _lib.get("_phasek", "cdecl")
	_phasek.argtypes = [c_int, c_double, c_double, POINTER(c_double), c_double]
	_phasek.restype = POINTER(c_double)
	break

# /apps/fafa/pyx/anPy/afa/xu.h: 137
if _libs["libxux64.so"].has("_round", "cdecl"):
	_round = _libs["libxux64.so"].get("_round", "cdecl")
	_round.argtypes = [c_double, c_int]
	_round.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 138
if _libs["libxux64.so"].has("_roundup", "cdecl"):
	_roundup = _libs["libxux64.so"].get("_roundup", "cdecl")
	_roundup.argtypes = [c_double, c_int]
	_roundup.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 139
if _libs["libxux64.so"].has("_roundown", "cdecl"):
	_roundown = _libs["libxux64.so"].get("_roundown", "cdecl")
	_roundown.argtypes = [c_double, c_int]
	_roundown.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 140
if _libs["libxux64.so"].has("_avg", "cdecl"):
	_avg = _libs["libxux64.so"].get("_avg", "cdecl")
	_avg.argtypes = [POINTER(c_double), c_int]
	_avg.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 141
if _libs["libxux64.so"].has("_max", "cdecl"):
	_max = _libs["libxux64.so"].get("_max", "cdecl")
	_max.argtypes = [POINTER(c_double), c_int]
	_max.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 142
if _libs["libxux64.so"].has("_min", "cdecl"):
	_min = _libs["libxux64.so"].get("_min", "cdecl")
	_min.argtypes = [POINTER(c_double), c_int]
	_min.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 143
if _libs["libxux64.so"].has("_std", "cdecl"):
	_std = _libs["libxux64.so"].get("_std", "cdecl")
	_std.argtypes = [POINTER(c_double), c_int]
	_std.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 144
if _libs["libxux64.so"].has("_prod", "cdecl"):
	_prod = _libs["libxux64.so"].get("_prod", "cdecl")
	_prod.argtypes = [POINTER(c_double), c_int]
	_prod.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 145
if _libs["libxux64.so"].has("_sum", "cdecl"):
	_sum = _libs["libxux64.so"].get("_sum", "cdecl")
	_sum.argtypes = [POINTER(c_double), c_int]
	_sum.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 146
if _libs["libxux64.so"].has("_var", "cdecl"):
	_var = _libs["libxux64.so"].get("_var", "cdecl")
	_var.argtypes = [POINTER(c_double), c_int]
	_var.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 147
if _libs["libxux64.so"].has("_momentw", "cdecl"):
	_momentw = _libs["libxux64.so"].get("_momentw", "cdecl")
	_momentw.argtypes = [c_int, POINTER(c_double), c_double, c_double, POINTER(c_double)]
	_momentw.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 148
if _libs["libxux64.so"].has("_moment", "cdecl"):
	_moment = _libs["libxux64.so"].get("_moment", "cdecl")
	_moment.argtypes = [c_int, POINTER(c_double), c_double, c_double]
	_moment.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 149
if _libs["libxux64.so"].has("_ran3", "cdecl"):
	_ran3 = _libs["libxux64.so"].get("_ran3", "cdecl")
	_ran3.argtypes = [POINTER(c_int)]
	_ran3.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 150
if _libs["libxux64.so"].has("_ran_gauss", "cdecl"):
	_ran_gauss = _libs["libxux64.so"].get("_ran_gauss", "cdecl")
	_ran_gauss.argtypes = [POINTER(c_int), c_int, POINTER(c_double)]
	_ran_gauss.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 151
if _libs["libxux64.so"].has("_dsort", "cdecl"):
	_dsort = _libs["libxux64.so"].get("_dsort", "cdecl")
	_dsort.argtypes = [POINTER(c_double), c_int]
	_dsort.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 152
if _libs["libxux64.so"].has("_isort", "cdecl"):
	_isort = _libs["libxux64.so"].get("_isort", "cdecl")
	_isort.argtypes = [POINTER(c_double), POINTER(c_int), c_int]
	_isort.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 153
if _libs["libxux64.so"].has("acompare", "cdecl"):
	acompare = _libs["libxux64.so"].get("acompare", "cdecl")
	acompare.argtypes = [POINTER(None), POINTER(None)]
	acompare.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 154
if _libs["libxux64.so"].has("_isortstr", "cdecl"):
	_isortstr = _libs["libxux64.so"].get("_isortstr", "cdecl")
	_isortstr.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int), c_int]
	_isortstr.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 155
if _libs["libxux64.so"].has("bcompare", "cdecl"):
	bcompare = _libs["libxux64.so"].get("bcompare", "cdecl")
	bcompare.argtypes = [POINTER(None), POINTER(None)]
	bcompare.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 157
if _libs["libxux64.so"].has("_iter", "cdecl"):
	_iter = _libs["libxux64.so"].get("_iter", "cdecl")
	_iter.argtypes = [c_double, c_double, c_double, String, CFUNCTYPE(UNCHECKED(c_int), c_double, POINTER(c_double), String)]
	_iter.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 158
if _libs["libxux64.so"].has("_bisect", "cdecl"):
	_bisect = _libs["libxux64.so"].get("_bisect", "cdecl")
	_bisect.argtypes = [c_double, c_double, c_double, c_double, String, CFUNCTYPE(UNCHECKED(c_int), c_double, POINTER(c_double), String)]
	_bisect.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 159
if _libs["libxux64.so"].has("prnerr", "cdecl"):
	prnerr = _libs["libxux64.so"].get("prnerr", "cdecl")
	prnerr.argtypes = [POINTER(FILE), String, String, c_double, c_int]
	prnerr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 160
if _libs["libxux64.so"].has("keychk", "cdecl"):
	keychk = _libs["libxux64.so"].get("keychk", "cdecl")
	keychk.argtypes = []
	keychk.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 161
if _libs["libxux64.so"].has("fkeychk", "cdecl"):
	fkeychk = _libs["libxux64.so"].get("fkeychk", "cdecl")
	fkeychk.argtypes = [POINTER(POINTER(c_double)), String]
	fkeychk.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 162
if _libs["libxux64.so"].has("_filecvt", "cdecl"):
	_filecvt = _libs["libxux64.so"].get("_filecvt", "cdecl")
	_filecvt.argtypes = [String, String, c_int, c_int]
	_filecvt.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 163
if _libs["libxux64.so"].has("_cipher", "cdecl"):
	_cipher = _libs["libxux64.so"].get("_cipher", "cdecl")
	_cipher.argtypes = [String, c_int, c_int, c_int]
	_cipher.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 164
if _libs["libxux64.so"].has("_nmoments", "cdecl"):
	_nmoments = _libs["libxux64.so"].get("_nmoments", "cdecl")
	_nmoments.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_nmoments.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 165
if _libs["libxux64.so"].has("_vmoments", "cdecl"):
	_vmoments = _libs["libxux64.so"].get("_vmoments", "cdecl")
	_vmoments.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	_vmoments.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 166
if _libs["libxux64.so"].has("_Cmpnd", "cdecl"):
	_Cmpnd = _libs["libxux64.so"].get("_Cmpnd", "cdecl")
	_Cmpnd.argtypes = [c_double, c_double, c_int]
	_Cmpnd.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 167
if _libs["libxux64.so"].has("_DscPrcQuote", "cdecl"):
	_DscPrcQuote = _libs["libxux64.so"].get("_DscPrcQuote", "cdecl")
	_DscPrcQuote.argtypes = [c_int, c_double, c_double, c_double]
	_DscPrcQuote.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 168
if _libs["libxux64.so"].has("_SelDsFct", "cdecl"):
	_SelDsFct = _libs["libxux64.so"].get("_SelDsFct", "cdecl")
	_SelDsFct.argtypes = [c_double, c_double, c_double, c_int, POINTER(c_double), POINTER(c_double)]
	_SelDsFct.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 169
if _libs["libxux64.so"].has("_NfvTVD", "cdecl"):
	_NfvTVD = _libs["libxux64.so"].get("_NfvTVD", "cdecl")
	_NfvTVD.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
	_NfvTVD.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 170
if _libs["libxux64.so"].has("BbNfv", "cdecl"):
	BbNfv = _libs["libxux64.so"].get("BbNfv", "cdecl")
	BbNfv.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	BbNfv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 172
if _libs["libxux64.so"].has("_NpvTVD", "cdecl"):
	_NpvTVD = _libs["libxux64.so"].get("_NpvTVD", "cdecl")
	_NpvTVD.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
	_NpvTVD.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 173
if _libs["libxux64.so"].has("BbNpv", "cdecl"):
	BbNpv = _libs["libxux64.so"].get("BbNpv", "cdecl")
	BbNpv.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	BbNpv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 175
if _libs["libxux64.so"].has("BbIrv", "cdecl"):
	BbIrv = _libs["libxux64.so"].get("BbIrv", "cdecl")
	BbIrv.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_double, c_double]
	BbIrv.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 177
if _libs["libxux64.so"].has("BbIrr", "cdecl"):
	BbIrr = _libs["libxux64.so"].get("BbIrr", "cdecl")
	BbIrr.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_double, c_double]
	BbIrr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 179
if _libs["libxux64.so"].has("BbLinVec", "cdecl"):
	BbLinVec = _libs["libxux64.so"].get("BbLinVec", "cdecl")
	BbLinVec.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), c_int]
	BbLinVec.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 180
if _libs["libxux64.so"].has("_fndOffsetPrd", "cdecl"):
	_fndOffsetPrd = _libs["libxux64.so"].get("_fndOffsetPrd", "cdecl")
	_fndOffsetPrd.argtypes = [c_int, POINTER(c_double), c_double]
	_fndOffsetPrd.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 181
if _libs["libxux64.so"].has("keyDpcy", "cdecl"):
	keyDpcy = _libs["libxux64.so"].get("keyDpcy", "cdecl")
	keyDpcy.argtypes = [POINTER(POINTER(c_char)), POINTER(POINTER(c_char)), POINTER(c_int), POINTER(c_int), c_int]
	keyDpcy.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 182
if _libs["libxux64.so"].has("_mkPath", "cdecl"):
	_mkPath = _libs["libxux64.so"].get("_mkPath", "cdecl")
	_mkPath.argtypes = [String]
	_mkPath.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 183
if _libs["libxux64.so"].has("_rmPath", "cdecl"):
	_rmPath = _libs["libxux64.so"].get("_rmPath", "cdecl")
	_rmPath.argtypes = [String]
	_rmPath.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 184
if _libs["libxux64.so"].has("_readPath", "cdecl"):
	_readPath = _libs["libxux64.so"].get("_readPath", "cdecl")
	_readPath.argtypes = [String]
	_readPath.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 185
if _libs["libxux64.so"].has("_cdPath", "cdecl"):
	_cdPath = _libs["libxux64.so"].get("_cdPath", "cdecl")
	_cdPath.argtypes = [String]
	_cdPath.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 186
if _libs["libxux64.so"].has("interpolateCalc", "cdecl"):
	interpolateCalc = _libs["libxux64.so"].get("interpolateCalc", "cdecl")
	interpolateCalc.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	interpolateCalc.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 187
if _libs["libxux64.so"].has("calc_link", "cdecl"):
	calc_link = _libs["libxux64.so"].get("calc_link", "cdecl")
	calc_link.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), c_int]
	calc_link.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 188
if _libs["libxux64.so"].has("calc_cubicSpline", "cdecl"):
	calc_cubicSpline = _libs["libxux64.so"].get("calc_cubicSpline", "cdecl")
	calc_cubicSpline.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_double)]
	calc_cubicSpline.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 189
if _libs["libxux64.so"].has("calc_sp3", "cdecl"):
	calc_sp3 = _libs["libxux64.so"].get("calc_sp3", "cdecl")
	calc_sp3.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_double)]
	calc_sp3.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 190
if _libs["libxux64.so"].has("cubicSpline", "cdecl"):
	cubicSpline = _libs["libxux64.so"].get("cubicSpline", "cdecl")
	cubicSpline.argtypes = [POINTER(c_double), POINTER(c_double), c_int, c_double, c_double, POINTER(c_double)]
	cubicSpline.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 191
if _libs["libxux64.so"].has("cubicSplint", "cdecl"):
	cubicSplint = _libs["libxux64.so"].get("cubicSplint", "cdecl")
	cubicSplint.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_double]
	cubicSplint.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 290
if _libs["libxux64.so"].has("_dscprc", "cdecl"):
	_dscprc = _libs["libxux64.so"].get("_dscprc", "cdecl")
	_dscprc.argtypes = [c_int, c_int, c_int, c_double]
	_dscprc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 291
if _libs["libxux64.so"].has("_dscfactor", "cdecl"):
	_dscfactor = _libs["libxux64.so"].get("_dscfactor", "cdecl")
	_dscfactor.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_double]
	_dscfactor.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 292
if _libs["libxux64.so"].has("_dsc2r", "cdecl"):
	_dsc2r = _libs["libxux64.so"].get("_dsc2r", "cdecl")
	_dsc2r.argtypes = [c_double, c_double]
	_dsc2r.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 293
if _libs["libxux64.so"].has("_adc", "cdecl"):
	_adc = _libs["libxux64.so"].get("_adc", "cdecl")
	_adc.argtypes = [c_int, c_int]
	_adc.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 294
if _libs["libxux64.so"].has("_yyyymmdd_btwn", "cdecl"):
	_yyyymmdd_btwn = _libs["libxux64.so"].get("_yyyymmdd_btwn", "cdecl")
	_yyyymmdd_btwn.argtypes = [POINTER(c_long), POINTER(c_long), c_long, c_long, c_int]
	_yyyymmdd_btwn.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 295
if _libs["libxux64.so"].has("_date_apart", "cdecl"):
	_date_apart = _libs["libxux64.so"].get("_date_apart", "cdecl")
	_date_apart.argtypes = [c_long, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	_date_apart.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 296
if _libs["libxux64.so"].has("_mmddyy_apart", "cdecl"):
	_mmddyy_apart = _libs["libxux64.so"].get("_mmddyy_apart", "cdecl")
	_mmddyy_apart.argtypes = [c_long, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	_mmddyy_apart.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 297
if _libs["libxux64.so"].has("_yyyymmdd_apart", "cdecl"):
	_yyyymmdd_apart = _libs["libxux64.so"].get("_yyyymmdd_apart", "cdecl")
	_yyyymmdd_apart.argtypes = [c_long, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	_yyyymmdd_apart.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 298
if _libs["libxux64.so"].has("_dayboundry", "cdecl"):
	_dayboundry = _libs["libxux64.so"].get("_dayboundry", "cdecl")
	_dayboundry.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	_dayboundry.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 299
if _libs["libxux64.so"].has("_yy_yyyy", "cdecl"):
	_yy_yyyy = _libs["libxux64.so"].get("_yy_yyyy", "cdecl")
	_yy_yyyy.argtypes = [c_int]
	_yy_yyyy.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 300
if _libs["libxux64.so"].has("_leapdays", "cdecl"):
	_leapdays = _libs["libxux64.so"].get("_leapdays", "cdecl")
	_leapdays.argtypes = [c_int]
	_leapdays.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 301
if _libs["libxux64.so"].has("_isleapyear", "cdecl"):
	_isleapyear = _libs["libxux64.so"].get("_isleapyear", "cdecl")
	_isleapyear.argtypes = [c_int]
	_isleapyear.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 302
if _libs["libxux64.so"].has("_check_date", "cdecl"):
	_check_date = _libs["libxux64.so"].get("_check_date", "cdecl")
	_check_date.argtypes = [c_int, c_int, c_int, c_int, c_int]
	_check_date.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 303
if _libs["libxux64.so"].has("_julian", "cdecl"):
	_julian = _libs["libxux64.so"].get("_julian", "cdecl")
	_julian.argtypes = [c_int, c_int, c_int]
	_julian.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 304
if _libs["libxux64.so"].has("_j360", "cdecl"):
	_j360 = _libs["libxux64.so"].get("_j360", "cdecl")
	_j360.argtypes = [c_int, c_int, c_int]
	_j360.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 305
if _libs["libxux64.so"].has("_days_btwn", "cdecl"):
	_days_btwn = _libs["libxux64.so"].get("_days_btwn", "cdecl")
	_days_btwn.argtypes = [POINTER(c_long), POINTER(c_long), c_int, c_int, c_int, c_int, c_int, c_int, c_int]
	_days_btwn.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 307
if _libs["libxux64.so"].has("_adjfeb", "cdecl"):
	_adjfeb = _libs["libxux64.so"].get("_adjfeb", "cdecl")
	_adjfeb.argtypes = [c_int, c_int, c_int]
	_adjfeb.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 308
if _libs["libxux64.so"].has("_weekday", "cdecl"):
	_weekday = _libs["libxux64.so"].get("_weekday", "cdecl")
	_weekday.argtypes = [c_int, c_int, c_int]
	_weekday.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 309
if _libs["libxux64.so"].has("_nweekday", "cdecl"):
	_nweekday = _libs["libxux64.so"].get("_nweekday", "cdecl")
	_nweekday.argtypes = [c_int, c_int, c_int, c_int]
	_nweekday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 310
if _libs["libxux64.so"].has("_nfwday", "cdecl"):
	_nfwday = _libs["libxux64.so"].get("_nfwday", "cdecl")
	_nfwday.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int]
	_nfwday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 311
if _libs["libxux64.so"].has("BbDateVec", "cdecl"):
	BbDateVec = _libs["libxux64.so"].get("BbDateVec", "cdecl")
	BbDateVec.argtypes = [POINTER(c_long), POINTER(c_long), c_int, c_int, c_int, c_int, POINTER(POINTER(c_char)), c_int, c_int, POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), c_long]
	BbDateVec.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 314
if _libs["libxux64.so"].has("_datevec", "cdecl"):
	_datevec = _libs["libxux64.so"].get("_datevec", "cdecl")
	_datevec.argtypes = [POINTER(c_long), c_int, c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(POINTER(c_char))]
	_datevec.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 316
if _libs["libxux64.so"].has("BbAddDatePrd", "cdecl"):
	BbAddDatePrd = _libs["libxux64.so"].get("BbAddDatePrd", "cdecl")
	BbAddDatePrd.argtypes = [POINTER(c_long), POINTER(c_long), c_int, c_int, c_int, c_int, POINTER(POINTER(c_char))]
	BbAddDatePrd.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 317
if _libs["libxux64.so"].has("BbAddDate", "cdecl"):
	BbAddDate = _libs["libxux64.so"].get("BbAddDate", "cdecl")
	BbAddDate.argtypes = [POINTER(c_long), c_int, c_int, c_int, c_int, c_int, POINTER(POINTER(c_char))]
	BbAddDate.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 318
if _libs["libxux64.so"].has("_bday", "cdecl"):
	_bday = _libs["libxux64.so"].get("_bday", "cdecl")
	_bday.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int), c_int, c_int, POINTER(POINTER(c_char))]
	_bday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 319
if _libs["libxux64.so"].has("_addbday", "cdecl"):
	_addbday = _libs["libxux64.so"].get("_addbday", "cdecl")
	_addbday.argtypes = [c_int, c_long, c_int, POINTER(POINTER(c_char))]
	_addbday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 320
if _libs["libxux64.so"].has("_isholiday", "cdecl"):
	_isholiday = _libs["libxux64.so"].get("_isholiday", "cdecl")
	_isholiday.argtypes = [c_long, c_int, POINTER(POINTER(c_char))]
	_isholiday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 321
if _libs["libxux64.so"].has("_isweekday", "cdecl"):
	_isweekday = _libs["libxux64.so"].get("_isweekday", "cdecl")
	_isweekday.argtypes = [c_long]
	_isweekday.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 322
if _libs["libxux64.so"].has("_accrued_days", "cdecl"):
	_accrued_days = _libs["libxux64.so"].get("_accrued_days", "cdecl")
	_accrued_days.argtypes = [c_int]
	_accrued_days.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 323
if _libs["libxux64.so"].has("_julianday", "cdecl"):
	_julianday = _libs["libxux64.so"].get("_julianday", "cdecl")
	_julianday.argtypes = [c_long]
	_julianday.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 324
if _libs["libxux64.so"].has("_j360day", "cdecl"):
	_j360day = _libs["libxux64.so"].get("_j360day", "cdecl")
	_j360day.argtypes = [c_long]
	_j360day.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 325
if _libs["libxux64.so"].has("_j2yyyymmdd", "cdecl"):
	_j2yyyymmdd = _libs["libxux64.so"].get("_j2yyyymmdd", "cdecl")
	_j2yyyymmdd.argtypes = [c_long]
	_j2yyyymmdd.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 326
if _libs["libxux64.so"].has("_fudate", "cdecl"):
	_fudate = _libs["libxux64.so"].get("_fudate", "cdecl")
	_fudate.argtypes = [c_long, c_int, c_int]
	_fudate.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 327
if _libs["libxux64.so"].has("_endofmonth", "cdecl"):
	_endofmonth = _libs["libxux64.so"].get("_endofmonth", "cdecl")
	_endofmonth.argtypes = [c_long]
	_endofmonth.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 328
if _libs["libxux64.so"].has("_daycount", "cdecl"):
	_daycount = _libs["libxux64.so"].get("_daycount", "cdecl")
	_daycount.argtypes = [c_int, c_double, c_double, c_int, POINTER(c_double), POINTER(c_double)]
	_daycount.restype = POINTER(c_double)

# /apps/fafa/pyx/anPy/afa/xu.h: 330
if _libs["libxux64.so"].has("caldat", "cdecl"):
	caldat = _libs["libxux64.so"].get("caldat", "cdecl")
	caldat.argtypes = [c_long, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
	caldat.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 331
if _libs["libxux64.so"].has("flmoon", "cdecl"):
	flmoon = _libs["libxux64.so"].get("flmoon", "cdecl")
	flmoon.argtypes = [c_int, c_int, POINTER(c_long), POINTER(c_double)]
	flmoon.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 332
if _libs["libxux64.so"].has("adddate", "cdecl"):
	adddate = _libs["libxux64.so"].get("adddate", "cdecl")
	adddate.argtypes = [c_long, c_int, c_int, c_int, c_int, c_int, POINTER(POINTER(c_char))]
	adddate.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 333
if _libs["libxux64.so"].has("nextdateL", "cdecl"):
	nextdateL = _libs["libxux64.so"].get("nextdateL", "cdecl")
	nextdateL.argtypes = [c_long, c_int]
	nextdateL.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 334
if _libs["libxux64.so"].has("nextdate", "cdecl"):
	nextdate = _libs["libxux64.so"].get("nextdate", "cdecl")
	nextdate.argtypes = [c_double, c_int]
	nextdate.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 335
if _libs["libxux64.so"].has("nextdate30", "cdecl"):
	nextdate30 = _libs["libxux64.so"].get("nextdate30", "cdecl")
	nextdate30.argtypes = [c_double, c_int]
	nextdate30.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 336
if _libs["libxux64.so"].has("strdate", "cdecl"):
	strdate = _libs["libxux64.so"].get("strdate", "cdecl")
	strdate.argtypes = [c_long, c_int]
	if sizeof(c_int) == sizeof(c_void_p):
		strdate.restype = ReturnString
	else:
		strdate.restype = String
		strdate.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 337
if _libs["libxux64.so"].has("str2date", "cdecl"):
	str2date = _libs["libxux64.so"].get("str2date", "cdecl")
	str2date.argtypes = [String, c_int]
	str2date.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 338
if _libs["libxux64.so"].has("_fut2yyyymm", "cdecl"):
	_fut2yyyymm = _libs["libxux64.so"].get("_fut2yyyymm", "cdecl")
	_fut2yyyymm.argtypes = [String, POINTER(c_int), POINTER(c_int)]
	_fut2yyyymm.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 339
if _libs["libxux64.so"].has("_fut2mo", "cdecl"):
	_fut2mo = _libs["libxux64.so"].get("_fut2mo", "cdecl")
	_fut2mo.argtypes = [c_char]
	_fut2mo.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 340
if _libs["libxux64.so"].has("bmg2dct", "cdecl"):
	bmg2dct = _libs["libxux64.so"].get("bmg2dct", "cdecl")
	bmg2dct.argtypes = [c_int, POINTER(c_int)]
	bmg2dct.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 418
if _libs["libxux64.so"].has("_durCalc", "cdecl"):
	_durCalc = _libs["libxux64.so"].get("_durCalc", "cdecl")
	_durCalc.argtypes = [c_double, c_double, c_double, c_double, c_double]
	_durCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 419
if _libs["libxux64.so"].has("_cvxCalc", "cdecl"):
	_cvxCalc = _libs["libxux64.so"].get("_cvxCalc", "cdecl")
	_cvxCalc.argtypes = [c_double, c_double, c_double, c_double, c_double]
	_cvxCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 420
if _libs["libxux64.so"].has("_dv01Calc", "cdecl"):
	_dv01Calc = _libs["libxux64.so"].get("_dv01Calc", "cdecl")
	_dv01Calc.argtypes = [c_double, c_double, c_double, c_double]
	_dv01Calc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 421
if _libs["libxux64.so"].has("_yv01Calc", "cdecl"):
	_yv01Calc = _libs["libxux64.so"].get("_yv01Calc", "cdecl")
	_yv01Calc.argtypes = [c_double, c_double, c_double, c_double]
	_yv01Calc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 422
if _libs["libxux64.so"].has("_rdv1Calc", "cdecl"):
	_rdv1Calc = _libs["libxux64.so"].get("_rdv1Calc", "cdecl")
	_rdv1Calc.argtypes = [c_double, c_double, c_double, c_double]
	_rdv1Calc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 423
if _libs["libxux64.so"].has("_piCalc", "cdecl"):
	_piCalc = _libs["libxux64.so"].get("_piCalc", "cdecl")
	_piCalc.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, c_double, c_double]
	_piCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 424
if _libs["libxux64.so"].has("BbAcrFrDay", "cdecl"):
	BbAcrFrDay = _libs["libxux64.so"].get("BbAcrFrDay", "cdecl")
	BbAcrFrDay.argtypes = [c_long, c_long, c_long, c_long, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	BbAcrFrDay.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 426
if _libs["libxux64.so"].has("_get_arm_strip_neg", "cdecl"):
	_get_arm_strip_neg = _libs["libxux64.so"].get("_get_arm_strip_neg", "cdecl")
	_get_arm_strip_neg.argtypes = [c_int, c_int, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_double, c_double, c_double]
	_get_arm_strip_neg.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 431
if _libs["libxux64.so"].has("_arm_cpn", "cdecl"):
	_arm_cpn = _libs["libxux64.so"].get("_arm_cpn", "cdecl")
	_arm_cpn.argtypes = [POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_double, c_double, c_double, c_double, c_double]
	_arm_cpn.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 433
if _libs["libxux64.so"].has("_hybridarm_cpn", "cdecl"):
	_hybridarm_cpn = _libs["libxux64.so"].get("_hybridarm_cpn", "cdecl")
	_hybridarm_cpn.argtypes = [POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_double, c_double, c_double, c_double, c_double, c_double]
	_hybridarm_cpn.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 435
if _libs["libxux64.so"].has("_get_arm_strip", "cdecl"):
	_get_arm_strip = _libs["libxux64.so"].get("_get_arm_strip", "cdecl")
	_get_arm_strip.argtypes = [c_int, c_int, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_get_arm_strip.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 438
if _libs["libxux64.so"].has("_get_frm_strip", "cdecl"):
	_get_frm_strip = _libs["libxux64.so"].get("_get_frm_strip", "cdecl")
	_get_frm_strip.argtypes = [c_int, c_int, c_double, c_double, c_double, c_double, POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_get_frm_strip.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 441
if _libs["libxux64.so"].has("_mbs_cfs", "cdecl"):
	_mbs_cfs = _libs["libxux64.so"].get("_mbs_cfs", "cdecl")
	_mbs_cfs.argtypes = [c_int, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_mbs_cfs.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 443
if _libs["libxux64.so"].has("_frm_cfs", "cdecl"):
	_frm_cfs = _libs["libxux64.so"].get("_frm_cfs", "cdecl")
	_frm_cfs.argtypes = [c_int, c_int, c_double, c_double, POINTER(c_double), c_double, POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_frm_cfs.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 446
if _libs["libxux64.so"].has("_frm_cashflow", "cdecl"):
	_frm_cashflow = _libs["libxux64.so"].get("_frm_cashflow", "cdecl")
	_frm_cashflow.argtypes = [c_int, c_double, c_double, c_double, c_double, POINTER(c_double)]
	_frm_cashflow.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 448
if _libs["libxux64.so"].has("_frm_cfs_1", "cdecl"):
	_frm_cfs_1 = _libs["libxux64.so"].get("_frm_cfs_1", "cdecl")
	_frm_cfs_1.argtypes = [c_int, c_int, c_double, c_double, c_double, POINTER(c_double), c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_frm_cfs_1.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 450
if _libs["libxux64.so"].has("_arm_index_rate", "cdecl"):
	_arm_index_rate = _libs["libxux64.so"].get("_arm_index_rate", "cdecl")
	_arm_index_rate.argtypes = [POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_double, c_double, c_double, c_double, c_double]
	_arm_index_rate.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 452
if _libs["libxux64.so"].has("_min3", "cdecl"):
	_min3 = _libs["libxux64.so"].get("_min3", "cdecl")
	_min3.argtypes = [c_double, c_double, c_double]
	_min3.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 453
if _libs["libxux64.so"].has("_max3", "cdecl"):
	_max3 = _libs["libxux64.so"].get("_max3", "cdecl")
	_max3.argtypes = [c_double, c_double, c_double]
	_max3.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 454
if _libs["libxux64.so"].has("_cpr2smm", "cdecl"):
	_cpr2smm = _libs["libxux64.so"].get("_cpr2smm", "cdecl")
	_cpr2smm.argtypes = [c_double]
	_cpr2smm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 455
if _libs["libxux64.so"].has("_smm2cpr", "cdecl"):
	_smm2cpr = _libs["libxux64.so"].get("_smm2cpr", "cdecl")
	_smm2cpr.argtypes = [c_double]
	_smm2cpr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 456
if _libs["libxux64.so"].has("_smm2abs", "cdecl"):
	_smm2abs = _libs["libxux64.so"].get("_smm2abs", "cdecl")
	_smm2abs.argtypes = [c_double, c_int]
	_smm2abs.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 457
if _libs["libxux64.so"].has("_abs2smm", "cdecl"):
	_abs2smm = _libs["libxux64.so"].get("_abs2smm", "cdecl")
	_abs2smm.argtypes = [c_double, c_int]
	_abs2smm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 458
if _libs["libxux64.so"].has("_smm2psa", "cdecl"):
	_smm2psa = _libs["libxux64.so"].get("_smm2psa", "cdecl")
	_smm2psa.argtypes = [c_double, c_int]
	_smm2psa.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 459
if _libs["libxux64.so"].has("_psa2smm", "cdecl"):
	_psa2smm = _libs["libxux64.so"].get("_psa2smm", "cdecl")
	_psa2smm.argtypes = [c_double, c_int]
	_psa2smm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 460
if _libs["libxux64.so"].has("_psa2cpr", "cdecl"):
	_psa2cpr = _libs["libxux64.so"].get("_psa2cpr", "cdecl")
	_psa2cpr.argtypes = [c_double, c_int]
	_psa2cpr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 461
if _libs["libxux64.so"].has("_sda2mdr", "cdecl"):
	_sda2mdr = _libs["libxux64.so"].get("_sda2mdr", "cdecl")
	_sda2mdr.argtypes = [c_double, c_int]
	_sda2mdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 462
if _libs["libxux64.so"].has("_sda2cdr", "cdecl"):
	_sda2cdr = _libs["libxux64.so"].get("_sda2cdr", "cdecl")
	_sda2cdr.argtypes = [c_double, c_int]
	_sda2cdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 463
if _libs["libxux64.so"].has("_cdr2mdr", "cdecl"):
	_cdr2mdr = _libs["libxux64.so"].get("_cdr2mdr", "cdecl")
	_cdr2mdr.argtypes = [c_double]
	_cdr2mdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 464
if _libs["libxux64.so"].has("_mdr2cdr", "cdecl"):
	_mdr2cdr = _libs["libxux64.so"].get("_mdr2cdr", "cdecl")
	_mdr2cdr.argtypes = [c_double]
	_mdr2cdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 465
if _libs["libxux64.so"].has("_mdr2sda", "cdecl"):
	_mdr2sda = _libs["libxux64.so"].get("_mdr2sda", "cdecl")
	_mdr2sda.argtypes = [c_double, c_int]
	_mdr2sda.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 466
if _libs["libxux64.so"].has("_pld2cdr", "cdecl"):
	_pld2cdr = _libs["libxux64.so"].get("_pld2cdr", "cdecl")
	_pld2cdr.argtypes = [c_double, c_int]
	_pld2cdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 467
if _libs["libxux64.so"].has("_pld2mdr", "cdecl"):
	_pld2mdr = _libs["libxux64.so"].get("_pld2mdr", "cdecl")
	_pld2mdr.argtypes = [c_double, c_int]
	_pld2mdr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 468
if _libs["libxux64.so"].has("_str_p32", "cdecl"):
	_str_p32 = _libs["libxux64.so"].get("_str_p32", "cdecl")
	_str_p32.argtypes = [String]
	_str_p32.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 469
if _libs["libxux64.so"].has("_p2basr", "cdecl"):
	_p2basr = _libs["libxux64.so"].get("_p2basr", "cdecl")
	_p2basr.argtypes = [c_double, c_int]
	_p2basr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 470
if _libs["libxux64.so"].has("_p100basr", "cdecl"):
	_p100basr = _libs["libxux64.so"].get("_p100basr", "cdecl")
	_p100basr.argtypes = [c_double, c_int]
	_p100basr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 471
if _libs["libxux64.so"].has("_p2base", "cdecl"):
	_p2base = _libs["libxux64.so"].get("_p2base", "cdecl")
	_p2base.argtypes = [c_double, c_int, c_int]
	_p2base.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 472
if _libs["libxux64.so"].has("_p100base", "cdecl"):
	_p100base = _libs["libxux64.so"].get("_p100base", "cdecl")
	_p100base.argtypes = [c_double, c_int, c_int]
	_p100base.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 473
if _libs["libxux64.so"].has("_p32str", "cdecl"):
	_p32str = _libs["libxux64.so"].get("_p32str", "cdecl")
	_p32str.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_p32str.restype = ReturnString
	else:
		_p32str.restype = String
		_p32str.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 474
if _libs["libxux64.so"].has("_p64str", "cdecl"):
	_p64str = _libs["libxux64.so"].get("_p64str", "cdecl")
	_p64str.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_p64str.restype = ReturnString
	else:
		_p64str.restype = String
		_p64str.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 475
if _libs["libxux64.so"].has("_p128str", "cdecl"):
	_p128str = _libs["libxux64.so"].get("_p128str", "cdecl")
	_p128str.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_p128str.restype = ReturnString
	else:
		_p128str.restype = String
		_p128str.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 476
if _libs["libxux64.so"].has("_p256str", "cdecl"):
	_p256str = _libs["libxux64.so"].get("_p256str", "cdecl")
	_p256str.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_p256str.restype = ReturnString
	else:
		_p256str.restype = String
		_p256str.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 477
if _libs["libxux64.so"].has("_ppy_factor", "cdecl"):
	_ppy_factor = _libs["libxux64.so"].get("_ppy_factor", "cdecl")
	_ppy_factor.argtypes = [c_int, POINTER(c_double), c_double, c_int]
	_ppy_factor.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 478
if _libs["libxux64.so"].has("_cdollar", "cdecl"):
	_cdollar = _libs["libxux64.so"].get("_cdollar", "cdecl")
	_cdollar.argtypes = [c_double, c_int]
	if sizeof(c_int) == sizeof(c_void_p):
		_cdollar.restype = ReturnString
	else:
		_cdollar.restype = String
		_cdollar.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 479
if _libs["libxux64.so"].has("_p32", "cdecl"):
	_p32 = _libs["libxux64.so"].get("_p32", "cdecl")
	_p32.argtypes = [c_double]
	_p32.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 480
if _libs["libxux64.so"].has("_p100", "cdecl"):
	_p100 = _libs["libxux64.so"].get("_p100", "cdecl")
	_p100.argtypes = [c_double]
	_p100.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 481
if _libs["libxux64.so"].has("_p32r", "cdecl"):
	_p32r = _libs["libxux64.so"].get("_p32r", "cdecl")
	_p32r.argtypes = [c_double]
	_p32r.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 482
if _libs["libxux64.so"].has("_prc32", "cdecl"):
	_prc32 = _libs["libxux64.so"].get("_prc32", "cdecl")
	_prc32.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_prc32.restype = ReturnString
	else:
		_prc32.restype = String
		_prc32.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 483
if _libs["libxux64.so"].has("_prc256", "cdecl"):
	_prc256 = _libs["libxux64.so"].get("_prc256", "cdecl")
	_prc256.argtypes = [c_double]
	if sizeof(c_int) == sizeof(c_void_p):
		_prc256.restype = ReturnString
	else:
		_prc256.restype = String
		_prc256.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 484
if _libs["libxux64.so"].has("_prc100", "cdecl"):
	_prc100 = _libs["libxux64.so"].get("_prc100", "cdecl")
	_prc100.argtypes = [String]
	_prc100.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 485
if _libs["libxux64.so"].has("dbl2int", "cdecl"):
	dbl2int = _libs["libxux64.so"].get("dbl2int", "cdecl")
	dbl2int.argtypes = [c_double]
	dbl2int.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 486
if _libs["libxux64.so"].has("_tbillc", "cdecl"):
	_tbillc = _libs["libxux64.so"].get("_tbillc", "cdecl")
	_tbillc.argtypes = [c_double, c_double, c_double, c_int]
	_tbillc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 487
if _libs["libxux64.so"].has("_bey2r", "cdecl"):
	_bey2r = _libs["libxux64.so"].get("_bey2r", "cdecl")
	_bey2r.argtypes = [c_double, c_double, c_int]
	_bey2r.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 488
if _libs["libxux64.so"].has("calc_xprd", "cdecl"):
	calc_xprd = _libs["libxux64.so"].get("calc_xprd", "cdecl")
	calc_xprd.argtypes = [c_double, c_double, c_int]
	calc_xprd.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 489
if _libs["libxux64.so"].has("calc_days", "cdecl"):
	calc_days = _libs["libxux64.so"].get("calc_days", "cdecl")
	calc_days.argtypes = [c_long, c_long, c_int]
	calc_days.restype = c_long

# /apps/fafa/pyx/anPy/afa/xu.h: 490
if _libs["libxux64.so"].has("calc_xfract", "cdecl"):
	calc_xfract = _libs["libxux64.so"].get("calc_xfract", "cdecl")
	calc_xfract.argtypes = [c_long, c_long, c_long, c_int, c_int, POINTER(c_double)]
	calc_xfract.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 492
if _libs["libxux64.so"].has("calc_xfr", "cdecl"):
	calc_xfr = _libs["libxux64.so"].get("calc_xfr", "cdecl")
	calc_xfr.argtypes = [c_long, c_long, c_long, c_int, c_int, POINTER(c_double)]
	calc_xfr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 494
if _libs["libxux64.so"].has("calc_acr_fr", "cdecl"):
	calc_acr_fr = _libs["libxux64.so"].get("calc_acr_fr", "cdecl")
	calc_acr_fr.argtypes = [c_long, c_long, c_long, c_long, c_double, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	calc_acr_fr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 497
if _libs["libxux64.so"].has("calc_tra", "cdecl"):
	calc_tra = _libs["libxux64.so"].get("calc_tra", "cdecl")
	calc_tra.argtypes = [c_int, c_long, c_long, c_long, c_double, c_double, c_long, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), c_long, c_int, c_int, c_int]
	calc_tra.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 502
if _libs["libxux64.so"].has("calcPydm", "cdecl"):
	calcPydm = _libs["libxux64.so"].get("calcPydm", "cdecl")
	calcPydm.argtypes = [c_int, c_long, c_long, c_long, c_double, c_long, c_double, c_double, c_double, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_long, c_long, c_long, POINTER(c_double), c_double]
	calcPydm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 507
if _libs["libxux64.so"].has("calc_pydm", "cdecl"):
	calc_pydm = _libs["libxux64.so"].get("calc_pydm", "cdecl")
	calc_pydm.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double]
	calc_pydm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 511
if _libs["libxux64.so"].has("xpmt_cf", "cdecl"):
	xpmt_cf = _libs["libxux64.so"].get("xpmt_cf", "cdecl")
	xpmt_cf.argtypes = [c_int, c_int, c_double, c_double, c_int, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	xpmt_cf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 516
if _libs["libxux64.so"].has("pmt_cf", "cdecl"):
	pmt_cf = _libs["libxux64.so"].get("pmt_cf", "cdecl")
	pmt_cf.argtypes = [c_int, c_int, c_double, c_int, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	pmt_cf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 521
if _libs["libxux64.so"].has("bln_cf", "cdecl"):
	bln_cf = _libs["libxux64.so"].get("bln_cf", "cdecl")
	bln_cf.argtypes = [c_int, c_double, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int]
	bln_cf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 526
if _libs["libxux64.so"].has("col_cf", "cdecl"):
	col_cf = _libs["libxux64.so"].get("col_cf", "cdecl")
	col_cf.argtypes = [c_int, c_double, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_int]
	col_cf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 531
if _libs["libxux64.so"].has("col_cfn", "cdecl"):
	col_cfn = _libs["libxux64.so"].get("col_cfn", "cdecl")
	col_cfn.argtypes = [c_int, c_double, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_int]
	col_cfn.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 536
if _libs["libxux64.so"].has("col_cfpmt", "cdecl"):
	col_cfpmt = _libs["libxux64.so"].get("col_cfpmt", "cdecl")
	col_cfpmt.argtypes = [c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
	col_cfpmt.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 542
if _libs["libxux64.so"].has("col_cfvec", "cdecl"):
	col_cfvec = _libs["libxux64.so"].get("col_cfvec", "cdecl")
	col_cfvec.argtypes = [c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, c_int, c_int, c_int, c_int]
	col_cfvec.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 548
if _libs["libxux64.so"].has("col_snk", "cdecl"):
	col_snk = _libs["libxux64.so"].get("col_snk", "cdecl")
	col_snk.argtypes = [c_int, c_double, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_int]
	col_snk.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 555
if _libs["libxux64.so"].has("_datebase", "cdecl"):
	_datebase = _libs["libxux64.so"].get("_datebase", "cdecl")
	_datebase.argtypes = [c_int, c_int]
	_datebase.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 556
if _libs["libxux64.so"].has("_initDblVec", "cdecl"):
	_initDblVec = _libs["libxux64.so"].get("_initDblVec", "cdecl")
	_initDblVec.argtypes = [c_int, POINTER(c_double), c_double, c_double, POINTER(c_double)]
	_initDblVec.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 557
if _libs["libxux64.so"].has("_gnrBondCf", "cdecl"):
	_gnrBondCf = _libs["libxux64.so"].get("_gnrBondCf", "cdecl")
	_gnrBondCf.argtypes = [c_long, c_long, c_long, c_long, c_int, c_int, c_int, c_int, POINTER(POINTER(c_char)), c_int, c_int, c_double, POINTER(c_double), c_double, c_double, POINTER(c_double), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(c_int), POINTER(c_int), POINTER(c_long), POINTER(c_long)]
	_gnrBondCf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 562
if _libs["libxux64.so"].has("_yr2D", "cdecl"):
	_yr2D = _libs["libxux64.so"].get("_yr2D", "cdecl")
	_yr2D.argtypes = [c_char, c_double]
	_yr2D.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 563
if _libs["libxux64.so"].has("_dtcTyp", "cdecl"):
	_dtcTyp = _libs["libxux64.so"].get("_dtcTyp", "cdecl")
	_dtcTyp.argtypes = [c_int, c_int, c_int]
	_dtcTyp.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 564
if _libs["libxux64.so"].has("_dtcU", "cdecl"):
	_dtcU = _libs["libxux64.so"].get("_dtcU", "cdecl")
	_dtcU.argtypes = [c_int]
	_dtcU.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 565
if _libs["libxux64.so"].has("_dtcD", "cdecl"):
	_dtcD = _libs["libxux64.so"].get("_dtcD", "cdecl")
	_dtcD.argtypes = [c_int]
	_dtcD.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 566
if _libs["libxux64.so"].has("_dtcBse", "cdecl"):
	_dtcBse = _libs["libxux64.so"].get("_dtcBse", "cdecl")
	_dtcBse.argtypes = [c_int, c_int]
	_dtcBse.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 567
if _libs["libxux64.so"].has("tbill_calc", "cdecl"):
	tbill_calc = _libs["libxux64.so"].get("tbill_calc", "cdecl")
	tbill_calc.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_int), POINTER(c_int), c_long, c_long, c_long, c_int, c_int, c_int]
	tbill_calc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 569
if _libs["libxux64.so"].has("BbTBillCalc", "cdecl"):
	BbTBillCalc = _libs["libxux64.so"].get("BbTBillCalc", "cdecl")
	BbTBillCalc.argtypes = [POINTER(c_double), POINTER(c_double), c_long, c_long, c_long, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int)]
	BbTBillCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 571
if _libs["libxux64.so"].has("BbGnrBondCalc", "cdecl"):
	BbGnrBondCalc = _libs["libxux64.so"].get("BbGnrBondCalc", "cdecl")
	BbGnrBondCalc.argtypes = [c_long, c_long, c_long, c_long, c_int, c_int, c_int, c_int, POINTER(POINTER(c_char)), c_int, c_int, c_double, c_double, POINTER(c_double), c_double, c_double, POINTER(c_double), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(POINTER(c_double)), POINTER(c_int), POINTER(c_int), c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	BbGnrBondCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 578
if _libs["libxux64.so"].has("BbTBondCalc", "cdecl"):
	BbTBondCalc = _libs["libxux64.so"].get("BbTBondCalc", "cdecl")
	BbTBondCalc.argtypes = [c_double, c_double, c_long, c_long, c_long, c_int, c_int, c_double, c_double, c_double, POINTER(c_int), POINTER(c_long), POINTER(c_long), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	BbTBondCalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 582
if _libs["libxux64.so"].has("BbVcalc", "cdecl"):
	BbVcalc = _libs["libxux64.so"].get("BbVcalc", "cdecl")
	BbVcalc.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_double]
	BbVcalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 585
if _libs["libxux64.so"].has("_gnrBondCFlow", "cdecl"):
	_gnrBondCFlow = _libs["libxux64.so"].get("_gnrBondCFlow", "cdecl")
	_gnrBondCFlow.argtypes = [c_int, c_int, c_int, c_long, c_long, POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double), c_double, c_double, POINTER(c_double), POINTER(POINTER(c_double))]
	_gnrBondCFlow.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 587
if _libs["libxux64.so"].has("_sttlMatPrd", "cdecl"):
	_sttlMatPrd = _libs["libxux64.so"].get("_sttlMatPrd", "cdecl")
	_sttlMatPrd.argtypes = [c_long, c_long, c_int, c_int]
	_sttlMatPrd.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 588
if _libs["libxux64.so"].has("interpolateCalc", "cdecl"):
	interpolateCalc = _libs["libxux64.so"].get("interpolateCalc", "cdecl")
	interpolateCalc.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	interpolateCalc.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 589
if _libs["libxux64.so"].has("_parseycky", "cdecl"):
	_parseycky = _libs["libxux64.so"].get("_parseycky", "cdecl")
	_parseycky.argtypes = [String, POINTER(c_double), POINTER(c_double), POINTER(c_int)]
	_parseycky.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 590
if _libs["libxux64.so"].has("_depositC", "cdecl"):
	_depositC = _libs["libxux64.so"].get("_depositC", "cdecl")
	_depositC.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_int, c_double, c_double, c_int, c_int, c_int, POINTER(POINTER(c_char))]
	_depositC.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 591
if _libs["libxux64.so"].has("_depositStrp", "cdecl"):
	_depositStrp = _libs["libxux64.so"].get("_depositStrp", "cdecl")
	_depositStrp.argtypes = [c_double, c_long, c_long, c_int, c_double, c_int]
	_depositStrp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 592
if _libs["libxux64.so"].has("_dliborC", "cdecl"):
	_dliborC = _libs["libxux64.so"].get("_dliborC", "cdecl")
	_dliborC.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_double, c_int, c_int, POINTER(c_double), c_int, POINTER(POINTER(c_char))]
	_dliborC.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 593
if _libs["libxux64.so"].has("_futC", "cdecl"):
	_futC = _libs["libxux64.so"].get("_futC", "cdecl")
	_futC.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_double, String, c_int, c_int, c_int, c_int, POINTER(POINTER(c_char))]
	_futC.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 594
if _libs["libxux64.so"].has("_futStrp", "cdecl"):
	_futStrp = _libs["libxux64.so"].get("_futStrp", "cdecl")
	_futStrp.argtypes = [c_double, c_long, c_long, c_double, c_long, c_int, c_double, c_int]
	_futStrp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 595
if _libs["libxux64.so"].has("_lbrC", "cdecl"):
	_lbrC = _libs["libxux64.so"].get("_lbrC", "cdecl")
	_lbrC.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_double, c_int, c_double, c_int, c_int, POINTER(c_double), c_int, POINTER(POINTER(c_char))]
	_lbrC.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 596
if _libs["libxux64.so"].has("_swpC", "cdecl"):
	_swpC = _libs["libxux64.so"].get("_swpC", "cdecl")
	_swpC.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_double, c_double, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, POINTER(POINTER(c_char))]
	_swpC.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 597
if _libs["libxux64.so"].has("_swpStrp", "cdecl"):
	_swpStrp = _libs["libxux64.so"].get("_swpStrp", "cdecl")
	_swpStrp.argtypes = [c_int, c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double]
	_swpStrp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 598
if _libs["libxux64.so"].has("_swpcf", "cdecl"):
	_swpcf = _libs["libxux64.so"].get("_swpcf", "cdecl")
	_swpcf.argtypes = [POINTER(c_long), POINTER(c_long), POINTER(c_long), POINTER(c_long), c_double, c_double, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double), c_int, c_int, POINTER(POINTER(c_char))]
	_swpcf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 599
if _libs["libxux64.so"].has("_swpPr", "cdecl"):
	_swpPr = _libs["libxux64.so"].get("_swpPr", "cdecl")
	_swpPr.argtypes = [c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_double]
	_swpPr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 600
if _libs["libxux64.so"].has("ycStripping", "cdecl"):
	ycStripping = _libs["libxux64.so"].get("ycStripping", "cdecl")
	ycStripping.argtypes = [c_int, POINTER(POINTER(c_char)), POINTER(c_double), POINTER(c_double), POINTER(c_long), c_double, c_int, c_int, c_int, POINTER(POINTER(c_char)), c_int, c_int, POINTER(c_int), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	ycStripping.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 604
if _libs["libxux64.so"].has("prnSwc", "cdecl"):
	prnSwc = _libs["libxux64.so"].get("prnSwc", "cdecl")
	prnSwc.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	prnSwc.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 605
if _libs["libxux64.so"].has("arrange_vec", "cdecl"):
	arrange_vec = _libs["libxux64.so"].get("arrange_vec", "cdecl")
	arrange_vec.argtypes = [POINTER(c_double), POINTER(c_int), c_int]
	arrange_vec.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 606
for _lib in _libs.values():
	if not _lib.has("_dsfcnv", "cdecl"):
		continue
	_dsfcnv = _lib.get("_dsfcnv", "cdecl")
	_dsfcnv.argtypes = [c_int, c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_dsfcnv.restype = c_int
	break

# /apps/fafa/pyx/anPy/afa/xu.h: 607
if _libs["libxux64.so"].has("fwd2nxspot", "cdecl"):
	fwd2nxspot = _libs["libxux64.so"].get("fwd2nxspot", "cdecl")
	fwd2nxspot.argtypes = [c_double, c_double, c_double, c_double, c_double]
	fwd2nxspot.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 608
if _libs["libxux64.so"].has("spots2fwd", "cdecl"):
	spots2fwd = _libs["libxux64.so"].get("spots2fwd", "cdecl")
	spots2fwd.argtypes = [c_double, c_double, c_double, c_double, c_double]
	spots2fwd.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 609
if _libs["libxux64.so"].has("spot2cdsf", "cdecl"):
	spot2cdsf = _libs["libxux64.so"].get("spot2cdsf", "cdecl")
	spot2cdsf.argtypes = [c_double, c_double, c_double]
	spot2cdsf.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 610
if _libs["libxux64.so"].has("cdsf2spot", "cdecl"):
	cdsf2spot = _libs["libxux64.so"].get("cdsf2spot", "cdecl")
	cdsf2spot.argtypes = [c_double, c_double, c_double]
	cdsf2spot.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 611
if _libs["libxux64.so"].has("cdsf2parYld", "cdecl"):
	cdsf2parYld = _libs["libxux64.so"].get("cdsf2parYld", "cdecl")
	cdsf2parYld.argtypes = [c_double, c_double, c_double]
	cdsf2parYld.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 612
if _libs["libxux64.so"].has("parYld2cdsf", "cdecl"):
	parYld2cdsf = _libs["libxux64.so"].get("parYld2cdsf", "cdecl")
	parYld2cdsf.argtypes = [c_double, c_double, c_double]
	parYld2cdsf.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 613
if _libs["libxux64.so"].has("vecSpot2FrwCdsf", "cdecl"):
	vecSpot2FrwCdsf = _libs["libxux64.so"].get("vecSpot2FrwCdsf", "cdecl")
	vecSpot2FrwCdsf.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	vecSpot2FrwCdsf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 614
if _libs["libxux64.so"].has("_smm2popcalc", "cdecl"):
	_smm2popcalc = _libs["libxux64.so"].get("_smm2popcalc", "cdecl")
	_smm2popcalc.argtypes = [c_int, c_double, c_double, c_double, c_double]
	_smm2popcalc.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 615
if _libs["libxux64.so"].has("_pmt2sch", "cdecl"):
	_pmt2sch = _libs["libxux64.so"].get("_pmt2sch", "cdecl")
	_pmt2sch.argtypes = [c_int, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, c_int, c_int]
	_pmt2sch.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 616
if _libs["libxux64.so"].has("_sch2cfs", "cdecl"):
	_sch2cfs = _libs["libxux64.so"].get("_sch2cfs", "cdecl")
	_sch2cfs.argtypes = [c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(None)]
	_sch2cfs.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 617
if _libs["libxux64.so"].has("_RevMtgeWamAdj", "cdecl"):
	_RevMtgeWamAdj = _libs["libxux64.so"].get("_RevMtgeWamAdj", "cdecl")
	_RevMtgeWamAdj.argtypes = [c_int, c_int, c_int]
	_RevMtgeWamAdj.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 618
if _libs["libxux64.so"].has("_RevMtgeCFCalc", "cdecl"):
	_RevMtgeCFCalc = _libs["libxux64.so"].get("_RevMtgeCFCalc", "cdecl")
	_RevMtgeCFCalc.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(POINTER(None))]
	_RevMtgeCFCalc.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 619
if _libs["libxux64.so"].has("_RevMtgeCFCalcH", "cdecl"):
	_RevMtgeCFCalcH = _libs["libxux64.so"].get("_RevMtgeCFCalcH", "cdecl")
	_RevMtgeCFCalcH.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_RevMtgeCFCalcH.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 620
if _libs["libxux64.so"].has("_tsyModelRate", "cdecl"):
	_tsyModelRate = _libs["libxux64.so"].get("_tsyModelRate", "cdecl")
	_tsyModelRate.argtypes = [c_double, POINTER(c_double), c_int]
	_tsyModelRate.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 621
if _libs["libxux64.so"].has("_NSSRate", "cdecl"):
	_NSSRate = _libs["libxux64.so"].get("_NSSRate", "cdecl")
	_NSSRate.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_double]
	_NSSRate.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 622
if _libs["libxux64.so"].has("_NSRate", "cdecl"):
	_NSRate = _libs["libxux64.so"].get("_NSRate", "cdecl")
	_NSRate.argtypes = [c_double, c_double, c_double, c_double, c_double]
	_NSRate.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 747
if _libs["libxux64.so"].has("_pdfvec", "cdecl"):
	_pdfvec = _libs["libxux64.so"].get("_pdfvec", "cdecl")
	_pdfvec.argtypes = [c_int, c_double, c_double, c_double, POINTER(c_double), POINTER(c_double), c_int]
	_pdfvec.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 749
if _libs["libxux64.so"].has("_direction", "cdecl"):
	_direction = _libs["libxux64.so"].get("_direction", "cdecl")
	_direction.argtypes = [c_int, POINTER(c_double)]
	_direction.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 750
if _libs["libxux64.so"].has("_cdf_gaussian", "cdecl"):
	_cdf_gaussian = _libs["libxux64.so"].get("_cdf_gaussian", "cdecl")
	_cdf_gaussian.argtypes = [c_double]
	_cdf_gaussian.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 751
if _libs["libxux64.so"].has("_inverse_cdf_gaussian", "cdecl"):
	_inverse_cdf_gaussian = _libs["libxux64.so"].get("_inverse_cdf_gaussian", "cdecl")
	_inverse_cdf_gaussian.argtypes = [c_double]
	_inverse_cdf_gaussian.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 752
if _libs["libxux64.so"].has("_distr", "cdecl"):
	_distr = _libs["libxux64.so"].get("_distr", "cdecl")
	_distr.argtypes = [c_double, c_int, c_double, c_double]
	_distr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 753
if _libs["libxux64.so"].has("_distrZ", "cdecl"):
	_distrZ = _libs["libxux64.so"].get("_distrZ", "cdecl")
	_distrZ.argtypes = [c_double, c_int, c_double, c_double]
	_distrZ.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 754
if _libs["libxux64.so"].has("_distrZb", "cdecl"):
	_distrZb = _libs["libxux64.so"].get("_distrZb", "cdecl")
	_distrZb.argtypes = [c_double, c_int, c_double, c_double, c_double, c_double]
	_distrZb.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 755
if _libs["libxux64.so"].has("_correlogram", "cdecl"):
	_correlogram = _libs["libxux64.so"].get("_correlogram", "cdecl")
	_correlogram.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_correlogram.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 757
if _libs["libxux64.so"].has("calHst", "cdecl"):
	calHst = _libs["libxux64.so"].get("calHst", "cdecl")
	calHst.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_int)]
	calHst.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 759
if _libs["libxux64.so"].has("hstgrm", "cdecl"):
	hstgrm = _libs["libxux64.so"].get("hstgrm", "cdecl")
	hstgrm.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_int)]
	hstgrm.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 783
class struct_anon_38(Structure):
	pass

struct_anon_38.__slots__ = [
	'k',
	'n',
	'name',
	'm',
]
struct_anon_38._fields_ = [
	('k', c_int),
	('n', c_int),
	('name', POINTER(c_char) * int(80)),
	('m', POINTER(POINTER(c_double))),
]

DMAT = struct_anon_38# /apps/fafa/pyx/anPy/afa/xu.h: 783

# /apps/fafa/pyx/anPy/afa/xu.h: 787
if _libs["libxux64.so"].has("_xprintf", "cdecl"):
	_func = _libs["libxux64.so"].get("_xprintf", "cdecl")
	_restype = c_int
	_errcheck = None
	_argtypes = [POINTER(FILE), String]
	_xprintf = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /apps/fafa/pyx/anPy/afa/xu.h: 788
if _libs["libxux64.so"].has("_open_file", "cdecl"):
	_open_file = _libs["libxux64.so"].get("_open_file", "cdecl")
	_open_file.argtypes = [String, String]
	_open_file.restype = POINTER(FILE)

# /apps/fafa/pyx/anPy/afa/xu.h: 789
if _libs["libxux64.so"].has("_xopen", "cdecl"):
	_xopen = _libs["libxux64.so"].get("_xopen", "cdecl")
	_xopen.argtypes = [String, String]
	_xopen.restype = POINTER(FILE)

# /apps/fafa/pyx/anPy/afa/xu.h: 790
if _libs["libxux64.so"].has("_scan_dmat_f", "cdecl"):
	_scan_dmat_f = _libs["libxux64.so"].get("_scan_dmat_f", "cdecl")
	_scan_dmat_f.argtypes = [String]
	_scan_dmat_f.restype = POINTER(DMAT)

# /apps/fafa/pyx/anPy/afa/xu.h: 791
if _libs["libxux64.so"].has("_scan_dmat", "cdecl"):
	_scan_dmat = _libs["libxux64.so"].get("_scan_dmat", "cdecl")
	_scan_dmat.argtypes = [POINTER(FILE)]
	_scan_dmat.restype = POINTER(DMAT)

# /apps/fafa/pyx/anPy/afa/xu.h: 792
if _libs["libxux64.so"].has("_scan_mat_f", "cdecl"):
	_scan_mat_f = _libs["libxux64.so"].get("_scan_mat_f", "cdecl")
	_scan_mat_f.argtypes = [String, POINTER(c_int), POINTER(c_int)]
	_scan_mat_f.restype = POINTER(POINTER(c_double))

# /apps/fafa/pyx/anPy/afa/xu.h: 793
if _libs["libxux64.so"].has("_scan_mat", "cdecl"):
	_scan_mat = _libs["libxux64.so"].get("_scan_mat", "cdecl")
	_scan_mat.argtypes = [POINTER(FILE), POINTER(c_int), POINTER(c_int)]
	_scan_mat.restype = POINTER(POINTER(c_double))

# /apps/fafa/pyx/anPy/afa/xu.h: 794
if _libs["libxux64.so"].has("_prn_dmat", "cdecl"):
	_prn_dmat = _libs["libxux64.so"].get("_prn_dmat", "cdecl")
	_prn_dmat.argtypes = [POINTER(FILE), POINTER(DMAT), c_int, c_int, c_int]
	_prn_dmat.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 795
if _libs["libxux64.so"].has("_int_size", "cdecl"):
	_int_size = _libs["libxux64.so"].get("_int_size", "cdecl")
	_int_size.argtypes = [c_double]
	_int_size.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 796
if _libs["libxux64.so"].has("_substr", "cdecl"):
	_substr = _libs["libxux64.so"].get("_substr", "cdecl")
	_substr.argtypes = [String, c_int, c_int]
	if sizeof(c_int) == sizeof(c_void_p):
		_substr.restype = ReturnString
	else:
		_substr.restype = String
		_substr.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 797
if _libs["libxux64.so"].has("_substrX", "cdecl"):
	_substrX = _libs["libxux64.so"].get("_substrX", "cdecl")
	_substrX.argtypes = [String, c_int, c_int, String, String]
	if sizeof(c_int) == sizeof(c_void_p):
		_substrX.restype = ReturnString
	else:
		_substrX.restype = String
		_substrX.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 798
if _libs["libxux64.so"].has("_findRpl", "cdecl"):
	_findRpl = _libs["libxux64.so"].get("_findRpl", "cdecl")
	_findRpl.argtypes = [String, String, String, c_int]
	if sizeof(c_int) == sizeof(c_void_p):
		_findRpl.restype = ReturnString
	else:
		_findRpl.restype = String
		_findRpl.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 799
if _libs["libxux64.so"].has("_strupper", "cdecl"):
	_strupper = _libs["libxux64.so"].get("_strupper", "cdecl")
	_strupper.argtypes = [String]
	_strupper.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 800
if _libs["libxux64.so"].has("_strlower", "cdecl"):
	_strlower = _libs["libxux64.so"].get("_strlower", "cdecl")
	_strlower.argtypes = [String]
	_strlower.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 801
if _libs["libxux64.so"].has("_str1stcap", "cdecl"):
	_str1stcap = _libs["libxux64.so"].get("_str1stcap", "cdecl")
	_str1stcap.argtypes = [String]
	_str1stcap.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 802
if _libs["libxux64.so"].has("findNamKey", "cdecl"):
	findNamKey = _libs["libxux64.so"].get("findNamKey", "cdecl")
	findNamKey.argtypes = [String, String]
	findNamKey.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 803
if _libs["libxux64.so"].has("findNamKeyCase", "cdecl"):
	findNamKeyCase = _libs["libxux64.so"].get("findNamKeyCase", "cdecl")
	findNamKeyCase.argtypes = [String, String]
	findNamKeyCase.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 804
if _libs["libxux64.so"].has("uniqueNumKey", "cdecl"):
	uniqueNumKey = _libs["libxux64.so"].get("uniqueNumKey", "cdecl")
	uniqueNumKey.argtypes = [POINTER(c_double), POINTER(c_int), c_int]
	uniqueNumKey.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 805
if _libs["libxux64.so"].has("uniqueNamKeyCase", "cdecl"):
	uniqueNamKeyCase = _libs["libxux64.so"].get("uniqueNamKeyCase", "cdecl")
	uniqueNamKeyCase.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int), c_int]
	uniqueNamKeyCase.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 806
if _libs["libxux64.so"].has("uniqueNamKey", "cdecl"):
	uniqueNamKey = _libs["libxux64.so"].get("uniqueNamKey", "cdecl")
	uniqueNamKey.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int), c_int]
	uniqueNamKey.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 807
if _libs["libxux64.so"].has("_getsuffix", "cdecl"):
	_getsuffix = _libs["libxux64.so"].get("_getsuffix", "cdecl")
	_getsuffix.argtypes = [String, String, String]
	_getsuffix.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 808
if _libs["libxux64.so"].has("_getprefix", "cdecl"):
	_getprefix = _libs["libxux64.so"].get("_getprefix", "cdecl")
	_getprefix.argtypes = [String, String, String]
	_getprefix.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 809
if _libs["libxux64.so"].has("_iobvec", "cdecl"):
	_iobvec = _libs["libxux64.so"].get("_iobvec", "cdecl")
	_iobvec.argtypes = [c_int, c_int, c_int, POINTER(None), String, c_int]
	_iobvec.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 810
if _libs["libxux64.so"].has("_getstr", "cdecl"):
	_getstr = _libs["libxux64.so"].get("_getstr", "cdecl")
	_getstr.argtypes = [String, String, POINTER(c_int)]
	_getstr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 811
if _libs["libxux64.so"].has("isAccounting", "cdecl"):
	isAccounting = _libs["libxux64.so"].get("isAccounting", "cdecl")
	isAccounting.argtypes = [String, POINTER(c_double)]
	isAccounting.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 812
if _libs["libxux64.so"].has("isString", "cdecl"):
	isString = _libs["libxux64.so"].get("isString", "cdecl")
	isString.argtypes = [String, POINTER(c_int), POINTER(POINTER(c_char))]
	isString.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 813
if _libs["libxux64.so"].has("isBackslash", "cdecl"):
	isBackslash = _libs["libxux64.so"].get("isBackslash", "cdecl")
	isBackslash.argtypes = [String, c_int]
	isBackslash.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 814
if _libs["libxux64.so"].has("isOpr", "cdecl"):
	isOpr = _libs["libxux64.so"].get("isOpr", "cdecl")
	isOpr.argtypes = [String, POINTER(c_int), c_int, String]
	isOpr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 815
if _libs["libxux64.so"].has("isDlmr", "cdecl"):
	isDlmr = _libs["libxux64.so"].get("isDlmr", "cdecl")
	isDlmr.argtypes = [String, POINTER(c_int), c_int, String]
	isDlmr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 816
if _libs["libxux64.so"].has("isQuote", "cdecl"):
	isQuote = _libs["libxux64.so"].get("isQuote", "cdecl")
	isQuote.argtypes = [String, POINTER(c_int), c_int, String]
	isQuote.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 817
if _libs["libxux64.so"].has("isSpace", "cdecl"):
	isSpace = _libs["libxux64.so"].get("isSpace", "cdecl")
	isSpace.argtypes = [String, POINTER(c_int)]
	isSpace.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 818
if _libs["libxux64.so"].has("isConst", "cdecl"):
	isConst = _libs["libxux64.so"].get("isConst", "cdecl")
	isConst.argtypes = [String, POINTER(c_int)]
	isConst.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 819
if _libs["libxux64.so"].has("isReal", "cdecl"):
	isReal = _libs["libxux64.so"].get("isReal", "cdecl")
	isReal.argtypes = [String, POINTER(c_int)]
	isReal.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 820
if _libs["libxux64.so"].has("isIdf", "cdecl"):
	isIdf = _libs["libxux64.so"].get("isIdf", "cdecl")
	isIdf.argtypes = [String, POINTER(c_int)]
	isIdf.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 821
if _libs["libxux64.so"].has("isInteger", "cdecl"):
	isInteger = _libs["libxux64.so"].get("isInteger", "cdecl")
	isInteger.argtypes = [String, POINTER(c_int)]
	isInteger.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 822
if _libs["libxux64.so"].has("isVar", "cdecl"):
	isVar = _libs["libxux64.so"].get("isVar", "cdecl")
	isVar.argtypes = [String, POINTER(c_int)]
	isVar.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 823
if _libs["libxux64.so"].has("isDsign", "cdecl"):
	isDsign = _libs["libxux64.so"].get("isDsign", "cdecl")
	isDsign.argtypes = [String, POINTER(c_int)]
	isDsign.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 824
if _libs["libxux64.so"].has("cvt_dlmr", "cdecl"):
	cvt_dlmr = _libs["libxux64.so"].get("cvt_dlmr", "cdecl")
	cvt_dlmr.argtypes = [String, String]
	cvt_dlmr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 825
if _libs["libxux64.so"].has("hchr", "cdecl"):
	hchr = _libs["libxux64.so"].get("hchr", "cdecl")
	hchr.argtypes = [String]
	if sizeof(c_int) == sizeof(c_void_p):
		hchr.restype = ReturnString
	else:
		hchr.restype = String
		hchr.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 826
if _libs["libxux64.so"].has("_frwb", "cdecl"):
	_frwb = _libs["libxux64.so"].get("_frwb", "cdecl")
	_frwb.argtypes = [String, String, c_int, c_int, POINTER(None)]
	_frwb.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 827
if _libs["libxux64.so"].has("vryfname", "cdecl"):
	vryfname = _libs["libxux64.so"].get("vryfname", "cdecl")
	vryfname.argtypes = [String, POINTER(FILE)]
	vryfname.restype = POINTER(FILE)

# /apps/fafa/pyx/anPy/afa/xu.h: 828
if _libs["libxux64.so"].has("ixOpr", "cdecl"):
	ixOpr = _libs["libxux64.so"].get("ixOpr", "cdecl")
	ixOpr.argtypes = [String, POINTER(c_int), c_int, String, c_int]
	ixOpr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 829
for _lib in _libs.values():
	if not _lib.has("spChr", "cdecl"):
		continue
	spChr = _lib.get("spChr", "cdecl")
	spChr.argtypes = [String, String, c_int, String]
	if sizeof(c_int) == sizeof(c_void_p):
		spChr.restype = ReturnString
	else:
		spChr.restype = String
		spChr.errcheck = ReturnString
	break

# /apps/fafa/pyx/anPy/afa/xu.h: 830
if _libs["libxux64.so"].has("spcStr", "cdecl"):
	_func = _libs["libxux64.so"].get("spcStr", "cdecl")
	_restype = String
	_errcheck = None
	_argtypes = [String, String, c_int, c_int]
	spcStr = _variadic_function(_func,_restype,_argtypes,_errcheck)

# /apps/fafa/pyx/anPy/afa/xu.h: 831
if _libs["libxux64.so"].has("ixDlmr", "cdecl"):
	ixDlmr = _libs["libxux64.so"].get("ixDlmr", "cdecl")
	ixDlmr.argtypes = [String, POINTER(c_int), POINTER(POINTER(c_char)), c_int]
	ixDlmr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 832
if _libs["libxux64.so"].has("splitFix", "cdecl"):
	splitFix = _libs["libxux64.so"].get("splitFix", "cdecl")
	splitFix.argtypes = [POINTER(POINTER(POINTER(c_char))), String, POINTER(c_int), c_int]
	splitFix.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 833
if _libs["libxux64.so"].has("splitDlmr", "cdecl"):
	splitDlmr = _libs["libxux64.so"].get("splitDlmr", "cdecl")
	splitDlmr.argtypes = [POINTER(POINTER(POINTER(c_char))), String, POINTER(POINTER(c_char)), c_int]
	splitDlmr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 834
if _libs["libxux64.so"].has("chop", "cdecl"):
	chop = _libs["libxux64.so"].get("chop", "cdecl")
	chop.argtypes = [String]
	chop.restype = c_size_t

# /apps/fafa/pyx/anPy/afa/xu.h: 835
if _libs["libxux64.so"].has("parseMtrx", "cdecl"):
	parseMtrx = _libs["libxux64.so"].get("parseMtrx", "cdecl")
	parseMtrx.argtypes = [POINTER(POINTER(c_int)), POINTER(POINTER(POINTER(c_char))), POINTER(c_int), POINTER(POINTER(POINTER(POINTER(c_char)))), POINTER(c_int), POINTER(POINTER(POINTER(c_double))), c_int, POINTER(POINTER(c_char)), POINTER(POINTER(c_char)), c_int, c_int, c_int]
	parseMtrx.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 837
if _libs["libxux64.so"].has("parseFix", "cdecl"):
	parseFix = _libs["libxux64.so"].get("parseFix", "cdecl")
	parseFix.argtypes = [POINTER(POINTER(c_int)), POINTER(POINTER(POINTER(c_char))), POINTER(c_int), POINTER(POINTER(POINTER(POINTER(c_char)))), POINTER(c_int), POINTER(POINTER(POINTER(c_double))), c_int, POINTER(POINTER(c_char)), POINTER(c_int), c_int, c_int, c_int]
	parseFix.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 839
if _libs["libxux64.so"].has("parseTbl", "cdecl"):
	parseTbl = _libs["libxux64.so"].get("parseTbl", "cdecl")
	parseTbl.argtypes = [POINTER(POINTER(c_int)), POINTER(POINTER(POINTER(c_char))), POINTER(c_int), POINTER(POINTER(POINTER(POINTER(c_char)))), POINTER(c_int), POINTER(POINTER(POINTER(c_double))), c_int, POINTER(POINTER(c_char)), POINTER(POINTER(c_char)), POINTER(c_int), c_int, c_int, c_int]
	parseTbl.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 841
if _libs["libxux64.so"].has("parseGetPair", "cdecl"):
	parseGetPair = _libs["libxux64.so"].get("parseGetPair", "cdecl")
	parseGetPair.argtypes = [String, String, String, POINTER(POINTER(POINTER(c_char))), POINTER(POINTER(POINTER(c_char)))]
	parseGetPair.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 842
if _libs["libxux64.so"].has("explodeStr", "cdecl"):
	explodeStr = _libs["libxux64.so"].get("explodeStr", "cdecl")
	explodeStr.argtypes = [String, String, POINTER(POINTER(POINTER(c_char)))]
	explodeStr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 843
if _libs["libxux64.so"].has("implodeStr", "cdecl"):
	implodeStr = _libs["libxux64.so"].get("implodeStr", "cdecl")
	implodeStr.argtypes = [String, POINTER(POINTER(c_char)), c_int]
	if sizeof(c_int) == sizeof(c_void_p):
		implodeStr.restype = ReturnString
	else:
		implodeStr.restype = String
		implodeStr.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 844
if _libs["libxux64.so"].has("lcSpace", "cdecl"):
	lcSpace = _libs["libxux64.so"].get("lcSpace", "cdecl")
	lcSpace.argtypes = [String, POINTER(c_int)]
	lcSpace.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 845
if _libs["libxux64.so"].has("rmSpace", "cdecl"):
	rmSpace = _libs["libxux64.so"].get("rmSpace", "cdecl")
	rmSpace.argtypes = [String]
	if sizeof(c_int) == sizeof(c_void_p):
		rmSpace.restype = ReturnString
	else:
		rmSpace.restype = String
		rmSpace.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 846
if _libs["libxux64.so"].has("trimStr", "cdecl"):
	trimStr = _libs["libxux64.so"].get("trimStr", "cdecl")
	trimStr.argtypes = [String]
	trimStr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 847
if _libs["libxux64.so"].has("_xopenX", "cdecl"):
	_xopenX = _libs["libxux64.so"].get("_xopenX", "cdecl")
	_xopenX.argtypes = [String, String, POINTER(c_int)]
	_xopenX.restype = POINTER(FILE)

# /apps/fafa/pyx/anPy/afa/xu.h: 848
if _libs["libxux64.so"].has("_pcloseX", "cdecl"):
	_pcloseX = _libs["libxux64.so"].get("_pcloseX", "cdecl")
	_pcloseX.argtypes = [POINTER(FILE)]
	_pcloseX.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 849
if _libs["libxux64.so"].has("_popenX", "cdecl"):
	_popenX = _libs["libxux64.so"].get("_popenX", "cdecl")
	_popenX.argtypes = [String, String]
	_popenX.restype = POINTER(FILE)

# /apps/fafa/pyx/anPy/afa/xu.h: 850
if _libs["libxux64.so"].has("read_file2strv", "cdecl"):
	read_file2strv = _libs["libxux64.so"].get("read_file2strv", "cdecl")
	read_file2strv.argtypes = [String, POINTER(POINTER(POINTER(c_char))), c_int]
	read_file2strv.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 851
if _libs["libxux64.so"].has("_file2strv", "cdecl"):
	_file2strv = _libs["libxux64.so"].get("_file2strv", "cdecl")
	_file2strv.argtypes = [POINTER(FILE), POINTER(POINTER(POINTER(c_char)))]
	_file2strv.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 852
if _libs["libxux64.so"].has("writ_file2db", "cdecl"):
	writ_file2db = _libs["libxux64.so"].get("writ_file2db", "cdecl")
	writ_file2db.argtypes = [String, String, String]
	writ_file2db.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 853
if _libs["libxux64.so"].has("read_db2strv", "cdecl"):
	read_db2strv = _libs["libxux64.so"].get("read_db2strv", "cdecl")
	read_db2strv.argtypes = [String, POINTER(POINTER(POINTER(c_char))), String]
	read_db2strv.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 854
if _libs["libxux64.so"].has("read_db2strx", "cdecl"):
	read_db2strx = _libs["libxux64.so"].get("read_db2strx", "cdecl")
	read_db2strx.argtypes = [String, String, POINTER(POINTER(c_char)), String]
	read_db2strx.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 855
if _libs["libxux64.so"].has("read_bigfile", "cdecl"):
	read_bigfile = _libs["libxux64.so"].get("read_bigfile", "cdecl")
	read_bigfile.argtypes = [POINTER(c_int), c_int, c_int, POINTER(FILE)]
	read_bigfile.restype = POINTER(c_ubyte)
	read_bigfile.errcheck = lambda v,*a : cast(v, c_void_p)

# /apps/fafa/pyx/anPy/afa/xu.h: 949
if _libs["libxux64.so"].has("_oas_m", "cdecl"):
	_oas_m = _libs["libxux64.so"].get("_oas_m", "cdecl")
	_oas_m.argtypes = [c_int, POINTER(POINTER(c_double)), POINTER(c_double), c_int, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(POINTER(c_double))]
	_oas_m.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 953
if _libs["libxux64.so"].has("_oas", "cdecl"):
	_oas = _libs["libxux64.so"].get("_oas", "cdecl")
	_oas.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_int, c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	_oas.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 955
if _libs["libxux64.so"].has("_cal_pr", "cdecl"):
	_cal_pr = _libs["libxux64.so"].get("_cal_pr", "cdecl")
	_cal_pr.argtypes = [c_int, c_double, c_int, c_double, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	_cal_pr.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 957
if _libs["libxux64.so"].has("_cal_taylor_pr", "cdecl"):
	_cal_taylor_pr = _libs["libxux64.so"].get("_cal_taylor_pr", "cdecl")
	_cal_taylor_pr.argtypes = [c_int, POINTER(c_double), c_double]
	_cal_taylor_pr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 958
if _libs["libxux64.so"].has("_cal_oas", "cdecl"):
	_cal_oas = _libs["libxux64.so"].get("_cal_oas", "cdecl")
	_cal_oas.argtypes = [c_int, POINTER(c_double), c_double]
	_cal_oas.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 959
if _libs["libxux64.so"].has("_poly", "cdecl"):
	_poly = _libs["libxux64.so"].get("_poly", "cdecl")
	_poly.argtypes = [c_double, c_int, POINTER(c_double)]
	_poly.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 960
if _libs["libxux64.so"].has("_cal_taylor", "cdecl"):
	_cal_taylor = _libs["libxux64.so"].get("_cal_taylor", "cdecl")
	_cal_taylor.argtypes = [c_int, POINTER(c_double), POINTER(c_double), c_double, POINTER(c_double)]
	_cal_taylor.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 982
class struct_anon_39(Structure):
	pass

struct_anon_39.__slots__ = [
	'val',
	'delta',
	'gamma',
	'vega',
	'theta',
]
struct_anon_39._fields_ = [
	('val', c_double),
	('delta', c_double),
	('gamma', c_double),
	('vega', c_double),
	('theta', c_double),
]

OPTION_STRUCT = struct_anon_39# /apps/fafa/pyx/anPy/afa/xu.h: 982

# /apps/fafa/pyx/anPy/afa/xu.h: 993
if _libs["libxux64.so"].has("_binm", "cdecl"):
	_binm = _libs["libxux64.so"].get("_binm", "cdecl")
	_binm.argtypes = [c_int, c_int]
	_binm.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 994
if _libs["libxux64.so"].has("bnm_ame", "cdecl"):
	bnm_ame = _libs["libxux64.so"].get("bnm_ame", "cdecl")
	bnm_ame.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, POINTER(OPTION_STRUCT)]
	bnm_ame.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 997
if _libs["libxux64.so"].has("bnm_eur", "cdecl"):
	bnm_eur = _libs["libxux64.so"].get("bnm_eur", "cdecl")
	bnm_eur.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, c_int, POINTER(OPTION_STRUCT)]
	bnm_eur.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1000
if _libs["libxux64.so"].has("putcallb", "cdecl"):
	putcallb = _libs["libxux64.so"].get("putcallb", "cdecl")
	putcallb.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	putcallb.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1004
if _libs["libxux64.so"].has("black_div", "cdecl"):
	black_div = _libs["libxux64.so"].get("black_div", "cdecl")
	black_div.argtypes = [c_int, c_double, c_double, c_double, c_double, c_double, c_double, POINTER(OPTION_STRUCT)]
	black_div.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1007
if _libs["libxux64.so"].has("callbs_cash", "cdecl"):
	callbs_cash = _libs["libxux64.so"].get("callbs_cash", "cdecl")
	callbs_cash.argtypes = [c_double, c_double, c_double, c_double, c_double, POINTER(OPTION_STRUCT)]
	callbs_cash.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1010
if _libs["libxux64.so"].has("callbs_cashx", "cdecl"):
	callbs_cashx = _libs["libxux64.so"].get("callbs_cashx", "cdecl")
	callbs_cashx.argtypes = [c_double, c_double, c_double, c_double, c_double]
	callbs_cashx.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1012
if _libs["libxux64.so"].has("callbs_fut", "cdecl"):
	callbs_fut = _libs["libxux64.so"].get("callbs_fut", "cdecl")
	callbs_fut.argtypes = [c_double, c_double, c_double, c_double, c_double, POINTER(OPTION_STRUCT)]
	callbs_fut.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1014
if _libs["libxux64.so"].has("callbs_futx", "cdecl"):
	callbs_futx = _libs["libxux64.so"].get("callbs_futx", "cdecl")
	callbs_futx.argtypes = [c_double, c_double, c_double, c_double, c_double]
	callbs_futx.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1016
if _libs["libxux64.so"].has("putbs_cash", "cdecl"):
	putbs_cash = _libs["libxux64.so"].get("putbs_cash", "cdecl")
	putbs_cash.argtypes = [c_double, c_double, c_double, c_double, c_double, POINTER(OPTION_STRUCT)]
	putbs_cash.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1019
if _libs["libxux64.so"].has("putbs_cashx", "cdecl"):
	putbs_cashx = _libs["libxux64.so"].get("putbs_cashx", "cdecl")
	putbs_cashx.argtypes = [c_double, c_double, c_double, c_double, c_double]
	putbs_cashx.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1021
if _libs["libxux64.so"].has("putbs_fut", "cdecl"):
	putbs_fut = _libs["libxux64.so"].get("putbs_fut", "cdecl")
	putbs_fut.argtypes = [c_double, c_double, c_double, c_double, c_double, POINTER(OPTION_STRUCT)]
	putbs_fut.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1024
if _libs["libxux64.so"].has("putbs_futx", "cdecl"):
	putbs_futx = _libs["libxux64.so"].get("putbs_futx", "cdecl")
	putbs_futx.argtypes = [c_double, c_double, c_double, c_double, c_double]
	putbs_futx.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1026
if _libs["libxux64.so"].has("putcall", "cdecl"):
	putcall = _libs["libxux64.so"].get("putcall", "cdecl")
	putcall.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double, c_int, c_int, c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	putcall.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1073
class struct_anon_40(Structure):
	pass

struct_anon_40.__slots__ = [
	'dsr',
	'price',
	'yield',
	'coupon',
	'disc',
	'sy',
	'ftyp',
	'fq',
	'term',
	'nh',
	'hdy',
	'settle',
	'dated',
	'cutoff',
	'fpmt',
	'mat',
]
struct_anon_40._fields_ = [
	('dsr', String),
	('price', c_double),
	('yield', c_double),
	('coupon', c_double),
	('disc', c_double),
	('sy', c_double),
	('ftyp', c_int),
	('fq', c_double),
	('term', c_double),
	('nh', c_int),
	('hdy', POINTER(POINTER(c_char))),
	('settle', c_long),
	('dated', c_long),
	('cutoff', c_long),
	('fpmt', c_long),
	('mat', c_long),
]

XYCV = struct_anon_40# /apps/fafa/pyx/anPy/afa/xu.h: 1073

# /apps/fafa/pyx/anPy/afa/xu.h: 1086
class struct_anon_41(Structure):
	pass

struct_anon_41.__slots__ = [
	'disc',
	'tfr',
	'sr',
	'sy',
	'npb',
	'nud',
	'dud',
	'pdud',
	'ptsy',
]
struct_anon_41._fields_ = [
	('disc', c_double),
	('tfr', c_double),
	('sr', c_double),
	('sy', c_double),
	('npb', c_double),
	('nud', c_int),
	('dud', POINTER(c_double)),
	('pdud', POINTER(POINTER(c_double))),
	('ptsy', POINTER(POINTER(c_double))),
]

BNODE = struct_anon_41# /apps/fafa/pyx/anPy/afa/xu.h: 1086

# /apps/fafa/pyx/anPy/afa/xu.h: 1111
class struct_anon_42(Structure):
	pass

struct_anon_42.__slots__ = [
	'fntsy',
	'ntsy',
	'bflg',
	'vfrwd',
	'vdisc',
	'vtfr',
	'btsy',
	'prd',
	'knode',
	'nmonth',
	'pb',
	'km',
	'kn',
	'kp',
	'qap',
	'qbp',
	'qam',
	'qbm',
	'tol',
	'bound',
	'vsy',
	'bnode',
]
struct_anon_42._fields_ = [
	('fntsy', String),
	('ntsy', c_int),
	('bflg', c_int),
	('vfrwd', POINTER(c_double)),
	('vdisc', POINTER(c_double)),
	('vtfr', POINTER(c_double)),
	('btsy', POINTER(POINTER(XYCV))),
	('prd', c_int),
	('knode', c_int),
	('nmonth', c_int),
	('pb', POINTER(c_double)),
	('km', POINTER(c_double)),
	('kn', POINTER(c_double)),
	('kp', POINTER(c_double)),
	('qap', POINTER(c_double)),
	('qbp', POINTER(c_double)),
	('qam', POINTER(c_double)),
	('qbm', POINTER(c_double)),
	('tol', c_double),
	('bound', POINTER(c_int)),
	('vsy', POINTER(c_double)),
	('bnode', POINTER(POINTER(BNODE))),
]

BTREE = struct_anon_42# /apps/fafa/pyx/anPy/afa/xu.h: 1111

# /apps/fafa/pyx/anPy/afa/xu.h: 1114
if _libs["libxux64.so"].has("c_parcpn", "cdecl"):
	c_parcpn = _libs["libxux64.so"].get("c_parcpn", "cdecl")
	c_parcpn.argtypes = [c_int, c_int, POINTER(c_double), POINTER(c_double)]
	c_parcpn.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1115
if _libs["libxux64.so"].has("c_pf", "cdecl"):
	c_pf = _libs["libxux64.so"].get("c_pf", "cdecl")
	c_pf.argtypes = [c_int, c_int, c_double, POINTER(c_double), POINTER(c_double), c_int]
	c_pf.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1116
if _libs["libxux64.so"].has("c_cmt", "cdecl"):
	c_cmt = _libs["libxux64.so"].get("c_cmt", "cdecl")
	c_cmt.argtypes = [POINTER(POINTER(XYCV)), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
	c_cmt.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1118
if _libs["libxux64.so"].has("c_frwdr", "cdecl"):
	c_frwdr = _libs["libxux64.so"].get("c_frwdr", "cdecl")
	c_frwdr.argtypes = [POINTER(POINTER(XYCV)), c_int, POINTER(c_double), c_int]
	c_frwdr.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1119
if _libs["libxux64.so"].has("c_pt", "cdecl"):
	c_pt = _libs["libxux64.so"].get("c_pt", "cdecl")
	c_pt.argtypes = [POINTER(POINTER(XYCV)), c_int]
	c_pt.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1120
if _libs["libxux64.so"].has("c_tsycurve", "cdecl"):
	c_tsycurve = _libs["libxux64.so"].get("c_tsycurve", "cdecl")
	c_tsycurve.argtypes = [c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	c_tsycurve.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1123
if _libs["libxux64.so"].has("cby_irr", "cdecl"):
	cby_irr = _libs["libxux64.so"].get("cby_irr", "cdecl")
	cby_irr.argtypes = [c_double, c_double, c_double]
	cby_irr.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1141
if _libs["libxux64.so"].has("pearsn", "cdecl"):
	pearsn = _libs["libxux64.so"].get("pearsn", "cdecl")
	pearsn.argtypes = [POINTER(c_double), POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double), POINTER(c_double)]
	pearsn.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1142
if _libs["libxux64.so"].has("betai", "cdecl"):
	betai = _libs["libxux64.so"].get("betai", "cdecl")
	betai.argtypes = [c_double, c_double, c_double]
	betai.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1143
if _libs["libxux64.so"].has("betacf", "cdecl"):
	betacf = _libs["libxux64.so"].get("betacf", "cdecl")
	betacf.argtypes = [c_double, c_double, c_double]
	betacf.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1144
if _libs["libxux64.so"].has("beta", "cdecl"):
	beta = _libs["libxux64.so"].get("beta", "cdecl")
	beta.argtypes = [c_double, c_double]
	beta.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1145
if _libs["libxux64.so"].has("gammln", "cdecl"):
	gammln = _libs["libxux64.so"].get("gammln", "cdecl")
	gammln.argtypes = [c_double]
	gammln.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1146
if _libs["libxux64.so"].has("bico", "cdecl"):
	bico = _libs["libxux64.so"].get("bico", "cdecl")
	bico.argtypes = [c_int, c_int]
	bico.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1147
if _libs["libxux64.so"].has("factrl", "cdecl"):
	factrl = _libs["libxux64.so"].get("factrl", "cdecl")
	factrl.argtypes = [c_int]
	factrl.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1148
if _libs["libxux64.so"].has("factln", "cdecl"):
	factln = _libs["libxux64.so"].get("factln", "cdecl")
	factln.argtypes = [c_int]
	factln.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1149
if _libs["libxux64.so"].has("ksone", "cdecl"):
	ksone = _libs["libxux64.so"].get("ksone", "cdecl")
	ksone.argtypes = [POINTER(c_double), c_int, CFUNCTYPE(UNCHECKED(c_double), ), POINTER(c_double), POINTER(c_double)]
	ksone.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1150
if _libs["libxux64.so"].has("kstwo", "cdecl"):
	kstwo = _libs["libxux64.so"].get("kstwo", "cdecl")
	kstwo.argtypes = [POINTER(c_double), c_int, POINTER(c_double), c_int, POINTER(c_double), POINTER(c_double)]
	kstwo.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1152
if _libs["libxux64.so"].has("probks", "cdecl"):
	probks = _libs["libxux64.so"].get("probks", "cdecl")
	probks.argtypes = [c_double]
	probks.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1153
if _libs["libxux64.so"].has("gammp", "cdecl"):
	gammp = _libs["libxux64.so"].get("gammp", "cdecl")
	gammp.argtypes = [c_double, c_double]
	gammp.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1154
if _libs["libxux64.so"].has("gammq", "cdecl"):
	gammq = _libs["libxux64.so"].get("gammq", "cdecl")
	gammq.argtypes = [c_double, c_double]
	gammq.restype = c_double

# /apps/fafa/pyx/anPy/afa/xu.h: 1155
if _libs["libxux64.so"].has("gser", "cdecl"):
	gser = _libs["libxux64.so"].get("gser", "cdecl")
	gser.argtypes = [POINTER(c_double), c_double, c_double, POINTER(c_double)]
	gser.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1156
if _libs["libxux64.so"].has("gcf", "cdecl"):
	gcf = _libs["libxux64.so"].get("gcf", "cdecl")
	gcf.argtypes = [POINTER(c_double), c_double, c_double, POINTER(c_double)]
	gcf.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1187
class struct_anon_43(Structure):
	pass

struct_anon_43.__slots__ = [
	'm',
	'name',
	'val',
]
struct_anon_43._fields_ = [
	('m', c_int),
	('name', POINTER(POINTER(c_char))),
	('val', POINTER(POINTER(c_char))),
]

ENTRY = struct_anon_43# /apps/fafa/pyx/anPy/afa/xu.h: 1187

# /apps/fafa/pyx/anPy/afa/xu.h: 1191
if _libs["libxux64.so"].has("prnq", "cdecl"):
	prnq = _libs["libxux64.so"].get("prnq", "cdecl")
	prnq.argtypes = [POINTER(ENTRY)]
	prnq.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1192
if _libs["libxux64.so"].has("cgiq", "cdecl"):
	cgiq = _libs["libxux64.so"].get("cgiq", "cdecl")
	cgiq.argtypes = [POINTER(ENTRY)]
	cgiq.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1193
if _libs["libxux64.so"].has("postq", "cdecl"):
	postq = _libs["libxux64.so"].get("postq", "cdecl")
	postq.argtypes = [POINTER(ENTRY)]
	postq.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1194
if _libs["libxux64.so"].has("getq", "cdecl"):
	getq = _libs["libxux64.so"].get("getq", "cdecl")
	getq.argtypes = [POINTER(ENTRY)]
	getq.restype = c_int

# /apps/fafa/pyx/anPy/afa/xu.h: 1195
if _libs["libxux64.so"].has("getword", "cdecl"):
	getword = _libs["libxux64.so"].get("getword", "cdecl")
	getword.argtypes = [String, c_char]
	if sizeof(c_int) == sizeof(c_void_p):
		getword.restype = ReturnString
	else:
		getword.restype = String
		getword.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 1196
if _libs["libxux64.so"].has("makeword", "cdecl"):
	makeword = _libs["libxux64.so"].get("makeword", "cdecl")
	makeword.argtypes = [String, c_char]
	if sizeof(c_int) == sizeof(c_void_p):
		makeword.restype = ReturnString
	else:
		makeword.restype = String
		makeword.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 1197
if _libs["libxux64.so"].has("fmakeword", "cdecl"):
	fmakeword = _libs["libxux64.so"].get("fmakeword", "cdecl")
	fmakeword.argtypes = [POINTER(FILE), c_char, POINTER(c_int)]
	if sizeof(c_int) == sizeof(c_void_p):
		fmakeword.restype = ReturnString
	else:
		fmakeword.restype = String
		fmakeword.errcheck = ReturnString

# /apps/fafa/pyx/anPy/afa/xu.h: 1198
if _libs["libxux64.so"].has("x2c", "cdecl"):
	x2c = _libs["libxux64.so"].get("x2c", "cdecl")
	x2c.argtypes = [String]
	x2c.restype = c_char

# /apps/fafa/pyx/anPy/afa/xu.h: 1199
if _libs["libxux64.so"].has("unescape_url", "cdecl"):
	unescape_url = _libs["libxux64.so"].get("unescape_url", "cdecl")
	unescape_url.argtypes = [String]
	unescape_url.restype = None

# /apps/fafa/pyx/anPy/afa/xu.h: 1200
if _libs["libxux64.so"].has("plustospace", "cdecl"):
	plustospace = _libs["libxux64.so"].get("plustospace", "cdecl")
	plustospace.argtypes = [String]
	plustospace.restype = None

# /apps/fafa/pyx/anPy/afa/std.h: 48
try:
	TRUE = (1 == 1)
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 49
try:
	FALSE = (not TRUE)
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 53
try:
	NROUND = 1E-14
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 57
try:
	TOL = 1E-9
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 61
try:
	NINF = (-999999)
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 65
try:
	SCHAR = 80
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 66
try:
	MCHAR = 256
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 67
try:
	LCHAR = 2048
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 68
try:
	HCHAR = 10240
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 69
try:
	MBUF = 128000
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 70
try:
	LBUF = 512000
except:
	pass

# /apps/fafa/pyx/anPy/afa/std.h: 71
try:
	MAXPAR = 200
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 6
try:
	HUGE = 1e15
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 7
try:
	DATEFORMAT = 12345678
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 14
def _eq(x, y):
	return ((fabs ((x - y))) <= NROUND)

# /apps/fafa/pyx/anPy/afa/xu.h: 15
def _ne(x, y):
	return ((fabs ((x - y))) > NROUND)

# /apps/fafa/pyx/anPy/afa/xu.h: 16
def _ge(x, y):
	return ((x - y) > (-NROUND))

# /apps/fafa/pyx/anPy/afa/xu.h: 17
def _le(x, y):
	return ((x - y) < NROUND)

# /apps/fafa/pyx/anPy/afa/xu.h: 18
def _between(x, l, h):
	return ((x >= l) and (x <= h))

# /apps/fafa/pyx/anPy/afa/xu.h: 19
def _xif(ev, x, y):
	return ev and x or y

# /apps/fafa/pyx/anPy/afa/xu.h: 20
def _sqrt(x):
	return (pow ((c_double (ord_if_char(x))).value, 0.5))

# /apps/fafa/pyx/anPy/afa/xu.h: 21
def _cbrt(x):
	return (pow ((c_double (ord_if_char(x))).value, 0.333333333333))

# /apps/fafa/pyx/anPy/afa/xu.h: 22
def _square(x):
	return (x * x)

# /apps/fafa/pyx/anPy/afa/xu.h: 23
def _cube(x):
	return ((x * x) * x)

# /apps/fafa/pyx/anPy/afa/xu.h: 24
def _max2(x, y):
	return (x > y) and x or y

# /apps/fafa/pyx/anPy/afa/xu.h: 25
def _min2(x, y):
	return (x > y) and y or x

# /apps/fafa/pyx/anPy/afa/xu.h: 26
def _clip(x, y, z):
	return (_max2 (x, (_min2 (y, z))))

# /apps/fafa/pyx/anPy/afa/xu.h: 27
def _fmod(x, y):
	return (x - (y * (c_int (ord_if_char((x / y)))).value))

# /apps/fafa/pyx/anPy/afa/xu.h: 30
def _duration1pct(p, u, d, bp, ac):
	return (((((u - d) / (p + ac)) / 2.) / bp) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 31
def _convex1pct(p, u, d, bp, ac):
	return ((((((((-2.) * p) + u) + d) / (p + ac)) / bp) / bp) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 32
def _dv01mm(p, u, d, bp):
	return (((((u - d) / 2.) / p) / bp) * 10000.)

# /apps/fafa/pyx/anPy/afa/xu.h: 33
def _yv01tck(p, u, d, bp):
	return ((1. / (((((u - d) / 2.) / p) / bp) * 10000)) / 3200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 34
def _risk1pct(p, u, d, bp):
	return (((((((u - d) / 2.) / p) / bp) * 10000.) / p) * 10000.)

# /apps/fafa/pyx/anPy/afa/xu.h: 38
def _prn_double(x, file):
	return (fprintf (file, '%g ', (c_double (ord_if_char(x))).value))

# /apps/fafa/pyx/anPy/afa/xu.h: 39
def _prn_char(x, file):
	return (fprintf (file, '%s ', x))

# /apps/fafa/pyx/anPy/afa/xu.h: 40
def _prn_return(file):
	return (fprintf (file, '\\n'))

# /apps/fafa/pyx/anPy/afa/xu.h: 42
def _mey2bey(x):
	return (((pow ((1. + (x / 1200.)), 6.)) - 1.) * 200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 43
def _mey2aey(x):
	return (((pow ((1. + (x / 1200.)), 12.)) - 1.) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 44
def _aey2bey(x):
	return (((pow ((1. + (x / 100.)), 0.5)) - 1.) * 200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 45
def _bey2mey(x):
	return (((pow ((1. + (x / 200.)), 0.1666666666667)) - 1.) * 1200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 46
def _aey2mey(x):
	return (((pow ((1. + (x / 100.)), 0.0833333333333)) - 1.) * 1200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 47
def _bey2aey(x):
	return (((pow ((1. + (x / 200.)), 2.)) - 1.) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 48
def _mey2exp(x):
	return ((log ((1. + (x / 1200.)))) * 1200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 49
def _bey2exp(x):
	return ((log ((1. + (x / 200.)))) * 200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 50
def _aey2exp(x):
	return ((log ((1. + (x / 100.)))) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 51
def _exp2aey(x):
	return (((exp ((x / 100.))) - 1.) * 100.)

# /apps/fafa/pyx/anPy/afa/xu.h: 52
def _exp2bey(x):
	return (((exp ((x / 200.))) - 1.) * 200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 53
def _exp2mey(x):
	return (((exp ((x / 1200.))) - 1.) * 1200.)

# /apps/fafa/pyx/anPy/afa/xu.h: 55
def _payment(abal, awac, aterm):
	return ((abal * awac) / (1. - (1. / (pow ((1. + awac), (aterm * 1.))))))

# /apps/fafa/pyx/anPy/afa/xu.h: 57
def _poreg(abal, awac, aterm):
	return ((_payment (abal, awac, aterm)) - (abal * awac))

# /apps/fafa/pyx/anPy/afa/xu.h: 59
def _poppy(abal, awac, aterm, asmm):
	return (abal + ((_poreg (abal, awac, aterm)) * asmm))

# /apps/fafa/pyx/anPy/afa/xu.h: 61
def _remain_bal(abal, awac, aterm, asmm):
	return (abal - ((abal * asmm) + ((_poreg (abal, awac, aterm)) * (1 - asmm))))

# /apps/fafa/pyx/anPy/afa/xu.h: 63
def _fq2gap(x):
	return (x <= 0) and 0 or (floor (((36000 / x) + 0.5)))

# /apps/fafa/pyx/anPy/afa/xu.h: 64
def _rcnv4fq(x, f, g):
	return (((pow ((1 + (x / f)), (f / g))) - 1) * g)

# /apps/fafa/pyx/anPy/afa/xu.h: 65
def _factor(r, t, k):
	return ((1. - (pow ((1. + r), (((-t) * 1.) + k)))) / (1. - (pow ((1. + r), ((-t) * 1.)))))

# /apps/fafa/pyx/anPy/afa/xu.h: 66
def _fv(pmt, r, t):
	return ((pmt * ((pow ((1. + r), (t * 1.))) - 1)) / r)

# /apps/fafa/pyx/anPy/afa/xu.h: 67
def _pmt(bal, r, t):
	return (r > 0) and ((bal * r) / (1 - (pow ((1. + r), ((-t) * 1.))))) or 0.0

# /apps/fafa/pyx/anPy/afa/xu.h: 68
def _pv(pmt, r, t):
	return ((pmt * (1. - (pow ((1. + r), ((-t) * 1.))))) / r)

# /apps/fafa/pyx/anPy/afa/xu.h: 69
def _term(pmt, r, fv):
	return ((log ((1. + ((fv * r) / pmt)))) / (log ((1 + r))))

# /apps/fafa/pyx/anPy/afa/xu.h: 70
def _cterm(r, fv, pv):
	return ((log ((fv / pv))) / (log ((1. + r))))

# /apps/fafa/pyx/anPy/afa/xu.h: 71
def _rate(fv, pv, t):
	return ((pow ((fv / pv), (1. / t))) - 1.0)

# /apps/fafa/pyx/anPy/afa/xu.h: 933
try:
	MAXT = 601
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 984
try:
	CALL = 0
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 985
try:
	PUT = 1
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 986
try:
	DIVN = 0
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 987
try:
	BEUR = 1
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 988
try:
	BAME = 2
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 989
try:
	CASH = 3
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 990
try:
	FUT = 4
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1052
try:
	NB = 200
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1053
try:
	INTERPOLATE = 1
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1054
try:
	STRIP = 2
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1179
try:
	MAX_STRING = 80
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1180
try:
	LF = 10
except:
	pass

# /apps/fafa/pyx/anPy/afa/xu.h: 1181
try:
	CR = 13
except:
	pass

# No inserted files

# No prefix-stripping

# include all private prefix _{function}
all_vars = {k:v for (k,v) in globals().items() if callable(v)}
__all__ = list(all_vars.keys())
