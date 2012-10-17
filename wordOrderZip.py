import zipfile
import random
import os

def compare_word_order(orig_file,clean_up=True):
  """Compares the original version of the text in a file with the shuffled
  text for each verse
  
  ARGUMENTS:
  ==========
  orig_file: orig file in the paralysis format (verse number TAB verse text)
  clean_up: whether the shuffled and zip files should be removed (True) at the
            end of the calculations or not (False)
  """
  
  # read in original file (with verse numbers) and save the text in original
  # and shuffled form as a list of verses with each verse consisting of a
  # list of words
  orig_text_verses = list()
  rand_text_verses = list()
  with open(orig_file,mode="r",encoding="utf-8") as orig:
    for line in orig:
      try:
        line_text = line.strip().split("\t",1)[1].split()
      except:
        continue
      orig_text_verses.append(line_text)
      rand_text = [w for w in line_text]
      random.shuffle(rand_text)
      rand_text_verses.append(rand_text)
      
  # create a temporary folder where the temp files will be stored
  tmp_dir = "tmp/"
  try:
    os.mkdir(tmp_dir)
  except OSError:
    pass

  # make text file with normal word order
  normal_file = tmp_dir + orig_file[:-4] + "_norm.txt"
  with open(normal_file,mode="w",encoding="utf-8") as normal:
    for verse in orig_text_verses:
      normal.write(" ".join(verse) + "\n")
      
  # make text file with shuffled word order
  shuffled_file = tmp_dir + orig_file[:-4] + "_shuff.txt"
  with open(shuffled_file,mode="w",encoding="utf-8") as shuffled:
    for verse in rand_text_verses:
      shuffled.write(" ".join(verse) + "\n")
      
  # compare both files
  zip_file(normal_file)
  zip_file(shuffled_file)
  normal_size = os.path.getsize(normal_file + ".zip")
  shuffled_size = os.path.getsize(shuffled_file + ".zip")
  ratio = normal_size/shuffled_size
  diff = shuffled_size - normal_size
  
  print("Original: {}\nShuffled: {}\nDiff: {}\nRatio: {}".format(normal_size,
                                                       shuffled_size,diff,
                                                       ratio))
  
  # clean up
  if clean_up:
    os.remove(normal_file)
    os.remove(shuffled_file)
    os.remove(normal_file + ".zip")
    os.remove(shuffled_file + ".zip")
    os.rmdir(tmp_dir)
    
  
  
def zip_file(file):
  """This method zips the contents of a file and creates a new zipped file
  with the same name and the suffix ".zip".
  
  ARGUMENTS:
  ==========
  file: file to be zipped
  """
  
  file_zip = zipfile.ZipFile(file + ".zip","w",compression=8)
  file_zip.write(file)
  file_zip.close()
  
if __name__ == '__main__':
  compare_word_order("test.txt",False)