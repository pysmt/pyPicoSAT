import os
import platform
from cffi import FFI

__all__ = ['ffi', 'picosat']

PICOSAT_MINIMAL_H = """
#define PICOSAT_UNKNOWN         0
#define PICOSAT_SATISFIABLE     10
#define PICOSAT_UNSATISFIABLE   20

typedef struct PicoSAT PicoSAT;
const char *picosat_version (void);
PicoSAT * picosat_init (void);          /* constructor */
void picosat_reset (PicoSAT *);         /* destructor */
int picosat_inc_max_var (PicoSAT *);
int picosat_push (PicoSAT *);
int picosat_pop (PicoSAT *);
int picosat_add (PicoSAT *, int lit);
void picosat_assume (PicoSAT *, int lit);
int picosat_sat (PicoSAT *, int decision_limit);
int picosat_deref (PicoSAT *, int lit);
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMES = ["libpicosat.so",
          os.path.join(BASE_DIR, "libpicosat.so"),
         # TODO: Ideally, supporting multiple OS should boild down to trying to
         # open the right shared library, e.g.:
         # "libpicosat.dylib",
         # os.path.join(BASE_DIR, "libpicosat.dylib"),
         # "picosat.dll",
         # os.path.join(BASE_DIR, "libpicosat.dylib"),
         ]
ffi = FFI()
ffi.cdef(PICOSAT_MINIMAL_H)


picosat = None
for libname in NAMES:
    try:
        picosat = ffi.dlopen(libname)
    except OSError:
        picosat = None
    if picosat: break

if not picosat:
    raise ImportError("Cannot find %s." % libname)


if __name__ == "__main__":
    # Demo
    v_cdata = picosat.picosat_version()
    # Picosat Version
    print(ffi.string(v_cdata))
    # Defines work as expected
    print(picosat.PICOSAT_SATISFIABLE)
    pico = picosat.picosat_init()
    picosat.picosat_add(pico, 1)
    picosat.picosat_add(pico, -1)
    picosat.picosat_add(pico, 0)
    res = picosat.picosat_sat(pico, -1)
    assert res == picosat.PICOSAT_SATISFIABLE
    print("SAT")
    picosat.picosat_reset(pico)
