# SpamFinder
Spam Finder!! Using Regular Expressions to find email addresses and phone numbers  
On the web, many people who want to give their email addresses or phone numbers for people to contact them 
will try to make it hard for spammers to automatically search text for email addresses and phone numbers by 
giving non-standard forms of them, sometimes called obfuscation.  
You may have seen examples like:  
jurafsky(at)cs.stanford.edu  jurafsky at csli dot stanford dot edu  
Similarly, for phone numbers, given examples like:  
TEL +1-650-723-0293  Phone:  (650) 723-0293  

There is a directory called SpamLord that has the following structure:  
SpamLord/  SpamLord.py  data/   dev/    aiken    ashishg    . . .   devGold  
In the data/dev directory are text files that have html text with obscured emails and phone numbers from faculty and staff at Stanford.
In the data/devGold file are the corresponding standard form emails and phone numbers;  these are the correct answers.  
The program SpamLord.py is set up so that you can write a set of regular expressions with
parentheses to pick out the parts of the email address or phone numbers that match it in their obscured form.  
Then there is a function “process_filename” that goes through lines of the file, matches all the regular expressions 
and builds up a result list called “res” that has the name of the file, an ‘e’ or ‘p’ for email or phone, and the standard 
format email address or phone number.  

The rest of the program processes all the files in the dev directory and combines the standard form results,
it compares them with the devGold file and reports how many your program got right.  
In the evaluation part,  
• the true positive section displays e-mails and phone numbers which the code correctly matches, 
• the false positive section displays e-mails which the code regular expressions match but which are not correct, and
• the false negative section displays e-mails and phone numbers which the starter code did not match, but which do exist in the html files
