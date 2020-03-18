import re

raw_text = '''
Once upon a time, long, long ago a king and queen ruled over a distant land. 
The queen was kind and lovely and all the people of the realm adored her.
The only sadness in the queen's life was that she wished for a child but
did not have one. One winter day, the queen was doing needle work while
gazing out her ebony window at the new fallen snow. A bird flew by the window
startling the queen and she pricked her finger. A single drop of blood fell
on the snow outside her window. As she looked at the blood on the snow she
said to herself, "Oh, how I wish that I had a daughter that had skin as white
as snow, lips as red as blood, and hair as black as ebony." Soon after that,
the kind queen got her wish when she gave birth to a baby girl who had skin
white as snow, lips red as blood, and hair black as ebony. They named the baby
princess Snow White, but sadly, the queen died after giving birth to Snow White.
'''
text = re.sub('[\.,"]', '', raw_text)
distinct_words = list(set(filter(lambda s: len(s) > 0, re.split(r'\s', text))))
words = list(filter(lambda s: len(s) > 0, re.split(r'\s', text)))
