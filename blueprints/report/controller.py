def BLogic_data(url_base_line, url_args_dict):
    
    args = {}

    args['request_type'] = url_base_line[url_base_line.find('/report/')+8:url_base_line.rfind('/')]

    for item in url_args_dict:
        args[item] = url_args_dict[item]
    return args