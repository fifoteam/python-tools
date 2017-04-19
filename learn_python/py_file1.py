file_object = open('thefile.txt')
try:
     all_the_text = file_object.readline( )
     print (all_the_text)
finally:
     file_object.close( )
     
     
     
     