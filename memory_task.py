# import libraries
import pandas as pd
import numpy as np
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim
from psychopy.core import Clock, quit, wait, getTime
from psychopy.hardware.keyboard import Keyboard
from psychopy import event, data
import random
import os

# set up the dialogue box
exp_info = {'participant_nr': '', 'age': '','sex':''}
dlg = DlgFromDict(exp_info)

if not dlg.OK:
    print("User pressed 'Cancel'!") 
    quit()

print(f"Started experiment for participant {exp_info['participant_nr']} "f"with age {exp_info['age']}.")

# id needs to be numeric
p_name = exp_info['participant_nr']

if not p_name or not p_name.isdigit():
    print("Error: Participant Number must be a valid number. Quitting.")
    quit()
    
# prepare filename
# separate results list for distraction and retrieval phase
# store trial results
distraction_results = [] 
recall_results = []

# Initialize window
# white color (111)
win = Window(size=(1280, 720), fullscr=False, monitor='testMonitor', color=(0.0, 0.0, 0.0), units='height')
# initialize clock, keyboard
clock=Clock()
kb = Keyboard()
kb.clearEvents()

seed_value = int(p_name)

# Apply the seed for reproducible distraction tasks
# random math problems for distraction task but still predictable
# random for participants
random.seed(seed_value) 
np.random.seed(seed_value)

# typing input; user must press 'enter' to submit

def collect_typed_response(win, prompt_list, initial_text="", max_duration=None):
    """Presents a list of prompt stimuli and collects a typed response."""
    
    current_response = initial_text
    response_stim = TextStim(win, text= "", pos=(0, -0.2), height=0.05, color='white', font='Arial')
    
    kb.clearEvents()
    start_time = clock.getTime()
    
    while True:
        # Draw the main stimuli and the current response
        for stim in prompt_list:
            stim.draw()
        response_stim.text = "Answer: " + current_response + "_"
        response_stim.draw()
        win.flip()
        
        # Check for key presses
        keys = kb.getKeys(keyList=None, waitRelease=False, clear=True)
        
        for key in keys:
            if key.name == 'escape':
                win.close()
                quit()
            elif key.name == 'return':
                # This calculates time from when the problem appeared to when ENTER was pressed
                trial_rt = clock.getTime() - start_time 
                return current_response, trial_rt
            elif key.name == 'backspace':
                current_response = current_response[:-1]
            elif key.name == 'space':
                current_response += " "
            elif len(key.name) == 1:
                current_response += key.name
                
        # Check for time limit
        if max_duration is not None and (clock.getTime() - start_time) > max_duration:
            return current_response, max_duration # Return time limit as RT
            
# load dataset
wordlist_df = pd.read_csv("wordlist.csv")
print("Wordlist loaded successfully.")

# randomize the trial order for each participant
wordlist_df = wordlist_df.sample(frac=1, random_state=seed_value).reset_index(drop=True)

# welcome screen
welcome_txt_stim = TextStim(win, text="Welcome to this experiment! \n\n[Press SPACEBAR to continue]",font="Arial", color='white', pos=(0, 0), height=0.05)
welcome_txt_stim.draw()
win.flip()

event.waitKeys(keyList=['space', 'escape'])
kb.clearEvents()

# encoding phase
encoding_instruct_text = (
    "In this task, you will view sequences of words arranged in sets of three. \n" 
    "Each word will appear on the screen individually and the set be separated by fixation cross. \n\n" 
    "[Press the SPACEBAR to begin]"
)
encoding_instruct_stim = TextStim(win, text=encoding_instruct_text, height=0.06, color='white', font='Arial', pos=(0, 0))
encoding_instruct_stim.draw()
win.flip()
event.waitKeys(keyList=['space', 'escape'])

# stimulus should be large and centered and spaced

word_stim = TextStim(win, text="Placeholder", height=0.15, color='white', font='Arial', pos=(0, 0))
fix_stim = TextStim(win, text="+", height=0.15, color='white', font='Arial', pos=(0, 0))

encoding_duration = 4.0 # Time the words are on screen
fixation_duration = 0.8 # Fixation cross duration
iti_duration = 0.05 # Inter-trial interval

for i, row in wordlist_df.iterrows():
    trial_num = i + 1
    
    word_set = [row['Word 1'], row['Word 2'], row['Word 3']]
    
    # word 1
    word_stim.text = word_set[0]
    word_stim.draw()
    win.flip()
    wait(encoding_duration)
    
    # Tiny blank interval
    win.flip()
    wait(iti_duration)
    
    # word 2
    word_stim.text = word_set[1]
    word_stim.draw()
    win.flip()
    wait(encoding_duration)
    
    win.flip()
    wait(iti_duration)
    
    # word 3
    word_stim.text = word_set[2]
    word_stim.draw()
    win.flip()
    wait(encoding_duration)
    
    # fixation Cross
    fix_stim.draw()
    win.flip()
    wait(fixation_duration)
    
    
# end of task 1
encoding_end_txt = TextStim(win, text="Task 1 is completed!\n Please notify the researcher. \n\n[Press SPACEBAR to continue]", height=0.06, color='white', font='Arial', pos=(0, 0))
encoding_end_txt.draw()
win.flip()
# until the spacebar is pressed
event.waitKeys(keyList=['space','escape'])
kb.clearEvents()


# Phase 2: distraction task to prevent stimuli rehearsals

