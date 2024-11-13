import pandas as pd
import schemdraw
from schemdraw.flow import *
import os

class aflow:
    min_down_arrow_length = 0.5
    right_arrow_length = 2

    def __init__(self, csv_name):
        """
        Initializes an aflow instance.

        Args:
            csv_name (str): Path to the CSV file containing flow data.
        """
        self.df = pd.read_csv(csv_name)

    def render_flow(self, triggering_event, save_path=None):
        """
        Generates a flow diagram based on a triggering event and optionally saves it.

        Args:
            triggering_event (str): Name of the triggering event (present in 
            the CSV).
            save_path (str, optional): Path where the flow diagram should be saved.
        """
        # Creates a dictionary for the triggering_event from CSV
        event_dict = self._make_dict(triggering_event)

        with schemdraw.Drawing() as d:
            # Set the background color to white (or any color you prefer)
            d.background = '#FFFFFF'  # You can change this to any color, e.g., 'lightgray'

            # Sets up event
            w, h, str_ = self._format_box(triggering_event)
            d += Process(w=w, h=h).label(str_)
            d += Arrow(w=self.right_arrow_length).right()

            # Does decision tree
            self.d, _ = self._make_tree(d, event_dict, None)

            # Save the image if save_path is provided
            if save_path:
                self.save_flow(save_path)

    
    def save_flow(self, output_string, dpi=300):
        """
        Saves the generated flow diagram.

        Args:
            output_string (str): Filename to save the diagram to.
            dpi (int, optional): Resolution of the saved image. Defaults to 300.
        """
        print(f"Attempting to save flow diagram to {output_string}...")
        self.d.save(output_string, dpi=dpi)

    def _make_dict(self, triggering_event):
        """
        Creates a dictionary representing the flow diagram based on a 
        triggering event.

        Args:
            triggering_event: The specific event to build the diagram around.

        Returns:
            A nested dictionary where:
            - **Keys** are locations.
            - **Values** are dictionaries, where:
                - **Keys** are powers invoked.
                - **Values** are lists of citations related to the power and 
                  location.
        """

        # Equivalent to graph data
        event_dict = {}

        # Loops through all rows
        for index, row in self.df.iterrows():

            # If any triggering events in row are triggering event.
            row_triggering_events = row['Triggering Event']
            if triggering_event in row_triggering_events.split(','):

                # Adds location to event dictionary
                location = row['Location']
                if location not in event_dict:
                    event_dict[location] = {}

                # Gets powers and replaces dumb tag with commas with smarter 
                # tag without commas
                powers = row['Powers Invoked']
                dumb_tag = '\"Troop, Uniformed Service, or National Guard'
                dumb_tag += ' Deployment\"'
                smart_tag = 'Troop/Uniformed Service/National Guard Deployment'
                powers = powers.replace(dumb_tag, smart_tag)

                # For each power...
                for power in powers.split(','):

                    # Adds power to dictionary
                    if power not in event_dict[location]:
                        event_dict[location][power] = []
                    
                    # Adds citation to power dictionary
                    event_dict[location][power].append(row['Citation'])

        return event_dict

    def _format_box(self, strings):
        """
        Formats a string or list of strings for display in a box.

        Args:
            strings: A string or a list of strings to be formatted.

        Returns:
            A tuple containing:
            - Width of the box.
            - Height of the box.
            - Formatted string for display.
        """
        if isinstance(strings, list):
            string = ''
            w = 0
            for str_ in strings:
                w_str, h_str, str_ = self._format_box(str_)
                str_ = str_ + '\n'
                if w_str > w:
                    w = w_str
                string += str_
            h = 1.3 + 0.45 * (len(strings) - 1)  # Expt found
            string = string[:-1]        
        else:
            string = strings
            w = 0.220 * len(string) + 1.153      # Expt found
            h = 1.3                              # Expt found
        return (w, h, string)

    def _format_diamond(self, string):
        """
        Formats a string for display in a diamond-shaped box.

        Args:
            string: The string to be formatted.

        Returns:
            A tuple containing:
            - Width of the diamond-shaped box.
            - Height of the diamond-shaped box.
            - Formatted string for display.
        """
        w = 0.448 * len(string) + 0.899          # Expt found
        h = 1.3                                  # Expt found
        return (w, h, string)

    def _make_tree(self, d, tree, next_tree):
        """
        Recursively builds a decision tree diagram.

        Args:
            d: The current `schemdraw.Drawing` object.
            tree: A dictionary representing the current node in the decision 
                  tree.
            next_tree: The next tree node in the sequence.

        Returns:
            A tuple containing:
                - The updated `schemdraw.Drawing` object.
                - The total length of down arrows for the current subtree.
        """
        # Initializes variables
        total_down_arrow_length = 0
        right_arrow_length = self.right_arrow_length
        min_down_arrow_length = self.min_down_arrow_length
    
        if isinstance(tree, dict):
            # Loops through all potential keys to determine width
            # This keeps tree aligned
            max_w = 0
            for key in tree.keys():
                key_with_Q = key + '?' # adds question mark to denote decision
                w, h, str_ = self._format_diamond(key_with_Q)
                if max_w < w:
                    max_w = w
                
            # Loops through all keys to add to tree
            tree_keys_list = list(tree.keys())
            tree_keys_list.sort()
            for idx, key in enumerate(tree_keys_list):
                key_with_Q = key + '?'
                w, h, str_ = self._format_diamond(key_with_Q)
                total_down_arrow_length += h
                q = Decision(w=max_w, h=h, E='Yes', S='No').label(str_)
                d += q
                d += Arrow(w=right_arrow_length).right().at(q.E)
                if idx == len(tree.keys()) - 1 or isinstance(tree[key], dict):
                    d, down_arrow_length = self._make_tree(d, tree[key], None)
                else:
                    next_key = tree_keys_list[idx + 1]
                    next_tree = tree[next_key]
                    d, down_arrow_length = self._make_tree(d, tree[key], 
                                                           next_tree)

                # Sets up next question
                if idx != len(tree.keys()) - 1:
                    d += Arrow().down(down_arrow_length).at(q.S)
                else:
                    d += Arrow().down(min_down_arrow_length).at(q.S)
        
                # Adds to sum of total down arrow length for return
                total_down_arrow_length += down_arrow_length
        
            # Explanation if all else fails...
            w, h, str_ = self._format_box('No Law')
            d += Process(w=w, h=h).label(str_)
        
            # Adds to total down arrow length
            total_down_arrow_length += down_arrow_length
        
        else:
        
            # Makes a box of relevant laws
            tree.sort()
            w, h, str_ = self._format_box(tree)
            d += Process(w=w, h=h).label(str_)
        
            # Adds total box length and min arrow length to get total down arrow
            # length
            if next_tree is None:
                mu_h = 0.5 * (h - 1.3)                             # Expt
            else:
                w, next_h, str_ = self._format_box(next_tree)
                mu_h = 0.5 * (h + next_h)
                mu_h -= 1.3
            total_down_arrow_length = min_down_arrow_length + mu_h # Expt
        
        
        return (d, total_down_arrow_length)
