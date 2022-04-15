import os

from NEAT.neat_run import NeatRun
from tkinter import *
from tkinter import messagebox


class App:

    """ Contains the methods for displaying the evolutionary process, including
        the Tkinter mainloop. Creates the neat object and controls the running
        of each generation. """

    NET_WIDTH = 0.57
    NET_HEIGHT = 0.995

    CANVAS_BG = "black"
    NODE_COLOUR = "black"
    NODE_BORDER_COLOUR = "white"
    NODE_RADIUS = 20
    NODE_BORDER_SIZE = 3
    NODE_FONT = "ariel 10"
    NODE_TEXT_COLOUR = "white"

    FRAME_BORDER_COLOUR = "white"
    FRAME_BORDER_SIZE = 1

    CONN_COLOUR = "green"
    CONN_DISABLED_COLOUR = "red"
    CONN_WIDTH = 2
    DISABLED_CONN_WIDTH = 3

    STATS_IPADX = 153
    STATS_PADX = 5
    STATS_BG = "black"
    STATS_TITLE_FONT = "ariel 19 underline"
    STATS_FONT = "ariel 18"
    STATS_TEXT_BG = "black"
    STATS_TEXT_FG = "white"

    CONNS_IPADX = 60
    CONNS_PADX = 0
    CONNS_BG = "black"
    CONNS_FONT = "ariel 12"
    CONNS_TITLE_FONT = "ariel 19 underline"
    CONNS_TEXT_BG = "black"
    CONNS_TEXT_FG = "white"

    CONTROL_BG = "black"
    CONTROL_FRAME_FONT = "ariel 14"
    CONTROL_FRAME_FONT_FG = "black"
    CONTROL_FRAME_LABEL_BG = "black"
    CONTROL_FRAME_LABEL_FG = "white"
    CONTROL_BUTTON_OFF_BG = "#7c7f83"  # grey
    CONTROL_BUTTON_ON_BG = "#457aba"  # blue
    CONTROL_FRAME_PAD_Y = 10

    RUN_BUTTON_WIDTH = 10
    RUN_BUTTON_HEIGHT = 1

    SKIP_BUTTON_WIDTH = 3
    SKIP_BUTTON_HEIGHT = 1

    SPECIES_BUTTON_WIDTH = 9
    SPECIES_BUTTON_HEIGHT = 1
    POP_BUTTON_WIDTH = 9
    POP_BUTTON_HEIGHT = 1

    CHOOSE_GEN_ENTRY_WIDTH = 4
    CHOOSE_GEN_BUTTON_WIDTH = 7
    CHOOSE_GEN_BUTTON_HEIGHT = 1

    SAVE_NET_ENTRY_WIDTH = 10
    SAVE_BUTTON_WIDTH = 4
    SAVE_BUTTON_HEIGHT = 1

    def __init__(self, config, fitness):

        """ Initialises the display. """

        self.__neat = NeatRun(config)
        self.__curr_agent_pop_index = 0
        self.__curr_agent_specie_index = 0
        self.__curr_species_id = 0
        self.__num_gen_skip = 1
        self.__search_mode = "p"
        self.__exit = False

        self.__root = Tk()
        self.__root.attributes("-fullscreen", True)
        self.__root.config(bg="black")
        self.__root.option_add("*font", "ariel 20")

        self.__root.bind("<Escape>", self.__escape_pressed)
        self.__root.bind("<Return>", lambda args: self.__return_pressed(fitness))
        self.__root.bind("<Right>", self.__lr_pressed)
        self.__root.bind("<Left>", self.__lr_pressed)
        self.__root.bind("<Up>", self.__ud_pressed)
        self.__root.bind("<Down>", self.__ud_pressed)

        self.__cnv = Canvas(self.__root, width=self.__root.winfo_screenwidth() * App.NET_WIDTH,
                            height=self.__root.winfo_screenheight() * App.NET_HEIGHT, bg=App.CANVAS_BG)
        self.__cnv.grid(row=0, column=0, rowspan=2)

        # STATS_FRAME
        self.__stats_frame = Frame(self.__root, bg=App.STATS_BG, highlightbackground=App.FRAME_BORDER_COLOUR,
                                   highlightthickness=App.FRAME_BORDER_SIZE)
        self.__stats_frame.grid(row=0, column=1, sticky="nw", padx=App.STATS_PADX)

        self.__stats_title = Label(self.__stats_frame, text="Stats",
                                   font=App.STATS_TITLE_FONT, bg=App.STATS_TEXT_BG,
                                   fg=App.STATS_TEXT_FG)
        self.__stats_title.grid(row=0, column=0, ipadx=App.STATS_IPADX)
        self.__fitness_threshold_lbl = Label(self.__stats_frame, text=f"Fitness Threshold: {config.fitness_threshold}",
                                             font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                             fg=App.STATS_TEXT_FG)
        self.__fitness_threshold_lbl.grid(row=1, column=0, sticky='w')
        self.__pop_size_lbl = Label(self.__stats_frame, text=f"Population Size: {config.pop_size}",
                                    font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                    fg=App.STATS_TEXT_FG)
        self.__pop_size_lbl.grid(row=2, column=0, sticky='w')
        self.__species_target_lbl = Label(self.__stats_frame, text=f"Species Target: {config.target_species_num}",
                                          font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                          fg=App.STATS_TEXT_FG)
        self.__species_target_lbl.grid(row=3, column=0, sticky='w')

        self.__gen_num_lbl = Label(self.__stats_frame, text="Generation Number: ",
                                   font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                   fg=App.STATS_TEXT_FG)
        self.__gen_num_lbl.grid(row=4, column=0, sticky='w')
        self.__num_species_lbl = Label(self.__stats_frame, text="Species: ",
                                       font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                       fg=App.STATS_TEXT_FG)
        self.__num_species_lbl.grid(row=5, column=0, sticky='w')
        self.__dist_threshold_lbl = Label(self.__stats_frame, text="Distance Threshold: ",
                                          font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                          fg=App.STATS_TEXT_FG)
        self.__dist_threshold_lbl.grid(row=6, column=0, sticky='w')
        self.__agent_id_lbl = Label(self.__stats_frame, text="Agent id: ",
                                    font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                    fg=App.STATS_TEXT_FG)
        self.__agent_id_lbl.grid(row=7, column=0, sticky='w')
        self.__agent_fitness_lbl = Label(self.__stats_frame, text="Agent Fitness: ",
                                         font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                         fg=App.STATS_TEXT_FG)
        self.__agent_fitness_lbl.grid(row=8, column=0, sticky='w')
        self.__pop_avg_fitness_lbl = Label(self.__stats_frame, text="Population Average Fitness: ",
                                           font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                           fg=App.STATS_TEXT_FG)
        self.__pop_avg_fitness_lbl.grid(row=9, column=0, sticky='w')
        self.__species_id_lbl = Label(self.__stats_frame, text="Species ID: ",
                                      font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                      fg=App.STATS_TEXT_FG)
        self.__species_id_lbl.grid(row=10, column=0, sticky='w')
        self.__species_avg_fitness_lbl = Label(self.__stats_frame, text="Species Average Fitness: ",
                                               font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                               fg=App.STATS_TEXT_FG)
        self.__species_avg_fitness_lbl.grid(row=11, column=0, sticky='w')
        self.__agent_species_size_lbl = Label(self.__stats_frame, text="Agent Species Size: ",
                                              font=App.STATS_FONT, bg=App.STATS_TEXT_BG,
                                              fg=App.STATS_TEXT_FG)
        self.__agent_species_size_lbl.grid(row=12, column=0, sticky='w')

        # CONNS_FRAME
        self.__conns_frame = Frame(self.__root, bg=App.CONNS_BG)
        self.__conns_frame.grid(row=0, column=2, rowspan=2, sticky="ne", padx=App.CONNS_PADX)
        self.__conns_title = Label(self.__conns_frame, text="Connections",
                                   font=App.CONNS_TITLE_FONT, bg=App.CONNS_TEXT_BG, fg=App.CONNS_TEXT_FG)
        self.__conns_title.grid(row=0, column=0, columnspan=2, ipadx=App.CONNS_IPADX, sticky='n')
        self.__conn_labels = []

        # CONTROL_FRAME
        self.__control_frame = Frame(self.__root, bg=App.CONTROL_BG)
        self.__control_frame.grid(row=1, column=1, columnspan=2, stick='sw')

        self.__until_found_lbl = Label(self.__control_frame, text="=> Found: ", font=App.CONTROL_FRAME_FONT,
                                       bg=App.CONTROL_FRAME_LABEL_BG, fg=App.CONTROL_FRAME_LABEL_FG)
        self.__until_found_lbl.grid(row=0, column=0)
        self.__run_button = Button(self.__control_frame, text="Run", font=App.CONTROL_FRAME_FONT,
                                   width=App.RUN_BUTTON_WIDTH,
                                   height=App.RUN_BUTTON_HEIGHT,
                                   bg=App.CONTROL_BUTTON_OFF_BG,
                                   activebackground=App.CONTROL_BUTTON_ON_BG,
                                   activeforeground=App.CONTROL_FRAME_FONT_FG,
                                   command=lambda: self.__run_pressed(fitness))
        self.__run_button.grid(row=0, column=1, columnspan=3, pady=App.CONTROL_FRAME_PAD_Y)

        self.__skip_label = Label(self.__control_frame, text="Skip: ", font=App.CONTROL_FRAME_FONT,
                                  bg=App.CONTROL_FRAME_LABEL_BG, fg=App.CONTROL_FRAME_LABEL_FG)
        self.__skip_label.grid(row=1, column=0, pady=App.CONTROL_FRAME_PAD_Y)

        self.__skip_one_button = Button(self.__control_frame, text="1", width=App.SKIP_BUTTON_WIDTH,
                                        height=App.SKIP_BUTTON_HEIGHT, bg=App.CONTROL_BUTTON_ON_BG,
                                        activebackground=App.CONTROL_BUTTON_OFF_BG,
                                        activeforeground=App.CONTROL_FRAME_FONT_FG,
                                        command=lambda: self.__switch_num_gen_skip(1))
        self.__skip_one_button.grid(row=1, column=1, pady=App.CONTROL_FRAME_PAD_Y, sticky='w')
        self.__skip_ten_button = Button(self.__control_frame, text="10", width=App.SKIP_BUTTON_WIDTH,
                                        height=App.SKIP_BUTTON_HEIGHT, bg=App.CONTROL_BUTTON_OFF_BG,
                                        activebackground=App.CONTROL_BUTTON_OFF_BG,
                                        activeforeground=App.CONTROL_FRAME_FONT_FG,
                                        command=lambda: self.__switch_num_gen_skip(10))
        self.__skip_ten_button.grid(row=1, column=1, pady=App.CONTROL_FRAME_PAD_Y, columnspan=2)
        self.__skip_two_five_button = Button(self.__control_frame, text="25", width=App.SKIP_BUTTON_WIDTH,
                                             height=App.SKIP_BUTTON_HEIGHT, bg=App.CONTROL_BUTTON_OFF_BG,
                                             activebackground=App.CONTROL_BUTTON_OFF_BG,
                                             activeforeground=App.CONTROL_FRAME_FONT_FG,
                                             command=lambda: self.__switch_num_gen_skip(25))
        self.__skip_two_five_button.grid(row=1, column=2, pady=App.CONTROL_FRAME_PAD_Y, sticky='e')

        self.__search_mode_lbl = Label(self.__control_frame, text="Search Mode: ", font=App.CONTROL_FRAME_FONT,
                                       bg=App.CONTROL_FRAME_LABEL_BG, fg=App.CONTROL_FRAME_LABEL_FG)
        self.__search_mode_lbl.grid(row=2, column=0, pady=App.CONTROL_FRAME_PAD_Y)
        self.__pop_button = Button(self.__control_frame, text="Population", font=App.CONTROL_FRAME_FONT,
                                   width=App.POP_BUTTON_WIDTH,
                                   height=App.POP_BUTTON_HEIGHT, bg=App.CONTROL_BUTTON_ON_BG,
                                   activebackground=App.CONTROL_BUTTON_OFF_BG,
                                   activeforeground=App.CONTROL_FRAME_FONT_FG,
                                   command=lambda: self.__switch_search_mode("p"))
        self.__pop_button.grid(row=2, column=1, pady=App.CONTROL_FRAME_PAD_Y)
        self.__species_button = Button(self.__control_frame, text="Species", font=App.CONTROL_FRAME_FONT,
                                       width=App.SPECIES_BUTTON_WIDTH,
                                       height=App.SPECIES_BUTTON_HEIGHT, bg=App.CONTROL_BUTTON_OFF_BG,
                                       activebackground=App.CONTROL_BUTTON_OFF_BG,
                                       activeforeground=App.CONTROL_FRAME_FONT_FG,
                                       command=lambda: self.__switch_search_mode("s"))
        self.__species_button.grid(row=2, column=2, pady=App.CONTROL_FRAME_PAD_Y)

        self.__choose_gen_lbl = Label(self.__control_frame, text="Choose Gen: ", font=App.CONTROL_FRAME_FONT,
                                      bg=App.CONTROL_FRAME_LABEL_BG, fg=App.CONTROL_FRAME_LABEL_FG)
        self.__choose_gen_lbl.grid(row=3, column=0)
        self.__choose_gen_entry = Entry(self.__control_frame, width=App.CHOOSE_GEN_ENTRY_WIDTH)
        self.__choose_gen_entry.grid(row=3, column=1, pady=App.CONTROL_FRAME_PAD_Y)
        self.__choose_gen_button = Button(self.__control_frame, text="Confirm", font=App.CONTROL_FRAME_FONT,
                                          width=App.CHOOSE_GEN_BUTTON_WIDTH,
                                          height=App.CHOOSE_GEN_BUTTON_HEIGHT,
                                          bg=App.CONTROL_BUTTON_OFF_BG,
                                          activebackground=App.CONTROL_BUTTON_ON_BG,
                                          activeforeground=App.CONTROL_FRAME_FONT_FG,
                                          command=lambda: self.__choose_gen_confirm(fitness))
        self.__choose_gen_button.grid(row=3, column=2, pady=App.CONTROL_FRAME_PAD_Y)

        self.__save_net_lbl = Label(self.__control_frame, text="Save As: ", font=App.CONTROL_FRAME_FONT,
                                    bg=App.CONTROL_FRAME_LABEL_BG, fg=App.CONTROL_FRAME_LABEL_FG)
        self.__save_net_lbl.grid(row=4, column=0)
        self.__save_net_entry = Entry(self.__control_frame, width=App.SAVE_NET_ENTRY_WIDTH)
        self.__save_net_entry.grid(row=4, column=1, columnspan=2, pady=App.CONTROL_FRAME_PAD_Y, sticky='w')
        self.__save_net_button = Button(self.__control_frame, text="Save", font=App.CONTROL_FRAME_FONT,
                                        width=App.SAVE_BUTTON_WIDTH,
                                        height=App.SAVE_BUTTON_HEIGHT,
                                        bg=App.CONTROL_BUTTON_OFF_BG,
                                        activebackground=App.CONTROL_BUTTON_ON_BG,
                                        activeforeground=App.CONTROL_FRAME_FONT_FG,
                                        command=self.__save_net)
        self.__save_net_button.grid(row=4, column=2, pady=App.CONTROL_FRAME_PAD_Y, sticky='e')

        self.__root.mainloop()

    # Private Methods
    def __escape_pressed(self, event):
        self.__exit = True
        quit()

    def __return_pressed(self, fitness):

        """ Calls the method which skips self.__num_gen_skip
            number of generations. """

        self.__new_gen(fitness, self.__num_gen_skip)

    def __lr_pressed(self, event):

        """ Moves to the next agent in the population or species depending on
            self.__search_mode. """

        if self.__neat.gen_num == -1:
            return
        if self.__search_mode == 'p':
            match event.keysym:
                case "Right":
                    if self.__search_mode == 'p':
                        if self.__curr_agent_pop_index < self.__neat.config.pop_size - 1:
                            self.__curr_agent_pop_index += 1
                        else:
                            self.__curr_agent_pop_index = 0
                case "Left":
                    if self.__curr_agent_pop_index > 0:
                        self.__curr_agent_pop_index -= 1
                    else:
                        self.__curr_agent_pop_index = self.__neat.config.pop_size - 1
            agent = self.__neat.population[self.__curr_agent_pop_index]
            self.__curr_species_id = agent.species_id
        else:
            match event.keysym:
                case "Right":
                    if self.__curr_agent_specie_index < self.__neat.species[self.__curr_species_id].size - 1:
                        self.__curr_agent_specie_index += 1
                    else:
                        self.__curr_agent_specie_index = 0
                case "Left":
                    if self.__curr_agent_specie_index > 0:
                        self.__curr_agent_specie_index -= 1
                    else:
                        self.__curr_agent_specie_index = self.__neat.species[self.__curr_species_id].size - 1
            agent = self.__neat.species[self.__curr_species_id].agents[self.__curr_agent_specie_index]
            self.__curr_agent_pop_index = self.__neat.population.index(agent)
        self.__update_display(agent)

    def __ud_pressed(self, event):

        """ Moves to the next species when the search mode is 's' """

        if self.__search_mode == 'p' or self.__neat.gen_num == -1:
            return
        match event.keysym:
            case "Up":
                if self.__curr_species_id < len(self.__neat.species) - 1:
                    self.__curr_species_id += 1
                else:
                    self.__curr_species_id = 0
            case "Down":
                if self.__curr_species_id > 0:
                    self.__curr_species_id -= 1
                else:
                    self.__curr_species_id = len(self.__neat.species) - 1
        self.__curr_agent_specie_index = 0
        agent = self.__neat.species[self.__curr_species_id].agents[self.__curr_agent_specie_index]
        self.__update_display(agent)

    def __run_pressed(self, fitness):

        """ Runs the evolutionary process until an agent's fitness exceed
            the fitness threshold """

        found = False
        while not found:
            self.__new_gen(fitness, 1)
            if self.__neat.get_fittest_agent().fitness > self.__neat.config.fitness_threshold:
                found = True

    def __switch_num_gen_skip(self, skip):

        """ Changes self.__num_gen_skip to the value selected by the user.
            Also changes the colours of the buttons. """

        match self.__num_gen_skip:
            case 1:
                self.__skip_one_button.config(bg=App.CONTROL_BUTTON_OFF_BG)
            case 10:
                self.__skip_ten_button.config(bg=App.CONTROL_BUTTON_OFF_BG)
            case 25:
                self.__skip_two_five_button.config(bg=App.CONTROL_BUTTON_OFF_BG)
        match skip:
            case 1:
                self.__skip_one_button.config(bg=App.CONTROL_BUTTON_ON_BG)
            case 10:
                self.__skip_ten_button.config(bg=App.CONTROL_BUTTON_ON_BG)
            case 25:
                self.__skip_two_five_button.config(bg=App.CONTROL_BUTTON_ON_BG)
        self.__num_gen_skip = skip

    def __switch_search_mode(self, mode):

        """ Changes the self.__search_mode to the mode selected by the user.
            Also changes the colours of the buttons. """

        match self.__search_mode:
            case 'p':
                self.__pop_button.config(bg=App.CONTROL_BUTTON_OFF_BG)
            case 's':
                self.__species_button.config(bg=App.CONTROL_BUTTON_OFF_BG)
        match mode:
            case 'p':
                self.__pop_button.config(bg=App.CONTROL_BUTTON_ON_BG)
            case 's':
                self.__species_button.config(bg=App.CONTROL_BUTTON_ON_BG)
        self.__search_mode = mode

    def __choose_gen_confirm(self, fitness):

        """ Calculates how many generations must be skipped depending on the generation
            entered by the user. Calls the method which skips to the chosen generation. """

        self.__root.focus()
        try:
            gen = int(self.__choose_gen_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Entry", "Must be an integer.")
            return
        if gen > self.__neat.gen_num:
            self.__choose_gen_entry.delete(0, "end")
            self.__new_gen(fitness, gen - self.__neat.gen_num)
        else:
            messagebox.showwarning("Invalid Entry", "Value must be greater than the current generation number.")

    def __new_gen(self, fitness, gen):

        """ Calls the main NEAT sequence. Calls the method which is in charge of
            updating the display. Loops for the number of generations passed into
            the method. """

        for i in range(gen):
            self.__neat.generation(fitness)
            fittest_agent = self.__neat.get_fittest_agent()
            self.__curr_agent_pop_index = self.__neat.population.index(fittest_agent)
            self.__curr_agent_specie_index = fittest_agent.species_id
            self.__update_display(fittest_agent)

    def __save_net(self):

        """ Saves the current displayed network to a text file. """

        self.__root.focus()
        if self.__neat.gen_num == -1:
            return
        try:
            file = open(self.__save_net_entry.get(), "w")
        except os.error:
            messagebox.showwarning("Invalid File Name", "Enter a valid file name")
            return
        self.__save_net_entry.delete(0, "end")
        for conn in self.__neat.population[self.__curr_agent_pop_index].conn_genes:
            for value in conn.__dict__.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.write("\n")
        for node in self.__neat.population[self.__curr_agent_pop_index].node_genes:
            for value in node.__dict__.values():
                file.write(str(value) + ",")
            file.write("\n")
        file.close()

    def __update_display(self, agent):

        """ Calls the methods which update the display. """

        self.__update_canvas(agent)
        self.__update_conns(agent)
        self.__update_stats(agent)
        if self.__exit:
            quit()
        self.__root.update()

    def __update_canvas(self, agent):

        """ Draws the passed agent to the canvas """

        self.__cnv.delete("all")

        num_layers = max((node.layer for node in agent.node_genes)) + 1
        x_spacing = self.__cnv.winfo_width() / (num_layers + 1)
        x_current = 0
        c_nodes = []

        for i in range(num_layers):
            num_in_layer = 0
            for node in agent.node_genes:
                if node.layer == i:
                    num_in_layer += 1

            y_spacing = self.__cnv.winfo_height() / (num_in_layer + 1)
            y_current = 0
            x_current += x_spacing

            for node in agent.node_genes:
                if node.layer == i:
                    y_current += y_spacing
                    c_node = self.__cnv.create_oval(x_current - App.NODE_RADIUS, y_current - App.NODE_RADIUS,
                                                    x_current + App.NODE_RADIUS, y_current + App.NODE_RADIUS,
                                                    fill=App.NODE_COLOUR, outline=App.NODE_BORDER_COLOUR,
                                                    width=App.NODE_BORDER_SIZE)
                    c_text = self.__cnv.create_text(x_current, y_current - 30,
                                                    text="ID = " + str(node.id), font=App.NODE_FONT,
                                                    fill=App.NODE_TEXT_COLOUR)
                    c_nodes.append([node, c_node, c_text])

        for conn in agent.conn_genes:
            x1 = App.NODE_RADIUS
            y1 = App.NODE_RADIUS
            x2 = App.NODE_RADIUS
            y2 = App.NODE_RADIUS
            for c_node in c_nodes:
                if c_node[0].id == conn.input:
                    x1 += self.__cnv.coords(c_node[1])[0]
                    y1 += self.__cnv.coords(c_node[1])[1]
                elif c_node[0].id == conn.output:
                    x2 += self.__cnv.coords(c_node[1])[0]
                    y2 += self.__cnv.coords(c_node[1])[1]

            if conn.enabled:
                colour = App.CONN_COLOUR
                width = App.CONN_WIDTH
            else:
                colour = App.CONN_DISABLED_COLOUR
                width = App.DISABLED_CONN_WIDTH

            self.__cnv.create_line(x1, y1, x2, y2, fill=colour, width=width)

    def __update_conns(self, agent):

        """ Prints the connections of the passed agent on the display. """

        for label in self.__conn_labels:
            label.destroy()
        self.__conn_labels = []
        row = 0
        count = 0
        for conn in agent.conn_genes:
            if count % 2 == 0:
                row += 1
                column = 0
            else:
                column = 1
            count += 1
            text = f"{conn.input} == {round(conn.weight, 2)} ==> {conn.output}"
            if conn.enabled:
                colour = App.CONNS_TEXT_FG
            else:
                colour = App.CONN_DISABLED_COLOUR
            label = Label(self.__conns_frame, text=text, font=App.CONNS_FONT,
                          bg=App.CONNS_TEXT_BG, fg=colour)
            label.grid(row=row, column=column, columnspan=1)
            self.__conn_labels.append(label)

    def __update_stats(self, agent):

        """ Updates the summary statistics """

        self.__gen_num_lbl.config(text=f"Generation Number: {self.__neat.gen_num}")
        self.__num_species_lbl.config(text=f"Number of species: {len(self.__neat.species)}")
        self.__dist_threshold_lbl.config(text=f"Distance Threshold: {round(self.__neat.distance_threshold, 2)}")
        self.__agent_id_lbl.config(text=f"Agent ID: {self.__neat.population.index(agent)}")
        self.__agent_fitness_lbl.config(text=f"Agent Fitness: {round(agent.fitness, 5)}")
        pop_avg_fitness = round(sum(agent.fitness for agent in self.__neat.population)/self.__neat.config.pop_size, 2)
        self.__pop_avg_fitness_lbl.config(text=f"Population Average Fitness: {pop_avg_fitness}")
        self.__species_id_lbl.config(text=f"Species ID: {agent.species_id}")
        s_avg_fitness = round(self.__neat.species[agent.species_id].avg_fitness, 2)
        self.__species_avg_fitness_lbl.config(text=f"Species Average Fitness: {s_avg_fitness}")
        self.__agent_species_size_lbl.config(text=f"Agent Species Size: {self.__neat.species[agent.species_id].size}")