distraction_instruct_text = (
    "This is a simple arithmetic task.\n" 
    "You should type your answer out and press ENTER after finished.\n\n"
    "[Press the SPACEBAR to begin]"
)
distraction_instruct_stim = TextStim(win, text=distraction_instruct_text, height=0.05, color='white', font='Arial', pos=(0, 0))
type_here_stim = TextStim(win, text="Answer:", height=0.04, pos=(-0.15, -0.2), color='white')
distraction_instruct_stim.draw()
win.flip()
event.waitKeys(keyList=['space', 'escape'])

kb.clearEvents()

# Generate 30 Distraction Problems
distraction_problems = []
for i in range(30):
    op_type = np.random.choice(['+', '-'])
    if op_type == '+':
        num1 = np.random.randint(10, 50)
        num2 = np.random.randint(10, 50)
        problem = f"{num1} {op_type} {num2}"
        answer = num1 + num2
    else: # subtraction
        num1 = np.random.randint(30, 80)
        num2 = np.random.randint(5, num1 - 10)
        problem = f"{num1} {op_type} {num2}"
        answer = num1 - num2
    
    distraction_problems.append({'Problem': problem, 'Correct_Answer': str(answer)})

distraction_time_limit = 180.0 # 3 minutes
start_time = clock.getTime()
distraction_stim = TextStim(win, text="Placeholder", height=0.06, color='white', font='Arial', pos=(0, 0.2))
prompt_stim_distraction = TextStim(win, text="Type your answer and press ENTER:", height=0.05, color='white', font='Arial', pos=(0, 0.4))

for i, problem in enumerate(distraction_problems):
    elapsed = clock.getTime() - start_time
    if elapsed >= distraction_time_limit:
        break # Time's up
        
    # Prepare problem stimulus
    distraction_stim.text = f"{problem['Problem']} = ?"
    
    # Collect response (MUST be actively typed, not auto-advanced)
    user_response, rt = collect_typed_response(win, prompt_list=[prompt_stim_distraction, distraction_stim], max_duration=(distraction_time_limit - elapsed))
    
    # Check if it broke out due to timeout
    if clock.getTime() - start_time >= distraction_time_limit:
        break
        
    # Record trial data
    user_response_clean = "".join(filter(str.isdigit, user_response)) 
    is_correct = '1' if user_response_clean == problem['Correct_Answer'] else '0'
    
    distraction_results.append({
        'Trial_ID': i + 1, 
        'Problem': problem['Problem'], 
        'Correct_Answer': problem['Correct_Answer'], 
        'User_Response': user_response, 
        'RT': rt, 
        'Correct': '1' if user_response_clean == problem['Correct_Answer'] else '0'
    })
    
    # Brief ITI
    win.flip()
    wait(0.5)
    
    #save distraction file immediately
pd.DataFrame(distraction_results).to_csv(f'{p_name}_distraction_task.csv', index=False)

# Feedback/Wait after Distraction
distraction_end_txt = TextStim(win, text="Task 2 is completed!\n Please notify the researcher.\n\n [Press SPACEBAR to continue]", height=0.06, color='white', font='Arial')
distraction_end_txt.draw()
win.flip()

event.waitKeys(keyList=['space', 'escape'])
kb.clearEvents()

# Phase 3: retrieval task to assess memory
recall_instruct_text = (
    "For each trial, you will see the first two words from previous phase.\n"
    "Your task is to type the third word you remembered in the original set.\n"
    "After typing, press ENTER to submit your answer.\n\n"
    "[Press the SPACEBAR to begin]"
)

recall_instruct_stim = TextStim(win, text="Type the 3rd word from the set and press ENTER:", height=0.04, color='white', font='Arial', pos=(0, 0.4))

# Show the long instructions text first
TextStim(win, text=recall_instruct_text, height=0.04).draw()
win.flip()
event.waitKeys(keyList=['space', 'escape'])

# stimulus presentation #large, centered, spaced
recall_stim = TextStim(win, text="Placeholder", height=0.05, color='white', font='Arial', pos=(0, 0.2), alignText='center')

for i, row in wordlist_df.iterrows():
    trial_num = i + 1
    
    # cues
    cue1 = row['Word 1']
    cue2 = row['Word 2']
    target = row['Word 3']
    
    # valence
    valence_val = row['Valence']
    
    # cues with large spacing, as requested
    stim_text = f"{cue1}          {cue2}          ?" 
    recall_stim.text = stim_text
    
    # Collect response (MUST be actively typed)
    user_response, rt = collect_typed_response(win, prompt_list=[recall_instruct_stim, recall_stim])
    
    # Record trial data
    user_response_clean = user_response.strip().lower()
    target_clean = target.strip().lower()
    
    # Check for correct recall (case-insensitive)
    is_correct = '1' if user_response_clean == target_clean else '0'
    
    recall_results.append({
        'Phase': 'Recall',
        'Trial_ID': trial_num,
        'Cue_1': cue1,
        'Cue_2': cue2,
        'Target': target,
        'Valence': valence_val,
        'User_Response': user_response,
        'RT': rt,
        'Correct': is_correct
    })
    
    # Brief ITI
    win.flip()
    wait(0.5)

# save retrieval phase data
pd.DataFrame(recall_results).to_csv(f'{p_name}_recall_task.csv', index=False)
# ending sentence
end_text = TextStim(win, text="Task 3 is completed!\n Thank you for your participation.\n\n Please notify the researcher.", height=0.06, color='white', font='Arial', pos=(0, 0))
end_text.draw()
win.flip()
event.waitKeys(keyList=['space']) # Wait for manual exit from researcher

win.close()
quit()

