"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
Please do not make this code or the data public.
This version has two start email patterns as developed in the lab session.
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
epatterns = []

#***********************************************************
#Added Pattern for following Phones numbers matching 
#***********************************************************

# Emails with optional space in them 
epatterns.append('([A-Za-z.]+)\s?@\s?([A-Za-z.]+)\.edu')

# Emails with capital .EDU as domain name
epatterns.append('([A-Za-z.]+)\s@\s([A-Za-z.]+)\.EDU')

#cheriton file : uma at cs.Stanford.EDU
epatterns.append('([A-Za-z.]+)\s?at\s?([A-Za-z.]+)\.EDU')

#engler where 
epatterns.append('([A-Za-z.]+)\s+WHERE+\s([A-Za-z.]+)+\s+DOM+\sedu')

#for levoy file
#melissa&#x40;graphics.stanford.edu  
#ada&#x40;graphics.stanford.edu 
epatterns.append('([A-Za-z.]+)&#x40;([A-Za-z.]+)\.edu')

#for ouster file
#ouster (followed by &ldquo;@cs.stanford.edu&rdquo;) 
epatterns.append('([A-Za-z.]+)\s+\([A-Za-z.\s&]+;@([A-Za-z.]+)\.edu[A-Za-z.\s&]+;\)')
#teresa.lynn (followed by "@stanford.edu")
epatterns.append('([A-Za-z.]+)\s+\([A-Za-z.\s&]+"@([A-Za-z.]+)\.edu"\)')

#uma at cs dot stanford dot edu      : false positive ( replaced space)
#serafim at cs dot stanford dot edu
#hager at cs dot jhu dot edu
epatterns.append('([A-Za-z.]+)\s+at+\s([A-Za-z.\s]+)\s+dot+\sedu')

#jks at robotics;stanford;edu        : false positive ( replaced ;)
epatterns.append('([A-Za-z]+)\sat\s([A-Za-z;]+)\;\edu')

#subh file : subh AT stanford DOT edu
epatterns.append('([A-Za-z.]+)\s+AT+\s([A-Za-z.]+)+\s+DOT+\sedu')

#pal file : pal at cs stanford edu, :  false positive ( replaced space)
epatterns.append('([A-Za-z]+)\sat\s([A-Za-z\s]+)\s\edu')

#for dlwh file  d-l-w-h-@-s-t-a-n-f-o-r-d-.-e-d-u  :: emails with dash in it - false positive
epatterns.append('([A-Za-z\-]+)@([A-Za-z\-]+)\.\-e\-d\-u')

#lam at cs.stanford.edu and not (server at cs.stanford.edu) :: server@cs.stanford.edu - false positive
epatterns.append('([A-Za-z.]+[^Server])\s+at+\s([A-Za-z.]+)\.edu')
 
#vladlen file : vladlen at <!-- die!--> stanford <!-- spam pigs!--> dot <!-- die!--> edu
epatterns.append('([A-Za-z.]+)\sat\s<[A-Za-z\s!-]+>\s([A-Za-z\s]+)\s<[A-Za-z\s!-]+>\sdot\s<[A-Za-z\s!-]+>\sedu') 

#obfuscate('stanford.edu','jurafsky'); == jurafsky@stanford.edu
epatterns_custom = []
epatterns_custom.append('obfuscate\(\'([A-Za-z]+.edu)\',\'([A-Za-z]+)\'\)') 

#support at gradiance dt com   => support@gradiance.com
compatterns = []
compatterns.append('([A-Za-z.]+)\s+at+\s([A-Za-z.]+)+\sdt+\scom')

#for noraml .coms part 3rd
compatterns.append('([A-Za-z.]+)\s+@+\s([A-Za-z.]+)\.com')


#***********************************************************
#END Pattern emails  matching 
#***********************************************************


# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []

#***********************************************************
#Added Pattern for following Phones numbers matching 
#***********************************************************

#for numbers like XXX-YYY-ZZZZ eg. 650-723-1614
ppatterns.append('(\d{3})-(\d{3})-(\d{4})')

#for numbers like (XXX)YYY-ZZZZ eg. (650)723-1614
ppatterns.append('\((\d{3})\)(\d{3})-(\d{4})')

#for numbers like (XXX) YYY-ZZZZ eg. (650) 724-6354
ppatterns.append('\((\d{3})\)\s(\d{3})-(\d{4})')

#for numbers like XXX YYY ZZZZ eg. 650 723 5666
ppatterns.append('(\d{3})\s(\d{3})\s(\d{4})')

#for numbers like [XXX] YYY-ZZZZ and [XXX]YYY-ZZZZ eg. [650] 723-5499  [650]723-5499
ppatterns.append('\[(\d{3})\]\s?(\d{3})-(\d{4})')

#for numbers like XXX YYY-ZZZZ eg. 650 723-3432 
ppatterns.append('(\d{3})\s(\d{3})-(\d{4})')

#***********************************************************
#END Pattern Phones numbers matching 
#***********************************************************


""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you may should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
	for epat in epatterns:
		# each epat has 2 sets of parentheses so each match will have 2 items in a list
		matches = re.findall(epat,line)
		for m in matches:
			# string formatting operator % takes elements of list m
		        #   and inserts them in place of each %s in the result string 
			email = '%s@%s.edu' % m
			# dlwh 'd-l-w-h-@-s-t-a-n-f-o-r-d-.edu'
			email = email.replace('-','')  
			'''
				('hager', 'e', 'hager@cs.dot.jhu.dot.edu'),
				('hager', 'e', 'hager@cs.dot.jhu.edu'),
				('serafim', 'e', 'serafim@cs.dot.stanford.d
				('serafim', 'e', 'serafim@cs.dot.stanford.e
				('subh', 'e', 'uma@cs.dot.stanford.dot.edu'
				('subh', 'e', 'uma@cs.dot.stanford.edu')])
			'''
			email = email.replace(' dot ','.') 
			email = email.replace('dot.','')
			# set([('jks', 'e', 'jks@robotics;stanford.edu')])
			email = email.replace(';','.') 
			'''
			[('hager', 'e', 'hager@cs.jhu edu'),
			('pal', 'e', 'pal@cs stanford.edu'),
			('serafim', 'e', 'serafim@cs.stanford ed
			('subh', 'e', 'uma@cs.stanford edu')])
			'''
			email = email.replace(' ','.') 
			res.append((name,'e',email))
		
	for epat_custom in epatterns_custom:
		# each epat has 2 sets of parentheses so each match will have 2 items in a list
		matches = re.findall(epat_custom,line)
		for m in matches:
			# string formatting operator % takes elements of list m
			#   and inserts them in place of each %s in the result string 
			email = '%s@%s' % m
			ename = email.split('@',1)[1]
			edomain = email.split('@',1)[0]
			res.append((name,'e',ename+'@'+edomain))
	
	for compat in compatterns:
		# each epat has 2 sets of parentheses so each match will have 2 items in a list
		matches = re.findall(compat,line)
		for m in matches:
			# string formatting operator % takes elements of list m
			#   and inserts them in place of each %s in the result string 
			email = '%s@%s.com' % m
			res.append((name,'e',email))
		
        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            matches = re.findall(ppat,line)
            for m in matches:
                phone = '%s-%s-%s' % m
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
