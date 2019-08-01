import textwrap

init_text = '''
wssqdwfv sdwefsgg
b ghjuyiluo. wssqdwfv sdw
efsggb ghjuyiluo. 
wssqdwfv sdwefsggb ghjuyiluo. ws
sqdwfv sdwefs
ggb ghjuyiluo. 
wssqdwfv sdwefsggb ghjuyiluo. wssqdwfv s
dwefsggb ghjuyiluo. 
wssqdwfv sdwefsggb ghjuyiluo. wssqdwfv
 sdwefsggb ghjuyiluo. 
wssqdwfv sdwefsggb ghjuyiluo. 

 '''

dend_txt = textwrap.dedent(init_text)
result_txt = textwrap.fill(dend_txt, initial_indent='==>',
                      subsequent_indent=' ' * 8,
                      width=50)
print(result_txt)
