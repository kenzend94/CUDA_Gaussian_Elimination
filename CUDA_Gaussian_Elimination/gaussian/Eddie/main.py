import tkinter as tk
import os
from bst import BDD, BDDNode

#import Test_NN
#from Train_Neural_Net import train_NN


# Global strings for file names.
TEST_FILE_NAME = 'Chandler was bored when he named this'
ANS_FILE_NAME = 'We have been trying to reach you about your cars extended warrenty'
NEURAL_NET = 'GRU.V.4.02.h5'   # this is the model you type in or the one automatically selected.
TRAIN_NEW = False


def search_file(f_name, new_file=False,return_list=''):
    '''This will return the next available file name or a\n 
    list of training files to choose from. return_list\n
    requires the desired file type. eg. \'.csv\''''
    if new_file:
        version = 0
        ext = '.'+f_name.split('.')[-1]
        f_name= f_name[0:-(len(ext))]
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f_name in f:
                if 1+int(f.split('.')[3])>version:
                    version = 1+int(f.split('.')[3])
                    
        new_file= f_name+'.'+str(version)+ext
        print('new file name was given as: {}'.format(new_file))
        return new_file
    
    elif return_list != '':
        new_file = []
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if return_list in f and f_name in f:
                new_file.append(f)
        return new_file
    
    else:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f_name == f:
                return f_name
        print('There is no file with that name.')
        raise ValueError('File name passed into search_files\n\
                          does not exist in current directory.')



"""def create_text_entry_interface():
    def submit_text():
        '''Change global files to user selection'''
        global TEST_FILE_NAME
        global ANS_FILE_NAME
        global NEURAL_NET
        TEST_FILE_NAME = t_fname.get()
        ANS_FILE_NAME = answer_fname.get()
        print(net_fname.get(),TEST_FILE_NAME, ANS_FILE_NAME)
        if TRAIN_NEW:
            NEURAL_NET = search_file(net_fname.get(),new_file=True)
        else:
            NEURAL_NET = search_file(net_fname.get())
        #print("User text:", t_text,ans_text)
        text_entry_window.destroy()
    selected_option = option_var.get()
    
    text_entry_window = tk.Tk()
    text_entry_window.title("Data File Selection")
    text_entry_window.geometry('500x500')

    text_label = tk.Label(text_entry_window, text="Please enter the desired file name for recieved data:",height=5,width=50)
    text_label.pack()
    t_fname = tk.Entry(text_entry_window,width=50)
    t_fname.pack()

    text_label = tk.Label(text_entry_window, text="Please enter the desired file name for answer data:",height=5,width=50)
    text_label.pack()
    answer_fname = tk.Entry(text_entry_window,width=50)
    answer_fname.pack()
    
    text_label = tk.Label(text_entry_window, text="Please enter the desired file name for the Neural Net model",height=5,width=50)
    text_label.pack()
    if selected_option == "Train New":
        global TRAIN_NEW
        TRAIN_NEW = True
        net_fname = tk.Entry(text_entry_window,width=50)
        net_fname.pack()
    else:
        net_choices = search_file('GRU.V.3',return_list='.png')

        net_fname = tk.StringVar(text_entry_window)
        net_fname.set(str(net_choices[0]))
        
        net_menu = tk.OptionMenu(text_entry_window, net_fname, *net_choices)
        net_menu.pack(padx=25, pady=20)#,side='left'
    #this is the Run button under the text box.
    submit_button = tk.Button(text_entry_window, text="Run", command=submit_text)
    submit_button.pack(padx=25,pady=25)
    text_entry_window.mainloop()"""


