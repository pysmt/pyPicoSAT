/* -*- swig -*- */
/* SWIG interface file to create the Python API for PicoSAT */
/* author: Andrea Micheli <micheli.andrea@gmail.com> */

%include "typemaps.i"

/***************************************************************************/

/* EXTRA_SWIG_CODE_TAG */


/* %typemap(in) FILE * { */
/* %#if PY_VERSION_HEX < 0x03000000 */
/*   if (!PyFile_Check($input)) { */
/*       PyErr_SetString(PyExc_TypeError, "Need a file!"); */
/*       goto fail; */
/*   } */
/*   $1 = PyFile_AsFile($input); */
/* %#else */
/*   int fd = PyObject_AsFileDescriptor($input); */
/*   $1 = fdopen(fd, "w"); */
/* %#endif */
/* } */



%ignore picosat_set_output ;

%module picosat
%{
#include "picosat.h"
/* EXTRA_C_INCLUDE_TAG */
%}

%include "picosat.h"
/* EXTRA_SWIG_INCLUDE_TAG */

%{

/* EXTRA_C_STATIC_CODE_TAG */

%}


%inline %{

/* EXTRA_C_INLINE_CODE_TAG */
static FILE* picosat_set_output_fd(PicoSAT* self, int fd) {
    FILE* fout = fdopen(fd, "w");
    picosat_set_output(self, fout);
    return fout;
}

static void picosat_flushout(FILE* fout) {
    fflush(fout);
}

%}


%pythoncode %{

## EXTRA_PYTHON_CODE_TAG
def picosat_set_output(picosat, fileout):
    picosat_set_output_fd(picosat, fileout.fileno())

%}
