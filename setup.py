#!/usr/bin/env python

import os, sys
import optparse
import subprocess
import tempfile
from distutils.core import setup, Extension
import distutils.ccompiler

def msg(s):
    sys.stdout.write(s)
    sys.stdout.write('\n')
    sys.stdout.flush()

p = optparse.OptionParser('%prog [options] [-- [setup_options]]')
p.add_option('--picosat-dir', help='The directory where PicoSAT distribution ' \
             'has been extracted and compiled', default="./")
p.add_option('--extra-swig-code', help='file with extra SWIG code')
p.add_option('--extra-c-include-code', help='file with extra C headers')
p.add_option('--extra-swig-include-code',
             help='file with extra SWIG include directives')
p.add_option('--extra-c-static-code', help='file with extra C static code')
p.add_option('--extra-c-inline-code', help='file with extra C inline code')
p.add_option('--extra-python-code', help='file with extra Python code')
p.add_option('--extra-compile-args', help='extra compilation args', default="")
p.add_option('--extra-link-args', help='extra link args', default="")
p.add_option('--extra-libraries', help='extra libraries', default="")
p.add_option('--swig-only', help='only run SWIG '
             '(do not compile generated bindings)', action='store_true')
p.add_option('--swig-tool', help='custom path to the swig executable')
p.add_option('--extra-include-dir', help='extra include directories',
             action='append', default=[])
p.add_option('--extra-lib-dir', help='extra library directories',
             action='append', default=[])

try:
    idx = sys.argv.index('--')
    optargs = sys.argv[1:idx]
    argv = sys.argv[idx+1:]
except ValueError:
    optargs, argv = sys.argv[1:], []
sys.argv = [sys.argv[0]] + argv

def error(msg):
    sys.stderr.write(msg)
    sys.stderr.write('\n')
    p.print_help(sys.stderr)
    sys.exit(-1)

opts, args = p.parse_args(optargs)

if args:
    sys.argv = [sys.argv[0]] + args + sys.argv[1:]

with open(os.path.join(os.path.dirname(__file__), 'picosat_python.i')) as f:
    swigdata = f.read()

def inject(data, tag, filenames):
    if filenames:
        if not isinstance(filenames, list):
            filenames = [filenames]

        d = ""
        for filename in filenames:
            with open(filename) as f:
                d += f.read()
        data = data.replace(tag, d)
    return data


swigdata = inject(swigdata, '/* EXTRA_SWIG_CODE_TAG */', opts.extra_swig_code)
swigdata = inject(swigdata, '/* EXTRA_C_INCLUDE_TAG */',
                  opts.extra_c_include_code)
swigdata = inject(swigdata, '/* EXTRA_SWIG_INCLUDE_TAG */',
                  opts.extra_swig_include_code)
swigdata = inject(swigdata, '/* EXTRA_C_STATIC_CODE_TAG */',
                  opts.extra_c_static_code)
swigdata = inject(swigdata, '/* EXTRA_C_INLINE_CODE_TAG */',
                  opts.extra_c_inline_code)
swigdata = inject(swigdata, '## EXTRA_PYTHON_CODE_TAG', opts.extra_python_code)

msg("Generating Python wrapper with SWIG...")
swig = 'swig'
if opts.swig_tool:
    swig = opts.swig_tool


fd, swigfile = tempfile.mkstemp('.c')
out = os.fdopen(fd, 'w')
out.write(swigdata)
out.close()

swig_cmd = [swig, '-I.', '-python', '-o',
            'picosat_python_wrap.c'] + \
            ['-I%s' % p for p in opts.extra_include_dir] + [swigfile]
msg(' '.join(swig_cmd))
p = subprocess.Popen(swig_cmd)
p.communicate()
if os.path.exists(swigfile):
    os.unlink(swigfile)

if p.returncode == 0 and not opts.swig_only:
    incdirs = [args.picosat_dir] + opts.extra_include_dir
    libdirs = [args.picosat_dir] + opts.extra_lib_dir
    msg("Compiling the extension module...")
    extra_compile_args = opts.extra_compile_args.split()
    if distutils.ccompiler.get_default_compiler() == 'unix':
        extra_compile_args += ['-Wno-unused', '-Wno-uninitialized']
    extra_link_args = opts.extra_link_args.split()
    libraries = opts.extra_libraries.split() + ['picosat']
    if sys.platform == 'win32':
        libraries.append('psapi')
    setup(name='picosat', version='0.1',
          description='PicoSAT API',
          ext_modules=[Extension('_picosat', ['picosat_python_wrap.c'],
                                 define_macros=[('SWIG','1')],
                                 include_dirs=incdirs,
                                 library_dirs=libdirs,
                                 extra_compile_args=extra_compile_args,
                                 extra_link_args=extra_link_args,
                                 libraries=libraries,
                                 language='c',
                                 )]
          )
