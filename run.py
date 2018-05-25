import file_helper

FILENAME = "data_samples/simple.tcx"

if __name__ == "__main__":
    my_helper = file_helper.FileHelper()
    workout1 = my_helper.load(FILENAME, "tcx")
    print(workout1)
