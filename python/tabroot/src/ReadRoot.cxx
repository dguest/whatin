// Author: Dan Guest <dguest@cern.ch>
// Fri Jun  8 11:09:41 CEST 2012

#include "ReadRoot.hh"
#include <string> 
#include <vector> 
#include "TFile.h"
#include "TTree.h"
#include "TList.h"
#include "TObjArray.h"
#include "TDirectoryFile.h"
#include "TKey.h"
#include <stdexcept> 
#include <cassert> 


std::vector<std::string> read_file(std::string file_name, 
				   std::vector<std::string> dir_path){ 


  TFile file(file_name.c_str()); 
  std::vector<std::string> entry_names = read_file(file, dir_path); 
  return entry_names; 
}; 


std::vector<std::string> read_file(TDirectory& dir, 
				   std::vector<std::string> dir_path){ 

  std::vector<std::string> entry_names; 
  if (dir_path.size() && dir_path.at(0).size()) { 
    std::string head_dir = dir_path.at(0); 

    TKey* key = dir.GetKey(head_dir.c_str()); 
    // if the key exists and is a directory, decend into it
    if (key && !strcmp(key->GetClassName(),"TDirectoryFile") ) { 
      TDirectory* subdir = dynamic_cast<TDirectory*> 
	(dir.Get(head_dir.c_str())); 

      std::vector<std::string>::iterator sub_dir_begin 
	= dir_path.begin(); 
      sub_dir_begin++; 
      std::vector<std::string> sub_dir_path; 
      sub_dir_path.assign(sub_dir_begin,dir_path.end()); 

      std::vector<std::string> tails = read_file(*subdir, sub_dir_path); 
      for (std::vector<std::string>::iterator itr = tails.begin(); 
      	   itr != tails.end(); itr++) { 
	entry_names.push_back(head_dir + "/" + *itr); 
      }
    }
    else if (key && !strcmp(key->GetClassName(),"TTree")) { 
      TTree* tree = dynamic_cast<TTree*> (dir.Get(head_dir.c_str())); 
      TObjArray* leaf_list = tree->GetListOfLeaves(); 
      int n_leaf = leaf_list->GetEntries(); 
      for (int leaf_n = 0; leaf_n < n_leaf; leaf_n++) { 
	TObject* the_leaf = leaf_list->At(leaf_n); 
	std::string leaf_name = the_leaf->GetName(); 
	entry_names.push_back(head_dir + "/" + leaf_name); 
      }
    }
    // if not, return matches 
    else { 
      TList* keys = dir.GetListOfKeys(); 
      int n_entries = keys->GetEntries(); 
      for (int i = 0; i < n_entries; i++){ 
	TKey* the_key = dynamic_cast<TKey*>(keys->At(i)); 
	entry_names.push_back(the_key->GetName()); 
      }
    } 
  }
  else{ // last dir is empty
    TList* keys = dir.GetListOfKeys(); 
    int n_entries = keys->GetEntries(); 
    for (int i = 0; i < n_entries; i++){ 
      TKey* the_key = dynamic_cast<TKey*>(keys->At(i)); 
      entry_names.push_back(the_key->GetName()); 
    }
  }
  return entry_names; 
}; 