def on_option_selected():
    selected_option = option_var.get()
    #print("Selected option:", selected_option)
    global firstw
    if firstw:
        main_window.destroy()
        firstw=False
    #inside this if loop will return a drop menu with all the files you can choose.
    if selected_option == 'Present':
        def submit_f_names():
            '''Change global files to user selected ones.'''
            global ANS_FILE_NAME
            global TEST_FILE_NAME
            global NEURAL_NET
            TEST_FILE_NAME = node_name.get()
            ANS_FILE_NAME = selected_node.get()
            NEURAL_NET = selected_node1.get()
            presentation_window.destroy()
            #print(TEST_FILE_NAME,ANS_FILE_NAME, NEURAL_NET)
            if bdd.root is None:
                if int(ANS_FILE_NAME) in bdd.terminal_nodes:
                    ANS_FILE_NAME = bdd.terminal_nodes[int(ANS_FILE_NAME)]
                    NEURAL_NET = bdd.terminal_nodes[int(NEURAL_NET)]
                    TEST_FILE_NAME = bdd.make_node(TEST_FILE_NAME, bdd.find(value=ANS_FILE_NAME),bdd.find(value=NEURAL_NET))
                    bdd.root = TEST_FILE_NAME
                    bdd.create_dotfile()
                    on_option_selected()
            else:
                #print(bdd.find(value=ANS_FILE_NAME), bdd.find(value=NEURAL_NET))

                TEST_FILE_NAME = bdd.make_node(TEST_FILE_NAME, bdd.find(value=ANS_FILE_NAME),bdd.find(value=NEURAL_NET))
                bdd.root = TEST_FILE_NAME
                bdd.create_dotfile()
                on_option_selected()

        presentation_window = tk.Tk()
        presentation_window.title("Class Final Project")
        presentation_window.geometry('1200x1200')
        presentation_window.configure(background='black')
        presentation_window.grid_columnconfigure(1, weight=0)
        presentation_window.grid_columnconfigure(2, weight=0)
        presentation_window.grid_columnconfigure(3, weight=0)
        presentation_window.grid_columnconfigure(4, weight=0)
        presentation_window.grid_columnconfigure(5, weight=0)

        # add an image
        #rnn_photo = tk.PhotoImage(file='RNN_layer.png')
        #image = tk.Label(presentation_window, image=rnn_photo, width=550, bg="black")
        #image.grid(row=5, column=3, columnspan=3,rowspan=10, stick="N")
        #add the Raytheon Logo image.
        #dot_file = 'Graph_image.dot'  # Replace with your .dot file path
        #temp_fig = convert_dot_to_image(dot_file, 'png')
        nn_photo = tk.PhotoImage(file='BDDtree.png')
        image = tk.Label(presentation_window, image=nn_photo, bg="black")
        image.grid(row=50, column=20, columnspan=10,rowspan=50, stick="W")#
        
        '''
        #add the Raytheon Logo image.
        photo = tk.PhotoImage(file='Raytheon_logo_small.png')
        image = tk.Label(presentation_window,image=photo,width=250,bg="white")
        image.grid(row=0,column=1,columnspan=1,rowspan=5,stick="W")'''

        #add ECE Logo
        ece_photo = tk.PhotoImage(file='UoU_ece_logo_small.png')
        image = tk.Label(presentation_window,image=ece_photo,bg="white")
        image.grid(row=0,column=0,rowspan=5,columnspan=1,stick="W")

        #add the options for noise
        options_label = tk.Label(presentation_window,background='black',foreground='white', text="Enter the name of your new node.")
        options_label.grid(row=5, column=0, columnspan=2,rowspan=1, stick="S")#pack()#side='left'

        #f_test_choices = search_file('n', return_list='.png')
        node_name = tk.Entry(presentation_window,width=30)
        #node_name.pack()
        #selected_test_data.set(str(f_test_choices[0]))
        #f_test_menu = tk.OptionMenu(presentation_window, selected_test_data, *f_test_choices)
        node_name.configure(background='red2',foreground='white',highlightcolor='red')
        node_name.grid(row=6, column=0, columnspan=2,rowspan=1, stick="N")#.pack(padx=25, pady=20)#,side='left'
        f_node = bdd.inorder()
        nodes = []
        for n in f_node:
            if n not in nodes:
                nodes.append(n)
        f_node = nodes
        
        '''try:
            for i in nodes:
                f_node.append(i.variable)
        except:
            pass'''
        if len(f_node)<2:
           f_node=['1','0']
        options_label = tk.Label(presentation_window,background='black',foreground='white', text="select the if true then -> node.")
        options_label.grid(row=8, column=0, columnspan=2,rowspan=1, stick="S")#.pack()#side='right'
        selected_node1 = tk.StringVar(presentation_window)
        selected_node1.set(next(iter(f_node)))
        f_ans_menu = tk.OptionMenu(presentation_window, selected_node1, *f_node)
        f_ans_menu.configure(activebackground='SpringGreen4',activeforeground='black',
          background='red2',foreground='white',highlightcolor='red')
        f_ans_menu.grid(row=9, column=0, columnspan=2,rowspan=1, stick="N")#.pack(padx=25, pady=20)#,side='right'


        options_label = tk.Label(presentation_window,background='black',foreground='white', text="select the else -> node.")
        options_label.grid(row=10, column=0, columnspan=2,rowspan=1, stick="S")#.pack()#side='right'
        selected_node = tk.StringVar(presentation_window)
        selected_node.set(str(f_node[0]))
        f_ans_menu = tk.OptionMenu(presentation_window, selected_node, *f_node)
        f_ans_menu.configure(activebackground='SpringGreen4',activeforeground='black',
          background='red2',foreground='white',highlightcolor='red')
        f_ans_menu.grid(row=11, column=0, columnspan=2,rowspan=1, stick="N")#.pack(padx=25, pady=20)#,side='right'

        run_button = tk.Button(presentation_window, foreground='white', background='red2',highlightcolor='SpringGreen4',activebackground='SpringGreen4', text="Update BDD", command=submit_f_names)
        run_button.grid(pady=15,row=16, column=0, columnspan=2,rowspan=1, stick="N")#.pack(padx=5, pady=10)

        presentation_window.mainloop()
        
    '''else:
        create_text_entry_interface()'''

