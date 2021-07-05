def get_tweets():
    print("Do something")
    with open('workfile', 'r') as f:
        lines = [line for line in f.readlines()] # f.readlines()

    print(lines)
    print(len(lines))
        #data = f.read()
    #    print(lines)
    #    number = lines
    #    print(number)
    if len(lines) > 0:
            with open('workfile', 'a') as f:
                f.write("testing123"+",")
                f.write("\n")
    else:
        with open('workfile', 'a') as f:
            f.write("testing"+",")
            f.write("\n")


# Adding Tweets to Database from CSV idea
# https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/