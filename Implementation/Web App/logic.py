def get_tweets():
    print("Do something")
    with open('workfile', 'r') as f:
        lines = [line for line in f.readlines()] # f.readlines()

    stripped_line = [s.rstrip() for s in lines]
    print(stripped_line)

    if len(stripped_line) > 0:
        value = int(stripped_line[-1]) + 1
        with open('workfile', 'a') as f:
            f.write(str(value)+"\n")
            #f.write("\n")
    else:
        with open('workfile', 'a') as f:
            f.write("1"+"\n")
            #f.write("\n")

    # query database for the records matching value



# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/