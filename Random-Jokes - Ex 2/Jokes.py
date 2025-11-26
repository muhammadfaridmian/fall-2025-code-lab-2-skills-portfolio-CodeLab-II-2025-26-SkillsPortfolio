import tkinter as tk
import random

class JokeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Joke Teller")
        self.window.geometry("500x300")
        self.window.configure(bg='#f0f8ff')
        
        # Load jokes from file
        self.jokes = []
        self.load_jokes()
        
        self.current_joke = None
        self.setup_label = None
        self.punchline_label = None
        
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from the text file"""
        jokes_data = """Why did the chicken cross the road?To get to the other side.
What happens if you boil a clown?You get a laughing stock.
Why did the car get a flat tire?Because there was a fork in the road!
How did the hipster burn his mouth?He ate his pizza before it was cool.
What did the janitor say when he jumped out of the closet?SUPPLIES!!!!
Have you heard about the band 1023MB?It's probably because they haven't got a gig yet…
Why does the golfer wear two pants?Because he's afraid he might get a "Hole-in-one."
Why should you wear glasses to maths class?Because it helps with division.
Why does it take pirates so long to learn the alphabet?Because they could spend years at C.
Why did the woman go on the date with the mushroom?Because he was a fun-ghi.
Why do bananas never get lonely?Because they hang out in bunches.
What did the buffalo say when his kid went to college?Bison.
Why shouldn't you tell secrets in a cornfield?Too many ears.
What do you call someone who doesn't like carbs?Lack-Toast Intolerant.
Why did the can crusher quit his job?Because it was soda pressing.
Why did the birthday boy wrap himself in paper?He wanted to live in the present.
What does a house wear?A dress.
Why couldn't the toilet paper cross the road?Because it got stuck in a crack.
Why didn't the bike want to go anywhere?Because it was two-tired!
Want to hear a pizza joke?Nahhh, it's too cheesy!
Why are chemists great at solving problems?Because they have all of the solutions!
Why is it impossible to starve in the desert?Because of all the sand which is there!
What did the cheese say when it looked in the mirror?Halloumi!
Why did the developer go broke?Because he used up all his cache.
Did you know that ants are the only animals that don't get sick?It's true! It's because they have little antibodies.
Why did the donut go to the dentist?To get a filling.
What do you call a bear with no teeth?A gummy bear!
What does a vegan zombie like to eat?Graaains.
What do you call a dinosaur with only one eye?A Do-you-think-he-saw-us!
Why should you never fall in love with a tennis player?Because to them... love means NOTHING!
What did the full glass say to the empty glass?You look drunk.
What's a potato's favorite form of transportation?The gravy train
What did one ocean say to the other?Nothing, they just waved.
What did the right eye say to the left eye?Honestly, between you and me something smells.
What do you call a dog that's been run over by a steamroller?Spot!
What's the difference between a hippo and a zippo?One's pretty heavy and the other's a little lighter
Why don't scientists trust Atoms?They make up everything."""
        
        # Split into lines and process each joke
        lines = jokes_data.strip().split('\n')
        for line in lines:
            if '?' in line:
                setup, punchline = line.split('?', 1)
                self.jokes.append((setup + '?', punchline))
    
    def create_widgets(self):
        """Create all the GUI widgets"""
        # Title
        title_label = tk.Label(self.window, text="Joke Teller Assistant", 
                              font=("Arial", 18, "bold"), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=20)
        
        # Tell me a joke button
        self.joke_btn = tk.Button(self.window, text="Alexa tell me a Joke", 
                                 command=self.tell_joke,
                                 font=("Arial", 12, "bold"),
                                 bg='#3498db', fg='white',
                                 width=20, height=2)
        self.joke_btn.pack(pady=10)
        
        # Setup label (for joke question)
        self.setup_label = tk.Label(self.window, text="", 
                                   font=("Arial", 12), bg='#f0f8ff', fg='#2c3e50',
                                   wraplength=400)
        self.setup_label.pack(pady=10)
        
        # Punchline label (for joke answer)
        self.punchline_label = tk.Label(self.window, text="", 
                                       font=("Arial", 12, "bold"), bg='#f0f8ff', fg='#e74c3c',
                                       wraplength=400)
        self.punchline_label.pack(pady=10)
        
        # Frame for the button
        button_frame = tk.Frame(self.window, bg='#f0f8ff')
        button_frame.pack(pady=20)
        
        # Show punchline button
        self.punchline_btn = tk.Button(button_frame, text="Show Punchline", 
                                      command=self.show_punchline,
                                      font=("Arial", 10),
                                      bg='#f39c12', fg='white',
                                      state='disabled')
        self.punchline_btn.pack(side='left', padx=5)
        
        # Next joke button
        self.next_btn = tk.Button(button_frame, text="Next Joke", 
                                 command=self.next_joke,
                                 font=("Arial", 10),
                                 bg='#2ecc71', fg='white',
                                 state='disabled')
        self.next_btn.pack(side='left', padx=5)
        
        # Quit button
        quit_btn = tk.Button(button_frame, text="Quit", 
                            command=self.window.quit,
                            font=("Arial", 10),
                            bg='#e74c3c', fg='white')
        quit_btn.pack(side='left', padx=5)
    
    def tell_joke(self):
        """Tell a random joke"""
        if self.jokes:
            self.current_joke = random.choice(self.jokes)
            self.setup_label.config(text=self.current_joke[0])
            self.punchline_label.config(text="")
            
            # Enable buttons
            self.punchline_btn.config(state='normal')
            self.next_btn.config(state='normal')
    
    def show_punchline(self):
        """Show the punchline of the current joke"""
        if self.current_joke:
            self.punchline_label.config(text=self.current_joke[1])
    
    def next_joke(self):
        """Show next random joke"""
        self.tell_joke()
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Run the app
if __name__ == "__main__":
    app = JokeApp()
    app.run()