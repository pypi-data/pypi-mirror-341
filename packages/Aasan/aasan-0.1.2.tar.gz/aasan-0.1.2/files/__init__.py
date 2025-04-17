def readFile(file_dir):
    """open(file_dir, "r").read()"""
    file_content = open(file_dir, "r").read()
    return file_content

def writeFile(file_dir):
    file_dir.write("Now the file has more content!")
    return None


if __name__ == "__main__":
    pass
