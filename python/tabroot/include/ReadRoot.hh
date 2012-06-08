// C++ component in root auto-complete utility
// Author: Dan Guest <dguest@cern.ch>
// Fri Jun  8 11:08:47 CEST 2012

#ifndef READ_ROOT
#define READ_ROOT

#include <string> 
#include <vector>

class TFile; 
class TDirectory; 

std::vector<std::string> read_file(std::string file, 
				   std::vector<std::string> dir_path); 
std::vector<std::string> read_file(TDirectory& dir, 
				   std::vector<std::string> dir_path); 

#endif // READ_ROOT
