import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TFile

import re

root_hack_index = 0
def rootHack():
    global root_hack_index
    root_hack_string = str(root_hack_index)
    root_hack_index += 1
    return root_hack_string

def getListFrom(file_name, expand_list = []):
    """
    builds a list of object info in <file_name>. 
    
    for each object, the list gives: Class, Name, [size]. 

    for objects where size isn't found only two entries are given. 
    """
    import re

    the_file = TFile(file_name)

    stuff_list,d = getKeysInDir(the_file, expand_list)

    if d:
        d += [the_file]

    return stuff_list,d

def getKeysInDir(the_file, expand_list = []):
    
    key_list = the_file.GetListOfKeys()
    
    n_keys = key_list.GetEntries()

    stuff_list = []
    d_list = []
    
    
    breakdown_path_list = [d.split('/') for d in expand_list]
    paths_dict = {x[0] : x[1:] for x in breakdown_path_list}

    keys_checked = set()
    for i in xrange(n_keys): 
        the_key = key_list.At(i)
            
        key_name = the_key.GetName()
        if key_name in keys_checked: continue
        keys_checked.add(key_name)
        key_class = the_key.GetClassName()
        
        entry = [key_class, key_name]

        the_obj = the_key.ReadObj()
        try:
            obj_size = the_obj.GetEntries()
            entry.append(obj_size)
        except AttributeError:
            entry.append(None)
            pass

        if expand_list and key_name in paths_dict:

            cont_path = ['/'.join(paths_dict[key_name])]
            if key_class == 'TTree':
                entry.append(getTreeList(the_obj, cont_path))

            else: 
                try: 
                    inner_stuff_list,d = getKeysInDir(the_obj,cont_path)
                    entry.append(inner_stuff_list)
                    d_list += d
                except AttributeError:
                    if the_key.GetClassName() == 'TObjString': 
                        str_data = the_obj.GetString().Data()
                        entry.append([[str_data,'']])
                    else:
                        d_list += drawHist(the_key)
                except ReferenceError: 
                    print 'could not expand %s' % key_name

        stuff_list.append(entry)
            
    return stuff_list,d_list

def drawHist(the_key):
    # basic setup
    from ROOT import gROOT, gStyle, TCanvas
    gROOT.SetStyle('Plain')
    gStyle.SetPalette(1)

    # special draw options
    draw_dict = {'TH2':'colz'}
    
    the_obj = the_key.ReadObj()
    try:
        draw_string = ''
        for key,val in draw_dict.iteritems():
            if key in the_key.GetClassName():
                draw_string = val

        name = rootHack()
        canvas = TCanvas(name,name,100,100,600,400)
        the_obj.Draw(draw_string)
        return [canvas]
    except TypeError:
        print 'could not draw %s' % key_name


def getTreeList(the_tree, expand_list = None):
    """
    returns a list of pairs for tree_name, 

    first entry is type, second is leaf name. 
    """

    leaves = the_tree.GetListOfLeaves()

    n_leaves = leaves.GetEntries()

    return_pairs = []
    
    for i in xrange(n_leaves):
        leaf = leaves.At(i)
        leaf_name = leaf.GetName()
        type_name = leaf.GetTypeName()
        entry = [type_name,leaf_name]

        if expand_list and leaf_name in expand_list: 
            expand_list.remove(leaf_name)
            entry.append(1)
            entry.append([[' entry','value']])
            leaf_list = getLeafList(the_tree, leaf_name)
            for leaf_val in leaf_list: 
                entry[-1].append(leaf_val)

        return_pairs.append(entry)

    return return_pairs

def getLeafList(tree, leaf_name, max_entries = 20): 
    n_entries = tree.GetEntries()
    max_entries_possible = min(n_entries,max_entries)
    leaf_list = []
    for i in xrange(max_entries_possible):
        tree.GetEntry(i)
        leaf_list.append([str(i).rjust(5),str(tree.__getattr__(leaf_name))])

    return leaf_list

def getFileFrom(files_string, expand_list = None):
    """
    builds file listing the contents of root files given by files_string
    """
    import tempfile


    file_list = files_string.split(',')
    d_list = []

    out_file = tempfile.TemporaryFile()

    for file_name in file_list:

        if len(file_list) > 1:
            out_file.write(file_name + ':\n')

        try: 
            file_expand_list = expand_list[:]
        except TypeError:
            file_expand_list = None

        # get the list for this file
        stuff_list,d = getListFrom(file_name, file_expand_list)
        d_list += d

        # dump the list
        more_stuff = dumpList(stuff_list)
        more_stuff.seek(0)
        for line in more_stuff:
            out_file.write(line)

        if len(file_list) > 1: out_file.write('\n')


    return out_file,d_list

def dumpList(stuff_list, tab_in = 0):
    col_1 = tab_in

    col_1_widths = []
    col_2_widths = []

    for stuff in stuff_list: 
        col_1_widths.append(len(stuff[0]))
        col_2_widths.append(len(stuff[1]))

    col_1_wid = max(col_1_widths) + 2
    col_2_wid = max(col_2_widths) + 2

    import tempfile
    out_file = tempfile.TemporaryFile()
    for stuff in stuff_list:
        stuff_type = stuff[0]
        name = stuff[1]
            
        the_line = ('-'*col_1 + 
                    stuff_type.ljust(col_1_wid) +
                    name.ljust(col_2_wid) )
        # if there's a given object size, write it
        if len(stuff) > 2 and stuff[2]: 
            the_line += str(stuff[2])

        the_line += '\n'

        out_file.write(the_line)

        # recursive calls
        if len(stuff) > 3:
            inner_file = dumpList(stuff[3], tab_in = 1 + tab_in)
            inner_file.seek(0)
            for inner_line in inner_file:
                out_file.write(inner_line)
            

    return out_file

def dump(stuff_file):
    stuff_file.seek(0)
    for line in stuff_file:
        print line.strip()
