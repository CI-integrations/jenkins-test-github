def _check_undefined_vars(self, tree):
    undefined_vars = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            undefined_vars.discard(node.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            undefined_vars.add(node.id)

import click

@click.group()
@click.pass_context
def todo(ctx):
    '''Simple CLI Todo App'''
    ctx.ensure_object(dict)
    #Open todo.txt – first line contains latest ID, rest contain tasks and IDs
    with open('./todo.txt') as f:
        content = f.readlines()
    #Transfer data from todo.txt to the context
    ctx.obj['LATEST'] = int(content[:1][0])
    ctx.obj['TASKS'] = {en.split('```')[0]:en.split('```')[1][:-1] for en in content[1:]}

@todo.command()
@click.pass_context
def tasks(ctx):
    '''Display tasks'''
    if ctx.obj['TASKS']:
        click.echo('YOUR TASKS\n**********')
        #Iterate through all the tasks stored in the context
        for i, task in ctx.obj['TASKS'].items():
            click.echo('• ' + task + ' (ID: ' + i + ')')
        click.echo('')
    else:
        click.echo('No tasks yet! Use ADD to add one.\n')

@todo.command()
@click.pass_context
@click.option('-add', '--add_task', prompt='Enter task to add')
def add(ctx, add_task):
    '''Add a task'''
    if add_task:
        #Add task to list in context 
        ctx.obj['TASKS'][ctx.obj['LATEST']] = add_task
        click.echo('Added task "' + add_task + '" with ID ' + str(ctx.obj['LATEST']))
        #Open todo.txt and write current index and tasks with IDs (separated by " ``` ")
        curr_ind = [str(ctx.obj['LATEST'] + 1)] 
        tasks = [str(i) + '```' + t for (i, t) in ctx.obj['TASKS'].items()]
        with open('./todo.txt', 'w') as f:
            f.writelines(['%s\n' % en for en in curr_ind + tasks])

@todo.command()
@click.pass_context
@click.option('-fin', '--fin_taskid', prompt='Enter ID of task to finish', type=int)
def done(ctx, fin_taskid):
    '''Delete a task by ID'''
    #Find task with associated ID
    if str(fin_taskid) in ctx.obj['TASKS'].keys():
        task = ctx.obj['TASKS'][str(fin_taskid)]
        #Delete task from task list in context
        del ctx.obj['TASKS'][str(fin_taskid)]
        click.echo('Finished and removed task "' + task + '" with id ' + str(fin_taskid))
        #Open todo.txt and write current index and tasks with IDs (separated by " ``` ")
        if ctx.obj['TASKS']:
            curr_ind = [str(ctx.obj['LATEST'] + 1)] 
            tasks = [str(i) + '```' + t for (i, t) in ctx.obj['TASKS'].items()]
            with open('./todo.txt', 'w') as f:
                f.writelines(['%s\n' % en for en in curr_ind + tasks])
        else:
            #Resets ID tracker to 0 if list is empty
            with open('./todo.txt', 'w') as f:
                f.writelines([str(0) + '\n'])
    else:
        click.echo('Error: no task with id ' + str(fin_taskid))

if __name__ == '__main__':
    todo()

import numpy as np

def Cal_IoU(GT_bbox, Pred_bbox):
    '''
    Args:
        GT_bbox:  the bounding box of the ground truth
        Pred_bbox: the bounding box of the predicted
    Returns:
        IoU: Intersection over Union
    '''
    #1. Calculate the area of the intersecting area
    ixmin = max(GT_bbox[0], Pred_bbox[0])
    iymin = max(GT_bbox[1], Pred_bbox[1])
    ixmax = min(GT_bbox[2], Pred_bbox[2])
    iymax = min(GT_bbox[3], Pred_bbox[3])
    iw = np.maximum(ixmax - ixmin + 1., 0.) # the weight of the area
    ih = np.maximum(iymax - iymin + 1., 0.) # the height of the area
    area = iw * ih

    #2. Calculate the area of all area
    #S = S1 + S2 - area
    S1 = (Pred_bbox[2] - GT_bbox[0] + 1) * (Pred_bbox[3] - GT_bbox[1] + 1)
    S2 = (GT_bbox[2] - GT_bbox[0] + 1) * (GT_bbox[3] - GT_bbox[1] + 1)
    S = S1 + S2 - area

    #3. Calculate the IoU
    iou = area / S
    return iou

if __name__ == "__main__":
    pred_bbox = np.array([40, 40, 100, 100])
    gt_bbox = np.array([70, 80, 110, 130])
    print(Cal_IoU(pred_bbox, gt_bbox))

import tkinter as tk
from tkinter import filedialog
from PIL import Image
root = tk.Tk()   # Tkinter window initialized
root.title('Converter')     # Title of the window
canvas1 = tk.Canvas(root, width=300, height=250, bg='orange', relief='raised')
canvas1.pack()
label1 = tk.Label(root, text='File Converter', bg='lightsteelblue2')   # giving a title to the screen
label1.config(font=('helvetica', 20))
canvas1.create_window(150, 60, window=label1)
im1 = None  # variable to store path of image


def getJPG():
    '''Function to get image location and open it with pillow'''
    global im1
    import_file_path = filedialog.askopenfilename()
    im1 = Image.open(import_file_path)


font = ('helvetica', 12, 'bold')
bg = 'royalblue'
fg = 'white'
browseButton_JPG = tk.Button(text="      Import JPEG File     ", command=getJPG, bg=bg, fg=fg, font=font)   # Browse button
canvas1.create_window(150, 130, window=browseButton_JPG)


def convertToPNG():
    '''Function to change file extenstion to png and save it to User's prefered location '''
    global im1
    if im1 is None:
        tk.messagebox.showerror("Error", "No File selected")
    else:
        export_file_path = filedialog.asksaveasfilename(defaultextension='.png')
        im1.save(export_file_path)


saveAsButton_PNG = tk.Button(text='Convert JPEG to PNG', command=convertToPNG, bg=bg, fg=fg, font=font)      # Convert button
canvas1.create_window(150, 180, window=saveAsButton_PNG)
root.mainloop()                    