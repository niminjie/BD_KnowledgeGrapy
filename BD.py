# encoding:utf8
from dataset import DataSet
from model import Model
from settings import DEBUG as DEBUG
from test import *
from util import *
import json
import seg
import sys
import timeit

def main():
    # Load json file
    ds_task1 = DataSet('dataset/entity.json')
    # ds_task1.json_print()
    hash_type = ds_task1.entity_categories()
    # gen_attr_list = get_general_attr_name(ds_task1, hash_type)
    # query_attr_in_spe_type(ds_task1, hash_type, 'VideoGame', 'genre')
    # create_model(ds_task1, hash_type, gen_attr_list)
    # test_train_sim(ds_task1, hash_type)
    # test_extract_categories(hash_type)
    # test_extract_text(ds_task1)
    # test_seg_des(ds_task1, '3ac567be298fa5e87ad120778d80d7ef', 'description')

def query_attr_in_spe_type(dataset, hash_type, type_name, attr_name):
    for type, en_name in hash_type.items():
        if type != type_name:
            continue
        for en in en_name:
            query_entity(dataset, en, attr_name)
                
def create_model(dataset, hash_type, gen_attr_list, specify_type = None, output_path='./neu/'):
    for type, list in hash_type.items():
        # if specify_type != None and type != specify_type:
            # continue
        # if type != "Movie":
            # continue
        print "Open %s" % type
        fo = open(output_path + type, 'w')
        print "Writing %s ..." % type
        attr_name_list = gen_attr_list[type]
        print "%s contains:" % type
        print attr_name_list
        for l1 in list:
            for l2 in list:
                if l1 == l2:
                    continue
                en_1 = dataset.entities[l1]
                en_2 = dataset.entities[l2]
                en_vector = []
                for attr_name in attr_name_list:
                    try:
                        s = str(round(sim_percent(en_1[attr_name], en_2[attr_name]), 2))
                        en_vector.append(s)
                        print "Appended %s, value: %s " % (attr_name, s)
                    except KeyError:
                        print "%s not found, add 0" % attr_name
                        en_vector.append(str(0.0))
                try:
                    s = str(minEditDist(en_1['description'][0], en_2['description'][0]))
                    en_vector.append(s)
                    print "Appended description, value: %s " % s
                    # print str(minEditDist(en_1['description'][0], en_2['description'][0]))
                except (KeyError, IndexError):
                    en_vector.append(str(0.0))
                    print "descrpition not found, add 0"
                # print ','.join(en_vector)
                print >> fo, "%s\t%s\t%s" % (l1, l2, ','.join(en_vector))
                print "%s\t%s\t%s" % (l1, l2, ','.join(en_vector))
                print '-' * 100
                fo.flush()
                # print "%s\t%s" %(l1, l2)
        fo.close()

def get_general_attr_name(dataset, hash_type):
    ''' Return type contains all attribute name '''
    gen_attr = {}
    for type, list in hash_type.items():
        gen_attr.setdefault(type, [])
        for key in list:
                for attr_name in dataset.entities[key]:
                    if attr_name == 'description':
                        continue
                    if attr_name not in gen_attr[type]:
                        gen_attr[type].append(attr_name)
    return gen_attr

def minEditDistR(target, source):
   ''' Minimum edit distance. Straight from the recurrence. '''
   i = len(target); j = len(source)

   if i == 0:  return j
   elif j == 0: return i

   return(min(minEditDistR(target[:i-1],source)+1,
              minEditDistR(target, source[:j-1])+1,
              minEditDistR(target[:i-1], source[:j-1])+substCost(source[j-1], target[i-1])))

def minEditDist(target, source):
    ''' Computes the min edit distance from target to source. '''
    
    n = len(target)
    m = len(source)
    distance = [[0 for i in range(m+1)] for j in range(n+1)]
    for i in range(1,n+1):
        # distance[i][0] = distance[i-1][0] + insertCost(target[i-1])
        distance[i][0] = distance[i-1][0] + 1

    for j in range(1,m+1):
        # distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])
        distance[0][j] = distance[0][j-1] + 1

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def substCost(x,y):
    if x == y: return 0
    else: return 2

def sim_percent(attr1, attr2):
    ''' Calculate similarity between director, inLanguage, actor...  '''
    if type(attr1) != type([1]):
        return 1.0 if attr1 == attr2 else 0.0
    cnt = 0
    for ele1 in attr1:
        for ele2 in attr2:
            if ele1 == ele2:
                cnt += 1
    # print attr1, attr2
    # print cnt * 1.0 / min(len(attr1), len(attr2))
    return cnt * 1.0 / min(len(attr1), len(attr2))

def query_entity(dataset, en_name, attr_name = None):
    '''
    Args:
        dataset:      DataSet
        en_name:      entity name 
    Return:
        en_name pretty print
    '''
    try:
        if attr_name != None:
            # print "%s\t%s:%s" %(en_name, attr_name, dataset.entities[en_name][attr_name])
            for i in dataset.entities[en_name][attr_name]:
                print i
            return
    except KeyError:
        pass
        # print "Have not found attribute name : %s" % attr_name
        return
    try:
        en_json = dataset.entities[en_name]
        print json.dumps(en_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
        # print >> fo, json.dumps(en_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')
        # print >> fo, en_name
        return
    except KeyError:
        print "Have not found entity name: %s" % en_name
        return 
    return 
    # return json.dumps(en_name, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

def extract_categories(cate, input_path='dataset/entity.json', output_path='./'):
    '''
    Args:
        cate:  {'Movie':['3ac567be298fa5e87ad120778d80d7ef',...],...}
    '''
    f_name_list = cate.keys()
    data = {}

    for line in open(input_path, 'r'):
        en_name, en_des = line.split('\t')
        en_name = en_name.strip()
        en_des = en_des.strip()
        data[en_name] = en_des
    
    for f_name in f_name_list:
        entity_list = cate[f_name]
        # print entity_list
        with open(output_path + '/' + f_name, 'w') as f:
            for en_name in entity_list:
                f.write("%s\t%s\n" % (en_name.strip(), data[en_name.strip()]))
                f.flush()

def find_same_attri(en_1, en_2):
    ''' Input two different entity name to get same attribute name '''
    if en_1 == en_2:
        return None;
    en_attr_1 = en_1.keys()
    en_attr_2 = en_2.keys()
    return [attr for attr in en_attr_1 if attr in en_attr_2]

def seg_des(dataset, en_name, attri_name):
    ''' Segment a attribute in a entity '''
    print en_name
    entity = dataset.entities[en_name]
    before_seg = entity[attri_name]
    after_seg = []
    for text in before_seg:
        after_seg.append(seg.cut(text))
    # after_seg = seg.cut(before_seg)
    dataset.entities[en_name][attri_name] = after_seg
    # print after_seg
    if DEBUG:
        for i in xrange(len(before_seg)):
            print 'CUT %s\n TO\n %s' % (before_seg[i], after_seg[i])
            print '-' * 50
        
if __name__ == '__main__':
    fo = open('cate_out', 'wa')
    main()
