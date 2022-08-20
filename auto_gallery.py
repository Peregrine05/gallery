# -*- coding: utf-8 -*-

import os
import sys
import csv
import wget
import subprocess
import imghdr
import glob
import re

# Monkeypatch bug in imagehdr
# https://bugs.python.org/issue28591
# https://stackoverflow.com/questions/36870661/imghdr-python-cant-detec-type-of-some-images-image-extension
def test_jpeg1(h, f):
    """JPEG data in JFIF format"""
    if b'JFIF' in h[:23]:
        return 'jpeg'


JPEG_MARK = b'\xff\xd8\xff\xdb\x00C\x00\x08\x06\x06' \
            b'\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f'

def test_jpeg2(h, f):
    """JPEG with small header"""
    if len(h) >= 32 and 67 == h[5] and h[:32] == JPEG_MARK:
        return 'jpeg'


def test_jpeg3(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b'JFIF', b'Exif') or h[:2] == b'\xff\xd8':
        return 'jpeg'

imghdr.tests.append(test_jpeg1)
imghdr.tests.append(test_jpeg2)
imghdr.tests.append(test_jpeg3)
# end
               
class AutoGallery:
  def __init__(self,source_csv):
    self.encoding = 'utf-8' # encoding=self.encoding
    
    self.thumbnail_abbr = '_TIMG' # Thumbnal IMaGe ; For whatever reason.
    self.thumbnail_suffix = 'jpg'
    self.thumbnail_ending = self.thumbnail_abbr + '.' + self.thumbnail_suffix
    self.thumbnail_q = '90%'
    self.thumbnail_w = '720'
    
    
    if os.path.isfile(source_csv):
      self.csv = source_csv
      print('csv file found')
    else:
      msg = 'csv file is missing: ' + source_csv
      sys.exit(msg)
    
    # orginal image location
    self.path_original = os.path.join('images', 'gallery')
    self.folder_test(self.path_original)
    
    # Thumbnail location (site hosted)
    self.path_thumbnail = os.path.join('ChunkyGallery', 'gallery', 'img', 'thumbnail')
    self.folder_test(self.path_thumbnail)
    self.rel_thumbnail = os.path.join('img', 'thumbnail')
    
    # Custom folder for gallery image pages
    self.path_html = os.path.join('ChunkyGallery', 'gallery', 'image_html') 
    self.folder_test(self.path_html)
    self.rel_html = os.path.join('image_html') 

    # gallery index.md
    self.path_indexmd = os.path.join('ChunkyGallery', 'gallery', 'index.md')
    if not os.path.isfile(self.path_indexmd):
      print('index.md is missing at: ', self.path_indexmd)
      sys.exit()
      
    # Easy dict key changes
    self.key_credit = 'Name to credit you under'
    self.key_title = 'Render name/title'
    self.key_upload ='Render upload'
    self.key_time = 'Timestamp'
    self.key_someone_else = 'Used someone else\'s creation?'
    self.key_version = 'Version of Chunky used (including snapshots)'
    self.key_features = 'What features of Chunky did you use?'
    self.key_original_img = 'Original' # Not in csv; Logging original file name useful
    self.key_original_ext = 'Original_ext' # Not given by G'drive
    
    self.templates = 'templates'
    self.original_page = 'gallery_original_image_page.html'
    self.container = 'gallery_item.html'

  def auto(self):
    # 1. Prase CSV to array of dict
    self.load_csv()
    print('')
    
    # # 2. download from Google Drive
    self.download_all_img()
    print('')
    
    # 3. generate thumbs
    self.gen_thumbnails()
    print('')
    
    # 4. generate image pages for originals using Github raw links
    self.gen_gallery_img_page()
    print('')
    
    # 5. generate gallery
    self.gen_index()
    print('')
    
    # 6. write csv
    self.write_csv()
    print('')
    
  def folder_test(self, TEST_DIR):
    if not os.path.isdir(TEST_DIR):
      os.makedirs(TEST_DIR)
      print('Folder missing, creating folder: ', TEST_DIR)

  def load_csv(self):
    with open(self.csv, 'r', encoding=self.encoding) as f:    
      self.gallery_dict = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    print('Loaded CSV')
    return self.gallery_dict
    
  def write_csv(self):
    dict_keys = self.gallery_dict[0].keys()
    with open(self.csv, 'w', newline='', encoding=self.encoding) as output_file:
      dict_writer = csv.DictWriter(output_file, dict_keys)
      dict_writer.writeheader()
      dict_writer.writerows(self.gallery_dict)
    print('Written CSV')
    
  def download_all_img(self):
    for i in range(len(self.gallery_dict)):
      
      username = self.gallery_dict[i][self.key_credit]
      rendername = self.gallery_dict[i][self.key_title]
      temp = username + '-' + rendername
      target_filename = temp.replace(' ', '_')
      target = os.path.join(self.path_original, target_filename)
      
      self.gallery_dict[i][self.key_original_img] = target_filename # save original_img name for later use
        
      if self.gallery_dict[i][self.key_upload] != 'null':
        _id = self.gallery_dict[i][self.key_upload].split('=')[1]
        url = str('https://drive.google.com/uc?id=' + _id)
        
        self.download_img(url, target)
        
        # Fix ext for newly downloaded images
        if os.path.exists(target):
          img_ext = imghdr.what(target)
          if img_ext==None:
            print('ERROR - Image extension could not be read for ' + target)
            sys.exit()
          else:
            if os.path.exists(target + '.' + img_ext):
              print('WARN - ' + target + '.' + img_ext + ' already has a copy with an extension?')
            else:
              print('>>> Fixing Extension to .' + img_ext)
              os.rename(target, target + '.' + img_ext)
              self.gallery_dict[i][self.key_original_ext] = img_ext           
      else:
        print('Skipping ' + target + ' as it has no Render upload')
      
      # Log our ext
      fuzzy_target = glob.glob(target + '.*')[0]
      #print('### ' + str(imghdr.what(fuzzy_target))) #debug
      if fuzzy_target:
        self.gallery_dict[i][self.key_original_ext] = imghdr.what(fuzzy_target)
        
         
  def download_img(self, url, target):
    if os.path.exists(target) or glob.glob(target + '.*'):
      print('Image ' + target + ' already exists, skipping.')
      return
    try:
      print('Downloading - ' + url + ' to target - ' + target)
      wget.download(url, target)
    except Exception as e:
      sys.exit(e)    

  def gen_thumbnails(self):
    for i in range(len(self.gallery_dict)):
      original = self.gallery_dict[i][self.key_original_img]
      source = os.path.join(self.path_original, original) + '.' + self.gallery_dict[i][self.key_original_ext]
      dest = os.path.join(self.path_thumbnail, original + self.thumbnail_ending)
      self.create_thumb(source, dest)
      
          
  def create_thumb(self, source, dest):
    if os.path.isfile(dest):
      print('Thumbnail ' + dest + ' already exists, skipping.')
      return
    try:
      print('generating thumbnail for ', source)
      #print('magick', source, '-resize', self.thumbnail_w , '-quality', self.thumbnail_q , dest)
      subprocess.run(['magick', source, '-resize', self.thumbnail_w , '-quality', self.thumbnail_q , dest])
    except Exception as e:
      sys.exit(e)
  
  def gen_gallery_img_page(self):
    for i in range(len(self.gallery_dict)):
      file = self.gallery_dict[i][self.key_original_img]
      username = self.gallery_dict[i][self.key_credit]
      rendername = self.gallery_dict[i][self.key_title]
      original_file = self.gallery_dict[i][self.key_original_img]
      original_file_ext = self.gallery_dict[i][self.key_original_ext]
      
      title = rendername + ' - ' + username
      url = 'https://raw.githubusercontent.com/chunky-dev/gallery/main/images/gallery/' + file + '.' + original_file_ext
      
      self.create_html(title, url, original_file)
      
  def create_html(self, title, url, original_file):
    template_file = os.path.join(self.templates, self.original_page)
    new_file = os.path.join(self.path_html, original_file + '.html')
    
    if os.path.isfile(new_file):
      print('html ' + new_file + ' already exists, skipping.')
      return
    
    if os.path.isfile(template_file):
      print('Creating html for ' + os.path.join(self.path_html, original_file + '.html'))
            
      with open(new_file, 'w', encoding=self.encoding) as outfile, open(template_file, 'r', encoding=self.encoding) as template:
        for line in template:
          line = line.replace('PAGE_TITLE', title).replace('ORIGINAL_URL', url)
          outfile.write(line)
    else:
      msg = 'orginal image page template is missing: ' + os.path.join(self.templates, self.original_page)
      sys.exit(msg)    
  

  def gen_index(self):
    # store start/end of index.md
    print('Loaing existing index.md')
    print('')
    lines = []
    with open(self.path_indexmd, 'r', encoding=self.encoding) as indexmd:
      lines = indexmd.readlines()

    gallery_start_num = 0
    gallery_end_num = 0
    for i in range(len(lines)):
      if '<!--GALLERY_START-->' in lines[i]:
        gallery_start_num = i+1
      if '<!--GALLERY_END-->' in lines[i]:
        gallery_end_num = i
        
    if gallery_start_num==0:
      print('missing <!--GALLERY_START--> tag in index.md')
      sys.exit()
    if gallery_end_num==0:
      print('missing <!--GALLERY_END--> tag in index.md')
      sys.exit()
    end_of_file = i
    
    # store index.md start/end for later
    gallery_indexmd_start = lines[0:gallery_start_num]
    gallery_indexmd_end = lines[gallery_end_num:end_of_file]
    
    gallery_containers = []
    
    # generate new gallery containers
    for i in range(len(self.gallery_dict)):
      
      original_img = self.gallery_dict[i][self.key_original_img]
      render_title = self.gallery_dict[i][self.key_title]
      username = self.gallery_dict[i][self.key_credit]
      someone_else = self.gallery_dict[i][self.key_someone_else]
      
      temp = self.gen_gallery_container(original_img, render_title, username, someone_else)
      gallery_containers.extend(temp)
    
    # combine to produce new index.md. start, containers, end
    print('')
    print('Writing new index.md')
    new_gallery_indexmd = []
    new_gallery_indexmd.extend(gallery_indexmd_start + gallery_containers + gallery_indexmd_end)
    
    with open(self.path_indexmd, 'w', encoding=self.encoding) as indexmd: #self.path_indexmd
      for line in new_gallery_indexmd:
          indexmd.write(line)

  def gen_gallery_container(self, original_img, render_title, username, someone_else):
    template_file = os.path.join(self.templates, self.container)
    
    third_party = self.third_party_credits(someone_else)
    
    gallery_original = str(os.path.join(self.rel_html, original_img + '.html')) #ORIGINAL_HTML
    gallery_alt = render_title + ' by ' + username #ALT_TEXT
    gallery_timg = str(os.path.join(self.rel_thumbnail, original_img + self.thumbnail_ending)) #TIMG
    gallery_desc = '\"' + render_title + '\"' + ' by ' + username + third_party
    
    print('Creating gallery container for ' + gallery_desc)
    
    temp = []
    
    if os.path.isfile(template_file):
      with open(template_file, 'r', encoding='utf-8') as template:
        for line in template:
          line = line.replace('ORIGINAL_HTML', gallery_original).replace('ALT_TEXT', gallery_alt).replace('TIMG', gallery_timg).replace('TITLE_CREDIT_PMC', gallery_desc)
          temp.append(str(line))
      return temp
    else:
      msg = 'container template missing: ' + os.path.join(self.templates, self.container)
      sys.exit(msg)  

  def third_party_credits(self, someone_else):
    if someone_else=='':
      return ''
      
    temp = []
    if ',' in someone_else:
      temp = someone_else.split(',')
    else:
      temp = [someone_else]
    
    builder = ' -'
    for x in temp:
      if 'http' in x or 'https' in x:
        if 'planetminecraft' in x:
          builder = builder + ' ' + '<a href="' + x +'">PMC</a>'
        else:
          builder = builder + ' ' + '<a href="' + x +'">Map Credit</a>'
      else:
        builder = builder + ' ' + x 
    return builder
  
  def debug(self):
    return self.gallery_dict
                     
                     
if __name__ == '__main__':
  gallery = AutoGallery('gallery.csv') # MUST BE UTF-8 (νησί)
  gallery.auto()
  
##
  
