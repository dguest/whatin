// python wrapper for root file path completion 
// Author: Daniel Guest (dguest@cern.ch)
#include <Python.h>
#include <string> 
#include <vector>
#include <stdexcept>

#include "ReadRoot.hh"
  
static const char* doc_string = 
  "read_root(root_file,dir_path) --> path completions"; 


PyObject* py_read_file(PyObject *self, 
		       PyObject *args, 
		       PyObject *keywds)
{
  const char* file_name; 
  PyObject* dir_path; 
  const char *kwlist[] = {
    "root_file",
    "dir_path", 
    NULL};
    
  bool ok = PyArg_ParseTupleAndKeywords
    (args, keywds, 
     "sO", // <-- tells the function to parse objects as strings

     // I think python people argue about whether this should be 
     // a const char** or a char**
     const_cast<char**>(kwlist),
     &file_name, 
     &dir_path ); 

  if (!ok) return NULL;

  int dir_path_len = PyList_Size(dir_path); 
  if (PyErr_Occurred() ) { 
    return NULL; 
  }
  std::vector<std::string> dir_path_vec; 
  for (int n = 0; n < dir_path_len; n++) { 
    PyObject* this_entry = PyList_GetItem(dir_path, n); 
    if (PyErr_Occurred() ) return NULL; 
    std::string this_seg = PyString_AsString(this_entry); 
    if (PyErr_Occurred() ) return NULL; 
    dir_path_vec.push_back(this_seg); 
  }

  typedef std::vector<std::string> SVec; 
  SVec entry_names; 
  
  try { 
    entry_names = read_file(file_name, dir_path_vec); 
  }
  catch (const std::runtime_error& e) { 
    PyErr_SetString(PyExc_IOError,e.what()); 
    return 0; 
  }
  
  PyObject* the_list = PyList_New(0); 
  for (SVec::const_iterator itr = entry_names.begin(); 
       itr != entry_names.end(); itr++) { 
    PyList_Append(the_list, PyString_FromString(itr->c_str())); 
  }
  return the_list; 

  // --- make sure you call INCREF if you return Py_None
  // Py_INCREF(Py_None);
  // return Py_None;
}



static PyMethodDef keywdarg_methods[] = {
  // The cast of the function is necessary since PyCFunction values
  // only take two PyObject* parameters, and keywdarg() takes
  // three.
  {"read_file", (PyCFunction)py_read_file, 
   METH_VARARGS | METH_KEYWORDS,
   doc_string},
  {NULL, NULL, 0, NULL}   /* sentinel */
};

extern "C" { 

  PyMODINIT_FUNC initpyread(void)
  {
    Py_InitModule("pyread", keywdarg_methods);
  }

}