bdd = BDD()
#bdd.create_dotfile()
global firstw
firstw = True

main_window = tk.Tk()


main_window.title("Binary Desision Diagram")
main_window.geometry("1200x800")
main_window.configure(background="white")
main_window.grid_columnconfigure(1, weight=0)
main_window.grid_columnconfigure(2, weight=0)
main_window.grid_columnconfigure(3, weight=0)

#add Project Title
project_name = tk.Label(main_window, 
  text="Live View and construction of BDD",
  font=('Times New Roman',36),fg='black',background='white')
project_name.grid(row=0,column=1,rowspan=1,columnspan=5,sticky='S')

#add the Raytheon Logo image.
photo = tk.PhotoImage(file='bdd_eg.png')
image = tk.Label( main_window, image=photo, bg="white")
image.grid(row=1,column=0,columnspan=3,rowspan=9,stick="W")

#add ECE Logo
ece_photo = tk.PhotoImage(file='UoU_ece_logo.png')
image = tk.Label(main_window, image=ece_photo, bg="white")
image.grid(row=1,column=3, rowspan=9,columnspan=5,stick="W")
'''
#add project overview image
overview_photo = tk.PhotoImage(file='project_overveiw.png')
image = tk.Label(main_window, image=overview_photo, bg="white")
image.grid(row=10,column=1, rowspan=9,columnspan=3,stick="N")
'''


# add group members
authors_label = tk.Label(main_window, text="Authors",font=('Times New Roman',24),fg='black',background='white')
authors_label.grid(row=11,column=3,rowspan=2,columnspan=2,sticky='S')
authors = tk.Label(main_window, text="Chandler Welch\nENTER NAME HERE\nENTER NAME HERE",font=('Times New Roman',12),fg='black',background='white')
authors.grid(row=13,column=3,rowspan=5,columnspan=2,sticky='N')

#add advisors
authors_label = tk.Label(main_window, text="Professor",font=('Times New Roman',24),fg='black',background='white')
authors_label.grid(row=11,column=5,rowspan=2,columnspan=2,sticky='S')
authors = tk.Label(main_window, text="PRIYANK KALLA",font=('Times New Roman',12),fg='black',background='white')
authors.grid(row=13,column=5,rowspan=5,columnspan=2,sticky='N')


option_var = tk.StringVar(main_window)
option_var.set("Present")

options_label = tk.Label(main_window, text="Select a configuration option:",background='white')
options_label.grid(row=11,column=0,rowspan=1,columnspan=2,sticky='W')
#options_label.pack()

option_menu = tk.OptionMenu(main_window,option_var, "Present")
option_menu.grid(row=12,column=0,rowspan=1,columnspan=2,sticky='W')
option_menu.configure(background='red3',activebackground='SpringGreen4',padx=2,pady=5)
#option_menu.pack(padx=25, pady=20,side='left')

submit_button = tk.Button(main_window, text="Submit", background='SpringGreen4',command=on_option_selected)
submit_button.grid(row=13,column=0,rowspan=1,columnspan=2,sticky='W',padx=2,pady=5)
#submit_button.pack(padx=25, pady=20)

main_window.mainloop()


def test_code():
    print(search_file('GRU.V.3.h5'),search_file('GRU.V.3.h5',new_file=True),search_file('a',return_list='.png'))
#test_code()