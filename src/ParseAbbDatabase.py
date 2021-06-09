
import json


def parseABBdbxToJson(dbname="", tojsonfile=""):
    if not dbname:
        return
    # Final Dictionary
    jsonblocks = {"data":{}}
    # Intermediate block counting
    block_count = 0
    # Block header
    block_header = ""
    # with open('./db/1K2101.BAX', 'r') as f:
    with open(dbname, 'r') as f:
        # Comments section
        jsonblocks["data"] = {"comments":{}}
        # Section flag
        flag = ""
        # looping through all lines        
        for line_no, line in enumerate(f):          
            # Comments section
            if(line.strip().startswith("(*")):                            
                jsonblocks["data"]["comments"].update({line_no:line.strip()})

            # Start with BEGIN DB Line
            elif(line.startswith("BEGIN DB")):
                jsonblocks["data"].update({"begin_db":{}})
            # Header section
            elif(line.startswith("HEADER")):
                flag = "header"
                jsonblocks["data"]["begin_db"].update({"header":{}})

            elif(flag == "header"):                
                # check new line character to flash the flag
                if(line == "\n"):
                    flag = ""
                else:
                    param = list(filter(None, (line.strip().split(" "*2))))
                    if(len(param) > 1):
                            jsonblocks["data"]["begin_db"]["header"].update({param[0].strip(): param[1].strip()})
                    else:
                        jsonblocks["data"]["begin_db"]["header"].update({param[0].strip(): ""})

            # Default Section
            elif(line.startswith("BEGIN GENERAL DEFAULTS")):
                # flag = "begin_general_defaults"
                flag = line.strip().replace(" ","_").lower()
                jsonblocks["data"]["begin_db"].update({flag:{}})

            elif(flag == "begin_general_defaults" and not line.startswith("END GENERAL DEFAULTS")):                
                if(line == "\n"):
                    block_count += 1                    
                elif not line.strip().startswith(":") and line.strip().startswith("DEFAULT"):                    
                    block_header = line.strip().replace(" ","_")
                    # append an header
                    jsonblocks["data"]["begin_db"]["begin_general_defaults"].update({block_header:{}})
                else:
                    if flag =="":
                        return
                    param = list(filter(None, (line.strip().replace(":", "").split(" "*2))))
                    if(len(param) > 1):
                        jsonblocks["data"]["begin_db"]["begin_general_defaults"][block_header].update({param[0].strip(): param[1].strip()})                            
                    else:                                                                                  
                        jsonblocks["data"]["begin_db"]["begin_general_defaults"][block_header].update({param[0]:""})

            elif(line.startswith("END GENERAL DEFAULTS")):
                flag = ""
                block_count = 0
                block_header = ""
                # Add an section for all Defined databases
                jsonblocks["data"]["begin_db"].update({"db":{}})

            # Group all defined databases under DB section
            elif(not line.startswith("END DB")):
                flag = "db"
                if(line == "\n"):
                    block_count += 1                  
                elif not line.strip().startswith(":"):
                    header = list(filter(None, (line.strip().split(" "*2))))
                    block_header = header[0].strip()
                    jsonblocks["data"]["begin_db"]["db"].update({block_header:{}})
                    # Add a custom property to keep database ref
                    jsonblocks["data"]["begin_db"]["db"][block_header].update({"TYPE":header[1].strip()})
                else:
                    if flag =="":
                        return
                    param = list(filter(None, (line.strip().replace(":", "").split(" "*2))))
                    if(len(param) > 1):
                        jsonblocks["data"]["begin_db"]["db"][block_header].update({param[0].strip(): param[1].strip()})                            
                    else:                                                                                  
                        jsonblocks["data"]["begin_db"]["db"][block_header].update({param[0]:""})






    # print (json.dumps(blocks, indent=2))
    # with open('data.json', 'w') as f:
    with open(tojsonfile, 'w') as f:
        json.dump(jsonblocks, f)



if __name__ == '__main__':
    # parseABBdbxToJson('./db/1K2101.BAX', 'data.json')

    with open('./data.json') as f:
        d = json.load(f)

        print(d["data"]["begin_db"]["db"]["AIC368"]["NAME"])