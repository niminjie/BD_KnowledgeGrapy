from settings import DEBUG as DEBUG

def extract_text(dataset):
    attr_text = {}
    for entity, attr_list in dataset.entities.items():
        for attr_name, text in attr_list.items():
            if attr_name == 'description':
                continue
            raw_text = []
            attr_text.setdefault(attr_name, [])
            get_text_in_depth(text, raw_text)
            # print '%s\t%s' % (attr_name, raw_text)
            for t in raw_text:
                if t not in attr_text[attr_name]:
                    attr_text[attr_name].append(t)
                    if DEBUG:
                        # print "%s appended a new text: %s" % (attr_name, t)
                        pass
    return attr_text

def text_each_other(attr_text):
    for attri_name, text in attr_text.items():
        with open('./text/' + attri_name, 'w') as f:
            # for t1 in text:
                # f.write("%s\n" % (t1.encode('gbk')))
            for t1 in text:
                for t2 in text:
                    if t1 == t2:
                        continue
                    print "%s\t%s" % (t1, t2)
                    # f.write("%s\t%s\n" % (t1.encode('gbk'), t2.encode('gbk')))
                    # f.flush()

def get_text_in_depth(text_list, out):
    if type(text_list) != type([1]):
        out.append(text_list)
        return 1
    if type(text_list[0]) != type([1]):
        for text in text_list:
            out.append(text)
        return 1
    get_text_in_depth(text_list[0], out)
