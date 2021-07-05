def get_tweets():
    print("Do something")
    with open('workfile', 'r') as f:
        lines = [line for line in f.readlines()] # f.readlines()

    stripped_line = [s.rstrip() for s in lines]
    print(stripped_line)
    #if len(lines) > 0:
     #   lines = lines.rstrip()
    print(lines)
    print(len(lines))
    #for line in lines:
    
        #data = f.read()
    #    print(lines)
    #    number = lines
    #    print(number)
    #lines = [lines.replace('\n', '') for x in lines]
    if len(lines) > 0:
            with open('workfile', 'a') as f:
                f.write("testing123"+"\n")
                #f.write("\n")
    else:
        with open('workfile', 'a') as f:
            f.write("testing"+"\n")
            #f.write("\n")


# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/